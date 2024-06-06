m = msh('fort.14');

%% Convert deg to cartesian
x_m = deg2km(m.p(:,1)) * 1000;
y_m = deg2km(m.p(:,2)) * 1000;
m.p(:,1) = x_m;
m.p(:,2) = y_m;
%% Make a hump in the middle, in the x-direction
xs = m.p(:,1);
center = 0.5 * (max(xs) + min(xs));
width = 1e-4;
%bathy = -exp(-width*(m.p(:,1)-center) .^ 2) + 5;


bathy = -exp(-(width*(m.p(:,1)-center)) .^ 2) - 1;

%% Remove boundary conditions
m.op = [];
m.bd = [];
m = make_bc(m, 'outer', 1);

%% set
m.b = bathy;
write(m, 'mesh', 'f14');

%% Test
%c = deg2km(center) * 1000;
%x1 = deg2km(min(xs)) * 1000;
%x2 = deg2km(max(xs)) * 1000;
x1 = min(xs);
x2 = max(xs);
c = center;

fun = @(x) exp(-(width*(x-c)) .^ 2) + 1;
fun2 = @(x) exp(-(width*(x-c)) .^ 2) + 1.001;

q = integral(fun, x1, x2);
q2 = integral(fun, x1, x2);

ys=  m.p(:,2);
vol = q * (max(ys) - min(ys));