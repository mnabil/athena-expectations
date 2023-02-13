import configparser

config = configparser.RawConfigParser()

config.read('../config.cfg')

datasource_name = config['datasource']['name']

def get_assetNames(context):
    assets = context.get_available_data_asset_names()
    asset_names = []
    for db_asset_name in assets[datasource_name]['default_inferred_data_connector_name']:
        db, name = db_asset_name.split('.')
        if db == 'default':  # which is our default db
            asset_names.append(name)
    return asset_names
