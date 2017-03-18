
import os
import sys
import glob
import time
import boto3
import argparse
import datetime
import subprocess

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--service-name', type=str, required=True, metavar='name',    help='Name of the service being created')
	parser.add_argument('--version',      type=str, required=True, metavar='version', help='Application\'s version tag')

	parser.add_argument('--aws-profile', type=str, default=os.environ.get('AWS_PROFILE', None),       metavar='profile', help='AWS profile to use (Default: env[AWS_PROFILE])')
	parser.add_argument('--aws-region',  type=str, default=os.environ.get('AWS_REGION', None), metavar='region',  help='AWS region to use (Default: env[AWS_REGION])')

	parser.add_argument('--extra-files', nargs='*',  type=str, help='Files required by the service\'s modules.')

	parser.add_argument('--force', action='store_true', help='Existing ressource are removed first instead of aborting.')

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

	s3 = aws.client('s3')
	ebs = aws.client('elasticbeanstalk')

	# Get service description

	services = aws.resource('dynamodb').Table('services')
	service = services.get_item(Key={ 'service' : args.service_name })
	if not 'Item' in service:
		print 'Cannot retrieve description of service {}'.format(args.service_name)
		exit(1)
	service = service['Item']
	
	appname = 'EBauth-{}'.format(args.service_name)
	applabel = '{}-{}'.format(appname, args.version)

	# Check if environement already exists (TODO)

	environments = ebs.describe_environments( ApplicationName='EBauth-application', VersionLabel=applabel, EnvironmentNames=[ appname ], IncludeDeleted=False )
	if len(environments['Environments']) > 0:
		assert len(environments['Environments']) == 1
		if environments['Environments'][0]['Status'].upper() == 'TERMINATED':
			pass
		elif args.force:
			ebs.terminate_environment(EnvironmentName=appname, TerminateResources=True, ForceTerminate=True)
			while True:
				environments = ebs.describe_environments( ApplicationName='EBauth-application', VersionLabel=applabel, EnvironmentNames=[ appname ], IncludeDeleted=False )
				if len(environments['Environments']) == 0:
					break

				print 'Waiting for environment {} to be terminated ({})'.format(applabel,  environments['Environments'][0]['Status'])
				time.sleep(10)

			print 'Removed existing environment `{}` from `EBauth-application`'.format(applabel)
		else:
			print 'Application `EBauth-application` already has an environment `{}`'.format(applabel)
			exit(1)

	# Check if version already exists

	application_versions = ebs.describe_application_versions(
	    ApplicationName='EBauth-application',
	    VersionLabels=[ applabel ],
	)
	if len(application_versions['ApplicationVersions']) > 0:
		if args.force:
			ebs.delete_application_version(ApplicationName='EBauth-application', VersionLabel=applabel, DeleteSourceBundle=True)
			print 'Removed existing version `{}` from `EBauth-application`'.format(applabel)
		else:
			print 'Application `EBauth-application` already has a version `{}`'.format(applabel)
			exit(1)

	# Bundle application

	bundle_path = '{}.zip'.format(applabel)
	if os.path.exists(bundle_path):
		os.remove(bundle_path)

	subprocess.call([ 'zip' , bundle_path , '.ebextensions/python.config' , 'requirements.txt' ])
	subprocess.call([ 'zip' , bundle_path , 'EBauth/__init__.py' , 'EBauth/server.py' , 'EBauth/users.py'  ])
	subprocess.call([ 'zip' , bundle_path , 'scripts/wsgi.py'  ])
	if len(args.extra_files) > 0:
		subprocess.call([ 'zip' , bundle_path ] + args.extra_files )

	bucket_name = 'EBauth-{}'.format(acctID).lower()
	with open(bundle_path,'r') as F:
		s3.put_object(Bucket=bucket_name, Key=bundle_path, Body=F)

	# Deploy application

	application_version = ebs.create_application_version(
	    ApplicationName='EBauth-application',
	    VersionLabel=applabel,
	    SourceBundle={
	        'S3Bucket': bucket_name,
	        'S3Key': bundle_path
	    },
	    Process=True
	)

	while True:
		application_versions = ebs.describe_application_versions(
		    ApplicationName='EBauth-application',
		    VersionLabels=[ applabel ],
		)
		assert len(application_versions['ApplicationVersions']) == 1
		if application_versions['ApplicationVersions'][0]['Status'].upper() == 'PROCESSED':
			break
		assert not application_versions['ApplicationVersions'][0]['Status'].upper() == 'FAILED'

		print 'Waiting for application version to be ready ({}).'.format(application_versions['ApplicationVersions'][0]['Status'])
		time.sleep(1)

	ebs.create_environment(
	    ApplicationName='EBauth-application',
	    EnvironmentName=appname,
	    CNAMEPrefix=appname,
	    Tags=[
	        { 'Key': 'EBauth', 'Value': applabel },
	    ],
	    VersionLabel=applabel,
	    SolutionStackName="64bit Amazon Linux 2016.09 v2.3.2 running Python 2.7",
	    OptionSettings=[
	        {
	            'Namespace': 'aws:autoscaling:launchconfiguration',
	            'ResourceName': 'AWSEBAutoScalingLaunchConfiguration',
                    'OptionName': 'IamInstanceProfile',
	            'Value': 'EBauth-instance-profile'
	        },{
	            'Namespace': 'aws:elasticbeanstalk:application:environment',
	            'OptionName': 'EBAUTH_SERVICE_NAME',
	            'Value': args.service_name
	        },{
	            'Namespace': 'aws:elasticbeanstalk:application:environment',
	            'OptionName': 'AWS_REGION',
	            'Value': aws.region_name
	        }
	    ]
	)


	while True:
		environments = ebs.describe_environments( ApplicationName='EBauth-application', VersionLabel=applabel, EnvironmentNames=[ appname ], IncludeDeleted=False )
		assert len(environments['Environments']) == 1
		if environments['Environments'][0]['Status'].upper() == 'READY':
			break

		print 'Waiting for environment {} to be ready ({})'.format(applabel,  environments['Environments'][0]['Status'])
		time.sleep(10)

