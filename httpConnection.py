import socket
import httpObject

class HttpConnectionReceiveException:
	pass
class HttpConnectionSendException:
	pass

class HttpConnection:
	def __init__(self, connection, address, bufsize = 1024):
		self.bufsize = bufsize
		self.connection = connection
		self.address = address

	def getAddress(self):
		return self.address

	def getData(self):
		try:
			plainData = self.connection.recv(self.bufsize)
		except socket.error:
			raise HttpConnectionReceiveException("Wans't able to receive data!")

		return httpObject.HttpObject(plainData)

	def sendData(self, httpObjectArg):
		plainData = httpObjectArg.getResponse()
		
		try:
			self.connection.sendall(plainData)
		except:
			raise HttpConnectionSendException

	def close(self):
		self.connection.close()
