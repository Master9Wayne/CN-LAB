clc; clear; close all;

data = [1 1 0 1 0 1 1 0 1 1];
gen  = [1 0 0 1 1];

r = length(gen) - 1;
dividend = [data zeros(1,r)];

work = dividend;

for i = 1:length(data)
    if work(i) == 1
        work(i:i+r) = xor(work(i:i+r), gen);
    end
end

remainder = work(end-r+1:end);
codeword = [data remainder];

fprintf('CRC remainder: ');
fprintf('%d', remainder);
fprintf('\n');

fprintf('Codeword: ');
fprintf('%d', codeword);
fprintf('\n');

% Receiver checks the codeword
receiver = codeword;

for i = 1:length(codeword)-r
    if receiver(i) == 1
        receiver(i:i+r) = xor(receiver(i:i+r), gen);
    end
end

rxRemainder = receiver(end-r+1:end);
fprintf('Valid codeword? %d\n', all(rxRemainder == 0));

% Flip the 5th bit from the left
corrupted = codeword;
corrupted(5) = 1 - corrupted(5);

receiver = corrupted;

for i = 1:length(corrupted)-r
    if receiver(i) == 1
        receiver(i:i+r) = xor(receiver(i:i+r), gen);
    end
end

rxRemainder = receiver(end-r+1:end);

fprintf('Corrupted codeword remainder: ');
fprintf('%d', rxRemainder);
fprintf('\n');
fprintf('Error detected? %d\n', any(rxRemainder ~= 0));
