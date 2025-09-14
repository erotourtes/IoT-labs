#!/bin/env python3

from io import BytesIO
import sys
import logging
import serial
import re
import zlib
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
        self.handle()

    def do_GET(self):
        match = re.match("/files/(.+)", self.path)
        if match:
            file_path = match.group(1)
            try:
              with open(file_path, "rb") as file:
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0)

                file_content = file.read()
                file_checksum = zlib.crc32(file_content)
                self.send_response(200)

                self.send_header("Content-Length",str(file_size + 4))
                self.end_headers()
                self.wfile.write(file_content)
                self.wfile.write(file_checksum.to_bytes(4, byteorder="big"))
            except Exception as e:
              print(e)
              body = f"No file with name {file_path}\n"
              self.send_response(404)
              self.send_header("Content-Length", str(len(body)))
              self.end_headers()
              self.wfile.write(body.encode())
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
