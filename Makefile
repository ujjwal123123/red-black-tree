test1e:
	python main.py < testcases/example1 | sdiff -WZi testcases/example1.output -

test2e:
	python main.py < testcases/example2 | sdiff -WZi testcases/example2.output -

test3e:
	python main.py < testcases/example3 | sdiff -WZi testcases/example3.output -

test1:
	python main.py < testcases/testcase1 | sdiff -WZi testcases/testcase1.output -

test2:
	python main.py < testcases/testcase2 | sdiff -WZi testcases/testcase2.output -

test3:
	python main.py < testcases/testcase3 | sdiff -WZi testcases/testcase3.output -

test4:
	python main.py < testcases/testcase4 | sdiff -WZi testcases/testcase4.output -