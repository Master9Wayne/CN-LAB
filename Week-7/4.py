import nest

r_mum = nest.Router("R-MUM")
r_blr = nest.Router("R-BLR")
r_che = nest.Router("R-CHE")
isp = nest.Router("ISP")

sw_mum = nest.Switch("SW-MUM")
sw_dc = nest.Switch("SW-DC")
sw_blr = nest.Switch("SW-BLR")
sw_che = nest.Switch("SW-CHE")

sales_pc = nest.Node("Sales-PC")
web_srv = nest.Node("Web-Server")
db_srv = nest.Node("DB-Server")

nest.Connect(sales_pc, sw_mum)
nest.Connect(sw_mum, r_mum)
nest.Connect(web_srv, sw_dc)
nest.Connect(db_srv, sw_dc)
nest.Connect(sw_dc, r_mum)

l1 = nest.Connect(r_mum, r_blr)
l2 = nest.Connect(r_mum, r_che)
l3 = nest.Connect(r_mum, isp)

l1[0].set_attributes(bandwidth="10mbit", delay="20ms")
l2[0].set_attributes(bandwidth="8mbit", delay="30ms")

sales_pc.get_interfaces()[0].set_address("192.168.10.10/24")
web_srv.get_interfaces()[0].set_address("192.168.40.10/24")

r_mum.get_interfaces()[0].set_address("192.168.10.1/24")
r_mum.get_interfaces()[1].set_address("192.168.40.1/24")
r_mum.get_interfaces()[2].set_address("10.1.1.1/30")
r_blr.get_interfaces()[0].set_address("10.1.1.2/30")
r_mum.get_interfaces()[3].set_address("10.1.2.1/30")
r_che.get_interfaces()[0].set_address("10.1.2.2/30")

r_mum.execute("iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE")
r_mum.add_route("0.0.0.0/0", "203.0.113.2")

nest.experiment.run()