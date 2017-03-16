
import os
import sys
import boto3
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--service-name', type=str, required=True, metavar='name', help='Name of the service being created')

	parser.add_argument('--aws-profile', type=str, default=os.environ.get('AWS_PROFILE', None),       metavar='profile', help='AWS profile to use (Default: env[AWS_PROFILE])')
	parser.add_argument('--aws-region',  type=str, default=os.environ.get('AWS_REGION', 'us-east-1'), metavar='region',  help='AWS region to use (Default: env[AWS_REGION])')

	args = parser.parse_args()

	# AWS connection
	if not args.aws_profile is None and not args.aws_region is None:
		aws = boto3.session.Session(profile_name=args.aws_profile, region_name=args.aws_region)
	elif not args.aws_profile is None:
		aws = boto3.session.Session(profile_name=args.aws_profile)
	elif not args.aws_region is None:
		aws = boto3.session.Session(region_name=args.aws_region)
	else:
		aws = boto3.session.Session()

	# DynamoDB tables
	services = aws.resource('dynamodb').Table('services')
	identities = aws.resource('dynamodb').Table('identities')

	services.delete_item(Key={ 'service' : args.service_name })
	print '# Service {} unregistered.'.format(args.service_name)

	items = identities.query(
	    ProjectionExpression="service, #U", ExpressionAttributeNames={ "#U": "user" },
	    KeyConditionExpression=boto3.dynamodb.conditions.Key('service').eq(args.service_name)
	)

	for item in items['Items']:
		print '## User {} removed from {}.'.format(item['user'],item['service'])
		identities.delete_item(Key=item)
