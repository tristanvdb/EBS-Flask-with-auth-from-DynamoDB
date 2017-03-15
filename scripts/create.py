
import os
import sys
import md5
import boto3
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('service', type=str, help='')

	parser.add_argument('--password-secret', type=str, required=True, metavar='secret',  help='Secret used to salt passwords (and original root account)')

	parser.add_argument('--token-secret',  type=str, required=True, metavar='secret',  help='Secret used to encode authentication tokens')
	parser.add_argument('--token-timeout', type=int, default=3600,  metavar='seconds', help='Token timeout in seconds (default 1 hour)')

	parser.add_argument('--admin-username', type=str, default='admin', metavar='username', help='Username for the administrator')
	parser.add_argument('--admin-password', type=str, required=True,   metavar='password', help='Password for the administrator')

	args = parser.parse_args()

	# TODO default for secrets and admin password

	aws_profile = os.environ.get('SERVER_AWS_PROFILE')
	aws_region = os.environ.get('SERVER_AWS_REGION', 'us-east-1')

	if aws_profile is None:
		aws = boto3.session.Session(region_name=aws_region)
	else:
		aws = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)

	services = aws.resource('dynamodb').Table('services')

	services.put_item(Item={
	    'service' : args.service,
	    'password' : {
	         'secret' : args.password_secret
	    },
	    'token' : {
	        'secret' : args.token_secret,
	        'timeout' : str(args.token_timeout)
	    }
	})

	identities = aws.resource('dynamodb').Table('identities')

	identities.put_item(Item={
	    'service' : args.service,
	    'user' : args.admin_username,
	    'password' : md5.new(args.admin_password + args.password_secret).hexdigest(),
	    'priviledges' : [ 'user' , 'admin' ]
	})

	print 'Registered service: {}'.format(args.service)
	print '  Password:'
	print '    Secret:         {}'.format(args.password_secret)
	print '  Token:'
	print '    Secret:         {}'.format(args.token_secret)
	print '    Timeout:        {}'.format(args.token_timeout)
	print '  Administrator:'
	print '    Username:       {}'.format(args.admin_username)
	print '    Password:       {}'.format(args.admin_password)

