#!/bin/bash

#####
##
## FSPF preparation
cd /
export SCONE_MODE=SIM
mkdir -p /fspf/fspf-file
mkdir -p /fspf/native-files
mv -v /keycloak/ /keycloak.mv
mv -v /usr/lib/jvm /usr/lib/jvm.mv

/opt/scone/bin/scone fspf create /fspf/fspf-file/fs.fspf
/opt/scone/bin/scone fspf addr /fspf/fspf-file/fs.fspf / --not-protected --kernel /
/opt/scone/bin/scone fspf addr /fspf/fspf-file/fs.fspf /keycloak/ --authenticated --kernel /keycloak/
/opt/scone/bin/scone fspf addf /fspf/fspf-file/fs.fspf /keycloak/ /keycloak.mv /keycloak/
/opt/scone/bin/scone fspf addr /fspf/fspf-file/fs.fspf /usr/lib/jvm/ --authenticated --kernel /usr/lib/jvm/
/opt/scone/bin/scone fspf addf /fspf/fspf-file/fs.fspf /usr/lib/jvm/ /usr/lib/jvm.mv/ /usr/lib/jvm/
/opt/scone/bin/scone fspf encrypt /fspf/fspf-file/fs.fspf |tee /fspf/native-files/keytag

chmod +x /keycloak/bin/*.sh
chmod +x /usr/lib/jvm/java-21-openjdk/bin/*
chmod +x /usr/lib/jvm/java-21-openjdk/lib/jexec
chmod +x /usr/lib/jvm/java-21-openjdk/lib/jspawnhelper

echo "generated SCONE_FSPF_KEY=$(cat /fspf/native-files/keytag | awk '{print $11}')"
echo "generated SCONE_FSPF_TAG=$(cat /fspf/native-files/keytag | awk '{print $9}')"
echo "generated SCONE_FSPF=/fspf/fspf-file/fs.fspf"

rm -rf /fspf/native-files
rm -rf /keycloak.mv
rm -rf /usr/lib/jvm.mv
