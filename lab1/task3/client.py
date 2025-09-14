#!/bin/env python3

import serial

def main():
    ser = serial.Serial("/tmp/serial_connection", timeout=1)

    http_request = (
      "GET /hello HTTP/1.1\r\n"
      "Host: serial\r\n"
      "User-Agent: pyserial-client\r\n"
      "\r\n"
    )

    ser.write(http_request.encode())
    ser.flush()

    response = ser.read_until(b'\r\n\r\n')
    if not response:
      print("No reponse")

    headers = response.decode().split('\r\n')
    for h in headers:
      if h.lower().startswith("content-length:"):
        length = int(h.split(":")[1].strip())
        response += ser.read(length)
        break

    print(f"Res: {response.decode()}")

if __name__ == "__main__":
    main()
