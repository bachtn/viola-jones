SETUP=setup.py

all:
	python3 $(SETUP) build_ext --inplace
	python3 src/main.py

check:
	python3 tests/integralImageTest.py
	python3 tests/haarTest.py
	python3 tests/dataTest.py

clean:
	$(RM) -r build
