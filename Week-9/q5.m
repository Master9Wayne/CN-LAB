clc; clear; close all;

prefix = 26;
totalAddresses = 2^(32-prefix);
usableHosts = totalAddresses - 2;

fprintf('Prefix: /%d\n', prefix);
fprintf('Addresses per subnet: %d\n', totalAddresses);
fprintf('Usable hosts per subnet: %d\n', usableHosts);

subnets = {
    '192.168.10.0',   '192.168.10.1',   '192.168.10.62',  '192.168.10.63';
    '192.168.10.64',  '192.168.10.65',  '192.168.10.126', '192.168.10.127';
    '192.168.10.128', '192.168.10.129', '192.168.10.190', '192.168.10.191';
    '192.168.10.192', '192.168.10.193', '192.168.10.254', '192.168.10.255'
};

disp(array2table(subnets, 'VariableNames', ...
    {'Network','FirstUsable','LastUsable','Broadcast'}));

% Test the required address
[network, broadcast] = subnetInfo('192.168.10.77', 26);
fprintf('Test network: %s\n', network);
fprintf('Test broadcast: %s\n', broadcast);

function [network, broadcast] = subnetInfo(ip, prefix)
    octets = sscanf(ip, '%d.%d.%d.%d')';
    ipNum = uint32(0);

    for k = 1:4
        ipNum = bitor(bitshift(ipNum, 8), uint32(octets(k)));
    end

    if prefix == 0
        mask = uint32(0);
    else
        mask = bitshift(uint32(2^prefix-1), 32-prefix);
    end

    netNum = bitand(ipNum, mask);
    broadNum = bitor(netNum, bitcmp(mask));

    network = sprintf('%u.%u.%u.%u', ...
        bitand(bitshift(netNum,-24),255), ...
        bitand(bitshift(netNum,-16),255), ...
        bitand(bitshift(netNum,-8),255), ...
        bitand(netNum,255));

    broadcast = sprintf('%u.%u.%u.%u', ...
        bitand(bitshift(broadNum,-24),255), ...
        bitand(bitshift(broadNum,-16),255), ...
        bitand(bitshift(broadNum,-8),255), ...
        bitand(broadNum,255));
end
