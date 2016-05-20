__author__ = 'musunuru'
import threading

from vm_manager import Vm_manger_vagrant

def create_vm(config):
    vm = Vm_manger_vagrant()
    vm.create_vm(config)


def run_thread(config):
    t = threading.Thread(target=create_vm, args=(config,))
    t.start()

