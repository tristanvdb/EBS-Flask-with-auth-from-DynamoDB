
import argparse
import importlib

import EBauth

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	# TODO arguments?

	args = parser.parse_args()

	for module in EBauth.application.service['modules']:
		importlib.import_module(module)

	EBauth.application.run(debug=True)

