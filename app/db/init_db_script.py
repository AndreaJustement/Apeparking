import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.db.initialize_db import initialize_db
import asyncio

async def main():
    await initialize_db()

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
