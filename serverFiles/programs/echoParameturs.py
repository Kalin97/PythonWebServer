import sys

result = ""

for arg in sys.argv[1::]:
	result += str(arg) + "-"

sys.stdout.write(result)
sys.stdout.flush()

