
from asyncio import sleep
from http import client
from pymongo.cursor import CursorType

async def tail_oplog_example(client):
    oplog = client.local.oplog.rs
    first = await oplog.find().sort('$natural', 1).limit(-1).next()
    print(first)
    ts = first['ts']

    while True:
        # For a regular capped collection CursorType.TAILABLE_AWAIT is the
        # only option required to create a tailable cursor. When querying the
        # oplog, the oplog_replay option enables an optimization to quickly
        # find the 'ts' value we're looking for. The oplog_replay option
        # can only be used when querying the oplog. Starting in MongoDB 4.4
        # this option is ignored by the server as queries against the oplog
        # are optimized automatically by the MongoDB query engine.
        cursor_filter = {
          'ts': {'$gt': ts},
          'op': {'$eq': 'i'}
        }
        cursor = oplog.find(cursor_filter,
                            cursor_type=CursorType.TAILABLE_AWAIT,
                            oplog_replay=True)
        while cursor.alive:
            async for doc in cursor:
                ts = doc['ts']
                print(doc)
            # We end up here if the find() returned no documents or if the
            # tailable cursor timed out (no new documents were added to the
            # collection for more than 1 second).
            # await sleep(1)

import asyncio
import motor.motor_asyncio

client = client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo1:27017')
loop = asyncio.get_event_loop()
loop.run_until_complete(tail_oplog_example(client))