#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
using namespace ns3;
int main(int argc,char*argv[]){
  NodeContainer n; n.Create(5); // source, R1, R2, R3, destination
  InternetStackHelper internet; internet.Install(n);
  PointToPointHelper p; p.SetDeviceAttribute("DataRate",StringValue("5Mbps")); p.SetChannelAttribute("Delay",StringValue("5ms"));
  NetDeviceContainer d[4]; for(int k=0;k<4;k++) d[k]=p.Install(n.Get(k),n.Get(k+1));
  Ipv4AddressHelper ip; Ipv4InterfaceContainer ifs[4];
  for(int k=0;k<4;k++){std::ostringstream subnet; subnet<<"10.1."<<(k+1)<<".0"; ip.SetBase(subnet.str().c_str(),"255.255.255.0"); ifs[k]=ip.Assign(d[k]);}
  Ipv4GlobalRoutingHelper::PopulateRoutingTables();
  uint16_t port=7000; UdpServerHelper srv(port); auto s=srv.Install(n.Get(4)); s.Start(Seconds(1)); s.Stop(Seconds(10));
  UdpClientHelper cli(ifs[3].GetAddress(1),port); cli.SetAttribute("MaxPackets",UintegerValue(1000)); cli.SetAttribute("Interval",TimeValue(MilliSeconds(10))); cli.SetAttribute("PacketSize",UintegerValue(512));
  auto a=cli.Install(n.Get(0)); a.Start(Seconds(2)); a.Stop(Seconds(9));
  std::cout<<"Link subnets:\n"; for(int k=0;k<4;k++) std::cout<<"Link "<<k+1<<": "<<ifs[k].GetAddress(0)<<" <-> "<<ifs[k].GetAddress(1)<<"\n";
  Simulator::Stop(Seconds(10)); Simulator::Run(); std::cout<<"Packets received: "<<DynamicCast<UdpServer>(s.Get(0))->GetReceived(); Simulator::Destroy(); return 0;
}
