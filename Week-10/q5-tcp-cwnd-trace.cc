#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
using namespace ns3;
static void CwndChange(Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd) {
  *stream->GetStream() << Simulator::Now().GetSeconds() << "\t" << newCwnd << "\n";
}
int main(int argc,char*argv[]){
  NodeContainer n; n.Create(2); PointToPointHelper p; p.SetDeviceAttribute("DataRate",StringValue("5Mbps")); p.SetChannelAttribute("Delay",StringValue("10ms"));
  auto d=p.Install(n); InternetStackHelper internet; internet.Install(n); Ipv4AddressHelper ip; ip.SetBase("10.1.1.0","255.255.255.0"); auto i=ip.Assign(d);
  AsciiTraceHelper ascii; auto stream=ascii.CreateFileStream("cwnd-trace.txt");
  Config::ConnectWithoutContext("/NodeList/0/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow",MakeBoundCallback(&CwndChange,stream));
  uint16_t port=5000; PacketSinkHelper sink("ns3::TcpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port));
  auto s=sink.Install(n.Get(1)); s.Start(Seconds(0)); s.Stop(Seconds(20));
  BulkSendHelper src("ns3::TcpSocketFactory",InetSocketAddress(i.GetAddress(1),port)); src.SetAttribute("MaxBytes",UintegerValue(0));
  auto a=src.Install(n.Get(0)); a.Start(Seconds(1)); a.Stop(Seconds(19));
  Simulator::Stop(Seconds(20)); Simulator::Run();
  std::cout<<"TCP bytes received: "<<DynamicCast<PacketSink>(s.Get(0))->GetTotalRx()<<"\n";
  Simulator::Destroy(); return 0;
}
