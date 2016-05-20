import start
import os
import create_vol
import create_vm
import libvirt
import uuid
import reference_volume_xml as reference_xml
from randomChoice import randFunc
def vol_attach(volID,vid):
	print vid,volID
	print create_vm.vmList
	for i in create_vm.vmList:
		if i[0]==vid:
			vmname = i[1]
			pmID =i[3]+1
	Imagename = create_vol.mydir[volID-1]['name']
	HOSTNAME = os.getenv("HOSTNAME")
	connector="qemu+ssh://"+HOSTNAME+"/system"
	conn = libvirt.open(connector)
	domain=conn.lookupByName(vmname);
	VOLUME_LOCAL_XML = reference_xml.VOLUME_XML%("rbd",Imagename,HOSTNAME,randFunc())
	try:
		print VOLUME_LOCAL_XML
        	domain.attachDevice(VOLUME_LOCAL_XML)
        	return {"status": "1" }
    	except:
        	return {"status": "0"}
	

	
