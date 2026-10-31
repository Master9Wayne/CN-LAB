clc; clear; close all;

packetBytes = 1500;
bandwidths = [5 10 20 50];  % Mbps
distance = 1200e3;           % metres
speed = 2e8;                 % m/s
processing = 2e-3;           % seconds

packetBits = packetBytes * 8;
transmission = packetBits ./ (bandwidths * 1e6);
propagation = distance / speed;
totalDelay = transmission + propagation + processing;

disp(table(bandwidths', transmission'*1000, ...
    repmat(propagation*1000,4,1), totalDelay'*1000, ...
    'VariableNames', {'Bandwidth_Mbps','Transmission_ms', ...
    'Propagation_ms','TotalDelay_ms'}));

figure;
plot(bandwidths, totalDelay*1000, 'o-', 'LineWidth', 2);
xlabel('Bandwidth (Mbps)');
ylabel('Total One-Way Delay (ms)');
title('Bandwidth vs Total Delay');
grid on;
