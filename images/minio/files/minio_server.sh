#!/bin/bash

SERVICEADDRESS=":${SERVICEADDRESS:-9000}"
CONSOLEADDRESS=":${CONSOLEADDRESS:-9001}"

function unsetfspf (){
  echo "..:DBG:cleaning FSPF settings due to absence of complete cofiguration"
  unset SCONE_FSPF_KEY
  unset SCONE_FSPF_TAG
  unset SCONE_FSPF
}

date

if [ ${#SCONE_FSPF_KEY} -gt 0 ]; then
  echo "..:DBG:SCONE_FSPF_KEY=${SCONE_FSPF_KEY}"
  if [ ${#SCONE_FSPF_TAG} -gt 0 ]; then
    echo "..:DBG:SCONE_FSPF_TAG=${SCONE_FSPF_TAG}"
    if [ ${#SCONE_FSPF} -gt 0 ]; then
      echo "..:DBG:SCONE_FSPF=${SCONE_FSPF}"
      if [ "$SCONE_FSPF" == "/data/fspf.pb" ]; then
        if [ ! -f /data/fspf.pb ]; then
          cp -pv /fspf.pb /data/fspf.pb #|tee -a /data/minio.log
        fi
      else
        unsetfspf
      fi
    else
      unsetfspf
    fi
  else
    unsetfspf
  fi
else
  unsetfspf
fi

set |grep ^SCONE_

echo "..:DBG:SERVICEADDRESS='${SERVICEADDRESS}'"
echo "..:DBG:CONSOLEADDRESS='${CONSOLEADDRESS}'"

set -x
minio server /data --anonymous --address "$SERVICEADDRESS" --console-address "$CONSOLEADDRESS" 2>&1
