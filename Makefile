
clean:
	rm -rf build dist *.egg-info

build:
	python setup.py bdist_wheel --universal

publish:
	twine upload dist/*
