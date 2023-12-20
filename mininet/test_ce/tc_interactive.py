#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
import time
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info



def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet(controller=OVSController, waitConnected=True , link=TCLink, autoStaticArp=True)

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h1_eth0 = "h1_eth0"
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    h2_eth0 = "h2_eth0"

    info( '*** Adding switch\n' )

    s1 = net.addSwitch("s1")
    s1_eth0 = "s1_eth0"
    #s2 = net.addSwitch("s2")
    #s2_eth0 = "s2_eth0"

    info( '*** Creating links\n' )
    net.addLink( h1, s1)# , fName1=h1_eth0, fName2="s1_eth0")
    net.addLink( h2, s1)# , fName1=h2_eth0, fName2="s2_eth0")
    #net.addLink(s2, s1)#, bw=1, delay="10ms", fname1=s2_eth0, fname2=s1_eth0)

    for switch in net.switches:
        print("SWITCH: ", switch.name)
        for intf in switch.intfList():
            print(intf)


    info( '*** Starting network\n')
    net.start()

    info("*** Running Dualpi2 test")

    #h1.cmd("tc qdisc replace dev %s root handle 1: fq" % h1_eth0)
    #h2.cmd("tc qdisc replace dev %s root handle 1: fq" % h2_eth0)

    #s1.cmd("tc qdisc replace dev %s root handle 1: dualpi2" % s1_eth0)
    #s2.cmd("tc qdisc replace dev %s root handle 1: dualpi2" % s2_eth0)

    time.sleep(1)
    
    CLI(net)

    info( '*** Stopping network' )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
