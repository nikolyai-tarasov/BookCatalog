
import logging
import os
from pathlib import Path
from datetime import datetime

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = LOG_DIR / f"library_{datetime.now().strftime('%Y-%m-%d')}.log"


def setup_logger(name=None, log_dir=LOG_DIR, log_level=LOG_LEVEL, use_rotation=False):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    log_dir = Path(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    if use_rotation:
        from logging.handlers import TimedRotatingFileHandler
        file_handler = TimedRotatingFileHandler(f"{log_dir}/{name}.log", when='midnight', backupCount=7)
    else:
        file_handler = logging.FileHandler(f"{log_dir}/{name}.log", encoding='utf-8')

    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger