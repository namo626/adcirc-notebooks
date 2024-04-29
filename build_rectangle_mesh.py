"""This demo illustrates the built-in mesh types."""

# Copyright (C) 2008 Garth N. Wells
#
# This file is part of DOLFIN.
#
# DOLFIN is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DOLFIN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DOLFIN. If not, see <http://www.gnu.org/licenses/>.
#
# Modified by Anders Logg, 2008.
# Modified by Benjamin Kehlet 2012
#
# First added:  2008-07-11
# Last changed: 2012-11-12
# Begin demo

from dolfin import *
from matplotlib import pyplot as plt
import numpy as np
#parameters ["plotting_backend"] = "matplotlib"
'''
mesh = UnitIntervalMesh(10)
print("Plotting a UnitIntervalMesh")
plot(mesh, title="Unit interval")

mesh = UnitSquareMesh(10, 10)
print("Plotting a UnitSquareMesh")
plot(mesh, title="Unit square")

mesh = UnitSquareMesh(10, 10, "left")
print("Plotting a UnitSquareMesh")
plot(mesh, title="Unit square (left)")

mesh = UnitSquareMesh(10, 10, "crossed")
print("Plotting a UnitSquareMesh")
plot(mesh, title="Unit square (crossed)")

mesh = UnitSquareMesh(10, 10, "right/left")
print("Plotting a UnitSquareMesh")
plot(mesh, title="Unit square (right/left)")

#Generate rectangle mesh
'''
num_horiz = 2 #400
num_vert = 2 #=80

mesh1 = RectangleMesh(Point(0.0, 0.0),Point(800.0, 800.0), num_horiz, num_vert)

#extract node and element info
node_num = mesh1.num_vertices()
node_xy = mesh1.coordinates()
element_num = mesh1.num_cells()
element_node = mesh1.cells()

#specify grid file name
node_filename = 'small_square'

node_file = open(node_filename + ".grd", 'w')

node_file.write(node_filename+"\n")
node_file.write('%6d %6d \n' %(element_num,node_num))
depth=10000.0*np.ones(len(node_xy[:,0]))
#depth=30-25*np.tanh(node_xy[:,0]/10000)
i=1
for row in node_xy:
    node_file.write('%10d'%(i))
    for column in row:
        node_file.write( ' %15.10f' % column )
    node_file.write(' %15.10f' % depth[i-1])
    node_file.write ( '\n' )
    i=i+1

i=1
for elem in element_node:
    node_file.write('%5d'%(i))
    node_file.write(' %4d'%(len(elem)))
    if i%2 ==0:
        #need to flip nodes 2 and 3 of even elements to make CCW
        temp=elem[1]
        elem[1]=elem[2]
        elem[2]=temp

    for column in elem:
        column=column+1
        node_file.write(' %5d' % column)
    node_file.write('\n')
    i=i+1

#Now write boundary condition, still need to figure out how to automate
#we want tides on left side, land on other 3 sides
#first task is to split up each boundary nodestring
#left_tide_boundary=list(map(int,range(32081,0,-401)))

left_tide_boundary=list(map(int,range((num_horiz+1)*(num_vert+1)-num_horiz,0,-(num_horiz+1))))
#three boundaries combined to one
land_boundary=list(map(int,range(1,num_horiz+2))) #start with bottom booundary going counterclockwise
right_boundary=list(map(int,range((num_horiz+1)*2,(num_horiz+1)*(num_vert+1),num_horiz+1)))
top_boundary=list(map(int,range((num_horiz+1)*(num_vert+1),(num_horiz+1)*(num_vert+1)-num_horiz-1,-1)))


land_boundary.extend(right_boundary)
land_boundary.extend(top_boundary)


node_file.write('1 = Number of open boundaries \n')
node_file.write(str(len(left_tide_boundary))+' = Total number of open boundary nodes \n')
node_file.write(str(len(left_tide_boundary))+' = Number of nodes for open boundary 1 \n')
for n in left_tide_boundary:
    node_file.write(str(n)+'\n')

node_file.write('1 = Number of land boundaries \n')
node_file.write(str(len(land_boundary))+' = Total number of land boundary nodes \n')
node_file.write(str(len(land_boundary))+ ' 20 = Number of nodes for land boundary 1 \n')
for n in land_boundary:
    node_file.write(str(n)+'\n')
node_file.close ( )



idx=[]
for n in land_boundary:
    idx.append(n-1)
idx2=[]
for n in left_tide_boundary:
    idx2.append(n-1)

plot(mesh1)
plt.savefig(node_filename+'.png')
'''

pyplot.figure(1)
pyplot.scatter(node_xy[idx,0],node_xy[idx,1],color='r',label='land boundary')
pyplot.scatter(node_xy[idx2,0],node_xy[idx2,1],color='b',label='open boundary')
pyplot.legend()
pyplot.savefig("plot_boundary.png")


pyplot.figure(2)
x=node_xy[:,0]
y=node_xy[:,1]

#test1=plot(mesh1, title="Rectangle")
pyplot.figure(figsize=(100,20))
pyplot.scatter(x,y,color='r',marker=".")

examplex=np.empty(0)
exampley=np.empty(0)


#pyplot.scatter(x,y,color='r',marker=".")
examplex=np.empty(0)
exampley=np.empty(0)

node1=[]
node2=[]
node3=[]
for elem in element_node:
    node1.append(int(elem[0]))
    node2.append(int(elem[1]))
    node3.append(int(elem[2]))

    

for i in range(26):
#plot first side of the element
    examplex=np.append(examplex,np.array([x[node1[i]],x[node2[i]]]))
    exampley=np.append(exampley,np.array([y[node1[i]],y[node2[i]]]))
    #plt.plot(examplex,exampley,color="k")
    #plot second side of the element
    examplex=np.append(examplex,np.array([x[node2[i]],x[node3[i]]]))
    exampley=np.append(exampley,np.array([y[node2[i]],y[node3[i]]]))
    #plt.plot(examplex,exampley,color="k")
    #plot third side of element
    examplex=np.append(examplex,np.array([x[node3[i]],x[node1[i]]]))
    exampley=np.append(exampley,np.array([y[node3[i]],y[node1[i]]]))
    pyplot.plot(examplex,exampley,color="k")
    examplex=np.empty(0)
    exampley=np.empty(0)



pyplot.savefig("mesh.png",figsize=(50,10))
'''

#pyplot.figure(3)
#pyplot.scatter(node_xy[:,0],-depth)
#pyplot.title("elevation vs x")
#pyplot.savefig("depth_profile.png")
'''
mesh = RectangleMesh(-3.0, 2.0, 7.0, 6.0, 10, 10, "right/left")
print("Plotting a RectangleMesh")
plot(mesh, title="Rectangle (right/left)")

if has_cgal():
    mesh = CircleMesh(Point(0.0, 0.0), 1.0, 0.2)
    print("Plotting a CircleMesh")
    plot(mesh, title="Circle (unstructured)")

    mesh = EllipseMesh(Point(0.0, 0.0), [3.0, 1.0], 0.2)
    print("Plotting an EllipseMesh")
    plot(mesh, title="Ellipse mesh (unstructured)")

    mesh = SphereMesh(Point(0.0, 0.0, 0.0), 1.0, 0.2)
    print("Plotting a SphereMesh")
    plot(mesh, title="Sphere mesh (unstructured)")

    mesh = EllipsoidMesh(Point(0.0, 0.0, 0.0), [3.0, 1.0, 2.0], 0.2)
    print("Plotting an EllipsoidMesh")
    plot(mesh, title="Ellipsoid mesh (unstructured)")

mesh = UnitCubeMesh(10, 10, 10)
print("Plotting a UnitCubeMesh")
plot(mesh, title="Unit cube")

mesh = BoxMesh(0.0, 0.0, 0.0, 10.0, 4.0, 2.0, 10, 10, 10)
print("Plotting a BoxMesh")
plot(mesh, title="Box")

interactive()
'''
