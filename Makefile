SETUP=setup.py

all:
	python3 $(SETUP) build_ext --inplace
	python3 src/image.py

check:
	python3 tests/integralImageTest.py
	python3 tests/haarTest.py

clean:
	$(RM) -r build
