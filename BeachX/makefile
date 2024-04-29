SHELL := /bin/bash
NP = 3

INSTALL = /workspace/local/bin

all: adc-serial dg-serial coupling-serial
par: padcirc coupling

coupling-serial:
	cp ../../build/adcirc-dg .
	./adcirc-dg --solver 1 
	mv fort.63 fort.63.coupling; 
	mv fort.64 fort.64.coupling; 

eta3:
	cp ../../build/adcirc-dg .
	./adcirc-dg --solver 10
	mv fort.63 fort.63.eta3
	mv fort.64 fort.64.eta3

dg-serial:
	cp /workspace/dgswem/work/dgswem_serial .
	time ./dgswem_serial
	mv fort.63 fort.63.dg

adc-serial:
	cp ../../build/adcirc-dg .
	time ./adcirc-dg --solver 0
	mv fort.63 fort.63.adc
	mv fort.64 fort.64.adc

p0:
	cp ../../build/adcirc-dg .
	./adcirc-dg --solver 2
	mv fort.63 fort.63.p0

padcirc:
	rm -rf PE*
	adcprep --np $(NP) --partmesh
	adcprep --np $(NP) --prepall
	time mpirun -np $(NP) padcirc
	mv fort.61 fort.61.adc
	mv fort.63.nc fort.63.adc.nc

dgswem:
	rm -rf PE*
	adcprep-dg < in.prep
	time mpirun -np $(NP) dgswem
	mv fort.61 fort.61.dg

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

plot63-adg:
	singularity exec ./figuregen.sif mpirun -np $(NP) figuregen -I shin_adg.inp
plot63-adc:
	singularity exec ./figuregen.sif mpirun -np $(NP) figuregen -I shin.inp
plot63-p0:
	singularity exec ./figuregen.sif mpirun -np $(NP) figuregen -I shin_p0.inp
plot63-dg:
	singularity exec ./figuregen.sif mpirun -np 12 figuregen -I shin_dg.inp

plotbath:
	singularity exec ./figuregen.sif mpirun -np 2 figuregen -I bath5.inp

movie_adc:
	ffmpeg -r 5 -i adc_pics/beach_adc%04d.jpg -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" adc.mp4
movie_adg:
	ffmpeg -r 5 -i adg_pics/beach_adg%04d.jpg -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" adg.mp4

