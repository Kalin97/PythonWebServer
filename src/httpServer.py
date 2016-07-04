import socket
import httpConnection
import httpObject
import operationHandler
import threading
import os
import sys

class HttpSocketCreateException:
	def __init__(self, message):
		pass	
class HttpSocketAcceptException:
	def __init__(self, message):
		pass

class HttpServer:
	def __init__(self, hostname, port, rootDirectory, maxQuerySize = 5):
		self.acceptedConnections = 0
		self.handler = operationHandler.OperationHandler(rootDirectory)
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind((hostname, port))
			self.socket.listen(maxQuerySize)
		except socket.error:
			raise HttpSocketCreateException("Wasn't able to create socket!")

	def run(self):
		while True: 
			self.accept()
			self.acceptedConnections += 1

	def accept(self):
		try:
			conn, addr = self.socket.accept()
			connection = httpConnection.HttpConnection(conn, addr)

			# self.processConnection(connection)
			self.threadConnection(connection)
		except socket.error:
			raise HttpSocketAcceptException("Wasn't able to accept connection!")

	def threadConnection(self, connection):
		thread = threading.Thread(target = self.httpSession, args = (connection, ))
		thread.setDaemon(True)
		thread.start()

	def processConnection(self, connection):
		newpid = os.fork()
		if newpid == 0:
			self.httpSession(connection)
			sys.exit()

	def httpSession(self, httpConnection):
		httpObject = httpConnection.getData()
		response = ""
		if httpObject.IsValid():
			response = self.handler.handleHttpRequest(httpObject)

		httpObject.setBody(response)
		httpConnection.sendData(httpObject)
		httpConnection.close()

	def __del__(self):
		print "Accepted connections " + str(self.acceptedConnections)
		if self.socket:	self.socket.close()
