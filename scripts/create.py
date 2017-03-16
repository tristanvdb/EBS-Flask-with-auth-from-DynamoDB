
import os
import sys
import md5
import boto3
import string
import argparse

random_alphabet = string.ascii_letters + string.digits + '+.'
def random_str(n):
	return ''.join(map( lambda x: random_alphabet[ord(os.urandom(1)) % len(random_alphabet) ] , range(n) ))

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--service-name', type=str, required=True, metavar='name', help='Name of the service being created')

	parser.add_argument('--password-secret', type=str, default=None, metavar='secret',  help='Secret used to salt passwords (default: random string of length 16)')

	parser.add_argument('--token-secret',  type=str, default=None, metavar='secret',  help='Secret used to encode authentication tokens (default: random string of length 16)')
	parser.add_argument('--token-timeout', type=int, default=3600, metavar='seconds', help='Token timeout in seconds (default: 1 hour)')

	parser.add_argument('--admin-username', type=str, default='admin', metavar='username', help='Username for the administrator (default: "admin")')
	parser.add_argument('--admin-password', type=str, default=None,    metavar='password', help='Password for the administrator (default: random string of length 8)')

	parser.add_argument('--modules', type=lambda v: v.split(','), default=[ 'EBauth.api.user' , 'EBauth.api.test' ], metavar='LIST', help='Comma separated list of module to load (default: "EBauth.api.user" and "EBauth.api.test")')

	args = parser.parse_args()

	if args.password_secret is None:
		args.password_secret = random_str(16)
	if args.token_secret is None:
		args.token_secret = random_str(16)
	if args.admin_password is None:
		args.admin_password = random_str(8)

	# AWS connection
	aws_profile = os.environ.get('SERVER_AWS_PROFILE')
	aws_region = os.environ.get('SERVER_AWS_REGION', 'us-east-1')
	if aws_profile is None:
		aws = boto3.session.Session(region_name=aws_region)
	else:
		aws = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)

	# DynamoDB tables
	services = aws.resource('dynamodb').Table('services')
	identities = aws.resource('dynamodb').Table('identities')

	# Check if service already exists
	service = services.get_item(Key={ 'service' : args.service_name })
	if 'Item' in service:
		print 'Service {} already exists!'.format(args.service_name)
		exit(1)

	# Check if user already exists
	identity = identities.get_item(Key={ 'service' : args.service_name , 'user' : args.admin_username })
	if 'Item' in identity:
		print 'User {} for service {} already exists!'.format(args.admin_username, args.service_name)
		exit(1)

	# Add service to services table
	services.put_item(Item={
	    'service' : args.service_name,
	    'password' : {
	         'secret' : args.password_secret
	    },
	    'token' : {
	        'secret' : args.token_secret,
	        'timeout' : str(args.token_timeout)
	    },
	    'modules' : args.modules
	})
	print 'User {} for service {} added to identities table.'.format(args.admin_username, args.service_name)

	# Add administrator for service
	identities.put_item(Item={
	    'service' : args.service_name,
	    'user' : args.admin_username,
	    'password' : md5.new(args.admin_password + args.password_secret).hexdigest(),
	    'priviledges' : [ 'user' , 'admin' ]
	})
	print 'Service {} added to services table.'.format(args.service_name)

	# Create service description
	report = [
	  'Registered service: {}'.format(args.service_name),
	  '  Password:',
	  '    Secret:         {}'.format(args.password_secret),
	  '  Token:',
	  '    Secret:         {}'.format(args.token_secret),
	  '    Timeout:        {}'.format(args.token_timeout),
	  '  Administrator:',
	  '    Username:       {}'.format(args.admin_username),
	  '    Password:       {}'.format(args.admin_password),
	  '  Modules:'
	]
	for module in args.modules:
		report.append('                    {}'.format(module))
	with open('{}.txt'.format(args.service_name),'w') as F:
		F.write('\n'.join(report) + '\n')

	print 'Service description saved in {}.txt.'
	print 'Warning: it contains the administrator password!'

