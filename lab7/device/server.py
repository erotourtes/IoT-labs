#!/usr/bin/python3

import asyncio
import json
import random
from datetime import datetime

from aiocoap import resource, Context, Message
import aiocoap

class TelemetryResource(resource.Resource):
    async def render_get(self, request):
        print("Get request",  request)
        data = {
            "device_id": "sim-001",
            "timestamp": datetime.now().timestamp(),
            "temperature_c": round(random.uniform(15.0, 30.0), 2),
            "current_a": round(random.uniform(0.0, 5.0), 3),
            "humidity_pct": round(random.uniform(20.0, 80.0), 1),
        }
        payload = json.dumps(data).encode("utf-8")
        return aiocoap.Message(payload=payload, content_format=50)

async def main():
    root = resource.Site()
    root.add_resource(["telemetry"], TelemetryResource())

    await Context.create_server_context(root, bind=("::", 5683))
    print("CoAP device simulator running on coap://localhost:5683/telemetry")

    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
