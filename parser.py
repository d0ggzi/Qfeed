import logging
import sys

from sql import SQL

db = SQL()

if __name__ == "__main__":
    from client.client import app
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.run()