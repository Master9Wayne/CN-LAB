import nest

r_core = nest.Router("R-CORE")
r_border = nest.Router("R-BORDER")
isp = nest.Router("ISP")

sw_admin = nest.Switch("SW-ADMIN")
sw_acad = nest.Switch("SW-ACAD")
sw_hostel = nest.Switch("SW-HOSTEL")
sw_dc = nest.Switch("SW-DC")

admin_pc = nest.Node("Admin-PC")
faculty_pc = nest.Node("Faculty-PC")
student_pc = nest.Node("Student-PC")
lms_srv = nest.Node("LMS-Server")

nest.Connect(admin_pc, sw_admin)
nest.Connect(faculty_pc, sw_acad)
nest.Connect(student_pc, sw_hostel)
nest.Connect(lms_srv, sw_dc)

nest.Connect(sw_admin, r_core)
nest.Connect(sw_acad, r_core)
nest.Connect(sw_hostel, r_core)
nest.Connect(sw_dc, r_core)

c1 = nest.Connect(r_core, r_border)
c2 = nest.Connect(r_border, isp)

c1[0].set_attributes(bandwidth="100mbit", delay="5ms")
c2[0].set_attributes(bandwidth="50mbit", delay="20ms")

admin_pc.get_interfaces()[0].set_address("192.168.10.10/24")
faculty_pc.get_interfaces()[0].set_address("192.168.20.10/24")
student_pc.get_interfaces()[0].set_address("192.168.40.10/24")
lms_srv.get_interfaces()[0].set_address("192.168.50.20/24")

r_core.get_interfaces()[0].set_address("192.168.10.1/24")
r_core.get_interfaces()[1].set_address("192.168.20.1/24")
r_core.get_interfaces()[2].set_address("192.168.40.1/24")
r_core.get_interfaces()[3].set_address("192.168.50.1/24")

r_core.get_interfaces()[4].set_address("10.0.0.1/30")
r_border.get_interfaces()[0].set_address("10.0.0.2/30")

r_core.add_route("0.0.0.0/0", "10.0.0.2")
r_border.add_route("192.168.0.0/16", "10.0.0.1")
r_border.execute("iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE")

nest.experiment.run()