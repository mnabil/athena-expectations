from ruamel.yaml import YAML
import great_expectations as ge
from great_expectations.exceptions import DataContextError
import logging
import argparse
from utils import CustomArgParser
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

# READ CLI ARGS
c = CustomArgParser()
config = c.get_interface_args(__file__)
datasource_name = config.datasource_name
schema = config.schema
asset = config.asset_name
suite = getattr(config, 'suite_name', config.asset_name)

# Initializing context
context = ge.data_context.DataContext()

try:
    asset_name = asset
    suite_name = suite
    suite_exists = bool(
        context.get_expectation_suite(
            expectation_suite_name="%s" % suite))
except (DataContextError, Exception) as e:
    logger.error(
        "ERROR: Missing checkpoint arguments\nException: %s" % e)

yaml = YAML()  # yaml instance
context = ge.get_context()  # init GE context


yaml_config = f"""
name: {asset_name}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-validate-{asset_name}"
validations:
  - batch_request:
      datasource_name: {datasource_name}
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: {schema}.{asset_name}
      data_connector_query:
        index: -1
    expectation_suite_name: {suite_name}
"""  # adding checkpoint in checkpoints dir

print("your yaml config is:\n" + yaml_config)

if True:
    my_checkpoint = context.test_yaml_config(yaml_config=yaml_config)
    # validate that our yaml_configurations are

    print(my_checkpoint.get_config(mode="yaml"))

    # add this to my checkpoints store
    context.add_checkpoint(**yaml.load(yaml_config))

    # run checkpoint and then check the data docs
    context.run_checkpoint(checkpoint_name="%s" % asset_name)
else:
    logger.error(
        "asset_name : %s not in context assets" % asset_name)
