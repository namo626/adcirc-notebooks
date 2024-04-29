
TR2 = trirectangle([-100,10,5,40],8,69,'X');
triplot(TR2)

%% Create msh obj
m = msh('points', TR2.Points, 'elements', TR2.ConnectivityList);

%% Bathy
m.b = zeros(size(m.p,1),1) + 200; % fixed -200m bathymetry

%% Make BC
m = make_bc(m, 'outer', 0);

%% Open boundary
m = make_bc(m, 'outer', 1);

%% save
write(m, 'BeachX/fort', 'f14')