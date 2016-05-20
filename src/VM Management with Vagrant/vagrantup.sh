#!/bin/sh

cd /home/CMPE284/vagrant_playground/
rm -rf Vagrantfile
cp /home/CMPE284/mani_virt/cmpe284/Vagrantfile .
vagrant up $1