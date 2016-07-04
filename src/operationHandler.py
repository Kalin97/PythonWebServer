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

	def saveUserToDatabase(self, username, password):
		db = _mysql.connect(self.HOST, self.USERNAME, self.PASSWORD, self.DATABASE)
	#	try:
		db.query("INSERT INTO User(username, password) VALUES ('{}', '{}')".format(username, password))
	#	except _mysql.MySQLError:
#			raise self.RegisterOperationQueryError("Failed query")
       
        def canExecute(self, httpObject):
		return httpObject.getRequestPath() == "/register/"

        def execute(self, httpObject):
		self.saveUserToDatabase("TestingUsername", "TestingPassword")
                httpObject.setField("Content-Type", "text/plain")

		return "Successfuly registered"


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
