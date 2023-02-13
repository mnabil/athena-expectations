import great_expectations as ge
from great_expectations.cli.datasource import sanitize_yaml_and_save_datasource, check_if_datasource_name_exists
import configparser

config = configparser.RawConfigParser()


config.read('config.cfg')

# initializing our data context
context = ge.get_context()

#reading region and s3_path
aws_default_region = config['aws_settings']['aws_default_region']
aws_s3_path = config['aws_settings']['aws_athena_s3_staging_dir']

# setting up our connection string & datasource name
connection_string = "awsathena+rest://@athena.{region}.amazonaws.com/?s3_staging_dir={s3_path}".format(
    region=aws_default_region, s3_path=aws_s3_path)

datasource_name = config['datasource']['name']

# constructing yaml config which will be written to great_expecations.yml
example_yaml = f"""
name: {datasource_name}
class_name: Datasource
execution_engine:
  class_name: SqlAlchemyExecutionEngine
  connection_string: {connection_string}
data_connectors:
  default_runtime_data_connector_name:
    class_name: RuntimeDataConnector
    batch_identifiers:
      - default_identifier_name
  default_inferred_data_connector_name:
    class_name: InferredAssetSqlDataConnector
    include_schema_name: True"""
print(example_yaml)

# testing datasource config
context.test_yaml_config(yaml_config=example_yaml)

# checks if datasource exists & dumps yaml concfig in great_expecations.yml
sanitize_yaml_and_save_datasource(
    context, example_yaml, overwrite_existing=True)

# list our data sources
print(
    'successfuly added datasource, here is our list of connected datasources: \n%s' %
    context.list_datasources())
