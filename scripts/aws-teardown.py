
import os
import sys
import json
import boto3
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--aws-profile', type=str, default=os.environ.get('AWS_PROFILE', None),       metavar='profile', help='AWS profile to use (Default: env[AWS_PROFILE])')
	parser.add_argument('--aws-region',  type=str, default=os.environ.get('AWS_REGION', None), metavar='region',  help='AWS region to use (Default: env[AWS_REGION])')

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

	# TODO delete tables
	# TODO delete buckets
	# TODO delete roles
	# TODO delete policies
	# TODO delete applications

