test:
	nosetests --verbose --with-coverage

run:
	python megamente.py

sugar:
	-pkill -9 Xephyr
	-sugar-runner --resolution 1200x900
