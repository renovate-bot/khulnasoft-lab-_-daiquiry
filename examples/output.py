import logging
import sys

import daiquiry

# Log both to stdout and as JSON in a file called /dev/null. (Requires
# `python-json-logger`)
daiquiry.setup(
    level=logging.INFO,
    outputs=(
        daiquiry.output.Stream(sys.stdout),
        daiquiry.output.File("/dev/null", formatter=daiquiry.formatter.JSON_FORMATTER),
    ),
)

logger = daiquiry.getLogger(__name__, subsystem="example")
logger.info("It works and log to stdout and /dev/null with JSON")
