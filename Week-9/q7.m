clc; clear; close all;

G = 0:0.05:3;

pure = G .* exp(-2*G);
slotted = G .* exp(-G);

figure;
plot(G, pure, 'b-', 'LineWidth', 2);
hold on;
plot(G, slotted, 'r-', 'LineWidth', 2);
xlabel('Offered Load (G)');
ylabel('Normalized Throughput');
title('Pure ALOHA vs Slotted ALOHA');
legend('Pure ALOHA','Slotted ALOHA');
grid on;

[maxPure, i1] = max(pure);
[maxSlotted, i2] = max(slotted);

fprintf('Pure maximum = %.4f at G = %.2f\n', maxPure, G(i1));
fprintf('Slotted maximum = %.4f at G = %.2f\n', ...
    maxSlotted, G(i2));

testG = [0.5 1.0 2.0];
disp(table(testG', ...
    (testG .* exp(-2*testG))', ...
    (testG .* exp(-testG))', ...
    'VariableNames', {'G','PureThroughput','SlottedThroughput'}));
