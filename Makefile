default:
	chmod +x gatorLibrary.py

test1e:
	python3 gatorLibrary.py < testcases/example1 | sdiff -WZi testcases/example1.output -

test2e:
	python3 gatorLibrary.py < testcases/example2 | sdiff -WZi testcases/example2.output -

test3e:
	python3 gatorLibrary.py < testcases/example3 | sdiff -WZi testcases/example3.output -

test1:
	python3 gatorLibrary.py < testcases/testcase1 | sdiff -WZi testcases/testcase1.output -

test2:
	python3 gatorLibrary.py < testcases/testcase2 | sdiff -WZi testcases/testcase2.output -

test3:
	python3 gatorLibrary.py < testcases/testcase3 | sdiff -WZi testcases/testcase3.output -

test4:
	python3 gatorLibrary.py < testcases/testcase4 | sdiff -WZi testcases/testcase4.output -