import authentication
import socket
import httpObject
import re

class HttpConnectionReceiveException:
	def __init__(self, message):
		pass
class HttpConnectionSendException:
	def __init__(self, message):
		pass

class HttpConnection:
	def __init__(self, connection, address, bufsize = 1024):
		self.bufsize = bufsize
		self.connection = connection
		self.address = address

	def getAddress(self):
		return self.address

	def getData(self):
		plainData = ""
		try:
			plainData = self.receiveHeader()
			request = httpObject.HttpObject(plainData)

			if not request.requestRecieved(plainData):
				data = self.connection.recv(self.bufsize)
				plainData += data

			# auth = authentication.Authentication(request)
			# if auth.isGuest():
			# 	return httpObject.HttpObject.httpObjectWithCode(401, False, "Access Denied")

		except socket.error:
			raise HttpConnectionReceiveException("Wans't able to receive data!")

		return httpObject.HttpObject(plainData)

	def receiveHeader(self):
		plainData = ""
		while "\r\n\r\n" not in plainData:
			data = self.connection.recv(self.bufsize)
			plainData += data

		return plainData

	def sendData(self, httpObjectArg):
		plainData = httpObjectArg.getResponse()
		
		try:
			self.connection.sendall(plainData)
		except:
			raise HttpConnectionSendException("Wasn't able to send data")

	def close(self):
		self.connection.close()

	def __del__(self):
		if self.connection: self.close()
