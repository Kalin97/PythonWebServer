import socket
import httpConnection

class HttpSocketCreateException:
	pass
class HttpSocketAcceptException:
	pass

class HttpSocket:
	def __init__(self, hostname, port, maxQuerySize = 5):
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind((hostname, port))
			self.socket.listen(maxQuerySize)
		except socket.error:
			raise HttpSocketCreateException("Wasn't able to create socket!")

	def accept(self):
		try:
			conn, addr = self.socket.accept()
		except socket.error:
			raise HttpSocketAcceptException("Wasn't able to accept connection!")

		return httpConnection.HttpConnection(conn, addr)
