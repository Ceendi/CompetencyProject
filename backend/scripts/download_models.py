import sys
import argparse
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def download_transformer(model_name):
    logger.info(f"Downloading Transformers model: {model_name}...")
    try:
        AutoTokenizer.from_pretrained(model_name)
        AutoModelForSequenceClassification.from_pretrained(model_name)
        logger.info(f"Successfully downloaded: {model_name}")
    except Exception as e:
        logger.error(f"Error downloading model {model_name}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True, help="Name of the model to download")
    args = parser.parse_args()

    download_transformer(args.model_name)
