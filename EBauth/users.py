
import flask
from EBauth import application

@application.route('/users/token', methods = ['POST'])
@application.authenticated
def token(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'user' , 'action' : 'token' , 'data' : application.get_token(identity) })

@application.route('/users/add', methods = ['POST'])
@application.admin
def add(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'user' , 'action' : 'add' , 'data' : application.add_user() })


@application.route('/users/delete', methods = ['POST'])
@application.admin
def delete(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'user' , 'action' : 'delete' , 'data' : application.delete_user() })

