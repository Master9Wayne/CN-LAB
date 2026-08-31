import nest

r_hq = nest.Router("R-HQ")
r_pune = nest.Router("R-PUNE")
r_hyd = nest.Router("R-HYD")
isp = nest.Router("ISP")

sw_hq = nest.Switch("SW-HQ")
sw_pune = nest.Switch("SW-PUNE")
sw_hyd = nest.Switch("SW-HYD")

hr_pc = nest.Node("HR-PC")
eng_pc = nest.Node("ENG-PC")
sales_pc = nest.Node("SALES-PC")
pune_pc = nest.Node("PUNE-PC")
hyd_pc = nest.Node("HYD-PC")
file_server = nest.Node("FileServer")

nest.Connect(hr_pc, sw_hq)
nest.Connect(eng_pc, sw_hq)
nest.Connect(sales_pc, sw_hq)
nest.Connect(file_server, sw_hq)
nest.Connect(sw_hq, r_hq)

nest.Connect(pune_pc, sw_pune)
nest.Connect(sw_pune, r_pune)

nest.Connect(hyd_pc, sw_hyd)
nest.Connect(sw_hyd, r_hyd)

l1 = nest.Connect(r_hq, isp)
l2 = nest.Connect(r_pune, isp)
l3 = nest.Connect(r_hyd, isp)

l1[0].set_attributes(bandwidth="8mbit", delay="20ms")
l1[1].set_attributes(bandwidth="8mbit", delay="20ms")
l2[0].set_attributes(bandwidth="5mbit", delay="30ms")
l2[1].set_attributes(bandwidth="5mbit", delay="30ms")
l3[0].set_attributes(bandwidth="5mbit", delay="30ms")
l3[1].set_attributes(bandwidth="5mbit", delay="30ms")

hr_pc.get_interfaces()[0].set_address("192.168.20.2/24")
eng_pc.get_interfaces()[0].set_address("192.168.30.2/24")
sales_pc.get_interfaces()[0].set_address("192.168.40.2/24")
file_server.get_interfaces()[0].set_address("192.168.10.10/24")
pune_pc.get_interfaces()[0].set_address("192.168.120.2/24")
hyd_pc.get_interfaces()[0].set_address("192.168.220.2/24")

r_hq.execute("ip link add link eth0 name eth0.10 type vlan id 10")
r_hq.execute("ip addr add 192.168.10.1/24 dev eth0.10")
r_hq.execute("ip link set dev eth0.10 up")
r_hq.execute("ip link add link eth0 name eth0.20 type vlan id 20")
r_hq.execute("ip addr add 192.168.20.1/24 dev eth0.20")
r_hq.execute("ip link set dev eth0.20 up")

r_hq.get_interfaces()[1].set_address("10.0.0.1/30")
isp.get_interfaces()[0].set_address("10.0.0.2/30")
r_pune.get_interfaces()[1].set_address("10.0.0.5/30")
isp.get_interfaces()[1].set_address("10.0.0.6/30")
r_hyd.get_interfaces()[1].set_address("10.0.0.9/30")
isp.get_interfaces()[2].set_address("10.0.0.10/30")

r_hq.add_route("0.0.0.0/0", "10.0.0.2")
r_pune.add_route("0.0.0.0/0", "10.0.0.6")
r_hyd.add_route("0.0.0.0/0", "10.0.0.10")

isp.add_route("192.168.10.0/24", "10.0.0.1")
isp.add_route("192.168.20.0/24", "10.0.0.1")
isp.add_route("192.168.120.0/24", "10.0.0.5")
isp.add_route("192.168.220.0/24", "10.0.0.9")

nest.experiment.run()