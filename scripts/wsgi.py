
import argparse
import importlib

import EBauth

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	# TODO arguments?

	args = parser.parse_args()

	importlib.import_module('EBauth.api.user')
	importlib.import_module('EBauth.api.test')

	EBauth.application.run(debug=True)

