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
Q2 - Raw PHY frame test
Node 10: http://localhost:8081/
Node 20: http://localhost:8082/
At node 20 run: subscribe phy
At node 10 inspect phy[CONTROL] and phy[DATA], then send TxFrameReq commands.
'''

simulate {
  node '10', address: 10, location: [0.m, 0.m, 0.m],
    web: 8081, api: 1101, stack: "$home/etc/setup"
  node '20', address: 20, location: [1000.m, 0.m, 0.m],
    web: 8082, api: 1102, stack: "$home/etc/setup"
}
