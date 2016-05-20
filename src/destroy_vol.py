import libvirt
import create_vm
import get
import start
import os
import create_vol
def destroy(vid):
	try:
#os.system("sudo umount /mnt/ceph-block-device" + vid)
		print create_vol.mydir[int(vid)-1]['name']
		os.system("sudo rbd unmap /dev/rbd/rbd/" + create_vol.mydir[int(vid)-1]['name'])
		os.system("sudo rbd rm " + create_vol.mydir[int(vid)-1]['name'])
		temp =  create_vol.mydir
		for keys in temp:
			if(keys == int(vid)-1):
				del temp[keys]
				break;
		return {"status":"1"}
		
	except:
		return {"status":"0"}
