#!/bin/bash          

numberTests=100000
numberConcurrency=1000
directory="/home/kalin/Python/PythonWebServer/testLogs/"
outputPrefix="threading"

echo "Starting first test 1/3"
( ab -r -A username:password -n $numberTests -c $numberConcurrency http://localhost:50007/index.html ) > $directory$outputPrefix"FirstTest.txt"
echo "Starting second test 2/3"
( ab -r -A username:password -n $numberTests -c $numberConcurrency http://localhost:50007/?first=5\&second=8 ) >  $directory$outputPrefix"SecondTest.txt"
echo "Starting third test 3/3"
( ab -r -A username:password -n $numberTests -c $numberConcurrency http://localhost:50007/programs/echoParameturs.py?fdsa=fdasfdas\&f=a\&b=a ) >  $directory$outputPrefix"ThirdTest.txt"