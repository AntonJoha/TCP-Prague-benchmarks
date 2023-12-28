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
    h2 = net.addHost( "h2", ip='10.0.0.2' )
    h1_eth0 = "h1_eth0"
    h2_eth0 = "h2_eth0"

    info( '*** Adding switch\n' )

    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")

    info( '*** Creating links\n' )
    net.addLink( h1, s1, fname1=h1_eth0)
    net.addLink( h2, s2, fname1=h2_eth0, delay="15ms")
    net.addLink(s1, s2 )

    info( '*** Starting network\n')
    net.start()


    h1.cmd("tc qdisc replace dev %s root handle 1:  fq limit 2048000 flow_limit 1024000" % h1_eth0)
    h2.cmd("tc qdisc replace dev %s root handle 1: fq 2048000 flow_limit 1024000" % h2_eth0)


    for intf in s1.intfList():
        s1.cmd("tc qdisc add dev %s root handle 1: tbf rate 50mbit burst 1514 latency 20ms" % intf)

    for intf in s2.intfList():
        s2.cmd("tc qdisc add dev %s root handle 1: tbf rate 500mbit burst 1514 latency 20ms" % intf)
        s2.cmd("tc qdisc add dev %s parent 1: handle 110:\
                dualpi2 \
                target 15ms \
                tupdate 16ms \
                alpha 0.156250 beta 3.195312 \
                l4s_ect coupling_factor 2 \
                drop_on_overload \
                step_thresh 1ms \
                drop_dequeue \
                split_gso classic_protection 10%% limit 10000" % intf)


    s2.cmd("tc qdisc > settings")

    time.sleep(1)

    info("*** TCPDUMP started\n")
    h1.cmd("tcpdump -w capture_h1_%s.pcap &" % timestamp)

    info("*** Starting iperf server\n")
    h1.cmd("iperf -s -e > h1_dualpi &")

    time.sleep(1)

    info("*** Running Dualpi2 test\n")

    h2.cmd("iperf -c 10.0.0.1 -e -t 10 &")
    h2.cmd("iperf -c 10.0.0.1 -e -t 10 &")
    h2.cmd("iperf -c 10.0.0.1 -e -t 10 > h2_dualpi")
    info("*** Test done, cleaning up\n")

    h1.cmd("killall iperf")
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
