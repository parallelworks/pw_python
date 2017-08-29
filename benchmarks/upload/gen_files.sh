#!/bin/bash

updir=$(cd $(dirname $0); /bin/pwd)
rm -rf $updir/files
mkdir $updir/files

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   fallocate -l 1K files/1K.txt
   fallocate -l 1M files/1M.txt
   fallocate -l 100M files/100M.txt
   fallocate -l 2G files/2G.txt
   fallocate -l 4G files/4G.txt
   fallocate -l 10G files/10gG.txt
elif [[ "$unamestr" == 'Darwin' ]]; then
   mkfile 1K files/1K.txt
   mkfile 1M files/1M.txt
   mkfile 100M files/100M.txt
   mkfile 2G files/2G.txt
   mkfile 4G files/4G.txt
   mkfile 10G files/10gG.txt
fi
