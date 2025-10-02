#!/bin/bash

for modver in `cat requirements-py13.txt |grep -v "^#" |egrep -v '^lithops|^sm' |awk '{print $1}'`; do
  mod="`echo $modver |cut -d '<' -f 1 |cut -d '>' -f 1 |cut -d '=' -f 1`";
  ver="`echo $modver |cut -d '<' -f 2 |cut -d '>' -f 2 |cut -d '=' -f 2- |cut -d '=' -f 2`";
  chk="`pip list 2>/dev/null |grep -i -w ^$mod`";
  if [ -n "$chk" ]; then
    iver="`echo $chk |awk '{print $2}'`";
    if [[ "$iver" < "$ver" ]]; then
      echo "installed $mod, version $iver is less then $ver";
      echo "~~~~~ substitute for $modver";
      pip install --no-deps $modver;
    else
      echo "existing $modver. the $mod has $chk. keep it";
    fi;
  else
    echo "+++++ install $modver";
    pip install --no-deps $modver;
    pip list |grep -i -w $mod;
    echo "installed $modver:`pip list |grep -i -w $mod`";
  fi;
done;
pip uninstall -y psutil
