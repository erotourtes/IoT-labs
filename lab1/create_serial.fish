#!/bin/env fish

socat -d2 pty,raw,echo=0,link=/tmp/serial_simulator pty,raw,echo=0,link=/tmp/serial_connection
