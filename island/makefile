SHELL := /bin/bash
NP = 20

INSTALL = /workspace/local/bin

all: adc-serial dg-serial coupling-serial
par: padcirc coupling

coupling-serial:
	cp ../../build/adcirc-dg .
	if time ./adcirc-dg --solver 1 ; then \
		mv fort.63 fort.63.coupling; \
		#gprof ./adcirc-dg > coupling.prof; \
		# conda run -n chg gprof2dot coupling.prof | dot -Tpng -Gdpi=300 -o coupling_prof.png; \
	fi

noflux:
	cp ../../build/adcirc-dg .
	./adcirc-dg --solver 1 --disable_flux
	mv fort.63 fort.63.noflux

dg-serial:
	cp $(INSTALL)/dgswem_serial .
	time ./dgswem_serial
	mv fort.61 fort.61.dg
	mv fort.63 fort.63.dg
	gprof ./dgswem_serial > dg.prof

adc-serial:
	cp ../../build/adcirc-dg .
	./adcirc-dg --solver 0
	mv fort.63 fort.63.adc

padcirc:
	rm -rf PE*
	adcprep --np $(NP) --partmesh
	adcprep --np $(NP) --prepall
	time mpirun -np $(NP) padcirc
	mv fort.61 fort.61.adc
	mv fort.63.nc fort.63.adc.nc

coupling-prep:
	rm -rf PE*
	dadcprep --np $(NP) --partmesh
	dadcprep --np $(NP) --prepall

coupling-run:
	cp ../../build/padcirc-dg .
	time mpirun -np $(NP) ./padcirc-dg
	cp fort.61 fort.61.coupling
	cp fort.63.nc fort.63.coupling.nc

coupling: coupling-prep coupling-run

plot_adg:
	singularity exec ./figuregen.sif mpirun -np 8 figuregen -I shin_adg.inp
plot_adc:
	singularity exec ./figuregen.sif mpirun -np 8 figuregen -I shin_adc.inp
plotbath:
	singularity exec ./figuregen.sif mpirun -np 2 figuregen -I bath5.inp
