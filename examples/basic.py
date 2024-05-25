import logging

import daiquiry

daiquiry.setup(level=logging.INFO)

logger = daiquiry.getLogger(__name__)
logger.info("It works and log to stderr by default with color!")
