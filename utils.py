import pyvista as pv
import netCDF4 as nc
import numpy as np
import meshio

def read14(num_points):
    arr = np.loadtxt(root + 'fort.14', skiprows=2, max_rows=num_points, usecols=(1,2,3))
    return arr
def read63(filename):
    with open(root + '/' + filename) as f1:
        l1 = f1.readline()
        l1 = f1.readline()
        info = l1.split()
        l1 = f1.readline()

        num_data = int(info[0])
        num_nodes = int(info[1])

        # Allocate array with num_data rows
        arr = np.zeros((num_data, num_nodes))

        # Loop over the file
        for i in range(num_data):
            for j in range(num_nodes):
                l = f1.readline().split()
                arr[i,j] = float(l[1])

            # Junk
            l = f1.readline()

        return arr

def plot63(f14, f63):
    # Find min and max of grid to plot
    minX = np.min(f14[:,0])
    minY = np.min(f14[:,1])
    maxX = np.max(f14[:,0])
    maxY = np.max(f14[:,1])

    # Plot the first snapshot

def getStation(file1, st, comp=1):
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
                if comp == 2:
                    x = lines[2]
                else:
                    x = lines[1]

                if x == "NaN":
                    y = np.nan
                else:
                    y = float(x)

                # If dry, set to zero
                if y < -1000:
                    y = 0.

                elev1.append(y)

    time = np.arange(len(elev1))*dt*skip/86400.

    return time, np.array(elev1)


pv.global_theme.font.color = 'black'


def read_nc(filename, mode="maxele", frame=None, region=None):
    ds = nc.Dataset(filename)
    # get mesh
    connectivity = ds["element"][...].data - 1  # element connectivity
    x = ds["x"][...].data  # longitude
    y = ds["y"][...].data  # latitude
    times = ds["time"][...].data
    print(len(times))

    if mode == "maxele":
        data = ds["zeta_max"][...].data

    elif mode == "maxvel":
        data = ds["vel_max"][...].data

    elif mode == "64":
        if not frame:
            frame = len(times) - 1

        vx = ds["u-vel"][frame].data
        vy = ds["v-vel"][frame].data
        data = (vx**2 + vy**2) ** 0.5

    elif mode == "63":
        if not frame:
            frame = len(times) - 1
        data = ds["zeta"][frame].data
    else:
        quit()

    ds.close()

    points = np.c_[x, y]
    points = np.c_[points, range(len(points))]

    # Extract subdomain of that frame for plotting, if specified
    if not region:
        cells = [("triangle", connectivity)]
    else:
        min_x = region[0]; max_x = region[1]
        min_y = region[2]; max_y = region[3]
        mask = (
            (points[:, 0] > min_x - 0.5)
            & (points[:, 0] < max_x + 0.5)
            & (points[:, 1] > min_y - 0.5)
            & (points[:, 1] < max_y + 0.5)
        )
        points = points[mask]
        old_idxs = points[:, 2].astype(int)
        kept_idxs = np.flatnonzero(mask)

        old2new_idxs = {old_idx: new_idx for new_idx, old_idx in enumerate(kept_idxs)}

        new_elements = connectivity[
            (
                mask[connectivity[:, 0]]
                & mask[connectivity[:, 1]]
                & mask[connectivity[:, 2]]
            )
        ]
        """(3)"""
        new_elements = np.vectorize(lambda old_idx: old2new_idxs[old_idx])(new_elements)

        cells = [("triangle", new_elements)]
        data = data[old_idxs]

    print(np.max(data))

    points = points[:, 0:2]
    points = np.c_[points, np.zeros(len(points))]

    mesh = meshio.Mesh(points, cells, point_data={mode: data})
    mesh.write(filename + ".vtk")

def plot_vtk(filename, mode, show_edges=True, clim=[-0.1,0.1], title="Plot"):
    grid = pv.read(filename)
    plotter = pv.Plotter()
    plotter.set_background("white")
    sargs = dict(vertical=True)
    plotter.add_mesh(
        grid,
        show_scalar_bar=True,
        scalar_bar_args=sargs,
        color=True,
        scalars=mode,
        cmap="jet",
        clim=clim,
        show_edges=show_edges
    )

    # orient view
    plotter.view_xy()
    plotter.link_views()
    plotter.show_axes()
    plotter.show_bounds()
    plotter.add_title(title)

    # get image of view
    plotter.show()

    return plotter

def plot_main(filename, show_edges=True, mode="63", frame=1, clim=[-0.1,0.1], region=None, title="Plot"):
    read_nc(filename, mode=mode, frame=frame, region=region)
    plotter = plot_vtk(filename + ".vtk", mode=mode,show_edges=show_edges, clim=clim,
                       title=title)
    return plotter
