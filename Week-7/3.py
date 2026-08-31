import nest

r_hospital = nest.Router("R-HOSPITAL")
r_clinic = nest.Router("R-CLINIC")
sw_hospital = nest.Switch("SW-HOSPITAL")
sw_clinic = nest.Switch("SW-CLINIC")

doc_pc = nest.Node("Doc-PC")
admin_pc = nest.Node("Admin-PC")
med_device = nest.Node("Med-Device")
staff_pc = nest.Node("Staff-PC")
patient_pc = nest.Node("Patient-PC")

nest.Connect(doc_pc, sw_hospital)
nest.Connect(admin_pc, sw_hospital)
nest.Connect(sw_hospital, r_hospital)

nest.Connect(med_device, sw_clinic)
nest.Connect(staff_pc, sw_clinic)
nest.Connect(patient_pc, sw_clinic)
nest.Connect(sw_clinic, r_clinic)

wan = nest.Connect(r_hospital, r_clinic)
wan[0].set_attributes(bandwidth="512kbit", delay="50ms")
wan[1].set_attributes(bandwidth="512kbit", delay="50ms")

doc_pc.get_interfaces()[0].set_address("192.168.20.10/24")
admin_pc.get_interfaces()[0].set_address("192.168.30.10/24")

med_device.get_interfaces()[0].set_address("10.10.30.10/24")
staff_pc.get_interfaces()[0].set_address("10.10.20.10/24")
patient_pc.get_interfaces()[0].set_address("10.10.20.20/24")

r_hospital.execute("ip link add link eth0 name eth0.20 type vlan id 20")
r_hospital.execute("ip addr add 192.168.20.1/24 dev eth0.20")
r_hospital.execute("ip link set dev eth0.20 up")

r_hospital.get_interfaces()[1].set_address("192.168.1.2/30")
r_clinic.get_interfaces()[0].set_address("10.10.10.2/30")

r_hospital.add_route("10.10.0.0/16", "10.10.10.2")
r_clinic.add_route("192.168.0.0/16", "192.168.1.2")

r_hospital.execute("tc qdisc add dev eth1 root handle 1: htb default 30")
r_hospital.execute("tc class add dev eth1 parent 1: classid 1:1 htb rate 512kbit")
r_hospital.execute("tc class add dev eth1 parent 1:1 classid 1:10 htb rate 300kbit ceil 512kbit prio 1")
r_hospital.execute("tc class add dev eth1 parent 1:1 classid 1:20 htb rate 100kbit ceil 512kbit prio 2")
r_hospital.execute("tc class add dev eth1 parent 1:1 classid 1:30 htb rate 112kbit ceil 512kbit prio 3")
r_hospital.execute("tc filter add dev eth1 protocol ip parent 1:0 prio 1 u32 match ip src 192.168.20.0/24 flowid 1:10")

nest.experiment.run()