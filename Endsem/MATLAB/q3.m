clc; clear; close all;

frameBytes = 1000;
bandwidth = 4e6;            % bits per second
propDelays = [5 10 20 40 80]; % ms

frameBits = frameBytes * 8;
transmission = frameBits / bandwidth;
rtt = 2 * propDelays / 1000;

efficiency = transmission ./ (transmission + rtt);
throughput = efficiency * bandwidth / 1e6;

fprintf('Frame transmission time = %.2f ms\n', ...
    transmission*1000);

disp(table(propDelays', efficiency'*100, throughput', ...
    'VariableNames', {'Propagation_ms','Efficiency_pct', ...
    'Throughput_Mbps'}));

figure;
plot(propDelays, efficiency*100, 'o-', 'LineWidth', 2);
xlabel('One-Way Propagation Delay (ms)');
ylabel('Efficiency (%)');
title('Stop-and-Wait Efficiency');
grid on;
