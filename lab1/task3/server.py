#!/bin/env python3

from io import BytesIO
import sys
import logging
import serial
from http.server import BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)

DEFAULT_ADDR = '/tmp/serial_simulator'
addr = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDR

conn = serial.serial_for_url(addr)

class SerialHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request_bytes, output_stream):
        self.rfile = BytesIO(request_bytes)
        self.wfile = output_stream
        self.client_address = ("serial", 0)
        # self.server = None
        self.handle()

    def do_GET(self):
        if self.path == "/hello":
            body = b"Hello over serial!\n"
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = b"Not found\n"
            self.send_response(404)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


while True:
  logging.info(f'Ready to receive requests on {addr}')
  request = conn.read_until(b'\r\n\r\n')
  logging.info('REQ (headers): %r', request)
  if not request:
    continue

  headers = request.decode().split('\r\n')
  for h in headers:
    if h.lower().startswith("content-length:"):
      length = int(h.split(":")[1].strip())
      request += conn.read(length)
      break

  response = BytesIO()

  SerialHTTPRequestHandler(request, response)
  conn.write(response.getvalue())
