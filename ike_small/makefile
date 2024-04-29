SHELL := /bin/bash
NP = 22

INSTALL = /workspace/local/bin

all: adc-serial dg-serial coupling-serial
par: padcirc coupling

copy:
	cp ../../build/adcirc-dg .
	cp ../../build/padcirc-dg .
	cp ../../build/dadcprep .

coupling-serial:
	cp ../../build/adcirc-dg .
	if time ./adcirc-dg ; then \
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

adc-serial:
	time adcirc
	mv fort.61 fort.61.adc

padcirc: copy
	rm -rf PE*
	./dadcprep --np $(NP) --partmesh
	./dadcprep --np $(NP) --prepall
	time mpirun -np $(NP) ./padcirc-dg --solver 0
	mv fort.63 fort.63.adc

coupling: copy
	rm -rf PE*
	./dadcprep --np $(NP) --partmesh
	./dadcprep --np $(NP) --prepall
	time mpirun -np $(NP) ./padcirc-dg --solver 1
	mv fort.63 fort.63.coupling
noflux: copy
	rm -rf PE*
	./dadcprep --np $(NP) --partmesh
	./dadcprep --np $(NP) --prepall
	time mpirun -np $(NP) ./padcirc-dg --solver 1 --disable_flux
	mv fort.63 fort.63.noflux

plot63:
	singularity exec ./figuregen.sif mpirun -np 8 figuregen -I shin2.inp
plotbath:
	singularity exec ./figuregen.sif mpirun -np 2 figuregen -I bath5.inp
