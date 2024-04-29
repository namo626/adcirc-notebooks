SHELL := /bin/bash
NP = 20

INSTALL = /workspace/local/bin
BUILD = /workspace/adcirc-cg/build

all: adc-serial dg-serial coupling-serial
par: padcirc coupling

coupling-serial:
	cp $(BUILD)/adcirc-dg .
	if time ./adcirc-dg ; then \
		mv fort.61 fort.61.coupling; \
		mv fort.63 fort.63.coupling; \
		gprof ./adcirc-dg > coupling.prof; \
		conda run -n chg gprof2dot coupling.prof | dot -Tpng -Gdpi=300 -o coupling_prof.png; \
	fi

dg-serial:
	cp $(INSTALL)/dgswem_serial .
	time ./dgswem_serial
	mv fort.61 fort.61.dg
	mv fort.63 fort.63.dg
	gprof ./dgswem_serial > dg.prof

adc-serial:
	time adcirc
	mv fort.61 fort.61.adc

padcirc:
	rm -rf PE*
	adcprep --np $(NP) --partmesh
	adcprep --np $(NP) --prepall
	time mpirun -np $(NP) padcirc
	mv fort.61 fort.61.adc

coupling:
	rm -rf PE*
	cp /workspace/adcirc-cg/build/dadcprep .
	cp /workspace/adcirc-cg/build/padcirc-dg .
	./dadcprep --np $(NP) --partmesh
	./dadcprep --np $(NP) --prepall
	time mpirun -np $(NP) ./padcirc-dg
	mv fort.61 fort.61.coupling
