
import flask
from EBauth import application

@application.route('/tests/users/public', methods = ['POST'])
@application.public
def public(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'test' , 'action' : 'public' })

@application.route('/tests/users/private', methods = ['POST'])
@application.authenticated
def private(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'test' , 'action' : 'private' })

@application.route('/tests/users/admin', methods = ['POST'])
@application.admin
def admin(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'test' , 'action' : 'admin' })

