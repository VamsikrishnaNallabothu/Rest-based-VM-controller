import libvirt
import os
import get
import start
from random import random
from uuid import uuid4
import subprocess

pmID=0
vmID=0
vmList=[]
	
def create_xml(vm_name, hypervisor,uid,path,ram,cpu,emulator_path,emulator1,arch_type):
   xml=r"<domain type='qemu"+r"'>\
      <name>"+vm_name+r"</name>\
      <memory>"+ ram +r"</memory>\
      <vcpu>"+cpu+r"</vcpu>\
      <os>\
        <type arch='x86_64' machine='pc-1.0'>hvm</type>\
        <boot dev='hd'/>\
      </os>\
      <features>\
        <acpi/>\
        <apic/>\
        <pae/>\
      </features>\
      <clock offset='utc'/>\
      <on_poweroff>destroy</on_poweroff>\
      <on_reboot>restart</on_reboot>\
      <on_crash>restart</on_crash>\
      <devices>\
        <emulator>/usr/bin/qemu-system-x86_64</emulator>\
        <disk type='file' device='disk'>\
          <driver name='qemu' type='raw'/>\
		<source file='" + path + "'/>		\
          <target dev='hda' bus='ide'/>\
          <alias name='ide0-0-0'/>\
          <address type='drive' controller='0' bus='0' unit='0'/>\
        </disk>\
        <controller type='ide' index='0'>\
          <alias name='ide0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>\
        </controller>\
        <serial type='pty'>\
          <source path='/dev/pts/2'/>\
          <target port='0'/>\
          <alias name='serial0'/>\
        </serial>\
        <console type='pty' tty='/dev/pts/2'>\
          <source path='/dev/pts/2'/>\
          <target type='serial' port='0'/>\
          <alias name='serial0'/>\
        </console>\
        <input type='mouse' bus='ps2'/>\
        <graphics type='vnc' port='5900' autoport='yes'/>\
        <sound model='ich6'>\
          <alias name='sound0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>\
        </sound>\
        <video>\
          <model type='cirrus' vram='9216' heads='1'/>\
          <alias name='video0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>\
        </video>\
        <memballoon model='virtio'>\
          <alias name='balloon0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>\
        </memballoon>\
      </devices>\
      <seclabel type='dynamic' model='apparmor' relabel='yes'>\
        <label>libvirt-10a963ef-9458-c30d-eca3-891efd2d5817</label>\
        <imagelabel>libvirt-10a963ef-9458-c30d-eca3-891efd2d5817</imagelabel>\
      </seclabel>\
    </domain>"

		
   return xml 

def create(attrs):
	global pmID,vmID,vmList

	#Attributes to XML
	name=attrs["name"]
	instance_type = int(attrs["instance_type"])
	image_id=attrs["image_id"]
	Image_name = image_id + ".img"
	Ram=get.Desc['types'][instance_type-1]['ram']
	Ram = Ram * 1024
	vcpu=int(get.Desc['types'][instance_type-1]['cpu'])
	counter = 1 
	machine = get.machine_list[pmID]

	# Get path for user machine
	user = machine[0]
	ip = machine[1]

	#Check free space in cpu
	free_cpu=int(subprocess.check_output("ssh " + user + "@" + ip + " nproc" ,shell=True))

	#Free space in machine
	avail_space=(subprocess.check_output("ssh " + user + "@" + ip + " free -m" ,shell=True))
	avail_space=avail_space.split("\n")
	avail_space=avail_space[1].split()
	avail_ram=int(avail_space[3])	
	avail_ram = avail_ram * 1024

	try:
		temp = (subprocess.check_output("ssh " + user + "@" + ip + " cat /proc/cpuinfo | grep lm " ,shell=True))
		bits = '64'
	except:
		bits = '32'
	
	os_arch = (((get.img_list[int(image_id)-1])[-1]).split('amd')[-1]).split('.')[0]

	while(free_cpu < vcpu or avail_ram < Ram or int(bits) < int(os_arch)):
		pmID=(pmID+1)%(len(get.machine_list))
		counter=counter+1
		if(counter > len(get.machine_list)):
			return {"Error" : " Specifications could not be satisfied, Virtual Machine cannot be created" }
		machine = get.machine_list[pmID]
		user = machine[0]
		ip = machine[1]


		free_cpu = int(subprocess.check_output("ssh " + user + "@" + ip + " nproc" ,shell=True))

		avail_space = (subprocess.check_output("ssh " + user + "@" + ip + " free -m" ,shell=True))
		avail_space = avail_space.split("\n")
		avail_space = avail_space[1].split()
		avail_ram = int(avail_space[3])	
		avail_ram = avail_ram * 1024

		os_arch = (((get.img_list[int(image_id)-1])[-1]).split('amd')[-1]).split('.')[0]
	
	vmID = vmID+1
	vmList.append([vmID,name,instance_type,pmID])
	pmID = (pmID+1)%(len(get.machine_list))
	uid = str(uuid4())
#try:
#		os.path.exists("~/"+Image_name+"/")
#	except:
	get.scp_img_path(int(image_id))
#		print Image_name

	Image_path = "/home/" + user + "/" + Image_name
	os.system("scp ~/" + Image_name + " " +  user + "@" + ip + ":" + Image_path + " 2> /dev/null")	

	connect = libvirt.open(get.make_path(user, ip))

	system_info = connect.getCapabilities()
	emulator_path = system_info.split("emulator>")
	emulator_path = emulator_path[1].split("<")[0] #location of xen/qemu
#	print emulator_path
	emulator1 = system_info.split("<domain type=")
	emulator1 = emulator1[1].split(">")[0] #type of emulator present on given machine xen/qemu
#	print emulator1
	arch_type = system_info.split("<arch>")
	arch_type = arch_type[1].split("<")[0] #archituctue of machine print arch_type


	req = connect.defineXML(create_xml(name, connect.getType().lower(),uid,Image_path,str(Ram),str(vcpu),emulator_path,emulator1,arch_type))
	try:
		req.create()
		return {"vmID": vmID}
	except:
		return {"vmID" : 0 }

def vm_type():
	return get.Desc

def image_list():
	print_imglist = []
	for i in get.image_list:
		mydict = {}
		mydict['id'] = i[0]
		mydict['name'] = i[1].split('.')[0]
		print_imglist.append(mydict)

	return {"Images" : print_imglist }
	
	 
