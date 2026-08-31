import nest

r1 = nest.Router("R1")
r2 = nest.Router("R2")
r3 = nest.Router("R3")
r4 = nest.Router("R4")

sw1 = nest.Switch("SW1")
sw2 = nest.Switch("SW2")
sw3 = nest.Switch("SW3")

cse_pc1 = nest.Node("CSE-PC1")
cse_pc2 = nest.Node("CSE-PC2")
ece_pc1 = nest.Node("ECE-PC1")
ece_pc2 = nest.Node("ECE-PC2")
me_pc1 = nest.Node("ME-PC1")
me_pc2 = nest.Node("ME-PC2")
server = nest.Node("Server")

nest.Connect(cse_pc1, sw1)
nest.Connect(cse_pc2, sw1)
nest.Connect(sw1, r1)

nest.Connect(ece_pc1, sw2)
nest.Connect(ece_pc2, sw2)
nest.Connect(sw2, r1)

nest.Connect(me_pc1, sw3)
nest.Connect(me_pc2, sw3)
nest.Connect(sw3, r2)

nest.Connect(server, r3)

r1_r2 = nest.Connect(r1, r2)
r2_r3 = nest.Connect(r2, r3)
r3_r4 = nest.Connect(r3, r4)

r1_r2[0].set_attributes(bandwidth="10mbit", delay="10ms")
r1_r2[1].set_attributes(bandwidth="10mbit", delay="10ms")
r2_r3[0].set_attributes(bandwidth="5mbit", delay="20ms")
r2_r3[1].set_attributes(bandwidth="5mbit", delay="20ms")
r3_r4[0].set_attributes(bandwidth="5mbit", delay="50ms")
r3_r4[1].set_attributes(bandwidth="5mbit", delay="50ms")

cse_pc1.get_interfaces()[0].set_address("192.168.10.2/24")
cse_pc2.get_interfaces()[0].set_address("192.168.10.3/24")
r1.get_interfaces()[0].set_address("192.168.10.1/24")

ece_pc1.get_interfaces()[0].set_address("192.168.20.2/24")
ece_pc2.get_interfaces()[0].set_address("192.168.20.3/24")
r1.get_interfaces()[1].set_address("192.168.20.1/24")

me_pc1.get_interfaces()[0].set_address("192.168.30.2/24")
me_pc2.get_interfaces()[0].set_address("192.168.30.3/24")
r2.get_interfaces()[0].set_address("192.168.30.1/24")

r1.get_interfaces()[2].set_address("10.0.0.1/24")
r2.get_interfaces()[1].set_address("10.0.0.2/24")

r2.get_interfaces()[2].set_address("20.0.0.1/24")
r3.get_interfaces()[0].set_address("20.0.0.2/24")

r3.get_interfaces()[1].set_address("30.0.0.1/24")
r4.get_interfaces()[0].set_address("30.0.0.2/24")

server.get_interfaces()[0].set_address("192.168.100.2/24")
r3.get_interfaces()[2].set_address("192.168.100.1/24")

r1.add_route("192.168.30.0/24", "10.0.0.2")
r1.add_route("192.168.100.0/24", "10.0.0.2")
r1.add_route("0.0.0.0/0", "10.0.0.2")

r2.add_route("192.168.10.0/24", "10.0.0.1")
r2.add_route("192.168.20.0/24", "10.0.0.1")
r2.add_route("192.168.100.0/24", "20.0.0.2")
r2.add_route("0.0.0.0/0", "20.0.0.2")

r3.add_route("192.168.10.0/24", "20.0.0.1")
r3.add_route("192.168.20.0/24", "20.0.0.1")
r3.add_route("192.168.30.0/24", "20.0.0.1")
r3.add_route("0.0.0.0/0", "30.0.0.2")

r4.add_route("192.168.0.0/16", "30.0.0.1")
r4.add_route("10.0.0.0/8", "30.0.0.1")

nest.experiment.run()