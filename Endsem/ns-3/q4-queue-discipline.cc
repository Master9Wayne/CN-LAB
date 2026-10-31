#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/traffic-control-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;

int main(int argc,char*argv[]){
  std::string queueType="FqCoDel"; CommandLine cmd; cmd.AddValue("queueType","Queue discipline: FqCoDel or PfifoFast",queueType); cmd.Parse(argc,argv);
  NodeContainer n; n.Create(3); InternetStackHelper internet; internet.Install(n);
  PointToPointHelper p; p.SetDeviceAttribute("DataRate",StringValue("1Mbps")); p.SetChannelAttribute("Delay",StringValue("5ms"));
  p.SetQueue("ns3::DropTailQueue<Packet>","MaxSize",QueueSizeValue(QueueSize("100p")));
  auto d1=p.Install(n.Get(0),n.Get(1)); auto d2=p.Install(n.Get(1),n.Get(2));
  TrafficControlHelper tch;
  if(queueType=="FqCoDel") tch.SetRootQueueDisc("ns3::FqCoDelQueueDisc");
  else tch.SetRootQueueDisc("ns3::PfifoFastQueueDisc");
  tch.Install(d2);
  Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); ip.Assign(d1);
  ip.SetBase("10.1.2.0","255.255.255.0"); auto i2=ip.Assign(d2); Ipv4GlobalRoutingHelper::PopulateRoutingTables();
  uint16_t port=9000; PacketSinkHelper sink("ns3::UdpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port));
  auto s=sink.Install(n.Get(2)); s.Start(Seconds(1)); s.Stop(Seconds(12));
  OnOffHelper src("ns3::UdpSocketFactory",InetSocketAddress(i2.GetAddress(1),port));
  src.SetAttribute("DataRate",StringValue("5Mbps")); src.SetAttribute("PacketSize",UintegerValue(1200));
  src.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]"));
  src.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]"));
  auto a=src.Install(n.Get(0)); a.Start(Seconds(2)); a.Stop(Seconds(11));
  FlowMonitorHelper fm; auto mon=fm.InstallAll(); Simulator::Stop(Seconds(12)); Simulator::Run(); mon->CheckForLostPackets();
  for(auto const&kv:mon->GetFlowStats()){auto x=kv.second; std::cout<<"tx="<<x.txPackets<<" rx="<<x.rxPackets<<" lost="<<x.lostPackets<<" meanDelayMs="<<(x.rxPackets?1000*x.delaySum.GetSeconds()/x.rxPackets:0)<<"\n";}
  Simulator::Destroy(); return 0;
}
