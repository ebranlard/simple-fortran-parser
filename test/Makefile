all:test
	
test:
	@python ./test_write.py
	diff Interface_gen*.f90
	diff ProfileTypes_gen*.f90
	diff ProfileAutoTools*.f90
	diff Interface*.h


clean:
	@rm -f *.h *.def *AutoTools.f90 *_gen.f90
