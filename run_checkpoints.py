import great_expectations as ge  # FIXME: update to latest
import logging
import argparse
from utils import CustomArgParser, get_assetNames
from tqdm import tqdm
import timeit
import sys


# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


# READ CLI ARGS
c = CustomArgParser()
config = c.get_interface_args(__file__)
checkpoint_name = config.checkpoint_name or config.asset_name


def main():
    context = ge.data_context.DataContext()  # initializing my GE context

    if not checkpoint_name:
        for checkpoint in tqdm(context.list_checkpoints()):
            logger.info("Running Checkpoint for {0}".format(checkpoint))
            context.run_checkpoint(checkpoint_name=checkpoint)
    else:
        logger.info("Running Checkpoint for {0}".format(checkpoint_name))
        # run checkpoint and then check the data docs
        checkpoint_result = context.run_checkpoint(
            checkpoint_name="{0}".format(checkpoint_name))

        # open the local data_docs
        validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[
            0]
        context.open_data_docs(
            resource_identifier=validation_result_identifier)


if __name__ == "__main__":
    main()
