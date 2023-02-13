# create_configure_expectations_suite.py
import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.data_context.types.resource_identifiers import (
    ExpectationSuiteIdentifier,
)
from great_expectations.exceptions import DataContextError
import json
import argparse
import logging
from utils.utils import get_assetNames
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

#initializing GE context
context = ge.data_context.DataContext()

# USE IN CLI
my_parser = argparse.ArgumentParser(
    description='Create Your Expectations Suite ex: python create_configure_suite --asset_name view1')
my_parser.add_argument(
    "--asset_name",  # name on the CLI - drop the `--` for positional/required parameters
    nargs=None,  # str not an array
    type=str,
    required=True
)

my_parser.add_argument(
    # name on the CLI - drop the `--` for positional/required parameters
    "--expectations_file",
    nargs=None,  # str not an array
    type=str,
    default="expectations_template_examples.json",  # default if nothing is provided
)

args = my_parser.parse_args()
asset_name = args.asset_name


expectation_suite_name = args.asset_name

try:
    # get this suit , if you found it
    suite = context.get_expectation_suite(
        expectation_suite_name=expectation_suite_name)

    print(
        f'Loaded ExpectationSuite "{suite.expectation_suite_name}" containing {len(suite.expectations)} expectations.'
    )
except DataContextError:
    # create this suite if you did not find it
    suite = context.create_expectation_suite(
        expectation_suite_name=expectation_suite_name
    )

    print(
        f'Created ExpectationSuite "{suite.expectation_suite_name}".')

try:
    with open(args.expectations_file, 'r') as f:
        expectations_list = json.load(f)
except Exception as e:
    logger.error("Parsing json file\nException: %s" % e)

# NOW ADD EXPECTATIONS TO YOUR EXPECTATIONS SUITE!
for exp in expectations_list:
    expectation_configuration = ExpectationConfiguration(
        expectation_type=exp['expectation_type'],
        kwargs=exp['kwargs'],
        meta=exp['meta']
    )
    suite.add_expectation(
        expectation_configuration=expectation_configuration)

# ADD suite expectatation
context.save_expectation_suite(
    expectation_suite=expectation_suite_name,
    expectation_suite_name=expectation_suite_name)

suite_identifier = ExpectationSuiteIdentifier(
    expectation_suite_name=expectation_suite_name)  # hold my suite
# build data docs again after adding expectations
context.build_data_docs(resource_identifiers=[suite_identifier])
# open data docs for me to view
context.open_data_docs(resource_identifier=suite_identifier)
