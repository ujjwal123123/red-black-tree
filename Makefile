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

diagrams:
	pyreverse -o png -d images -p gatorLibrary gatorLibrary.py
	pyreverse -o png -d images -p heap heap.py
	pyreverse -o png -d images -p tree tree.py
	pyreverse -o png -d images -p all gatorLibrary.py heap.py tree.py

pdf:
	pandoc -o README.pdf README.md --pdf-engine=tectonic

zip:
	zip -r Ujjwal_Goel.zip gatorLibrary.py heap.py tree.py Makefile README.pdf requirements.txt