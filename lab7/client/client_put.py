#!/usr/bin/python3

import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    context = await Context.create_client_context()
    await asyncio.sleep(2)
    payload = b"Hello, CoAP server! \n" * 1000
    request = Message(code=PUT, uri='coap://10.10.0.2/other/block', payload=payload)
    try:
        response = await context.request(request).response
    except Exception as e:
        logging.error('Failed to send PUT request:')
        logging.error(e)
    else:
        logging.info('PUT request sent successfully:')
        logging.info('Result: %s\n%r' % (response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main())
