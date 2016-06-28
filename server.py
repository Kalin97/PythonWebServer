import httpSocket
import httpConnection
import httpObject
import operationHandler

if __name__ == "__main__":
	httpServer = httpSocket.HttpSocket('', 50007)
	handler = operationHandler.OperationHandler()

	while True:
		httpConnection = httpServer.accept()

		httpObject = httpConnection.getData()

		response = handler.handleHttpRequest(httpObject)

		httpObject.setBody(response)

		httpConnection.sendData(httpObject)

		httpConnection.close()
