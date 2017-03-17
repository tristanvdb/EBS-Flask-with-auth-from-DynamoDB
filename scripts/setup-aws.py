
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

	acctID = aws.client('sts').get_caller_identity()['Account']

	# DynamoDB

	tbl_arns = dict()

	dynamodb = aws.client('dynamodb')

	tbl_arns.update(dynamodb_table(dynamodb, 'services',   [ ( 'service' , 'S' , 'HASH' ) ] ))
	tbl_arns.update(dynamodb_table(dynamodb, 'identities', [ ( 'service' , 'S' , 'HASH' ) , ( 'user' , 'S' , 'RANGE' ) ] ))

	# IAM

	iam = aws.client('iam')
	try:
		role = iam.get_role(RoleName='EBauth-instance')
		print 'IAM Role `EBauth-instance` already exists.'
	except:
		role = iam.create_role(
		    RoleName='EBauth-instance', 
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
		print 'IAM Role `EBauth-instance` created.'
	role_arn = role['Role']['Arn']

	try:
		policy = iam.get_policy(PolicyArn='arn:aws:iam::{}:policy/{}'.format(acctID, 'EBauth-instance-tables-access'))
		print 'IAM Policy `EBauth-instance-tables-access` already exists.'
	except Exception as e:
		policy = iam.create_policy(
		    PolicyName='EBauth-instance-tables-access',
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
		print 'IAM Policy `EBauth-instance-tables-access` created.'

	response = iam.attach_role_policy(RoleName='EBauth-instance', PolicyArn=policy['Policy']['Arn'])

	# EBS

	ebs = aws.client('elasticbeanstalk')

	## `EBauth` application TODO

