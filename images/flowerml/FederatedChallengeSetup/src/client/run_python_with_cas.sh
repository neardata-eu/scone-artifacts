#!/bin/bash

export SCONE_CAS_ADDR=scone-cas.cf
export SCONE_LAS_ADDR=141.76.44.249

sleep 7

echo -e "\n\nAttesting the public CAS:\n\n"

scone cas attest $SCONE_CAS_ADDR --only_for_testing-trust-any --only_for_testing-debug  --only_for_testing-ignore-signer -C -G -S

echo -e "\n\n\nStarting Python (flwr) \n\n\n"

#echo -e "${SESSION_IDEN}\n\n\n"

# More scone env vars are set in session file and docker compose file

SCONE_CONFIG_ID=$SESSION_IDEN/python_client python main.py



