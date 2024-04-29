import pytest
import numpy as np
import os
from test_adcirc import getStation

dire = "QuarterAnnular"
@pytest.fixture(scope="module")
def run_serial():
    os.chdir(dire)
    os.system("adcirc-dg > serial.out")
    os.system("mv fort.61 fort.61.serial")
    elev = getStation("fort.61.serial", 1)
    os.chdir("../")
    return elev

@pytest.fixture(scope="module")
def run_parallel():
    os.chdir(dire)
    os.system("rm -rf PE*")
    os.system("dadcprep --np 4 --partmesh > /dev/null")
    os.system("dadcprep --np 4 --prepall > /dev/null")
    os.system("mpirun -np 4 padcirc-dg > parallel.out")
    os.system("mv fort.61 fort.61.par")
    elev = getStation("fort.61.par", 1)
    os.chdir("../")

    return elev

def test_parallelization(run_serial, run_parallel):
    assert np.allclose(run_serial, run_parallel)
