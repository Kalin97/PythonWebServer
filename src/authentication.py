import httpObject
import base64

class Authentication:
	def __init__(self, httpObject):
		self.auth = False

		authUserPass = self.parseAuthHeader(httpObject)
		if authUserPass:
			username, password = authUserPass
			self.auth = self.authUser(username, password)

	def isGuest(self):
		return not self.auth

	def authUser(self, name, password):
		database = { "username": "password"}
		if name in database:
			return database[name] == password

		return False 

	def decode(self, encryptedPassword):
		return base64.b64decode(encryptedPassword)

	def parseAuthHeader(self, httpObject):
		field = httpObject.getHeaderField("Authorization")
		if not field:
			return None
		fields = field.split(" ", 1)
		if len(fields) < 2:
			return None

		encryptedPassword = fields[1]

		passwordUsername = self.decode(encryptedPassword)
		return passwordUsername.split(":")