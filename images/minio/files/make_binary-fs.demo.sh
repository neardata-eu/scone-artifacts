#!/bin/bash

#####
##
## preparation of file shield
ls -l /proc/mounts

find /bin /etc /lib /sbin /usr /var -type f >>files.txt
echo /proc/mounts >>files.txt
echo /proc/self/mounts >>files.txt
echo /proc/7/mounts >>files.txt
echo /proc/8/mounts >>files.txt
echo /data >>files.txt
echo /minio_server.sh >>files.txt
cat files.txt |while read f; do echo " -i '$f' \\"; done >files.txt.formatted

echo "SCONE_PRODUCTION=0 SCONE_NO_TIME_THREAD=1 SCONE_NO_FS_SHIELD=1 SCONE_MODE=auto /opt/scone/bin/rust-cli binary-fs / / -v --host-path=/etc/resolv.conf \\">>script
cat files.txt.formatted >>script
echo " --host-path=/etc/hosts">>script
chmod +x script
./script

ls -l /binary_fs_blob.s
ls -l /binary_fs.blob
ls -l /libbinary_fs_template.a

