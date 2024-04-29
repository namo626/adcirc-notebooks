SHELL := /bin/bash
NP = 2

INSTALL = /workspace/local/bin

all: adc-serial dg-serial coupling-serial
par: padcirc coupling
copy: 
	cp /workspace/adcirc-cg/build/adcirc-cuda .

nv : copy
	#nvprof --kernels g_INTERNAL_EDGE_HYDRO --metrics achieved_occupancy,flop_dp_efficiency ./adcirc-cuda	
	#nvprof  --metrics flop_dp_efficiency ./adcirc-cuda	
	nvprof  --metrics gld_efficiency ./adcirc-cuda	

coupling-serial:
	cp $(INSTALL)/adcirc-dg .
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
	dadcprep --np $(NP) --partmesh
	dadcprep --np $(NP) --prepall
	time mpirun -np $(NP) padcirc-dg
	mv fort.61 fort.61.coupling
