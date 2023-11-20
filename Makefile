default:
	chmod +x gatorLibrary
	pip install graphviz

test1e:
	./gatorLibrary < testcases/example1 | sdiff -WZi testcases/example1.output -

test2e:
	./gatorLibrary < testcases/example2 | sdiff -WZi testcases/example2.output -

test3e:
	./gatorLibrary < testcases/example3 | sdiff -WZi testcases/example3.output -

test1:
	./gatorLibrary < testcases/testcase1 | sdiff -WZi testcases/testcase1.output -

test2:
	./gatorLibrary < testcases/testcase2 | sdiff -WZi testcases/testcase2.output -

test3:
	./gatorLibrary < testcases/testcase3 | sdiff -WZi testcases/testcase3.output -

test4:
	./gatorLibrary < testcases/testcase4 | sdiff -WZi testcases/testcase4.output -