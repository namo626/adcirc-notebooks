function TR = trirectangle(R,Nx,Ny,trisub)

%% TRIRECTANGLE Triangulation of a rectangular area
%    TR = trirectangle(R,Nx,Ny,trisub) returns a triangulation of a
%    rectangle R, specified as a four-element vector of the form [x y w h]  
%    (explained below), by first subdiving R into a set of Nx*Ny sub-
%    rectangles of width and height w/Nx and h/Ny, respectively, and then 
%    splitting each rectangle into a set of triangles as specified by the 
%    character string trisub, where options for the subdivision of each 
%    subrectangle into triangles are as illustrated below:
%                 
%    trisub = '/':
%     ____           ____
%    |    |         |   /|
%    |    |   ==>   |  / |  
%    |    |         | /  |
%    |____|         |/___|
%                     
%    trisub = '\':  
%     ____           ____
%    |    |         |\   |                  
%    |    |   ==>   | \  |  
%    |    |         |  \ |
%    |____|         |___\|
%                   
%    trisub = 'X':
%     ___           ____ 
%    |    |        |\  /|
%    |    |  ==>   | \/ | 
%    |    |        | /\ |
%    |____|         /__\|  
%
%    trisub = '*':
%     ___           _____ 
%    |    |        |\ | /|
%    |    |  ==>   |_\|/_| 
%    |    |        | /|\ |
%    |____|        |/_|_\|  
%
%    
%
%    trisub = 'X-X':
%     ____ ____       ____ ____         ____ ____      ____ ____
%    |    |    |     |    |    |       |\  / \  /      \  / \  /|
%    |    |    | ... |    |    |  ==>  | \/___\/_  ... _\/___\/ |
%    |    |    |     |    |    |       | /\   /\        /\   /\ |
%    |____|____|     |____|____|       |/__\ /__\      /__\ /__\|                                              
%
%    As noted above, the input retangle R is specified as a four-element 
%    vector of the form [x y w h], where x and y define the coordinate for 
%    the lower left corner of R and w and h define the dimensions of the 
%    rectangle in the x and y directions, respectively, i.e., the width and
%    height.  
%
%    Example: TR1 = trirectangle([0,0,1,1],5,4,'/'); triplot(TR1);
%             TR2 = trirectangle([0,0,1,1],5,4,'\'); triplot(TR2);
%
%    See also triangulation, triplot, trirefine
%

%% Validate input

vR = @(x)validateattributes(x,{'numeric'},{'vector','real','numel',4});
vNxy = @(x)validateattributes(x,{'numeric'},{'scalar','positive','integer'});
vtri = @(x)validateattributes(x,{'char'},{'nonempty'});
ip = inputParser;
ip.addRequired('R',vR); ip.addRequired('Nx',vNxy); ip.addRequired('Ny',vNxy);
ip.addRequired('trisub',vtri); 
ip.parse(R,Nx,Ny,trisub);
ip.Results;

%% Create the triangulation

% Parition x and y into Nx and Ny pieces, respectively
x = linspace(R(1),R(1)+R(3),Nx+1)'; y = linspace(R(2),R(2)+R(4),Ny+1)';
% Take the Cartesian product of the points sets
[X,Y] = meshgrid(x,y);
% Switch number of elements per rectangle and additional points by case
switch trisub
    case {'/','\'}
        nT = 2;
        Xc = []; Yc = [];
    case 'X'
        nT = 4;
        [Xc,Yc] = meshgrid((x(1:end-1)+x(2:end))/2,(y(1:end-1)+y(2:end))/2);
    case 'X-X'
        nT = 4;
       [Xc,Yc] = meshgrid([x(1); (x(1:end-1)+x(2:end))/2; x(end)],...
           (y(1:end-1)+y(2:end))/2);
    case '*'
        nT = 6;
        [Xc,Yc] = meshgrid((x(1:end-1)+x(2:end))/2,(y(1:end-1)+y(2:end))/2);
end
% Initialize the connectivity list
ConnectivityList = zeros((size(X,1)-1)*(size(X,2)-1)*nT,3);
% Generate connectivity list based on case
k = 1; v3 = numel(X)+1;
for j = 1:size(X,2)-1
    for i = 1:size(X,1)-1
        switch trisub
            case '/'
                ConnectivityList(k,:)   = [ sub2ind(size(X),i,j), ...
                    sub2ind(size(X),i,j+1), sub2ind(size(X),i+1,j+1) ];
                ConnectivityList(k+1,:) = [ sub2ind(size(X),i,j), ...
                    sub2ind(size(X),i+1,j+1), sub2ind(size(X),i+1,j) ];
            case '\'
                ConnectivityList(k,:)   = [ sub2ind(size(X),i,j), ...
                    sub2ind(size(X),i,j+1), sub2ind(size(X),i+1,j) ];
                ConnectivityList(k+1,:) = [ sub2ind(size(X),i,j+1), ...
                    sub2ind(size(X),i+1,j+1), sub2ind(size(X),i+1,j) ];
            case 'X'
                ConnectivityList(k,:)   = [ sub2ind(size(X),i,j), ...
                    sub2ind(size(X),i,j+1), v3 ];
                ConnectivityList(k+1,:) = [ sub2ind(size(X),i,j+1), ...
                    sub2ind(size(X),i+1,j+1), v3 ];
                ConnectivityList(k+2,:) = [ sub2ind(size(X),i+1,j+1), ...
                    sub2ind(size(X),i+1,j), v3 ];
                ConnectivityList(k+3,:) = [ sub2ind(size(X),i+1,j), ...
                    sub2ind(size(X),i,j), v3 ];  
                v3 = v3+1; 
            case '*'
                
            case 'X-X'
                ConnectivityList(k,:)   = [ sub2ind(size(X),i,j), ...
                    sub2ind(size(X),i,j+1), v3+sub2ind(size(Xc),i,j+1)-1 ];
                ConnectivityList(k+1,:) = [ sub2ind(size(X),i+1,j+1), ...
                    sub2ind(size(X),i+1,j), v3+sub2ind(size(Xc),i,j+1)-1];  
                ConnectivityList(k+2,:) = [ sub2ind(size(X),i+1,j), ...
                    v3+sub2ind(size(Xc),i,j)-1, v3+sub2ind(size(Xc),i,j+1)-1 ];
                ConnectivityList(k+3,:) = [ sub2ind(size(X),i,j), ...
                    v3+sub2ind(size(Xc),i,j+1)-1, v3+sub2ind(size(Xc),i,j)-1 ];
        end
        k = k + nT;
    end
end
j = size(Xc,2)-1;
for i = 1:size(X,1)-1
    switch trisub
        case 'X-X'
            ConnectivityList(k,:) = [ sub2ind(size(X),i+1,j), ...
                v3+sub2ind(size(Xc),i,j)-1, v3+sub2ind(size(Xc),i,j+1)-1 ];
            ConnectivityList(k+1,:) = [ sub2ind(size(X),i,j), ...
                v3+sub2ind(size(Xc),i,j+1)-1, v3+sub2ind(size(Xc),i,j)-1 ];
    end
    k = k + 2;
end
% Create the triangulation point set
Points = cat(1,[X(:),Y(:)],[Xc(:),Yc(:)]);
% Contruct the triangulation
TR = triangulation(ConnectivityList,Points);

end