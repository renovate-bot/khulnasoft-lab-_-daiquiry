import daiquiry

daiquiry.setup(set_excepthook=False)
logger = daiquiry.getLogger(__name__)

# This exception will not pass through Daiquiry:
raise Exception("Something went wrong")
