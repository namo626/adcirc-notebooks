SHELL := /bin/bash
NP = 2

INSTALL = /workspace/local/bin

all: adc-serial dg-serial coupling-serial
par: padcirc coupling
copy: 
	cp ../../build/adcirc-dg .

coupling-serial: copy
	cp ../../build/adcirc-dg .
	if time ./adcirc-dg --solver 1 ; then \
		mv fort.61 fort.61.coupling; \
		mv fort.63 fort.63.coupling; \
		#gprof ./adcirc-dg > coupling.prof; \
		# conda run -n chg gprof2dot coupling.prof | dot -Tpng -Gdpi=300 -o coupling_prof.png; \
	fi

dg-serial:
	cp $(INSTALL)/dgswem_serial .
	time ./dgswem_serial
	mv fort.61 fort.61.dg
	mv fort.63 fort.63.dg
	gprof ./dgswem_serial > dg.prof

adc-serial: copy
	time ./adcirc-dg --solver 0
	mv fort.61 fort.61.adc

p0: copy
	time ./adcirc-dg --solver 2
	mv fort.61 fort.61.p0

padcirc:
	rm -rf PE*
	adcprep --np $(NP) --partmesh
	adcprep --np $(NP) --prepall
	time mpirun -np $(NP) padcirc
	mv fort.61 fort.61.adc

coupling:
	rm -rf PE*
	dadcprep --np $(NP) --partmesh
	dadcprep --np $(NP) --prepall
	time mpirun -np $(NP) padcirc-dg
	mv fort.61 fort.61.coupling
