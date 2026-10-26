#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;

int main(int argc, char *argv[]) {
    std::string rate = "5Mbps";
    CommandLine cmd; cmd.AddValue("rate", "Point-to-point data rate (5Mbps or 10Mbps)", rate); cmd.Parse(argc, argv);
    NodeContainer n; n.Create(2);
    PointToPointHelper p2p; p2p.SetDeviceAttribute("DataRate", StringValue(rate));
    p2p.SetChannelAttribute("Delay", StringValue("10ms"));
    NetDeviceContainer d = p2p.Install(n);
    InternetStackHelper internet; internet.Install(n);
    Ipv4AddressHelper ip; ip.SetBase("10.1.1.0", "255.255.255.0"); ip.Assign(d);
    uint16_t port = 9000;
    UdpServerHelper server(port); auto apps = server.Install(n.Get(1)); apps.Start(Seconds(1)); apps.Stop(Seconds(11));
    UdpClientHelper client(Ipv4Address("10.1.1.2"), port);
    client.SetAttribute("MaxPackets", UintegerValue(100000));
    client.SetAttribute("Interval", TimeValue(MilliSeconds(1)));
    client.SetAttribute("PacketSize", UintegerValue(1024));
    auto c = client.Install(n.Get(0)); c.Start(Seconds(2)); c.Stop(Seconds(10));
    FlowMonitorHelper fm; Ptr<FlowMonitor> mon = fm.InstallAll();
    Simulator::Stop(Seconds(11)); Simulator::Run();
    mon->CheckForLostPackets();
    auto stats = mon->GetFlowStats();
    for (const auto &kv : stats) {
        const auto &s = kv.second;
        if (s.rxPackets > 0) {
            double throughput = s.rxBytes * 8.0 / (9.0 * 1e6);
            double delayMs = 1000.0 * s.delaySum.GetSeconds() / s.rxPackets;
            std::cout << "Configured rate: " << rate << "\nReceived packets: " << s.rxPackets
                      << "\nThroughput: " << throughput << " Mbps\nAverage delay: " << delayMs << " ms\n";
        }
    }
    Simulator::Destroy(); return 0;
}
