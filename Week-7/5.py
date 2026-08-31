import nest

r_ch = nest.Router("R-CH")
r_psd = nest.Router("R-PSD")
r_scc = nest.Router("R-SCC")
r_wifi = nest.Router("R-WIFI")
isp = nest.Router("ISP")

sw_ch = nest.Switch("SW-CH")
sw_psd = nest.Switch("SW-PSD")

emp_pc = nest.Node("Emp-PC")
db_srv = nest.Node("Database-Server")
cctv_srv = nest.Node("CCTV-Server")
svc_pc = nest.Node("Service-PC")

nest.Connect(emp_pc, sw_ch)
nest.Connect(db_srv, sw_ch)
nest.Connect(cctv_srv, sw_ch)
nest.Connect(sw_ch, r_ch)
nest.Connect(svc_pc, sw_psd)
nest.Connect(sw_psd, r_psd)

l1 = nest.Connect(r_ch, r_psd)
l2 = nest.Connect(r_ch, r_scc)
l3 = nest.Connect(r_ch, r_wifi)
l4 = nest.Connect(r_ch, isp)

l1[0].set_attributes(bandwidth="20mbit", delay="20ms")
l2[0].set_attributes(bandwidth="15mbit", delay="25ms")
l3[0].set_attributes(bandwidth="50mbit", delay="15ms")

emp_pc.get_interfaces()[0].set_address("192.168.20.10/24")
db_srv.get_interfaces()[0].set_address("192.168.30.20/24")
svc_pc.get_interfaces()[0].set_address("192.168.60.10/24")

r_ch.get_interfaces()[0].set_address("192.168.20.1/24")
r_ch.get_interfaces()[1].set_address("10.0.0.1/30")
r_psd.get_interfaces()[0].set_address("10.0.0.2/30")
r_ch.get_interfaces()[4].set_address("203.0.113.1/30")

r_ch.execute("sysctl -w net.ipv4.ip_forward=1")
r_ch.execute("iptables -t nat -A POSTROUTING -o eth4 -j MASQUERADE")

nest.experiment.run()