import logging

# Set up global logger
fileHandler = logging.FileHandler("my_log.log")
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        fileHandler,
    ]
)
logger = logging.getLogger("simple_logger")
