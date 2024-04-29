import pytest
import numpy as np
import os

def getStation(file1, st):
    elev1 = []

    with open(file1) as f1:
        l1 = f1.readline()
        l1 = f1.readline()

        # Get timestep info
        info = l1.split()
        skip = float(info[3])
        dt = float(info[2]) / skip

        l1 = f1.readline()

        for lineno, line in enumerate(f1):
            lines = line.split()
            if lines[0] == str(st):
                x = float(lines[1])

                # If dry, set to zero
                if x < -100:
                    x = 0.

                elev1.append(x)

    return np.array(elev1)

def run_adcirc(folder, prog="adcirc", mpi=False):
    # run adcirc
    owd = os.getcwd()
    os.chdir(folder)
    if prog == "adcirc":
        if mpi:
            os.system("padcirc > /dev/null")
        else:
            os.system("adcirc > /dev/null")
    else:
        if mpi:
            os.system("padcirc-dg > /dev/null")
        else:
            os.system("adcirc-dg > /dev/null")

    # parse fort.61 into array
    fort61 = getStation('fort.61', 1)

    os.chdir(owd)
    return fort61



def temp_fort61(folder, mpi):
    adc = run_adcirc(folder, prog="adcirc", mpi=mpi)
    adc_dg = run_adcirc(folder, prog="dg", mpi=mpi)
    assert abs(adc[-1] - adc_dg[-1]) < 0.01

def test_QuaterAnnular():
    temp_fort61("QuarterAnnular", mpi=False)
