import httpObject

class OperationHandler:
	def __init__(self):
		self.operations = [
			AddOperation()
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