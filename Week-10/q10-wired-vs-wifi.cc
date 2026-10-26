#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;
int main(int argc,char*argv[]){
  NodeContainer wired; wired.Create(2); InternetStackHelper internet; internet.Install(wired);
  PointToPointHelper p; p.SetDeviceAttribute("DataRate",StringValue("10Mbps")); p.SetChannelAttribute("Delay",StringValue("5ms")); auto wd=p.Install(wired);
  Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); auto wi=ip.Assign(wd);
  NodeContainer sta; sta.Create(1); NodeContainer ap; ap.Create(1);
  YansWifiChannelHelper channel=YansWifiChannelHelper::Default(); YansWifiPhyHelper phy; phy.SetChannel(channel.Create());
  WifiHelper wifi; wifi.SetStandard(WIFI_STANDARD_80211g); WifiMacHelper mac; Ssid ssid=Ssid("compare");
  mac.SetType("ns3::StaWifiMac","Ssid",SsidValue(ssid),"ActiveProbing",BooleanValue(false)); auto sd=wifi.Install(phy,mac,sta);
  mac.SetType("ns3::ApWifiMac","Ssid",SsidValue(ssid)); auto ad=wifi.Install(phy,mac,ap);
  MobilityHelper mob; mob.SetMobilityModel("ns3::ConstantPositionMobilityModel"); mob.Install(sta); mob.Install(ap);
  internet.Install(sta); internet.Install(ap); ip.SetBase("10.1.2.0","255.255.255.0"); auto ai=ip.Assign(ad); auto si=ip.Assign(sd);
  uint16_t port=9000;
  PacketSinkHelper sinkW("ns3::UdpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port)); auto sw=sinkW.Install(wired.Get(1)); sw.Start(Seconds(1)); sw.Stop(Seconds(11));
  PacketSinkHelper sinkA("ns3::UdpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port)); auto sa=sinkA.Install(ap.Get(0)); sa.Start(Seconds(1)); sa.Stop(Seconds(11));
  OnOffHelper srcW("ns3::UdpSocketFactory",InetSocketAddress(wi.GetAddress(1),port)); srcW.SetAttribute("DataRate",StringValue("1Mbps")); srcW.SetAttribute("PacketSize",UintegerValue(1000)); srcW.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]")); srcW.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]")); auto aw=srcW.Install(wired.Get(0)); aw.Start(Seconds(2)); aw.Stop(Seconds(10));
  OnOffHelper srcA("ns3::UdpSocketFactory",InetSocketAddress(si.GetAddress(0),port)); srcA.SetAttribute("DataRate",StringValue("1Mbps")); srcA.SetAttribute("PacketSize",UintegerValue(1000)); srcA.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]")); srcA.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]")); auto aa=srcA.Install(sta.Get(0)); aa.Start(Seconds(2)); aa.Stop(Seconds(10));
  FlowMonitorHelper fm; auto mon=fm.InstallAll(); Simulator::Stop(Seconds(11)); Simulator::Run(); mon->CheckForLostPackets();
  std::cout<<"Wired bytes received: "<<DynamicCast<PacketSink>(sw.Get(0))->GetTotalRx()<<"\n";
  std::cout<<"Wi-Fi bytes received: "<<DynamicCast<PacketSink>(sa.Get(0))->GetTotalRx()<<"\n";
  for(auto const&kv:mon->GetFlowStats()){auto x=kv.second; std::cout<<"flow "<<kv.first<<" tx="<<x.txPackets<<" rx="<<x.rxPackets<<" loss="<<x.lostPackets<<" avgDelayMs="<<(x.rxPackets?1000*x.delaySum.GetSeconds()/x.rxPackets:0)<<"\n";}
  Simulator::Destroy(); return 0;
}
