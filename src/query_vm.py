import libvirt
import create_vm
import get
import start
def query(vid):
	mydict={}
	try:
		for i in create_vm.vmList:
			if i[0]==vid:
				mydict['vmID']=i[0]
				mydict['name']=i[1]
				mydict['instance_type']=i[2]
				mydict['pmID']=i[3]+1
				break
		return mydict
	except:
		return mydict
