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
Q4 - EchoAgent
Node 1: http://localhost:8081/
Node 2: http://localhost:8082/
EchoAgent.groovy must be in the UnetStack installation's classes/ directory.
'''

simulate {
  node '1', address: 1, location: [0.m, 0.m, 0.m],
    web: 8081, api: 1101, stack: "$home/etc/setup"

  node '2', address: 2, location: [1000.m, 0.m, 0.m],
    web: 8082, api: 1102,
    stack: {
      // Load the standard stack first, then add the custom agent.
      evaluate(new File(home, 'etc/setup.groovy'))
      container.add 'echo', new EchoAgent()
    }
}
