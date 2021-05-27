from flask import Blueprint, render_template, make_response, abort, url_for, request, json, redirect
from jinja2 import TemplateNotFound

pages = Blueprint('pages', __name__, url_prefix="/")


@pages.route("/")
def mainpage():
	try:
		return render_template('mainpage.html')
	except TemplateNotFound:
		abort(404)

@pages.route("/devices")
def devices():

	try:
		devices = json.loads(request.cookies.get('devices'))
	except TypeError:
		resp = make_response(redirect("/devices", code=302))
		resp.set_cookie('devices', json.dumps([{"id":"new", "alias":"New"}]))

		return resp

	id = request.args.get("id")

	if id == None:
		try:
			return render_template('devices.html', devices=devices)
		except TemplateNotFound:
			abort(404)
	elif id == 'new':
		try:
			return render_template('new_device.html')
		except TemplateNotFound:
			abort(404)
	else:
		try:
			dev = next(filter(lambda dev: dev.get('id') == id, devices))
		except StopIteration:
			return redirect("/devices", code=302)	

		try:
			return render_template('device_control.html', dev=dev)
		except TemplateNotFound:
			abort(404)

@pages.route("/add_device", methods = ['POST'])
def add_device():
	if request.method == 'POST':

		devices = json.loads(request.cookies.get('devices'))

		id = request.form['id']
		alias = request.form['alias']
		username = request.form['username']
		password = request.form['password']

		#if id is empty - redirect them back to the form
		if id == '':
			return redirect("/devices?id=new", code=302)

		#IF no alias is specified, use id
		if alias == '':
			alias = id

		#if the device already exists - delete it first (thus updating it)
		try:
			dev = next(filter(lambda dev: dev.get('id') == id, devices))
			devices.remove(dev)
		except StopIteration:
			pass

		devices.append({"id": id, "alias": alias, "username": username, "password": password})
		
		resp = make_response(redirect("/devices", code=302))
		resp.set_cookie('devices', json.dumps(devices))

		return resp

@pages.route("/remove_device")
def remove_device():
	
	devices = json.loads(request.cookies.get('devices'))
	id = request.args.get("id")

	try:
		dev = next(filter(lambda dev: dev.get('id') == id, devices))
	except StopIteration:
		return redirect("/devices", code=302)

	devices.remove(dev)
		
	resp = make_response(redirect("/devices", code=302))
	resp.set_cookie('devices', json.dumps(devices))

	return resp