SHELL := /bin/bash

CMD = cd $@; \
      rm max*; \
      cp ../../../build/adcirc-dg .; \
      ./adcirc-dg --solver 1 --stabilize; \
      mv fort.61 fort.61.stab; \
      mv fort.63 fort.63.stab;

CMD1 = cd $@; \
       rm max*; \
      cp ../../../build/adcirc-dg .; \
      ./adcirc-dg --solver 0; \
      mv fort.61 fort.61.adc; \
      mv fort.63 fort.63.adc;

CMD2 = cd $@; \
       rm max*; \
      cp ../../../build/adcirc-dg .; \
      ./adcirc-dg --solver 1; \
      mv fort.61 fort.61.coupling; \
      mv fort.63 fort.63.coupling;

.PHONY: Mesh1 Mesh2 Mesh3 Mesh4

all: Mesh1 Mesh2 Mesh3 Mesh4

Mesh1: 
	$(CMD)
	$(CMD1)
	$(CMD2)

Mesh2: 
	$(CMD)
	$(CMD1)
	$(CMD2)

Mesh3: 
	$(CMD)
	$(CMD1)
	$(CMD2)

Mesh4: 
	$(CMD)
	$(CMD1)
	$(CMD2)


