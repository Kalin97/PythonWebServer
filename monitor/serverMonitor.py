import subprocess
import time
import sys

LOG_FILE_NAME = 'monitorLogs/serverMemoryUsageLog.txt'

if __name__ == "__main__":
	tests = []
	try:
		while True:
			process = subprocess.Popen("ps -axo %mem,command | grep '\\bpython server.py'", shell=True, stdout=subprocess.PIPE)
			result = float(process.communicate()[0].split(" ", 2)[1])

			print(str(result) + "%")
			tests.append(result)
			time.sleep(1)
	except:
		print "Monitoring finished" 

	if len(tests) == 0:
		print "Was not able to track server.py, 0 results"
		sys.exit(1)

	maxMemory = max(tests)
	avgMemory = sum(tests) / float(len(tests))
	minMemory = min(tests)
	summaryInfo = "Memory usage:\nmax(%): {0}, avg(%): {1}, min(%): {2}".format(maxMemory, avgMemory, minMemory)
	with open(LOG_FILE_NAME, 'w') as f:
		f.write(summaryInfo)
