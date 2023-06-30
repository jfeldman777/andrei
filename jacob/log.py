import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def log(request, msg):
    logger.error(msg)
