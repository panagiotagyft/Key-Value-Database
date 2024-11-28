#!/bin/bash

# Διαβάζει το serverFile.txt
SERVER_FILE="../Broker/serverFile.txt"

# Έλεγχος αν το αρχείο υπάρχει
if [[ ! -f $SERVER_FILE ]]; then
    echo "Error: Το αρχείο $SERVER_FILE δεν βρέθηκε."
    exit 1
fi

# Εκκίνηση servers
while IFS=' ' read -r IP PORT; do
    echo "Starting server at $IP:$PORT"
    python3 kvServer.py -a "$IP" -p "$PORT" &
done < "$SERVER_FILE"

echo "All servers are starting..."
