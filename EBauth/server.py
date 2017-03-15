
import os
import md5
import boto3
import flask
import functools
import itsdangerous
import passlib.apps

class Server(flask.Flask):
	def __init__(self):
		# Connection to AWS 
		aws_profile = os.environ.get('AWS_PROFILE')
		aws_region = os.environ.get('AWS_REGION', 'us-east-1')
		if aws_profile is None:
			aws = boto3.session.Session(region_name=aws_region)
		else:
			aws = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)

		# Get service descrition
		service = os.environ.get('SERVER_SERVICE')
		assert not service is None
		service = aws.resource('dynamodb').Table('services').get_item(Key={ 'service' : service })
		assert 'Item' in service
		self.service = service['Item']

		# Get DynamoDB' identities table
		self.identities = aws.resource('dynamodb').Table('identities')

		# Initialize parent class: Flask
		flask.Flask.__init__(self, self.service['service'], template_folder='../templates')

		# Token serializer and encoding lambda
		self.serializer = itsdangerous.TimedJSONWebSignatureSerializer(self.service['token']['secret'], expires_in=int(self.service['token']['timeout']))
		self.tokenize = lambda X: None if X is None else self.serializer.dumps(X).decode('ascii')

		# lambda to salt passwords
		self.salted = lambda pwd: md5.new(pwd + self.service['password']['secret']).hexdigest()

	# Authentication method: check for token first then lookup identities table

	def __get_identity(self):
		if 'token' in flask.request.form:
			token = flask.request.form['token']
			auth  = None
		elif not flask.request.authorization is None:
			auth = flask.request.authorization
			token = auth.username
		else:
			return None

		try:
			# Try to decode the token/username
			return self.serializer.loads(token)

		except itsdangerous.SignatureExpired:
			# Expired token
			return None

		except itsdangerous.BadSignature:
			# Not a valid token
			if not auth is None:
				# check identities table
				identity = self.identities.get_item(Key={ 'service' : self.service['service'] , 'user': auth.username })
				if 'Item' in identity and self.salted(auth.password) == identity['Item']['password']:
					# User exists and password is correct
					return { 'user' : identity['Item']['user'] , 'priviledges' : identity['Item']['priviledges'] }

			# No auth field, user not found, or password does not match
			return None

	# Decorators for authenfication (with priviledges)

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

	def public(self, f):
		return self.__add_auth(f)

	def authenticated(self, f):
		return self.__add_auth(f, 'user')

	def admin(self, f):
		return self.__add_auth(f, 'admin')

	# Authentication Token

	def get_token(self, identity=None):
		if identity is None:
			identity = self.__get_identity()

		return { 'token' : self.tokenize(identity) }

	# User management

	def add_user(self):
		if not 'user' in flask.request.form:
			return 'Missing field: "user"'
		else:
			user = flask.request.form['user']
			identity = self.identities.get_item(Key={ 'service' : self.service['service'] , 'user': user })
			if 'Item' in identity:
				return 'User {} already exist!'.format(user)

		if not 'password' in flask.request.form:
			return 'Missing field: "password"'
		else:
			password = self.salted(flask.request.form['password'])

		if not 'priviledges' in flask.request.form:
			priviledges = [ 'user' ]
		else:
			priviledges = flask.request.form['priviledges'].split(',')

		self.identities.put_item(Item={ 'service' : self.service['service'] , 'user': user , 'password' : password , 'priviledges' : priviledges })

		return { 'user': user , 'priviledges' : priviledges }

	def delete_user(self):
		if not 'user' in flask.request.form:
			return 'Missing field: "user"'

		self.identities.delete_item(Key={ 'service' : self.service['service'] , 'user': user })

		return { 'user' : user }

