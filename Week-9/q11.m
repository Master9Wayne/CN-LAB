clc; clear; close all;

interarrival = [0 3 2 5 1 4 2 3];
service = [4 2 3 2 4 1 3 2];

n = length(service);

arrival = cumsum(interarrival);
start = zeros(1,n);
departure = zeros(1,n);
waiting = zeros(1,n);
systemTime = zeros(1,n);

for i = 1:n
    if i == 1
        start(i) = arrival(i);
    else
        start(i) = max(arrival(i), departure(i-1));
    end

    departure(i) = start(i) + service(i);
    waiting(i) = start(i) - arrival(i);
    systemTime(i) = departure(i) - arrival(i);
end

disp(table((1:n)', arrival', start', departure', ...
    waiting', systemTime', ...
    'VariableNames', {'Packet','Arrival_ms','Start_ms', ...
    'Departure_ms','Waiting_ms','SystemTime_ms'}));

[maxWait, idx] = max(waiting);
fprintf('Longest wait: Packet %d, %.2f ms\n', idx, maxWait);

figure;
plot(1:n, waiting, 'o-', 'LineWidth', 2);
xlabel('Packet Number');
ylabel('Waiting Time (ms)');
title('Router Queue Waiting Times');
grid on;
