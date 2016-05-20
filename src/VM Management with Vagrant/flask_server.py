

from flask import Flask
from flask import request
import vm_thread
import subprocess
from vm_manager import Vm_manager

app = Flask(__name__)

@app.route('/createvm', methods=['GET'])
def createvm():
    type =  request.args.get('type')
    node_name = request.args.get('name')
    ip = request.args.get('ip')
    if type == "vagrant":
        config = {"node_name": node_name, "ip":ip}
        vm_thread.run_thread(config)
    else:
        vm = Vm_manager()
        vm.virt_connection()
        vm.create_vm(node_name, 1097152, 1, "/home/CMPE284/Downloads/vamsi/lubuntu-16.04-desktop-i386.iso")
    return "done submiting job for create"

@app.route('/listvm', methods=['GET'])
def listvm():
    out = subprocess.check_output(["/home/CMPE284/mani_virt/cmpe284/vagrantstatus.sh"])
    li = out.split("\n")
    count = 0
    st = ""
    for i in li:
        if i == "":
            count+=1
            if count == 2:
                break
        st = st+i+"\n"
    print st
    return st

@app.route('/killvm', methods=['GET'])
def killvm():
     name = request.args.get('name')
     print name
     out = subprocess.check_output(["/home/CMPE284/mani_virt/cmpe284/vagrantdestroy.sh", name])
     print out
     return "destroy vm"





if __name__ == '__main__':
    app.run()
