import logging

import daiquiry
import daiquiry.formatter

daiquiry.setup(
    level=logging.INFO,
    outputs=(
        daiquiry.output.Stream(
            formatter=daiquiry.formatter.ColorFormatter(
                fmt="%(asctime)s [PID %(process)d] [%(levelname)s] "
                "%(name)s -> %(message)s"
            )
        ),
    ),
)

logger = daiquiry.getLogger(__name__)
logger.info("It works with a custom format!")
