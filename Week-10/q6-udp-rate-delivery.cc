#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;
int main(int argc,char*argv[]){
  std::string rate="500Kbps"; CommandLine cmd; cmd.AddValue("rate","Offered UDP rate (e.g. 500Kbps or 8Mbps)",rate); cmd.Parse(argc,argv);
  NodeContainer n; n.Create(2); PointToPointHelper p; p.SetDeviceAttribute("DataRate",StringValue("2Mbps")); p.SetChannelAttribute("Delay",StringValue("5ms"));
  auto d=p.Install(n); InternetStackHelper internet; internet.Install(n); Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); auto a=ip.Assign(d);
  uint16_t port=9000; PacketSinkHelper sink("ns3::UdpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port));
  auto s=sink.Install(n.Get(1)); s.Start(Seconds(1)); s.Stop(Seconds(11));
  OnOffHelper src("ns3::UdpSocketFactory",InetSocketAddress(a.GetAddress(1),port)); src.SetAttribute("DataRate",StringValue(rate)); src.SetAttribute("PacketSize",UintegerValue(1000));
  src.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]")); src.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]"));
  auto app=src.Install(n.Get(0)); app.Start(Seconds(2)); app.Stop(Seconds(10));
  FlowMonitorHelper fm; auto mon=fm.InstallAll(); Simulator::Stop(Seconds(11)); Simulator::Run(); mon->CheckForLostPackets();
  for(auto const&kv:mon->GetFlowStats()){auto x=kv.second; double pdr=x.txPackets?100.0*x.rxPackets/x.txPackets:0; std::cout<<"rate="<<rate<<" txPackets="<<x.txPackets<<" rxPackets="<<x.rxPackets<<" PDR="<<pdr<<"%\n";}
  Simulator::Destroy(); return 0;
}
