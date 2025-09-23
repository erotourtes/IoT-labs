#!/usr/bin/env python3

import asyncio
import json
import logging
from aiocoap import Context, Message, GET

TEMP_MAX = 28.0
TEMP_MIN = 10.0
CURRENT_MAX = 4.5
HUM_MAX = 75.0

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

async def fetch_telemetry():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri="coap://10.10.0.4/telemetry")
    response = await protocol.request(request).response
    data = json.loads(response.payload.decode())
    logging.info("Received: %s", data)
    check_alerts(data)

def check_alerts(msg):
    t = msg.get("temperature_c")
    c = msg.get("current_a")
    h = msg.get("humidity_pct")
    alerts = []
    if t is not None and (t > TEMP_MAX or t < TEMP_MIN):
        alerts.append(f"temperature out of range: {t}C")
    if c is not None and c > CURRENT_MAX:
        alerts.append(f"current too high: {c}A")
    if h is not None and h > HUM_MAX:
        alerts.append(f"humidity too high: {h}%")
    for a in alerts:
        logging.warning("ALERT: %s", a)

async def main():
    while True:
        try:
            await fetch_telemetry()
        except Exception as e:
            logging.error("Error fetching telemetry: %s", e)
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())
