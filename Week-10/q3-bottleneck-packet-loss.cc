#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;

int main(int argc,char*argv[]) {
    std::string bottleneckRate="1Mbps";
    CommandLine cmd; cmd.AddValue("bottleneckRate","Final link rate (1Mbps or 10Mbps)",bottleneckRate); cmd.Parse(argc,argv);
    NodeContainer senders; senders.Create(2); Ptr<Node> router=CreateObject<Node>(); Ptr<Node> receiver=CreateObject<Node>();
    InternetStackHelper internet; internet.Install(senders); internet.Install(router); internet.Install(receiver);
    PointToPointHelper access; access.SetDeviceAttribute("DataRate",StringValue("10Mbps")); access.SetChannelAttribute("Delay",StringValue("2ms"));
    auto a=access.Install(senders.Get(0),router); auto b=access.Install(senders.Get(1),router);
    PointToPointHelper bottleneck; bottleneck.SetDeviceAttribute("DataRate",StringValue(bottleneckRate));
    bottleneck.SetChannelAttribute("Delay",StringValue("10ms"));
    bottleneck.SetQueue("ns3::DropTailQueue<Packet>","MaxSize",QueueSizeValue(QueueSize("20p")));
    auto c=bottleneck.Install(router,receiver);
    Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); ip.Assign(a);
    ip.SetBase("10.1.2.0","255.255.255.0"); ip.Assign(b);
    ip.SetBase("10.1.3.0","255.255.255.0"); auto ci=ip.Assign(c);
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();
    for(uint16_t i=0;i<2;i++){
      uint16_t port=8000+i;
      UdpServerHelper srv(port); auto s=srv.Install(receiver); s.Start(Seconds(1)); s.Stop(Seconds(10));
      OnOffHelper src("ns3::UdpSocketFactory",InetSocketAddress(ci.GetAddress(1),port));
      src.SetAttribute("DataRate",StringValue("8Mbps")); src.SetAttribute("PacketSize",UintegerValue(1024));
      src.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]"));
      src.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]"));
      auto app=src.Install(senders.Get(i)); app.Start(Seconds(2)); app.Stop(Seconds(9));
    }
    FlowMonitorHelper fm; auto mon=fm.InstallAll(); Simulator::Stop(Seconds(10)); Simulator::Run(); mon->CheckForLostPackets();
    for(auto const &kv:mon->GetFlowStats()){
      const auto&s=kv.second; std::cout<<"Flow "<<kv.first<<" tx="<<s.txPackets<<" rx="<<s.rxPackets
        <<" lost="<<s.lostPackets<<" rxThroughput="<<(s.rxBytes*8.0/7.0/1e6)<<" Mbps\n";
    }
    Simulator::Destroy(); return 0;
}
