import great_expectations as ge  # FIXME: update to latest
import logging
import argparse
from utils.utils import get_assetNames
from tqdm import tqdm
import timeit
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

my_parser = argparse.ArgumentParser(
    description="set --asset_name for asset and make sure there's a suite created for that data source \nEx: python checkpoints.py --asset_name view1")

my_parser.add_argument(
    "--asset_name",  # name on the CLI - drop the `--` for positional/required parameters
    nargs=None,  # str not an array
    type=str,
    required=False
)

args = my_parser.parse_args()  # passing my arguments


def main():
    context = ge.data_context.DataContext()  # initializing my GE context

    asset_name = args.asset_name

    if not asset_name:
        for checkpoint in tqdm(context.list_checkpoints()):
            logger.info("Running Checkpoint for {0}".format(checkpoint))
            context.run_checkpoint(checkpoint_name=checkpoint)
    else:
        if asset_name in get_assetNames(context):
            logger.info("Running Checkpoint for {0}".format(asset_name))
            # run checkpoint and then check the data docs
            checkpoint_result = context.run_checkpoint(
                checkpoint_name="checkpoint_{0}".format(asset_name))

            # open the local data_docs
            validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[
                0]
            context.open_data_docs(
                resource_identifier=validation_result_identifier)

        else:
            logger.error(
                "asset_name : {0} not in context assets".format(asset_name))


if __name__ == "__main__":
    main()
