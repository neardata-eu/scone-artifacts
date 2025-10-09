#!/bin/bash

set -e

docker network rm federatedchallengesetup_challenge_net || true

docker build -t fl_challenge:team_name -f Dockerfile .   
docker build -t fl_challenge:team_name_sgx -f Dockerfile_scone .

sed -i 's/server_address="141.76.44.249:8080"/server_address="localhost:8080"/g' ./src/client/main.py
sed -i 's/server_address="server:8080"/server_address="localhost:8080"/g' ./src/client/main.py

docker-compose -f docker-compose-sgx-cas.yaml down
docker-compose -f docker-compose-sgx-cas.yaml run -d --rm las

./prepare_cas_session.sh

docker-compose -f docker-compose-sgx-cas.yaml down

docker-compose -f docker-compose-sgx-cas.yaml up --force-recreate --remove-orphans

