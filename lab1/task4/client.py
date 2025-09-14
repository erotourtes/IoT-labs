#!/bin/env python3

import serial
import zlib

def main():
    ser = serial.Serial("/tmp/serial_connection", timeout=1)

    file_with_crs = input("Which file to retreive\n")

    http_request = (
      f"GET /files/{file_with_crs} HTTP/1.1\r\n"
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
    file_with_crs = bytes()

    success = headers[0].startswith("HTTP/") and "200" in headers[0].split()[1]

    for h in headers:
      if h.lower().startswith("content-length:"):
        length = int(h.split(":")[1].strip())
        read_bytes = ser.read(length)
        response += read_bytes
        file_with_crs += read_bytes
        break

    if not success:
      print("Error retrieving a file:", file_with_crs.decode())
      return

    file = file_with_crs[:-4]
    crc = int.from_bytes(file_with_crs[-4:], byteorder="big")

    file_crc = zlib.crc32(file)

    if crc == file_crc:
      print("File integrity is confirmed")
    else:
      print("File integrity is not confirmed")

    print(f"Received file {file_with_crs}:\n\n {file.decode()}")

if __name__ == "__main__":
    main()
