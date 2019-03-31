all:test
	
test:
	@python ./test_write.py
	diff Interface_gen*.f90
	diff ProfileTypes_gen*.f90
# 	diff ProfileTypesMin*.f90


clean:
	@rm -f *.h *.def *AutoTools.f90 *_gen.f90
