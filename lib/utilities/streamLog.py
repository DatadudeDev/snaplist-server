import logging
import sys
import re

class ColorFormatter(logging.Formatter):
    FORMAT = "[%(asctime)s]: %(name)s: %(message)s (%(levelname)s)"
    COLORS = {
        'INFO': '\033[92m',  # Green
        'ERROR': '\033[91m',  # Red
        'WARNING': '\033[93m',  # Yellow
        'DEBUG': '\033[94m',  # Blue
        'CRITICAL': '\033[95m',  # Magenta
    }
    # Pink, light green, orange, and red color codes
    PINK = '\033[95m'
    LIGHT_GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

    def format(self, record):
        log_fmt = self.FORMAT
        color = self.COLORS.get(record.levelname, self.RESET)

        # Custom logic for coloring specific lines
        if "prompt:" in record.msg:
            color = self.PINK
        elif "Total running time" in record.msg:
            total_time = float(re.search(r"Total running time: ([\d.]+) seconds", record.msg).group(1))
            if total_time < 15:
                color = self.LIGHT_GREEN
            elif 15 <= total_time < 30:
                color = self.ORANGE
            else:
                color = self.RED
        # Enhanced check for HTTP status codes in the 400s or 500s
        elif re.search(r"(4\d\d|5\d\d) None", record.msg):
            color = self.RED

        formatter = logging.Formatter(log_fmt)
        formatted_record = formatter.format(record)
        return color + formatted_record + self.RESET

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("data/log.ansi"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    for handler in logging.root.handlers:
        handler.setFormatter(ColorFormatter())

setup_logging()

# Test logging to verify the adjustment
logging.debug('[2024-04-06 20:38:27,006]: urllib3.connectionpool: https://api.spotify.com:443 "POST /v1/playlists/6GHeKEQaMzHc74XRPpeivs/tracks HTTP/1.1" 502 None (DEBUG)')