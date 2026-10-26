#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;

int main(int argc, char *argv[]) {
    NodeContainer nodes; nodes.Create(4); // node 0 is hub/router, 1 TCP sender, 2 UDP sender, 3 receiver
    PointToPointHelper p; p.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    p.SetChannelAttribute("Delay", StringValue("2ms"));
    NetDeviceContainer d01=p.Install(nodes.Get(0),nodes.Get(1));
    NetDeviceContainer d02=p.Install(nodes.Get(0),nodes.Get(2));
    NetDeviceContainer d03=p.Install(nodes.Get(0),nodes.Get(3));
    InternetStackHelper internet; internet.Install(nodes);
    Ipv4AddressHelper ip;
    ip.SetBase("10.1.1.0","255.255.255.0"); ip.Assign(d01);
    ip.SetBase("10.1.2.0","255.255.255.0"); ip.Assign(d02);
    ip.SetBase("10.1.3.0","255.255.255.0"); ip.Assign(d03);
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();
    uint16_t tcpPort=5000, udpPort=6000;
    PacketSinkHelper tcpSink("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(),tcpPort));
    auto ts=tcpSink.Install(nodes.Get(3)); ts.Start(Seconds(1)); ts.Stop(Seconds(10));
    PacketSinkHelper udpSink("ns3::UdpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(),udpPort));
    auto us=udpSink.Install(nodes.Get(3)); us.Start(Seconds(1)); us.Stop(Seconds(10));
    OnOffHelper tcp("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address("10.1.3.2"),tcpPort));
    tcp.SetAttribute("DataRate",StringValue("2Mbps")); tcp.SetAttribute("PacketSize",UintegerValue(1024));
    tcp.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]"));
    tcp.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]"));
    auto ta=tcp.Install(nodes.Get(1)); ta.Start(Seconds(2)); ta.Stop(Seconds(9));
    OnOffHelper udp("ns3::UdpSocketFactory", InetSocketAddress(Ipv4Address("10.1.3.2"),udpPort));
    udp.SetAttribute("DataRate",StringValue("1Mbps")); udp.SetAttribute("PacketSize",UintegerValue(1024));
    udp.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]"));
    udp.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]"));
    auto ua=udp.Install(nodes.Get(2)); ua.Start(Seconds(2)); ua.Stop(Seconds(9));
    Simulator::Stop(Seconds(10)); Simulator::Run();
    std::cout << "TCP bytes received: " << DynamicCast<PacketSink>(ts.Get(0))->GetTotalRx() << "\n";
    std::cout << "UDP bytes received: " << DynamicCast<PacketSink>(us.Get(0))->GetTotalRx() << "\n";
    Simulator::Destroy(); return 0;
}
