import socket
import httpConnection
import httpObject
import operationHandler
import threading

class HttpSocketCreateException:
	pass
class HttpSocketAcceptException:
	pass

class HttpServer:
	def __init__(self, hostname, port, rootDirectory, maxQuerySize = 5):
		self.handler = operationHandler.OperationHandler(rootDirectory)
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind((hostname, port))
			self.socket.listen(maxQuerySize)
		except socket.error:
			raise HttpSocketCreateException("Wasn't able to create socket!")

	def run(self):
		while True: self.accept()

	def accept(self):
		try:
			conn, addr = self.socket.accept()
			connection = httpConnection.HttpConnection(conn, addr)

			thread = threading.Thread(target = self.httpSession, args = (connection, ))
			thread.setDaemon(True)
			thread.start()
		except socket.error:
			raise HttpSocketAcceptException("Wasn't able to accept connection!")

	def httpSession(self, httpConnection):
		httpObject = httpConnection.getData()
		response = self.handler.handleHttpRequest(httpObject)
		httpObject.setBody(response)
		httpConnection.sendData(httpObject)
		httpConnection.close()

	def __del__(self):
		if self.socket:	self.socket.close()
