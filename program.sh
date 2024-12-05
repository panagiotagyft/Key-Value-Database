#!/bin/bash  

# https://askubuntu.com/questions/974756/how-can-i-open-a-extra-console-and-run-a-program-in-it-with-one-command

# cd DataCreation 

# echo "Data Creation"
# python3 createData.py -k keyFile.txt -n 100 -d 3 -l 4 -m 5
# echo

# cd ..
cd KeyValueStore
echo "KeyValueStore"


cd Server
echo "Server"
gnome-terminal -- bash -c "./servers.sh; exec bash"
cd ..

cd Broker
echo "Broker"
gnome-terminal -- bash -c "python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k 2; exec bash"
cd ../..

# Function to handle Ctrl+C
free() {
  echo "Terminating all servers..."
  pkill -P $$  # kill all child pids (processes)
  exit 0
}

# https://www.reddit.com/r/bash/comments/1e8plnu/how_to_handle_ctrlc_in_bash_scripts/?rdt=39057
# Set the trap to catch SIGINT (Ctrl+C)
trap free SIGINT

wait

