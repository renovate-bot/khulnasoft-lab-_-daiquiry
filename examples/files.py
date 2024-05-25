import datetime
import logging

import daiquiry

daiquiry.setup(
    level=logging.DEBUG,
    outputs=(
        daiquiry.output.File("errors.log", level=logging.ERROR),
        daiquiry.output.TimedRotatingFile(
            "everything.log", level=logging.DEBUG, interval=datetime.timedelta(hours=1)
        ),
    ),
)

logger = daiquiry.getLogger(__name__)

logger.info("only to rotating file logger")
logger.error("both log files, including errors only")
