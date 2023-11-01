import asyncio
import logging
import sys
from client.client import app
from sql import SQL

db = SQL()

if __name__ == "__main__":
    from bot.app import main
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # app.run()
    asyncio.run(main())