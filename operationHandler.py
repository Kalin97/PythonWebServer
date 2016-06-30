import httpObject
import os.path
import subprocess
import re

class OperationHandler:
	def __init__(self, rootDirectory):
		self.rootDirectory = rootDirectory
		self.operations = [
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
			return "File not found"

		params = httpObject.getParams().values()

		return str(subprocess.check_output(["python", filePath] + params))
