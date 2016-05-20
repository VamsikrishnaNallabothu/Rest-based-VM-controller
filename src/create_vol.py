import os
import subprocess
import start

volID=0
mydir = {}
def create(attrs):
	name=attrs["name"]
	size=attrs["size"]
	actualsize=int(float(size)*(1024**3))
	try:
		global volID,mydir

#rbd.inst.create(ioctx,str(name),actualsize)
#		os.system("

		os.system("sudo rbd create " + name + " --size " + size + " -k /etc/ceph/ceph.client.admin.keyring");
		os.system("sudo modprobe rbd");
		os.system("sudo rbd map " + name + " --pool rbd --name client.admin -k /etc/ceph/ceph.client.admin.keyring");
#		os.system("sudo mkfs.ext4 -m0 /dev/rbd/rbd/" + name);
#		os.system("sudo mkdir /mnt/ceph-block-device" + volID );
#		os.system("sudo mount /dev/rbd/rbd/" + name + " /mnt/ceph-block-device" +volID);
		newd={}
		newd['name']=name;
		newd['size']=size;
		newd['status']="available";
		mydir[volID]=newd
		print mydir
		volID=volID+1
		return {"vmID" : volID}
	except:
		return {"vmID" : "0"}
	
