#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
import random
import time
import datetime
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

timestamp = str(datetime.datetime.now()).replace(" ", "_")

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet(controller=Controller,  waitConnected=True , link=TCLink, autoStaticArp=True)

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( "h1" , ip='10.0.0.1' )
    h1_eth0 = "h1_eth0"
    h2 = net.addHost( "h2", ip='10.0.0.2' )
    h2_eth0 = "h2_eth0"

    info( '*** Adding switch\n' )

    s1 = net.addSwitch("s1")
    s1_eth0 = "s1_eth0"
    s2 = net.addSwitch("s2")
    s2_eth0 = "s2_eth0"

    info( '*** Creating links\n' )
    net.addLink( h1, s1,  fName1=h1_eth0)
    net.addLink( h2, s2,  fName1=h2_eth0)
    net.addLink(s2, s1, bw=10, delay="1ms")

    info( '*** Starting network\n')
    net.start()

    info("*** Running Dualpi2 test")

    h1.cmd("tc qdisc replace dev %s root handle 1:  fq limit 2048000 flow_limit 1024000" % h1_eth0)
    h2.cmd("tc qdisc replace dev %s root handle 1: fq 2048000 flow_limit 1024000" % h2_eth0)


    for intf in s1.intfList():
        s1.cmd("tc qdisc replace dev %s root handle 1: dualpi2 target 15ms tupdate 16ms alpha 0.156250 beta 3.195312 l4s_ect coupling_factor 2 drop_on_overload step_thresh 1ms drop_dequeue split_gso classic_protection 10%% limit 100" % intf)

    for intf in s2.intfList():
        s2.cmd("tc qdisc replace dev %s root handle 1: dualpi2 target 15ms tupdate 16ms alpha 0.156250 beta 3.195312 l4s_ect coupling_factor 2 drop_on_overload step_thresh 1ms drop_dequeue split_gso classic_protection 10%% limit 100" % intf)

    s1.cmd("tc qdisc > settings")

    time.sleep(1)

    info("*** Hello")

    h1.cmd("tcpdump -w capture_h1_%s.pcap &" % timestamp)
    h2.cmd("tcpdump -w capture_h2_%s.pcap &" % timestamp)
    info("*** TCPDUMP started")

    h1.cmd("iperf -s -e > h1_dualpi &")
    time.sleep(1)

    h2.cmd("iperf -c 10.0.0.1 -e -t 60 &")
    h2.cmd("iperf -c 10.0.0.1 -e -t 60 &")
    h2.cmd("iperf -c 10.0.0.1 -e -t 60 > h2_dualpi")
    info("DONE")
    h1.cmd("killall iperf")
    time.sleep(1)
    info("*** New test")

    #s1.cmd("tc qdisc replace dev %s root handle 1: pfifo" % s1_eth0)
    #s2.cmd("tc qdisc replace dev %s root handle 1: pfifo" % s2_eth0)

    #h1.cmd("iperf -s -e > h1_pfifo &")
    #time.sleep(1)
    #h2.cmd("iperf -c 10.0.0.1 -e -t 10 > h2_pfifo")

    #s1.cmd("tc qdisc replace dev %s root handle 1: red" % s1_eth0)
    #s2.cmd("tc qdisc replace dev %s root handle 1: red" % s2_eth0)

    #h1.cmd("killall iperf")
    #time.sleep(1)

    #h1.cmd("iperf -s -e > h1_red &")
    #time.sleep(1)
    #h2.cmd("iperf -c 10.0.0.1 -e -t 10 > h2_red")

    info( '*** Stopping network' )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
