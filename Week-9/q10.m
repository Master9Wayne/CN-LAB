clc; clear; close all;

connection = {'A'; 'B'; 'C'};
bandwidth = [25; 50; 100];  % Mbps
fraction = [0.80; 0.55; 0.30];

fileMB = 150;
fileBits = fileMB * 1e6 * 8;

effective = bandwidth .* fraction;
downloadTime = fileBits ./ (effective * 1e6);

disp(table(connection, bandwidth, fraction, effective, downloadTime, ...
    'VariableNames', {'Connection','Nominal_Mbps', ...
    'UsableFraction','Effective_Mbps','DownloadTime_s'}));

[~, idx] = min(downloadTime);
fprintf('Fastest connection: %s\n', connection{idx});

figure;
bar(downloadTime);
set(gca, 'XTickLabel', connection);
xlabel('Connection');
ylabel('Download Time (seconds)');
title('Download Time Comparison');
grid on;
