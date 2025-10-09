#!/bin/bash

set -e

echo -e "\n\nStarting Python once to read mrenclave:\n\n"

PYTHON_MRENCLAVE=$(docker run -it --rm --device=/dev/sgx_enclave -v ./src/server:/app/code fl_challenge:team_name_sgx /bin/bash -c "SCONE_ALLOW_DLOPEN=2 SCONE_MODE=HW SCONE_HEAP=6G SCONE_SYSLIBS=1 SCONE_VERSION=1 SCONE_LOG=ERROR SCONE_FORK=1 /opt/conda/bin/python -V" | grep """Enclave hash""" | awk '{print $3}')

#PYTHON_MRENCLAVE=825b4b54233d060a408edda8ac761f1efa4b504a30b89d02b83ab7fb07baeb88


echo -e "\n\nMRENCLAVE of Python: ${PYTHON_MRENCLAVE}\n\n"

cp cas_session_template.yml cas_session_file.yml

sed -i "s/PYTHON_ENCLAVE_HASH/${PYTHON_MRENCLAVE}/g" cas_session_file.yml

RNDS=${RANDOM}-${RANDOM}

sed -i "s/RNDNR/${RNDS}/g" cas_session_file.yml

echo -e "\n\nGenerating keys for connection security to CAS:\n\n"

if [ ! -d "scone_cas_connection_keys" ]; then
	mkdir scone_cas_connection_keys
	openssl req -x509 -newkey rsa:4096 -out scone_cas_connection_keys/client.crt -keyout scone_cas_connection_keys/client-key.key  -days 31 -nodes -sha256 -subj "/C=US/ST=Dresden/L=Saxony/O=Scontain/OU=Org/CN=www.scontain.com" -reqexts SAN -extensions SAN -config <(cat /etc/ssl/openssl.cnf <(printf '[SAN]\nsubjectAltName=DNS:www.scontain.com')) 2>&1 > /dev/null
fi



echo -e "\n\nUploading the session to CAS:\n\n"

export SCONE_CAS_ADDR=scone-cas.cf

# Add -v for verbose output
curl -k  --cert scone_cas_connection_keys/client.crt --key scone_cas_connection_keys/client-key.key --data-binary @cas_session_file.yml https://$SCONE_CAS_ADDR:8081/session



SESSION_IDEN=$(cat cas_session_file.yml | grep "NEARDATA_DEMO" | awk '{print $2}')
sed -i "s/SESSION_IDEN=.*/SESSION_IDEN=${SESSION_IDEN}/g" docker-compose-sgx-cas.yaml
echo -e "\n\nCAS Session ID: $SESSION_IDEN"



sudo rm -rf data/input/*
sudo rm -rf data/output/*
mkdir -p data/output/client1
mkdir -p data/output/client2
mkdir -p data/output/server


echo -e "\n\n\nDownloading training data into encrypted volume.\n\n\n"
docker run -it --rm --network=host --device=/dev/sgx_enclave -e SCONE_CAS_ADDR=scone-cas.cf -e SCONE_LAS_ADDR=141.76.44.249 -e SCONE_CONFIG_ID=$SESSION_IDEN/python_data_prep -v ./src/client:/app/code -v ./data/input:/app/input  fl_challenge:team_name_sgx /bin/bash -c "python setup_data.py"



echo -e "\n\n\nReading traninig data outside SCONE.\n\n\n"
set +e
docker run -it --rm --network=host -v ./data/input:/app/input:ro -v ./src/hacker:/app/code fl_challenge:team_name /bin/bash -c "python main.py" 
set -e


echo -e "\n\n\nReading traninig data inside SCONE.\n\n\n"
docker run -it --rm --network=host --device=/dev/sgx_enclave -e SCONE_CAS_ADDR=scone-cas.cf -e SCONE_LAS_ADDR=141.76.44.249 -e SCONE_CONFIG_ID=$SESSION_IDEN/python_data_prep -v ./data/input:/app/input:ro -v ./src/hacker:/app/code fl_challenge:team_name_sgx /bin/bash -c "python main.py"


