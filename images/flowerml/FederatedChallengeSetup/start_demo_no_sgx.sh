#!/bin/bash

set -e

docker network rm  federatedchallengesetup_challenge_net || true


# the demo with CAS uses a different network setup (host vs docker)

sed -i 's/server_address="141.76.44.249:8080"/server_address="server:8080"/g' ./src/client/main.py
sed -i 's/server_address="localhost:8080"/server_address="server:8080"/g' ./src/client/main.py


sudo rm -rf data/input/*
sudo rm -rf data/output/*
mkdir -p data/output/client1
mkdir -p data/output/client2
mkdir -p data/output/server

echo -e "\n\n\nDownloading training data into encrypted volume.\n\n\n"
docker run --rm -v ./src/client:/app/code -v ./data/input:/app/input  fl_challenge:team_name /bin/bash -c "python setup_data.py"


docker-compose -f docker-compose.yaml up --force-recreate --remove-orphans

