

if __name__ == "__main__":
	import os
	import argparse

	parser = argparse.ArgumentParser()

	parser.add_argument('--service-name', type=str, default=os.environ.get('EBAUTH_SERVICE_NAME', None), metavar='name', help='Name of the service being created (Default: env[EBAUTH_SERVICE_NAME])')

	parser.add_argument('--aws-profile', type=str, default=os.environ.get('AWS_PROFILE', None),       metavar='profile', help='AWS profile to use (Default: env[AWS_PROFILE])')
	parser.add_argument('--aws-region',  type=str, default=os.environ.get('AWS_REGION', 'us-east-1'), metavar='region',  help='AWS region to use (Default: env[AWS_REGION])')

	parser.add_argument('--debug', action='store_true', help='Launch Flask in debug mode')

	args = parser.parse_args()

	os.environ['EBAUTH_SERVICE_NAME'] = args.service_name
	os.environ['AWS_PROFILE'] = args.aws_profile
	os.environ['AWS_REGION'] = args.aws_region

import importlib
import EBauth
for module in EBauth.application.service['modules']:
	importlib.import_module(module)

if __name__ == "__main__":
	EBauth.application.run(debug=args.debug)

