class HttpObjectParseException:
	def __init__(self, message):
		pass	

class HttpObject:
	def __init__(self, plainData = ""):
		self.valid = True
		self.methodType = ""
		self.params = {}
		self.body = plainData.split("\r\n\r\n", 1)[1] 
		self.httpVersion = "HTTP/1.1"
		self.headerFields = {}
		self.requestPath = ""
		self.message = "OK"
		self.code = 200 
		
		if not plainData == "":
			try:
				HttpObject.parseHttpRequest(self, plainData)
			except:
				raise HttpObjectParseException("Parsing error")

		if not self.getHeaderField("Content-Type"):
			self.setField("Content-Type", "text/plain")
	
	def getParams(self):
		return self.params

	def getMethodType(self):
		return self.methodType

	def getRequestPath(self):
		return self.requestPath

	def setBody(self, content):
		self.body = content

	def setField(self, key, value):
		self.headerFields[key] = value

	def IsValid(self):
		return self.valid

	def requestRecieved(self, requestPlain):
		bodyLength = len(requestPlain.split("\r\n\r\n", 1)[1])
		contentLength = self.getHeaderField("Content-Length")
		if contentLength == None:
			return True

		methodType = self.getMethodType()
		bodySended = contentLength == bodyLength
		return int(contentLength) == 0 or methodType not in "POST" or bodySended

	def getHeaderField(self, key):
		if key in self.headerFields:
			return self.headerFields[key]

		return None

	def getResponse(self):
		code = self.code
		httpVersion = self.httpVersion
		message = self.message

		if self.IsValid():
			contentType = self.headerFields["Content-Type"]
			contentLength = len(self.body)
	
			request = """{0} {1} {2}
Content-Type: {3}
Content-Length: {4}\r\n\r\n""".format(httpVersion, code, message, contentType, contentLength)
		else:
			request = "{0} {1} {2}".format(httpVersion, code, message)

		return request + self.body

	@staticmethod
	def parseHttpRequest(httpObject, plainData):
		header = plainData.split('\r\n\r\n', 1)[0]
		fields = header.split('\r\n')
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
		httpObject.methodType = methodType
		httpObject.params = HttpObject.parseParams(params)
		httpObject.httpVersion = firstLine[2]
		httpObject.headerFields = HttpObject.parseFields(fields)
		httpObject.requestPath = fullPath
		httpObject.code = 200 

		# host header required
		if httpObject.httpVersion == "HTTP/1.1" and not httpObject.getHeaderField("Host"):
			httpObject.code = 400
			httpObject.valid = False
			httpObject.message = "Bad Request"

		return httpObject

	@staticmethod
	def httpObjectWithCode(code, valid = True, message = "OK"):
		http = HttpObject()
		http.code = code
		http.valid = valid
		http.message = message

		return http

	@staticmethod
	def parseParams(plainParams):
		return { element.split("=", 1)[0]: element.split("=", 1)[1] for element in plainParams.split('&') if len(element.split("=", 1)) == 2 }
	
	@staticmethod
	def parseFields(fields):
		return { field.split(": ", 1)[0]: field.split(": ", 1)[1] for field in fields if len(field.split(": ", 1)) == 2 }
