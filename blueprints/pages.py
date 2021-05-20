from flask import Blueprint, render_template, make_response, abort, url_for, request, json, redirect
from jinja2 import TemplateNotFound

pages = Blueprint('pages', __name__, url_prefix="/")


@pages.route("/")
def mainpage():
	try:
		devices = [{"id": "new", "name": "New"}, {"id": "4fbd", "name": "old", "password": "password"}]

		resp = make_response(render_template('mainpage.html'))
		resp.set_cookie('devices', json.dumps(devices))
		return resp
	except TemplateNotFound:
		abort(404)

@pages.route("/devices")
def devices():

	devices = json.loads(request.cookies.get('devices'))
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
	print("AHAHAHAHA")

	if request.method == 'POST':

		devices = json.loads(request.cookies.get('devices'))

		id = request.form['id']
		name = request.form['name']
		password = request.form['password']

		devices.append({"id": id, "name": name, "password": password})
		
		resp = make_response(redirect("/devices", code=302))
		resp.set_cookie('devices', json.dumps(devices))

		return resp
