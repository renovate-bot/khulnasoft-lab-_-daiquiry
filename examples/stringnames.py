import logging

import daiquiry

daiquiry.setup(level=logging.INFO, outputs=("stdout", "stderr"))

logger = daiquiry.getLogger(__name__)
logger.info("It works and logs to both stdout and stderr!")
