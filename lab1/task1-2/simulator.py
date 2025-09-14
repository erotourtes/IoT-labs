#!/bin/env python3

import sys
import logging
import serial

DEFAULT_ADDR = '/tmp/serial_simulator'

logging.basicConfig(level=logging.INFO)

addr = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDR

conn = serial.serial_for_url(addr)


while True:
  logging.info('Ready to receive requests on (addr)')
  request = conn.readline()
  logging.info('REQ: %r', request)
  request = request.strip().decode().lower()
  reply = 'Test-conn, 24C, 385682,1.05A\n' if request == '*idn?' else "NACK\n"
  reply = reply.encode()
  logging.info('REP: %r', reply)
  conn.write(reply)
