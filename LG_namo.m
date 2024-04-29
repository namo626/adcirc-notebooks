clear all; close all;

%% Input problem data
%==========================================================================
DATA.geometry = 'Cartesian';         % 'Carteisan' or 'Polar'
DATA.geom1    = 60000;                   % x1 or r1
DATA.geom2    = 150000;              % x2 or r2    
DATA.h0       = 3;                   % Bathymetric coefficent
DATA.n        = 0;                   % Bathymetric power
DATA.amp      = 0.3048;                 % Tidal amplitude of forcing
DATA.freq     = 0.0001405257;         % Tidal frequency of forcing (Note: this frequency corresponds to an M2 tide)
DATA.phase    = 0;                   % Tidal Phase of forcing
DATA.tau      = 0.0025;                   % Linear bottom friction factor
DATA.g        = 9.81;                % Gravitational constant
%--------------------------------------------------------------------------
%% Test Quarter Annular with flag bathymetry
m = msh('fname', 'QuarterAnnularFlat/fort.14', 'nob', 1);
T = 5 * 86400.;
X = m.p;
[SE,U,V] = LG2D_Solutions(X,T,DATA);



%% Test station 1 time series
T = 0:10:(86400*5);
elev = [];
for i = 1:length(T)
    [SE,~] = LG2D_Solutions(xs(52,:),T(i),DATA);
    elev = [elev SE];
end


%% Load mesh 1
% Create initial condition at T = 0
msh_num = 4;
ncfile = [ 'LynchGray/Mesh' num2str(msh_num) '/fort.67.nc' ];
m = msh(['LynchGray/Mesh' num2str(msh_num) '/fort.14' ]);
xs = m.p; % x and y of nodes
T = 0; 

% Init condition
[SE,U,V] = LG2D_Solutions(xs,T,DATA);
ncwrite(ncfile, 'zeta1', SE);
ncwrite(ncfile, 'zeta2', SE);
ncwrite(ncfile, 'u-vel', U);
ncwrite(ncfile, 'v-vel', V);
ncwrite(ncfile, 'iths', 0);



%% Surface plot
RNDAY = 5;
T = RNDAY * 86400.;
[SE,U,V] = LG2D_Solutions(xs,T,DATA);

x = xs(:,1);
y = xs(:,2);
z = SE;
xlin = linspace(min(x), max(x), 50);
ylin = linspace(min(y), max(y), 50);
[X,Y] = meshgrid(xlin, ylin);
Z = griddata(x,y, z, X, Y, 'v4');

% close all;
% 
% figure;
% imagesc(Z);
% colorbar;
% clim([-0.2 0])

%% Plot ADCIRC results
T = readtable(['LynchGray/Mesh' num2str(msh_num) '/fort.63.coupling'], 'FileType', 'text');
np = size(m.p,1);
elev = table2array(T(end-np+1:end, "Var2"));
Z_out = griddata(x,y, elev, X, Y, 'v4');
figure;
set(gcf, 'Position', [200, 200, 1200, 500])

subplot(121);
imagesc(Z_out);
title(['Numerical Solution, Mesh ' num2str(msh_num)])
a = colorbar;
clim([-.2 0])

subplot(122);
imagesc(Z);
title('Analytical Solution')


colorbar;
clim([-.2 0])
%% Save
exportgraphics(gcf, 'LG4.png', 'Resolution',300);


%% L2 error
err = norm(z-elev, Inf);

%%
err4 = 0.0075;
err3 = 0.0142;
err2 = 0.0287;
err1 = 0.0855;
h1 = 15000;
h2 = 7500;
h3 = 3750;
h4 = 1875;
hs = [h4 h3 h2 h1];
rate = 1e-5.* hs;
figure;
loglog(hs, [err4 err3 err2 err1], '-square', 'DisplayName', 'DG-CG')
hold on
loglog(hs, rate, '--', 'DisplayName', 'k = 1')
xticks(hs)
title('Surface Elevation \zeta')
ylabel('L-\infty Error')
xlabel('h')
legend('Location','southeast')

%% Save
exportgraphics(gcf, 'convergence.png', 'Resolution',300);


