import libvirt
import create_vm
import get
import start
import os
import create_vol
def destroy(vid):
	try:
		cnt=0
		for i in create_vm.vmList:
			if i[0]==vid:
				break
			cnt=cnt+1
		machine=get.machine_list[i[3]]
		user=machine[0]
		ip=machine[1]
		print user	
		connect = libvirt.open(get.make_path(user,ip))
		req = connect.lookupByName(i[1])
		if req.isActive():
			req.destroy()
		req.undefine()
		del create_vm.vmList[cnt] 
		return {"status":"1"}
	
	except:
		return {"status":"0"}

