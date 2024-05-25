import logging

import daiquiry
import daiquiry.formatter

daiquiry.setup(
    level=logging.INFO,
    outputs=(
        daiquiry.output.Stream(
            formatter=daiquiry.formatter.ColorFormatter(
                fmt=(daiquiry.formatter.DEFAULT_FORMAT + " [%(subsystem)s is %(mood)s]")
            )
        ),
    ),
)

logger = daiquiry.getLogger(__name__, subsystem="example")
logger.info("It works and log to stderr by default with color!", mood="happy")
