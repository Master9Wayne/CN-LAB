import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.sim.channels.*

platform = RealTimePlatform

channel.model = ProtocolChannelModel
channel.communicationRange = 2000.m
channel.detectionRange = 2500.m
channel.interferenceRange = 3000.m
channel.pDetection = 1
channel.pDecoding = 1

println '''
Q3 - Unicast and broadcast datagrams
Node 1: http://localhost:8081/
Node 2: http://localhost:8082/
Node 3: http://localhost:8083/
At receivers, inspect datagram notifications (shells normally subscribe automatically).
'''

simulate {
  node '1', address: 1, location: [0.m, 0.m, 0.m],
    web: 8081, api: 1101, stack: "$home/etc/setup"
  node '2', address: 2, location: [500.m, 0.m, 0.m],
    web: 8082, api: 1102, stack: "$home/etc/setup"
  node '3', address: 3, location: [1000.m, 0.m, 0.m],
    web: 8083, api: 1103, stack: "$home/etc/setup"
}
