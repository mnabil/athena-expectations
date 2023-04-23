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
import sys
from utils import CustomArgParser

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

# READ CLI ARGS
c = CustomArgParser()
config = c.get_interface_args(__file__)
expectation_suite_name = config.suite_name or config.asset_name
expectations_json = config.expectations_file or "expectations_template_examples.json"

# initializing GE context
context = ge.data_context.DataContext()

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
    with open(expectations_json, 'r') as f:
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
    expectation_suite=suite,
    expectation_suite_name=expectation_suite_name)

suite_identifier = ExpectationSuiteIdentifier(
    expectation_suite_name=expectation_suite_name)
# build data docs again after adding expectations
context.build_data_docs(resource_identifiers=[suite_identifier])
# open data docs for me to view
context.open_data_docs(resource_identifier=suite_identifier)
