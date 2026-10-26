#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;
int main(int argc,char*argv[]){
  bool moving=true; CommandLine cmd; cmd.AddValue("moving","Use moving station (true/false)",moving); cmd.Parse(argc,argv);
  NodeContainer sta; sta.Create(1); NodeContainer ap; ap.Create(1);
  YansWifiChannelHelper channel=YansWifiChannelHelper::Default(); YansWifiPhyHelper phy; phy.SetChannel(channel.Create());
  WifiHelper wifi; wifi.SetStandard(WIFI_STANDARD_80211g); WifiMacHelper mac; Ssid ssid=Ssid("mobility-lab");
  mac.SetType("ns3::StaWifiMac","Ssid",SsidValue(ssid),"ActiveProbing",BooleanValue(false)); auto sd=wifi.Install(phy,mac,sta);
  mac.SetType("ns3::ApWifiMac","Ssid",SsidValue(ssid)); auto ad=wifi.Install(phy,mac,ap);
  MobilityHelper m; m.SetMobilityModel("ns3::ConstantPositionMobilityModel"); m.Install(ap);
  MobilityHelper sm; sm.SetMobilityModel("ns3::ConstantVelocityMobilityModel"); sm.Install(sta);
  sta.Get(0)->GetObject<ConstantVelocityMobilityModel>()->SetPosition(Vector(5,0,0));
  sta.Get(0)->GetObject<ConstantVelocityMobilityModel>()->SetVelocity(moving?Vector(1,0,0):Vector(0,0,0));
  InternetStackHelper internet; internet.Install(sta); internet.Install(ap); Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); ip.Assign(ad); auto si=ip.Assign(sd);
  uint16_t port=9000; PacketSinkHelper sink("ns3::UdpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port)); auto s=sink.Install(ap.Get(0)); s.Start(Seconds(1)); s.Stop(Seconds(16));
  OnOffHelper src("ns3::UdpSocketFactory",InetSocketAddress(si.GetAddress(0),port)); src.SetAttribute("DataRate",StringValue("1Mbps")); src.SetAttribute("PacketSize",UintegerValue(1000)); src.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]")); src.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]")); auto a=src.Install(sta.Get(0)); a.Start(Seconds(2)); a.Stop(Seconds(15));
  FlowMonitorHelper fm; auto mon=fm.InstallAll(); Simulator::Stop(Seconds(16)); Simulator::Run(); mon->CheckForLostPackets();
  for(auto const&kv:mon->GetFlowStats()){auto x=kv.second; std::cout<<"moving="<<moving<<" tx="<<x.txPackets<<" rx="<<x.rxPackets<<" lost="<<x.lostPackets<<" rxMbps="<<(x.rxBytes*8.0/13.0/1e6)<<"\n";}
  std::cout<<"Bytes received: "<<DynamicCast<PacketSink>(s.Get(0))->GetTotalRx()<<"\n"; Simulator::Destroy(); return 0;
}
