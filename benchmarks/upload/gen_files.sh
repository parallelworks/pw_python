#!/bin/bash

updir=$(cd $(dirname $0); /bin/pwd)
rm -rf $updir/files
mkdir $updir/files

unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   fallocate -l 1K $updir/files/1K.bin
   fallocate -l 1M $updir/files/1M.bin
   fallocate -l 100M $updir/files/100M.bin
   fallocate -l 2G $updir/files/2G.bin
   fallocate -l 4G $updir/files/4G.bin
   fallocate -l 10G $updir/files/10G.bin
elif [[ "$unamestr" == 'Darwin' ]]; then
#    mkfile 1K $updir/files/1K.bin
#    mkfile 1M $updir/files/1M.bin
#    mkfile 100M $updir/files/100M.bin
#    mkfile 2G $updir/files/2G.bin
   mkfile 4G $updir/files/4G.bin
#    mkfile 10G $updir/files/10G.bin
fi
