#!/bin/bash

server_file="../Broker/serverFile.txt"

# Check if the file exists
if [ ! -f "$server_file" ]; then
  echo "The file $server_file does not exist."
  exit 1
fi

# start KV Servers from serverFile.txt
while IFS=" " read -r ip port; do
  echo "Starting server at IP $ip and port $port..."
  python3 kvServer.py -a "$ip" -p "$port" &
done < "$server_file"

echo "All servers have been started."

