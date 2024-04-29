SHELL := /bin/bash

all: adc adg

adc: 
	time adcirc
	mv fort.61 fort.61.adc
	mv fort.63 fort.63.adc
adg: 
	time adcirc-dg
	mv fort.61 fort.61.adg
	mv fort.63 fort.63.adg
