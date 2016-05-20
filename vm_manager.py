import libvirt
import sys
import uuid
import subprocess

class Vm_manager:

    def __init__(self,qemu_url = None):
        self.qemu_url = "qemu:///system"
        self.con = ""
        self.vm_storage = "/var/lib/libvirt/images/vamsi.img"

    def virt_connection(self):
        self.conn = libvirt.open(self.qemu_url)
        if self.conn == None:
            print 'Failed to open connection to '+self.qemu_url


    def create_vm(self, name, ram, no_cpu, image_loc):
        str_out = self.create_xml(uuid.uuid4(), self.conn.getType().lower(), name, ram, no_cpu, image_loc , self.vm_storage)
        #str_out = self.create_xml_alt(1,uuid.uuid4(), name, ram, no_cpu, self.vm_storage)
        vm = self.conn.defineXML(str(str_out))
        vm.create()


    def close_conn(self):
        self.conn.close()

    def create_xml_alt(self,id, uuid, name, memory, cpu, img):
      xml = """<domain type='kvm' id='{0}'>
      <uuid>{1}</uuid>
      <name>{2}</name>
      <memory unit='KiB'>{3}</memory>
      <currentMemory unit='KiB'>{3}</currentMemory>
      <vcpu>{4}</vcpu>
      <features>
        <acpi/>
        <apic/>
        <pae/>
      </features>
      <clock offset='utc'/>
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>restart</on_crash>

      <devices>
          <disk type='file' device='cdrom'>
          <driver name='qemu' type='raw'/>
          <target dev='hda' bus='ide'/>
          </disk>

        <disk type='file' device='cdrom'>
          <driver name='qemu' type='raw'/>
          <source file='{5}'/>
          <target dev='hdc' bus='ide'/>
          <readonly/>
        </disk>
          <interface type='network'>  \
                    <source network='default'/>  \
                </interface>  \
                <on_crash>restart</on_crash>				\
                <graphics type='vnc' port='-1'/>  \
    </devices>
      <os>
      <type arch='i686' machine='pc'>hvm</type>
      <boot dev='cdrom'/>
      </os>
      </domain>""".format(id, uuid, name, memory, cpu, img)
      return xml

    def create_xml(_self, _uuid, arch, vm_name, memory, vcpu, image_location, storage_location):
        xml = "<domain type='" + str(arch) + "'>  \
                <uuid>" + str(_uuid)+ "</uuid> \
                <name>" + str(vm_name) + "</name>  \
                <memory>" + str(memory) + "</memory>  \
                <vcpu>" + str(vcpu) + "</vcpu>  \
                <os>  \
                    <type arch='x86_64' machine='pc'>hvm</type>  \
                    <boot dev='cdrom'/>  \
                </os>  \
                <devices>  \
                    <emulator>/usr/bin/qemu-system-x86_64</emulator>  \
                    <disk type='file' device='cdrom'>  \
                    <source file='" + str(image_location)+ "'/>  \
                  <target dev='hdc'/>  \
                  <readonly/>  \
                </disk>  \
                <disk type='file' device='disk'>  \
                    <source file='" + str(storage_location) + "'/>  \
                    <target dev='hda'/>  \
                </disk>  \
                <interface type='network'>  \
                    <source network='default'/>  \
                </interface>  \
                <on_crash>restart</on_crash>				\
                <graphics type='vnc' port='-1'/>  \
              </devices>  \
            </domain>"
        return xml


#vm = Vm_manager()
#vm.virt_connection()
#vm.create_vm("musunuru", 1097152, 1, "/home/CMPE284/Downloads/lubuntu-16.04-desktop-i386.iso")



class Vm_manger_vagrant:




    def __init__(self):
        pass

    def make_vagrant_file(self,data):

        vag_bottom_text = '''
        end'''

        vag_machine_config = '''
        config.vm.define "{node}" do |{node}|
        {node}.vm.hostname = "{node}"
        {node}.vm.network "public_network", auto_config: false,bridge: "wlan0"
        {node}.vm.provision "shell",
        run: "always",
        inline: "ifconfig eth1 {ip} netmask 255.255.255.0 up"
        config.vm.provider "virtualbox" do |v|
            v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
        end

        end
        '''.format(node=data["node"], ip=data["ip"])
        with open("Vagrantfile", "r") as f:
            vag_top_text = f.read()
        vag_top_text = vag_top_text[:vag_top_text.rfind('\n')]

        vag_text = vag_top_text+vag_machine_config+vag_bottom_text
        with open("Vagrantfile", "w") as f:
            f.write(vag_text)


    def create_vm(self,config=None):
        self.make_vagrant_file({"node":config["node_name"], "ip":config["ip"]})
        subprocess.check_output(["/home/CMPE284/mani_virt/cmpe284/vagrantup.sh", config["node_name"]])



#vm = Vm_manger_vagrant()
#vm.create_vm({"node_name":"node3", "ip":"192.168.0.97"})
