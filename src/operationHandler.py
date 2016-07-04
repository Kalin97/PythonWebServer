import httpObject
import os.path
import subprocess
import re
import uuid
import _mysql	

class OperationHandler:
	def __init__(self, rootDirectory):
		self.rootDirectory = rootDirectory
		self.operations = [
			RegisterOperation(),
			UploadFileOperation(rootDirectory),
			PythonOperation(rootDirectory),
			AddOperation(),
			SendFileOperation(rootDirectory)
		]

	def handleHttpRequest(self, httpObject):
		for operation in self.operations:
			if operation.canExecute(httpObject):
				return operation.execute(httpObject) 

		return ""

class AddOperation:
	def canExecute(self, httpObject):
		params = httpObject.getParams()
		return len(params) == 2

	def execute(self, httpObject):
		params = httpObject.getParams()
		httpObject.setField("Content-Type", "text/plain")

		try:
			return str(int(params["first"]) + int(params["second"]))
		except:
			print "not valid accumulation input"

		return ""

class RegisterOperation: 
	class RegisterOperationQueryError:
		def __init__(self, message):
			pass	

	HOST 	 = "localhost"
	USERNAME = "kalin97"
	PASSWORD = "kalin97"
	DATABASE = "web_server"

	USERNAME_FIELD = "username"
	PASSWORD_FIELD = "password"

	def saveUserToDatabase(self, username, password):
		conn = _mysql.connect(self.HOST, self.USERNAME, self.PASSWORD, self.DATABASE)
		try:
			conn.query("INSERT INTO User({}, {}) VALUES ('{}', '{}')".format(self.USERNAME_FIELD, self.PASSWORD_FIELD, username, password))
		except _mysql.MySQLError:
			raise self.RegisterOperationQueryError("Failed query")
       		finally:
			if conn:
				conn.close()
		 
	def canExecute(self, httpObject):
		return httpObject.getRequestPath() in "/register/"

        def execute(self, httpObject):
		params = httpObject.getParams()
		httpObject.setField("Content-Type", "text/plain")

		if self.USERNAME_FIELD in params and self.PASSWORD_FIELD in params:
			self.saveUserToDatabase(params[self.USERNAME_FIELD], params[self.PASSWORD_FIELD])
			return "Successfuly registered"
		else:
			return "Unvalid data"


class UploadFileOperation:
        def __init__(self, rootDirectory):
                self.rootDirectory = rootDirectory

        def canExecute(self, httpObject):
		return httpObject.getRequestPath() == "/upload/"

        def execute(self, httpObject):
		uploadDirectory = self.rootDirectory + "/upload/"
                httpObject.setField("Content-Type", "text/plain")

		requestBody = httpObject.body
		fileContent = requestBody.split("\r\n\r\n", 1)[1].split("------WebKitFormBoundary", 1)[0] 
		
		fileName = str(uuid.uuid4())
		with open(uploadDirectory + fileName, "wb") as file:
			file.write(fileContent)

		return "Successfuly uploaded"

class SendFileOperation:
	def __init__(self, rootDirectory):
		self.rootDirectory = rootDirectory

	def canExecute(self, httpObject):
		return not (httpObject.getRequestPath() in ("", "/"))

	def getFileContentType(self, filePath):
		contentType = str(subprocess.check_output(["file", "--mime-type", filePath]))
		contentType = re.sub(r'.+: ', '', contentType)
		contentType = re.sub('\n', '', contentType)
		return contentType

	def execute(self, httpObject):
		filePath = self.rootDirectory + "/" + httpObject.getRequestPath()

		if not os.path.exists(filePath):
			httpObject.setField("Content-Type", "text/plain")
			return "File not found"

		fileContent = ""

		with open(filePath, "rb") as file:
			byte = file.read(1)
			while byte != "":
				fileContent += byte
				byte = file.read(1)
			
		httpObject.setField("Content-Type", self.getFileContentType(filePath))

		return fileContent

class PythonOperation:
	def __init__(self, rootDirectory):
		self.rootDirectory = rootDirectory

	def canExecute(self, httpObject):
		return re.match(".+\.py", httpObject.getRequestPath())

	def execute(self, httpObject):
		filePath = self.rootDirectory + "/" + httpObject.getRequestPath()

		if not os.path.exists(filePath):
			httpObject.setField("Content-Type", "text/plain")
			return "File not found"

		params = httpObject.getParams().values()

		return str(subprocess.check_output(["python", filePath] + params))
