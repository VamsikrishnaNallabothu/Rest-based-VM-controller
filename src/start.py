#!/usr/bin/env python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import sys
import create_vm
import create_vol
import get
import destroy_vm
import destroy_vol
import query_vm
import rados
import attach_vol
#from bson.objectid import ObjectId
app = Flask(__name__)

@app.route('/server/vm/create/' , methods = ['GET'])
def request_create():
	vm={}
	vm['name']=request.args.get('name')
	vm['instance_type']=request.args.get('instance_type')
	vm['image_id']=request.args.get('image_id')
	return jsonify(create_vm.create(vm))

@app.route('/server/vm/destroy/' , methods = ['GET'])
def request_destroy():
	vmID=request.args.get('vmID')
	return jsonify(destroy_vm.destroy(int(vmID)))

@app.route('/server/vm/query/' , methods = ['GET'])
def request_query():
	vmID=request.args.get('vmID')
	return jsonify(query_vm.query(int(vmID)))

@app.route('/server/vm/types/')
def request_types():
	return jsonify(create_vm.vm_type())

@app.route('/server/vm/image/list')
def request_imagelist():
	return jsonify(create_vm.List_Images())

@app.route('/server/volume/create/')
def request_volume():
	vm={}
	vm['name']=request.args.get('name')
	vm['size']=request.args.get('size')
	return jsonify(create_vol.create(vm))

@app.route('/server/volume/query', methods = ['GET'])
def request_volume_info():
	volID = request.args.get('volumeid')
	return jsonify(query_vol.query(volID))
	
@app.route('/server/volume/destroy/' , methods = ['GET'])
def delete_volume():
	volID=request.args.get('volumeid')
	return jsonify(destroy_vol.destroy(volID))

@app.route('/server/volume/attach/' , methods = ['GET'])
def request_attach():
	volID=request.args.get('volumeid')
	vmID=request.args.get('vmID')
	return jsonify(attach_vol.vol_attach(int(volID),int(vmID)));

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Format: ./script pm_file image_file"
		exit(1)

	get.create_machines(sys.argv[1])
	get.create_images(sys.argv[2])
	get.CreateTypes(sys.argv[3])
   	app.run(debug = True)
	
