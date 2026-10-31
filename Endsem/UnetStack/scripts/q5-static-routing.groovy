import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.sim.channels.*

platform = RealTimePlatform

channel.model = ProtocolChannelModel
channel.communicationRange = 1000.m
channel.detectionRange = 1200.m
channel.interferenceRange = 1500.m
channel.pDetection = 1
channel.pDecoding = 1

println '''
Q5 - Static multi-hop routing
Node 11: http://localhost:8081/
Node 12: http://localhost:8082/
Node 13: http://localhost:8083/
StaticRouteInstaller.groovy must be in the UnetStack installation's classes/ directory.
'''

simulate {
  node '11', address: 11, location: [0.m, 0.m, 0.m],
    web: 8081, api: 1101,
    stack: {
      evaluate(new File(home, 'etc/setup.groovy'))
      container.add 'staticRoutes', new StaticRouteInstaller(13, 12)
    }

  node '12', address: 12, location: [1000.m, 0.m, 0.m],
    web: 8082, api: 1102,
    stack: {
      evaluate(new File(home, 'etc/setup.groovy'))
      container.add 'staticRoutes', new StaticRouteInstaller(13, 13, 11, 11)
    }

  node '13', address: 13, location: [2000.m, 0.m, 0.m],
    web: 8083, api: 1103,
    stack: {
      evaluate(new File(home, 'etc/setup.groovy'))
      container.add 'staticRoutes', new StaticRouteInstaller(11, 12)
    }
}
