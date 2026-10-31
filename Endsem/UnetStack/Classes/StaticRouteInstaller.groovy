import org.arl.fjage.*
import org.arl.unet.*
import org.arl.unet.net.*

/**
 * Installs static routes when the node stack starts.
 *
 * Constructor arguments are destination,nextHop pairs:
 *   new StaticRouteInstaller(13,12)          -> route to 13 via 12
 *   new StaticRouteInstaller(13,13,11,11)    -> routes to 13 via 13
 *                                               and 11 via 11
 *
 * The router uses its configured default link when `link` is omitted.
 */
class StaticRouteInstaller extends UnetAgent {

  private final int[] routePairs

  StaticRouteInstaller(int... routePairs) {
    this.routePairs = routePairs
  }

  @Override
  void startup() {
    if (routePairs == null || routePairs.length == 0 ||
        routePairs.length % 2 != 0) {
      log.warning('StaticRouteInstaller requires destination,nextHop pairs')
      return
    }

    AgentID routingAgent = agentForService(Services.ROUTING)
    if (routingAgent == null) {
      log.warning('No ROUTING service found; static routes not installed')
      return
    }

    for (int i = 0; i < routePairs.length; i += 2) {
      int destination = routePairs[i]
      int nextHop = routePairs[i + 1]

      send new EditRouteReq(
        recipient: routingAgent,
        op: RouteInfo.Operation.CREATE,
        to: destination,
        nextHop: nextHop,
        metric: 1.0
      )

      log.info("Requested static route to ${destination} via ${nextHop}")
    }
  }
}
