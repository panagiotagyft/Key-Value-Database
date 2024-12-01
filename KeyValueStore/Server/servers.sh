#!/bin/bash

IP="127.0.0.1"  # Ορισμός της μεταβλητής IP

# Εκκίνηση των servers σε διαφορετικές πόρτες
python3 kvServer.py -a "$IP" -p 8001 &
python3 kvServer.py -a "$IP" -p 8002 &
python3 kvServer.py -a "$IP" -p 8003 &

echo "Servers are starting on ports 8006, 8001, and 8010..."
