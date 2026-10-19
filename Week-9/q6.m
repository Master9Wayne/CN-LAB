clc; clear; close all;

names = {'A','B','C','D','E'};

C = [0 2 5 0 0;
     2 0 1 3 0;
     5 1 0 2 6;
     0 3 2 0 1;
     0 0 6 1 0];

% Convert zero non-diagonal entries to infinity
W = C;
W(W == 0) = Inf;
W(1:6:end) = 0;

G = graph(W, names, 'upper', 'omitselfloops');
% Use the original symmetric costs with zero for missing links.
G = graph(C, names, 'upper');

% MATLAB graph treats zero weights as absent edges.
% Positive links in C define the network.
figure;
p = plot(G, 'EdgeLabel', G.Edges.Weight);
title('Network Link Costs');
grid on;

% Shortest paths from A
for dest = 2:5
    [path, cost] = shortestpath(G, 1, dest);
    fprintf('A to %s: cost %.0f, path ', names{dest}, cost);
    fprintf('%s ', names{path});
    fprintf('\n');
end

% Highlight the shortest path from A to E
[path, cost] = shortestpath(G, 1, 5);
highlight(p, path, 'EdgeColor', 'r', 'LineWidth', 2);
fprintf('A to E cost = %.0f\n', cost);

% Change link B-D from 3 to 8
C2 = C;
C2(2,4) = 8;
C2(4,2) = 8;
G2 = graph(C2, names, 'upper');

fprintf('\nAfter changing B-D to 8:\n');
for dest = 2:5
    [path, cost] = shortestpath(G2, 1, dest);
    fprintf('A to %s: cost %.0f, path ', names{dest}, cost);
    fprintf('%s ', names{path});
    fprintf('\n');
end
