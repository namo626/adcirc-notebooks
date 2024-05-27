m2deg = 1/(111*1000);
deg2m = 1/m2deg;
bbox = m2deg*[0 100; 0 100];
pslg = m2deg*[0 0; 100 0; 100 100; 0 100; 0 0];
min_el = 1;
max_el = 2;
grade = 0.6;
R = 2;

gdat = geodata('pslg', pslg, 'bbox', bbox, 'h0', min_el);

%% Edge fx
fh = edgefx('geodata', gdat, 'fs', R, 'max_el', max_el, 'g', grade);

mshopts = meshgen('ef', fh, 'bou', gdat, 'plot_on', 1);
mshopts = mshopts.build;

m = mshopts.grd;
plot(m);

%% Put the hump in the middle
bath = zeros(size(m.p,1), 1); % base depth is 50 meters
center = m2deg*50;
radius = m2deg*20;
mask = ((m.p(:,1) - center).^2 + (m.p(:,2)-center).^2) <= radius^2;
bath(mask) = sqrt(radius^2 - (m.p(mask,1)-center).^2 - (m.p(mask,2)-center).^2);
m.b = bath * deg2m - 50; % convert depth to meters, base depth is 50m
m.b = -m.b; % flip bathymetry, by convention

%% Boundary conditions
m.bd = []; m.op = [];
m = make_bc(m, 'outer', 0);

%% Fort 15
% Add tides (this one is for Ike)
m = Make_f15(m, '05-Sep-2008 12:00', '14-Sep-2008 06:00', 2);


%% Write
write(m, 'humpv3', 'f14');
write(m, 'humpv3', 'f15');

