# Athena-Expectations
A component for QA-ing Athena Downstream Data sources, outputs &amp; deliveries , Uses [GreatExpectations.io](https://greatexpectations.io)


### Workflow (a set of simple steps)
1) configure your aws connections inside config.cfg 
2) create data source config to connect to AWS Athena
3) create expectations config for your athena assets
4) create checkpoints config for those suites 
5) run our checkpoints! 


### 1) How do I get set up? ###
* Run `python3 -m venv venvs/athena-expectations && source venvs/athena-expectations/bin/activate`
* Run  `pip install --upgrade pip && pip install -r requirements.txt`
* Run  `aws sso login` or Authenticate into AWS using AWS sso or config in ~/aws/cred
* A datasource_name , s3_path, schema name inside `config.cfg` file.

### 2) How to create DataSource for GreatExpectations ?
- Now That you added your config in config.cfg , we tell GE to write our configs for our selected DataSource
- Run `python create_configure_datasource.py` # it'll read config from config.cfg

### 3) How to create Expectations Suite for an Athena View ?
- make sure the tables/views are in the same datasource you just configured.
- pick your desired column & table level expectations from  https://greatexpectations.io/expectations/
- put your expectations as list of json dicts as exampled in `expectations_template_examples.json`
- Run `python create_configure_suite.py --asset_name [athena-view/table-asset]` # asset name is the name of the athena view
This will create an expectations suite in `expectations_template_examples.json` directory with your desired expectations.


### 4) How to create checkpoints for an expectation suite we just created ?
- make sure to know your asset_name & suite name of your expectations
- Run `python create_configure_checkpoint.py --asset_name [athena-view/table-asset]` # asset name is the name of the athena view

This will create checkpoint configurations in `checkpoints` directory
____________________________________________________________________________________________
## 5) Now That we have our Suites & Checkpoints Ready, we *RUN* our checkpoint

- make sure to know your asset_name
- Run  `python run_checkpoints.py --asset_name [athena-view/table-asset]` # will trigger all our created checkpoints if you don't pass --asset_name
- Open Your Great_expectations dashboard in your browser, located in `athena-expectations/great_expectations/uncommitted/data_docs/local_site/index.html`



## HOPE ALL YOUR EXPECTATIONS WERE MET!