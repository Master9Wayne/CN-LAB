clc; clear; close all;

capacity = [10 8 4];       % Mbps
propagation = [3 5 4];     % ms
payload = 1000;            % bytes
header = 40;               % bytes

packetBytes = payload + header;
packetBits = packetBytes * 8;

transmission = packetBits ./ (capacity * 1e6);
transmissionMs = transmission * 1000;

totalDelay = sum(transmissionMs) + sum(propagation);

[~, bottleneck] = min(capacity);
bottleneckCapacity = capacity(bottleneck);

fprintf('Packet size: %d bytes\n', packetBytes);
fprintf('Packet size: %d bits\n', packetBits);

disp(table((1:3)', capacity', transmissionMs', propagation', ...
    'VariableNames', {'Link','Capacity_Mbps', ...
    'Transmission_ms','Propagation_ms'}));

fprintf('First-packet delay: %.3f ms\n', totalDelay);
fprintf('Bottleneck link: %d\n', bottleneck);

payloadSizes = [500 1000 1500 3000];
efficiency = payloadSizes ./ (payloadSizes + header);
throughput = bottleneckCapacity .* efficiency;

disp(table(payloadSizes', efficiency'*100, throughput', ...
    'VariableNames', {'Payload_bytes','Efficiency_pct', ...
    'PayloadThroughput_Mbps'}));

figure;
plot(payloadSizes, efficiency*100, 'o-', 'LineWidth', 2);
xlabel('Payload Size (bytes)');
ylabel('Payload Efficiency (%)');
title('Payload Size vs Efficiency');
grid on;

figure;
plot(payloadSizes, throughput, 's-', 'LineWidth', 2);
xlabel('Payload Size (bytes)');
ylabel('Payload Throughput (Mbps)');
title('Payload Size vs Steady-State Throughput');
grid on;
