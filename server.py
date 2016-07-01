import httpServer

if __name__ == "__main__":
	hs = httpServer.HttpServer('', 50007, "/home/kalin/Python/PythonWebServer/serverFiles", 100)
	hs.run()
