SETUP=setup.py

all:
	python3 $(SETUP) build_ext --inplace
	python3 src/image.py

check:
	python3 tests/integralImageTest.py

clean:
	$(RM) -r build
