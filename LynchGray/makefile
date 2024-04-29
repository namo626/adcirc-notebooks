SHELL := /bin/bash

INSTALL = /workspace/local/bin
CMD = cd $@; \
      rm max*; \
      cp ../../../build/adcirc-dg .; \
      ./adcirc-dg; \
      mv fort.61 fort.61.coupling; \
      mv fort.63 fort.63.coupling;

CMD2 = cd $^; \
      adcirc; \
      mv fort.61 fort.61.adc; \
      mv fort.63 fort.63.adc;

.PHONY: Mesh1 Mesh2 Mesh3 Mesh4

all: Mesh1 Mesh2 Mesh3 Mesh4

Mesh1: 
	$(CMD)

Mesh2: 
	$(CMD)

Mesh3: 
	$(CMD)

Mesh4: 
	$(CMD)


