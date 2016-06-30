class HttpObjectParseException:
	pass

class HttpObject:
	def __init__(self, plainData):
		# try:
		HttpObject.parseHttpRequest(self, plainData)
		# except:
		# 	raise HttpObjectParseException("Parsing error")

		self.setField("Content-Type", "text/plain")

	def getParams(self):
		return self.params

	def getRequestPath(self):
		return self.requestPath

	def setBody(self, content):
		self.body = content

	def setField(self, key, value):
		self.headerFields[key] = value

	def getResponse(self):
		contentType = self.headerFields["Content-Type"]
		contentLength = len(self.body)

		request = """HTTP/1.0 200 OK
Content-Type: {0}
Content-Length: {1}\r\n\r\n""".format(contentType, contentLength)
		return request + self.body

	@staticmethod
	def parseHttpRequest(httpObject, plainData):
		header = plainData.split('\r\n\r\n', 1)[0]
		# requestBody = plainData.split('\n\n', 1)[1]
		fields = header.split('\n')
		firstLine = fields[0].split(' ')
		methodType = firstLine[0]
		fields.pop(0) 
		splitedUrl = firstLine[1].split('?', 1)

		fullPath = ""
		params = ""

		if len(splitedUrl) >= 1:
			fullPath = splitedUrl[0]

		if methodType == "GET" and len(splitedUrl) == 2:
			params = splitedUrl[1]
		elif methodType == "POST":
			params = plainData.split("\r\n\r\n", 1)[1]

		# Parsing http
		httpObject.body = ""
		httpObject.methodType = methodType
		httpObject.params = { element.split("=", 1)[0]: element.split("=", 1)[1] for element in params.split('&') if len(element.split("=", 1)) == 2 }
		httpObject.httpVersion = firstLine[2]
		httpObject.headerFields = { field.split(": ", 1)[0]: field.split(": ", 1)[1] for field in fields if len(field.split(": ", 1)) == 2 }
		httpObject.requestPath = fullPath

		return httpObject