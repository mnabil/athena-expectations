from ruamel.yaml import YAML
import great_expectations as ge
from great_expectations.exceptions import DataContextError
import logging
import argparse
import configparser
from utils.utils import get_assetNames
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

#reading datasource config
config = configparser.RawConfigParser()
config.read('config.cfg')

#reading datasource name
datasource_name = config['datasource']['name']
schema_name = config['datasource']['schema']
#Initializing context
context = ge.data_context.DataContext()

# USE IN CLI
my_parser = argparse.ArgumentParser(
    description="set --asset_name for asset and make sure there's a suite created \
        for that data source \nEx: python checkpoints.py --asset_name view1")

my_parser.add_argument(
    "--asset_name",  # name on the CLI - drop the `--` for positional/required parameters
    nargs=None,  # str not an array
    type=str,
    required=True
)
my_parser.add_argument(
    "--suite",  # name on the CLI - drop the `--` for positional/required parameters
    nargs=None,  # str not an array
    type=str,
    required=False
)
args = my_parser.parse_args()

try:
    asset_name = args.asset_name
    suite_name = getattr(args, 'suite', asset_name)
    suite_exists = bool(
        context.get_expectation_suite(
            expectation_suite_name="%s" %
            args.suite))
except (DataContextError, Exception) as e:
    logger.error(
        "ERROR: Missing checkpoint arguments\nException: %s" % e)

yaml = YAML()  # yaml instance
context = ge.get_context()  # init GE context

# if args.asset_name in get_assetNames(context):
yaml_config = f"""
name: checkpoint_{asset_name}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-validate-{asset_name}"
validations:
  - batch_request:
      datasource_name: {datasource_name}
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: {schema_name}.{asset_name}
      data_connector_query:
        index: -1
    expectation_suite_name: {suite_name}
"""  # adding checkpoint in checkpoints dir

print("your yaml config is:\n" + yaml_config)

if args.asset_name in get_assetNames(context):
    my_checkpoint = context.test_yaml_config(yaml_config=yaml_config)
    # validate that our yaml_configurations are

    print(my_checkpoint.get_config(mode="yaml"))

    # add this to my checkpoints store
    context.add_checkpoint(**yaml.load(yaml_config))

    # run checkpoint and then check the data docs
    context.run_checkpoint(checkpoint_name="checkpoint_%s" % asset_name)
else:
    logger.error(
        "asset_name : %s not in context assets" % asset_name)
