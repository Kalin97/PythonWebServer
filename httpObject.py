class HttpObjectParseException:
	pass

class HttpObject:
	def __init__(self, plainData):
		try:
			HttpObject.parseHttpRequest(self, plainData)
		except:
			raise HttpObjectParseException("Parsing error")

	def getParams(self):
		return self.params

	def setBody(self, content):
		self.body = content

	def getResponse(self):
		request = """HTTP/1.0 200 OK
Content-Type: text/plain
Content-Length: {0}
some-footer: some-value
another-footer: another-value

""".format(len(self.body))
		return request + self.body

	@staticmethod
	def parseHttpRequest(httpObject, plainData):
		header = plainData.split('\n\n', 1)[0]
		# requestBody = plainData.split('\n\n', 1)[1]
		fields = header.split('\n')
		firstLine = fields[0].split(' ')
		fields.pop(0) 
		splitedUrl = firstLine[1].split('?', 1)

		fullPath = ""
		params = ""

		if len(splitedUrl) >= 1:
			fullPath = splitedUrl[0]

		if len(splitedUrl) == 2:
			params = splitedUrl[1]

		# Parsing http
		httpObject.body = ""
		httpObject.methodType = firstLine[0]
		httpObject.params = { element.split("=", 1)[0]: element.split("=", 1)[1] for element in params.split('&') if len(element.split("=", 1)) == 2 }
		httpObject.httpVersion = firstLine[2]
		httpObject.headerFields = { field.split(": ", 1)[0]: field.split(": ", 1)[1] for field in fields if len(field.split(": ", 1)) == 2 }
		httpObject.requestPath = fullPath

		return httpObject