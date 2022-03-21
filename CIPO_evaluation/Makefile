all:
    # install pycocotools locally
	python3 setup.py build_ext --inplace
	rm -rf build

install:
	# install pycocotools to the Python site-packages
	python3 setup.py build_ext install
	rm -rf build

clean:
	rm -rf build
	rm -rf pycocotools.egg-info/
	rm -rf dist/
	rm pycocotools/_mask.cpython-38-x86_64-linux-gnu.so
	rm pycocotools/_mask.pyx