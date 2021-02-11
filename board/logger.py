import logging


# https://python-guide-kr.readthedocs.io/ko/latest/writing/logging.html
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
