
import os
import md5
import boto3
import flask
import functools
import itsdangerous
import passlib.apps

class Server(flask.Flask):
	def __init__(self):
		print os.environ.keys()

		self.service = os.environ.get('SERVER_SERVICE')
		assert not self.service is None

		self.password_secret  = os.environ.get('SERVER_PASSWORD_SECRET')
		assert not self.password_secret is None

		self.token_secret  = os.environ.get('SERVER_TOKEN_SECRET')
		assert not self.token_secret is None

		aws_profile = os.environ.get('SERVER_AWS_PROFILE')
		aws_region = os.environ.get('SERVER_AWS_REGION', 'us-east-1')

		flask.Flask.__init__(self, self.service, template_folder='../templates')

		self.serializer = itsdangerous.TimedJSONWebSignatureSerializer('{}:{}'.format(self.service, self.token_secret), expires_in=3600) # expire after one hour

		if aws_profile is None:
			aws = boto3.session.Session(region_name=aws_region)
		else:
			aws = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)

		self.identities = aws.resource('dynamodb').Table('servers-identities')

	def __hash_password(self, password):
		return md5.new(password + self.password_secret).hexdigest()

	def __get_identity(self):
		auth = flask.request.authorization
		if auth is None:
			return None

		try:
			return self.serializer.loads(auth.username)
		except itsdangerous.SignatureExpired:
			return None # expired token
		except itsdangerous.BadSignature:
			identity = self.identities.get_item(Key={ 'service' : self.service , 'user': auth.username })

			if not 'Item' in identity:
				return None

			if not 'password' in identity['Item'] and auth.username == 'admin' and auth.password == self.password_secret:
				return { 'user' : identity['Item']['user'] , 'priviledges' : identity['Item']['priviledges'] }

			hashed_password = self.__hash_password(auth.password)

			print auth.password
			print hashed_password
			print identity['Item']['password']

			if hashed_password == identity['Item']['password']:
				return { 'user' : identity['Item']['user'] , 'priviledges' : identity['Item']['priviledges'] }

			return None

	def __add_auth(self, f, priviledge=None):
		@functools.wraps(f)
		def decorated(*args, **kwargs):
			identity = self.__get_identity()
			if ( not priviledge is None ) and ( ( identity is None ) or ( not priviledge in identity['priviledges'] ) ):
				return flask.Response(
				    'Could not verify your access priviledge for that URL.\n', 401,
				    { 'WWW-Authenticate' : 'Basic realm="Authentification Required"' }
				)
			else:
				kwargs.update({ 'identity' : identity })
				return f(*args, **kwargs)
		return decorated

	# Decorators for the two priviledges of authenfication

	def public(self, f):
		return self.__add_auth(f)

	def authenticated(self, f):
		return self.__add_auth(f, 'user')

	def admin(self, f):
		return self.__add_auth(f, 'admin')

	# 

	def get_token(self, identity=None):
		if identity is None:
			identity = self.__get_identity()

		if not identity is None:
			token = self.serializer.dumps(identity).decode('ascii')
		else:
			token = None

		return { 'token' : token }

	def add_user(self):
		if not 'user' in flask.request.form:
			return 'Missing field: "user"'
		else:
			user = flask.request.form['user']
			identity = self.identities.get_item(Key={ 'service' : self.service , 'user': user })
			if 'Item' in identity:
				return 'User {} already exist!'.format(user)

		if not 'password' in flask.request.form:
			return 'Missing field: "password"'
		else:
			password = self.__hash_password(flask.request.form['password'])

		print flask.request.form['password']
		print password

		if not 'priviledges' in flask.request.form:
			priviledges = [ 'user' ]
		else:
			priviledges = flask.request.form['priviledges'].split(',')

		self.identities.put_item(Item={ 'service' : self.service , 'user': user , 'password' : password , 'priviledges' : priviledges })

		return { 'user': user , 'priviledges' : priviledges }

	def delete_user(self):
		if not 'user' in flask.request.form:
			return 'Missing field: "user"'

		self.identities.delete_item(Key={ 'service' : self.service , 'user': user })

		return { 'user' : user }

