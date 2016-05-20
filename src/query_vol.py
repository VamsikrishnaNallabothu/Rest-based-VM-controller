import libvirt
import get
import start
import create_vol
import create_vm
def query(volID):
	dic = {}
	try:
		temp = create_vol.mydir
		for keys in temp:
			if keys==volID-1:
				dic['volumeid'] = volID
				dic['name'] = temp[keys]['name']
				dic['size'] = temp[keys]['size']
				dic['status'] = temp[keys]['status']
				if dic['status'] == 'attached':
					dic['pmid'] = temp[keys]['pmid']
				break
		if dic == {} :
			return {"error" : "volumeid :" + volID +" does not exist"}
		else :
			return dic
	except:
		return {"error" : "volumeid :" + str(volID) +" does not exist"}

