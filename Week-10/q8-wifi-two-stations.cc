#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
using namespace ns3;
int main(int argc,char*argv[]){
  double distance=5.0; CommandLine cmd; cmd.AddValue("distance","Station separation from AP in metres",distance); cmd.Parse(argc,argv);
  NodeContainer wifiSta; wifiSta.Create(2); NodeContainer ap; ap.Create(1);
  YansWifiChannelHelper channel=YansWifiChannelHelper::Default(); YansWifiPhyHelper phy; phy.SetChannel(channel.Create());
  WifiHelper wifi; wifi.SetStandard(WIFI_STANDARD_80211g);
  WifiMacHelper mac; Ssid ssid=Ssid("lab-wifi");
  mac.SetType("ns3::StaWifiMac","Ssid",SsidValue(ssid),"ActiveProbing",BooleanValue(false));
  NetDeviceContainer staDev=wifi.Install(phy,mac,wifiSta);
  mac.SetType("ns3::ApWifiMac","Ssid",SsidValue(ssid)); NetDeviceContainer apDev=wifi.Install(phy,mac,ap);
  MobilityHelper mob; Ptr<ListPositionAllocator> pos=CreateObject<ListPositionAllocator>();
  pos->Add(Vector(0,0,0)); pos->Add(Vector(distance,0,0)); pos->Add(Vector(0,1,0)); mob.SetPositionAllocator(pos);
  mob.SetMobilityModel("ns3::ConstantPositionMobilityModel"); mob.Install(wifiSta); mob.Install(ap);
  InternetStackHelper internet; internet.Install(wifiSta); internet.Install(ap);
  Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); ip.Assign(apDev); auto staIf=ip.Assign(staDev);
  uint16_t port=9000; PacketSinkHelper sink("ns3::UdpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port)); auto s=sink.Install(ap.Get(0)); s.Start(Seconds(1)); s.Stop(Seconds(11));
  for(uint32_t i=0;i<2;i++){OnOffHelper src("ns3::UdpSocketFactory",InetSocketAddress(staIf.GetAddress(0),port)); src.SetAttribute("DataRate",StringValue("1Mbps")); src.SetAttribute("PacketSize",UintegerValue(1000)); src.SetAttribute("OnTime",StringValue("ns3::ConstantRandomVariable[Constant=1]")); src.SetAttribute("OffTime",StringValue("ns3::ConstantRandomVariable[Constant=0]")); auto a=src.Install(wifiSta.Get(i)); a.Start(Seconds(2)); a.Stop(Seconds(10));}
  FlowMonitorHelper fm; auto mon=fm.InstallAll(); Simulator::Stop(Seconds(11)); Simulator::Run(); mon->CheckForLostPackets();
  uint64_t tx=0,rx=0; for(auto const&kv:mon->GetFlowStats()){tx+=kv.second.txPackets;rx+=kv.second.rxPackets;}
  std::cout<<"Distance setting: "<<distance<<" m\nTx packets="<<tx<<" Rx packets="<<rx<<" PDR="<<(tx?100.0*rx/tx:0)<<"%\n";
  std::cout<<"Aggregate received bytes at AP: "<<DynamicCast<PacketSink>(s.Get(0))->GetTotalRx()<<"\n"; Simulator::Destroy(); return 0;
}
