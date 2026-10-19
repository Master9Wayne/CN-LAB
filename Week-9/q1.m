clc; clear; close all;

fileMB = 24;
capacity = 20;          % Mbps
factor = 0.75;

fileBits = fileMB * 1e6 * 8;
effectiveRate = capacity * factor;
transferTime = fileBits / (effectiveRate * 1e6);

fprintf('Effective rate: %.2f Mbps\n', effectiveRate);
fprintf('Transfer time: %.2f seconds\n', transferTime);

factors = [0.50 0.60 0.75 0.90 1.00];
rates = capacity * factors;
times = fileBits ./ (rates * 1e6);

disp(table(factors', rates', times', ...
    'VariableNames', {'UsableFraction','Rate_Mbps','Time_s'}));

figure;
plot(factors, times, 'o-', 'LineWidth', 2);
xlabel('Usable Capacity Factor');
ylabel('Transfer Time (seconds)');
title('Usable Capacity vs Transfer Time');
grid on;
