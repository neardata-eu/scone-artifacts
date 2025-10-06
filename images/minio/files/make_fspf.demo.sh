#!/bin/bash

#####
##
## FSPF preparation
cd /
export SCONE_MODE=SIM
scone fspf create fspf.pb
scone fspf addr fspf.pb / --kernel / --not-protected
scone fspf addr fspf.pb /data --encrypted --kernel /data
scone fspf encrypt fspf.pb |tee /fspf.keytag
echo "generated SCONE_FSPF_KEY=$(cat /fspf.keytag | awk '{print $11}')"
echo "generated SCONE_FSPF_TAG=$(cat /fspf.keytag | awk '{print $9}')"
echo "generated SCONE_FSPF=/fspf.pb"
ls -l /fspf.pb
