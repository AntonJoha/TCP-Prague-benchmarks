#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
import time
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet(controller=Controller,  waitConnected=True , link=TCLink, autoStaticArp=True)

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )

    info( '*** Adding switch\n' )
    s3 = net.addSwitch( 's3' )

    eth0 = "s3-eth0"
    eth1 = "s3-eth1"

    info( '*** Creating links\n' )
    net.addLink( h1, s3 , bw=10, delay="10ms", use_htb=True, intfName2=eth0, fName1=eth0)
    net.addLink( h2, s3 , bw=10, delay="10ms", use_htb=True, intfName2=eth1, fName1=eth1)


    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )

    for i in [eth0, eth1]:
        s3.cmd("tc qdisc replace dev %s root handle 1: fq limit 20480 flow_limit 10240" % i)

    h1.cmd("tc qdisc replace dev %s root handle 1: fq limit 20480 flow_limit 10240" % eth0)
    h2.cmd("tc qdisc replace dev %s root handle 1: fq limit 20480 flow_limit 10240 ce_threshold 2.0ms" % eth1)

    time.sleep(1)

    h1.cmd("killall iperf")
    time.sleep(1)
 
    h1.cmd("iperf -s -e > h1_fq &")
    time.sleep(1)
    h2.cmd("iperf -c 10.0.0.1 -e -t 10 > h2_fq")

    h1.cmd("killall iperf")
    time.sleep(1)

    for i in [eth0, eth1]:
        s3.cmd("tc qdisc replace dev %s root handle 1: pfifo" % i)
    h1.cmd("tc qdisc replace dev %s root handle 1: pfifo" % eth0)
    h2.cmd("tc qdisc replace dev %s root handle 1: pfifo" % eth1)




    h1.cmd("iperf -s -e > h1_pfifo &")
    time.sleep(1)
    h2.cmd("iperf -c 10.0.0.1 -e -t 10 > h2_pfifo")



    for i in [eth0, eth1]:
        s3.cmd("tc qdisc replace dev %s root handle 1: red limit 400000 min 30000 max 90000 avpkt 1000 burst 55" % i)
    h1.cmd("tc qdisc replace dev %s root handle 1: red limit 400000 min 30000 max 90000 avpkt 1000 burst 55" % eth0)
    h2.cmd("tc qdisc replace dev %s root handle 1: red limit 400000 min 30000 max 90000 avpkt 1000 burst 55" % eth1)
    
    time.sleep(1)

    h1.cmd("iperf -s -e > h1_red &")
    time.sleep(1)
    h2.cmd("iperf -c 10.0.0.1 -e -t 10 > h2_red")




    info( '*** Stopping network' )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
