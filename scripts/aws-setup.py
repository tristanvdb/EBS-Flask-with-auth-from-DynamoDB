
import os
import sys
import json
import boto3
import argparse

def dynamodb_table(dynamodb, name, schema):
	try:
		table = dynamodb.describe_table(TableName=name)
		assert 'Table' in table
		# FIXME check schema
		print "Table `{}` already exists.".format(name)
		return { name : table['Table']['TableArn'] }
	except:
		table = dynamodb.create_table(
		    TableName=name,
		    AttributeDefinitions=[ { 'AttributeName': n, 'AttributeType': t  } for ( n , t , k ) in schema ],
		    KeySchema=[ { 'AttributeName': n, 'KeyType': k } for ( n , t , k ) in schema  ],
		    ProvisionedThroughput={ 'ReadCapacityUnits': 5, 'WriteCapacityUnits': 1 }
		)
		print "Table `{}` created.".format(name)
		return { name : table['TableDescription']['TableArn'] }

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--aws-profile', type=str, default=os.environ.get('AWS_PROFILE', None), metavar='profile', help='AWS profile to use (Default: env[AWS_PROFILE])')
	parser.add_argument('--aws-region',  type=str, default=os.environ.get('AWS_REGION', None),  metavar='region',  help='AWS region to use (Default: env[AWS_REGION])')

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

	acctID = aws.client('sts').get_caller_identity()['Account']

	# DynamoDB

	tbl_arns = dict()

	dynamodb = aws.client('dynamodb')

	tbl_arns.update(dynamodb_table(dynamodb, 'services',   [ ( 'service' , 'S' , 'HASH' ) ] ))
	tbl_arns.update(dynamodb_table(dynamodb, 'identities', [ ( 'service' , 'S' , 'HASH' ) , ( 'user' , 'S' , 'RANGE' ) ] ))

	# S3

	s3 = aws.client('s3')

	bucket_name = 'EBauth-{}'.format(acctID).lower()
	try:
		s3.head_bucket(Bucket=bucket_name)
		print 'S3 Bucket `{}` already exists.'.format(bucket_name)
	except:
		s3.create_bucket(Bucket=bucket_name) # FIXME all buckets are created in us-east-1...
		print 'S3 Bucket `{}` created.'.format(bucket_name)

	# IAM

	iam = aws.client('iam')
	try:
		role = iam.get_role(RoleName='EBauth-instance-role')
		print 'IAM Role `EBauth-instance-role` already exists.'
	except:
		role = iam.create_role(
		    RoleName='EBauth-instance-role', 
		    AssumeRolePolicyDocument=json.dumps({
		        "Version": "2012-10-17",
		        "Statement": [
		            {
		                "Sid": "",
		                "Effect": "Allow",
		                "Principal": { "Service": "ec2.amazonaws.com" },
		                "Action": "sts:AssumeRole"
		            }
		        ]
		    })
		)
		print 'IAM Role `EBauth-instance-role` created.'
	role_arn = role['Role']['Arn']

	try:
		policy = iam.get_policy(PolicyArn='arn:aws:iam::{}:policy/{}'.format(acctID, 'EBauth-instance-policy-tables-access'))
		print 'IAM Policy `EBauth-instance-policy-tables-access` already exists.'
	except Exception as e:
		policy = iam.create_policy(
		    PolicyName='EBauth-instance-policy-tables-access',
		    PolicyDocument=json.dumps({
		        "Version": "2012-10-17",
		        "Statement": [
		            {
		                "Sid": "",
		                "Effect": "Allow",
		                "Action": [
		                    "dynamodb:GetItem",
		                    "dynamodb:PutItem"
		                ],
		                "Resource": tbl_arns.values()
		            }
		        ]
		    })
		)
		print 'IAM Policy `EBauth-instance-policy-tables-access` created.'

	iam.attach_role_policy(RoleName='EBauth-instance-role', PolicyArn=policy['Policy']['Arn'])

	try:
		iam.get_instance_profile(InstanceProfileName='EBauth-instance-profile')

		print 'IAM Instance Profile `EBauth-instance-profile` already exists.'
	except:
		iam.create_instance_profile(InstanceProfileName='EBauth-instance-profile')
		print 'IAM Instance Profile `EBauth-instance-profile` created.'
	iam.add_role_to_instance_profile(InstanceProfileName='EBauth-instance-profile', RoleName='EBauth-instance-role')

	# EBS

	ebs = aws.client('elasticbeanstalk')

	try:
		ebs.create_application(ApplicationName='EBauth-application')
		print 'EBS application `EBauth` created.'
	except:
		print 'EBS application `EBauth` already exist.'

