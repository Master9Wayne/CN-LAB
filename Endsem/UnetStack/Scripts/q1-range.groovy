import org.arl.fjage.*
import org.arl.unet.sim.channels.*

platform = RealTimePlatform

channel.model = ProtocolChannelModel
channel.soundSpeed = 1500.mps
channel.communicationRange = 1500.m
channel.detectionRange = 2000.m
channel.interferenceRange = 2500.m
channel.pDetection = 1
channel.pDecoding = 1

println '''
Q1 - ProtocolChannelModel range test
Node 1: http://localhost:8081/
Node 2: http://localhost:8082/
Node 3: http://localhost:8083/
For placement 2, change node 3 x-coordinate from 2400.m to 1800.m.
'''

simulate {
  node '1', address: 1, location: [0.m, 0.m, 0.m],
    web: 8081, api: 1101, stack: "$home/etc/setup"
  node '2', address: 2, location: [1200.m, 0.m, 0.m],
    web: 8082, api: 1102, stack: "$home/etc/setup"
  node '3', address: 3, location: [2400.m, 0.m, 0.m],
    web: 8083, api: 1103, stack: "$home/etc/setup"
}
