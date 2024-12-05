#!/bin/bash

server_file="../Broker/serverFile.txt"

# Check if the file exists
if [ ! -f "$server_file" ]; 
  then
    echo "The file $server_file does not exist."
    exit 1
fi

# Start KV Servers from serverFile.txt
while IFS=" " read -r ip port; do
  echo "Starting server at IP $ip and port $port..."
  python3 kvServer.py -a "$ip" -p "$port" &
done < "$server_file"

echo "All servers have been started."

# Function to handle Ctrl+C
free() {
  echo "Terminating all servers..."
  pkill -P $$  # kill all child pids (processes)
  exit 0
}

# https://www.reddit.com/r/bash/comments/1e8plnu/how_to_handle_ctrlc_in_bash_scripts/?rdt=39057
# Set the trap to catch SIGINT (Ctrl+C)
trap free SIGINT

# # Keep the script running to manage servers
# # Wait for all background processes
wait
# exit 0 