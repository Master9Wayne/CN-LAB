clc; clear; close all;

packet = 1:10;
status = [1 1 1 0 1 1 0 1 1 1];
delay = [12 15 11 NaN 18 14 NaN 20 13 16];

sent = length(packet);
received = sum(status);
lost = sent - received;

pdr = received / sent * 100;
plr = lost / sent * 100;

validDelay = delay(status == 1);

fprintf('Sent packets: %d\n', sent);
fprintf('Received packets: %d\n', received);
fprintf('Lost packets: %d\n', lost);
fprintf('Delivery ratio: %.2f%%\n', pdr);
fprintf('Loss ratio: %.2f%%\n', plr);
fprintf('Mean delay: %.2f ms\n', mean(validDelay));
fprintf('Median delay: %.2f ms\n', median(validDelay));
fprintf('Minimum delay: %.2f ms\n', min(validDelay));
fprintf('Maximum delay: %.2f ms\n', max(validDelay));

figure;
plot(packet, delay, 'bo-', 'LineWidth', 2);
hold on;
plot(packet(status == 0), zeros(1,lost), 'rx', ...
    'MarkerSize', 10, 'LineWidth', 2);
xlabel('Packet Number');
ylabel('Delay (ms)');
title('Packet Delays and Lost Packets');
legend('Received packet delays','Lost packets');
grid on;
