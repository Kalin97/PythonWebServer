import subprocess
import time

LOG_FILE_NAME = 'monitorLogs/serverMemoryUsageLog.txt'

if __name__ == "__main__":
	tests = []
	try:
		while True:
			process = subprocess.Popen("ps -axo %mem,command | grep -E '\\bpython server.py'", shell=True, stdout=subprocess.PIPE)
			result = float(process.communicate()[0].split(" ", 2)[1])

			print(str(result) + "%")
			tests.append(result)
			time.sleep(1)
	except:
		print "Unexpected end, test will be saved"


	maxMemory = max(tests)
	avgMemory = sum(tests) / float(len(tests))
	minMemory = min(tests)
	summaryInfo = "Memory usage:\nmax(%): {0}, avg(%): {1}, min(%): {2}".format(maxMemory, avgMemory, minMemory)
	with open(LOG_FILE_NAME, 'w') as f:
		f.write(summaryInfo)