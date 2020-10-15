#!/usr/bin/env python
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.nodelib import LinuxBridge
from mininet.log import setLogLevel

def set_ipv6(host, interface, ip):
    return host.cmd("ip -6 addr add " + ip + " dev " + interface)

def set_ipv6_gateway(host, gateway):
    return host.cmd("ip -6 route add default via " + gateway)

def set_ipv6_device_route(host, subnet, interface):
    return host.cmd("ip -6 route add " + subnet + " dev " + interface)

def set_ipv6_gateway_route(host, subnet, gateway, interface):
    # useful for the forward table
    return host.cmd("ip -6 route add " + subnet +
            " via " + gateway + " dev " + interface)

    


if __name__ == '__main__':
    setLogLevel('info')

    net = Mininet(switch=LinuxBridge, controller=None)

    h1 = net.addHost('h1', ip=None)

    # create rest of the topology here
    s1 = net.addSwitch('s1')
    r1 = net.addHost('r1', ip = None)
    s0 = net.addSwitch('s0')
    r2 = net.addHost('r2', ip = None)
    s2 = net.addSwitch('s2')
    h2 = net.addHost('h2', ip = None)
    r3 = net.addHost('r3', ip = None)
    s3 = net.addSwitch('s3')
    r4 = net.addHost('r4', ip = None)

    # addr info
    h1_eth0_addr = "2001:638:709:a::1/64"
    r1_eth0_addr = "2001:638:709:a::f/64"
    r1_eth1_addr = "2001:638:709:f::1/64"
    r2_eth0_addr = "2001:638:709:f::2/64"
    r2_eth1_addr = "2001:638:709:b::f/64"
    h2_eth0_addr = "2001:638:709:b::1/64"
    r3_eth0_addr = "2001:638:709:a::e/64"
    r3_eth1_addr = "2001:638:709:e::1/64"
    r4_eth0_addr = "2001:638:709:e::2/64"
    r4_eth1_addr = "2001:638:709:b::e/64"

    # subnet info
    subnet1_addr = "2001:638:709:a::/64"
    subnet2_addr = "2001:638:709:f::/64"
    subnet3_addr = "2001:638:709:b::/64"
    subnet4_addr = " 2001:638:709:e::/64"

    # link the router and switches
    net.addLink(h1, s1)
    net.addLink(s1, r1)
    net.addLink(r1, s0)
    net.addLink(s0, r2)
    net.addLink(r2, s2)
    net.addLink(s2, h2)
    net.addLink(s1, r3)
    net.addLink(r3, s3)
    net.addLink(s3, r4)
    net.addLink(r4, s2)

    # configure IPv6 addresses and forwarding table entries here

    # set ipv6 addr and gateway
    print "setup ipv6"
    print set_ipv6(h1, "h1-eth0", h1_eth0_addr)
    print set_ipv6(r1, "r1-eth0", r1_eth0_addr)
    print set_ipv6(r1, "r1-eth1", r1_eth1_addr)
    print set_ipv6(r2, "r2-eth0", r2_eth0_addr)
    print set_ipv6(r2, "r2-eth1", r2_eth1_addr)
    print set_ipv6(h2, "h2-eth0", h2_eth0_addr)
    print set_ipv6(r3, "r3-eth0", r3_eth0_addr)
    print set_ipv6(r3, "r3-eth1", r3_eth1_addr)
    print set_ipv6(r4, "r4-eth0", r4_eth0_addr)
    print set_ipv6(r4, "r4-eth1", r4_eth1_addr)
    print "done setup ipv6"

    # setup the local route
    print "setup forward rules"
    print set_ipv6_device_route(h1, subnet1_addr, "h1-eth0")
    print set_ipv6_device_route(r1, subnet1_addr, "r1-eth0")
    print set_ipv6_device_route(r1, subnet2_addr, "r1-eth1")
    print set_ipv6_device_route(r2, subnet2_addr, "r2-eth0")
    print set_ipv6_device_route(r2, subnet3_addr, "r2-eth1")
    print set_ipv6_device_route(h2, subnet3_addr, "h2-eth0")
    print set_ipv6_device_route(r3, subnet1_addr, "r3-eth0")
    print set_ipv6_device_route(r3, subnet4_addr, "r3-eth1")
    print set_ipv6_device_route(r4, subnet4_addr, "r4-eth0")
    print set_ipv6_device_route(r4, subnet3_addr, "r4-eth1")
    print "done setup forward rules"

    # setup the gateway
    print "setup gateway"
    print set_ipv6_gateway(h1, r1_eth0_addr[:-3])
    print set_ipv6_gateway(h2, r4_eth1_addr[:-3])
    print "done setup gateway"

    # setup router forward table
    print "setup router forward table"
    print set_ipv6_gateway_route(r1, subnet3_addr, r2_eth0_addr[:-3], "r1-eth1")
    print set_ipv6_gateway_route(r2, subnet1_addr, r1_eth1_addr[:-3], "r2-eth0")
    print set_ipv6_gateway_route(r3, subnet3_addr, r4_eth0_addr[:-3], "r3-eth1")
    print set_ipv6_gateway_route(r4, subnet1_addr, r3_eth1_addr[:-3], "r4-eth0")
    print "done setup router forward table"

    # router forwarding
    print "enable forwarding for routers"
    r1.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
    r2.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
    r3.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
    r4.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
    print "done enabling forwarding for routers"

    print h1.cmd("ip -V")
    

    net.start()
    CLI(net)
    net.stop()
