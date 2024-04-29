SHELL := /bin/bash
TIME = /usr/bin/time
NP = 20

INSTALL = /workspace/local/bin
BUILD = /workspace/adcirc-cg/build

.PHONY: padcirc coupling

all: adc-serial dg-serial coupling-serial
par: padcirc coupling dgswem

copy:
	cp $(BUILD)/adcirc-cuda .

nv: copy
	#nvprof --kernels g_INTERNAL_EDGE_HYDRO --metrics flop_dp_efficiency ./adcirc-cuda	
	#nvprof --metrics flop_dp_efficiency ./adcirc-cuda	
	nvprof --metrics gld_efficiency ./adcirc-cuda	

coupling-serial:
	cp $(BUILD)/adcirc-dg .
	if time ./adcirc-dg ; then \
		mv fort.61 fort.61.coupling; \
		mv fort.63 fort.63.coupling; \
		gprof ./adcirc-dg > coupling.prof; \
		conda run -n chg gprof2dot coupling.prof | dot -Tpng -Gdpi=300 -o coupling_prof.png; \
	fi

cuda: copy
	if time ./adcirc-cuda ; then \
		mv fort.61 fort.61.cuda; \
		gprof ./adcirc-cuda > cuda.prof; \
		conda run -n chg gprof2dot cuda.prof | dot -Tpng -Gdpi=300 -o cuda_prof.png; \
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
	$(TIME) -o padcirc.time mpirun -np $(NP) padcirc
	mv fort.61 fort.61.adc

coupling:
	rm -rf PE*
	cp $(BUILD)/padcirc-dg .
	dadcprep --np $(NP) --partmesh
	dadcprep --np $(NP) --prepall
	$(TIME) -o coupling.time mpirun -np $(NP) ./padcirc-dg
	mv fort.61 fort.61.coupling

dgswem:
	rm -rf PE*
	adcprep-dg < in.prep
	$(TIME) -o dg.time mpirun -np $(NP) dgswem
#mv fort.61 fort.61.dg
