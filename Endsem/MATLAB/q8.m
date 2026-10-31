clc; clear; close all;

rounds = 1:15;
cwnd = zeros(1,15);

ssthresh = 8;
cwnd(1) = 1;

for r = 2:10
    if cwnd(r-1) < ssthresh
        cwnd(r) = min(2*cwnd(r-1), ssthresh);
    else
        cwnd(r) = cwnd(r-1) + 1;
    end
end

% Loss after round 10
ssthresh = max(2, floor(cwnd(10)/2));
cwnd(11) = 1;

for r = 12:15
    if cwnd(r-1) < ssthresh
        cwnd(r) = min(2*cwnd(r-1), ssthresh);
    else
        cwnd(r) = cwnd(r-1) + 1;
    end
end

disp(table(rounds', cwnd', ...
    'VariableNames', {'Round','CongestionWindow'}));

figure;
plot(rounds, cwnd, 'o-', 'LineWidth', 2);
hold on;
xline(10, '--r', 'Loss event');
xlabel('Round Number');
ylabel('Congestion Window (segments)');
title('TCP Congestion Window');
grid on;
