import argparse
import pprint


class CustomArgParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.config_dict = {
            'configure_datasource': {
                '--datasource_name': "to specify datasource desired name",
                '--aws_default_region': "to specify aws region for the athena asset",
                '--aws_athena_s3_staging_dir': "to specify bucket which will contain athena query results"
            },
            'configure_suite':  {
                '--suite_name': "to specify the testing suite which will be created default: asset_name",
                '--asset_name': "to specify athena table name",
                '--expectations_file': "file which contains list of expectations that will be implemented for this suite default: expectations_template_examples.json in your project dir "
            },
            'configure_checkpoint':
            {
                '--datasource_name': "to specify datasource desired name",
                "--schema": "to specify athena schema name",
                '--asset_name': "to specify athena table name",
                '--suite_name': "to specify the testing suite which will be created default: asset_name"
            },
            'run_checkpoint':
            {
                '--checkpoint_name': "to specify checkpoint name, default: asset_name"
            }
        }

    def get_interface_args(self, interface):
        for config_group in self.config_dict:
            if config_group in interface:
                # pretty format my -h __doc__
                self.description = pprint.pformat(
                    self.config_dict[config_group])
                for arg_name in self.config_dict[config_group]:
                    if arg_name in ['--suite_name', '--expectations_file']:
                        self.add_argument(
                            arg_name,
                            nargs=None,
                            type=str,
                            required=False
                        )
                    else:
                        self.add_argument(
                            arg_name,
                            nargs=None,
                            type=str,
                            required=True
                        )
        return self.parse_args()


def get_assetNames(config, context):
    assets = context.get_available_data_asset_names()
    asset_names = []
    try:
        for db_asset_name in assets[config.datasource_name]['default_inferred_data_connector_name']:
            db, name = db_asset_name.split('.')
            if db == config.schema:  # which is our default db
                asset_names.append(name)
        return asset_names
    except:
        print("Data source is not created , please create your datasource or make sure you named you passed it correctly")
