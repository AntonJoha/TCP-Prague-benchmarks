#!/usr/bin/env python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
import os
import random
import time
import datetime
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import logging

log = logging.getLogger()

logging.basicConfig(level = logging.INFO)

def _get_dualpi2_command(intf, dualpi2_params):

    command = "tc qdisc add dev %s parent 1: handle 110: dualpi2" % intf

    for key in dualpi2_params:
        command += " " + str(key) + " " + dualpi2_params[key]

    command += " > %s_out_hello" % intf
    return command

def get_dualpi2_params():

    toReturn = {}
    toReturn["target"] = "15ms"
    toReturn["tupdate"] = "16ms"
    toReturn["alpha"] = "0.156250"
    toReturn["beta"] = "3.195312"
    toReturn["l4s_ect"] = ""
    toReturn["coupling_factor"] = "2"
    toReturn["drop_on_overload"] = ""
    toReturn["step_thresh"] = "1ms"
    toReturn["drop_dequeue"] = ""
    toReturn["split_gso"] = ""
    toReturn["classic_protection"] = "10%"
    toReturn["limit"] = "10000"
    return toReturn


#Just check if the output of tc qdisc contain fq, this means that it's used
#There exists a risk of false positives of course, but I don't think it's an issue in this simple case. 
def _assert_queue(node, q):
    node.cmd("tc qdisc | grep %s > /tmp/out_qdisc" % q)
    size = os.path.getsize("/tmp/out_qdisc")
    return size > 10

def run_experiment(dualpi2_params, delay="30ms", num_flows=3, iperf_time=10, tcpdump=False, outfile="result"):
    print(dualpi2_params)

    net = Mininet(controller=Controller,  waitConnected=True , link=TCLink, autoStaticArp=True)

    log.info( '*** Adding controller' )
    net.addController( 'c0' )

    log.info( '*** Adding hosts' )
    h1 = net.addHost( "h1" , ip='10.0.0.1' )
    h2 = net.addHost( "h2", ip='10.0.0.2' )
    h1_eth0 = "h1-eth0"
    h2_eth0 = "h2-eth0"

    log.info( '*** Adding switches' )

    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")

    log.info( '*** Creating links' )
    net.addLink( h1, s1, fname1=h1_eth0, delay=delay )
    net.addLink( h2, s2, fname1=h2_eth0)
    net.addLink(s1, s2 )


    net.start()
 
    log.info("*** Setting fq at end nodes")
    h1.cmd("tc qdisc replace dev %s root handle 1: fq" % h1_eth0)
    h1.cmd("tc qdisc")
    h2.cmd("tc qdisc replace dev %s root handle 1: fq "% h2_eth0)
    h2.cmd("tc qdisc")


    log.info("*** Assert that fq works")
    
    for i in [h1, h2]:
        if _assert_queue(i, "fq") == False:
            net.stop()
            log.warning("FQ couldn't be set for %s" % i.name)
            return


    for intf in s2.intfList():
        s2.cmd("tc qdisc replace dev %s root handle 1: tbf rate 50mbit burst 1514 latency 20ms" % (intf))
        s2.cmd(_get_dualpi2_command(intf, dualpi2_params))

    if _assert_queue(s2, "dualpi2") == False:
        net.stop()
        log.warning("dualpi2 couldn't be set for %s" % s2.name)
        return

    time.sleep(1)

    if tcpdump:
        timestamp = str(datetime.datetime.now()).replace(" ", "_")
        h1.cmd("tcpdump -w capture_h1_%s.pcap &" % timestamp)
        h2.cmd("tcpdump -w capture_h2_%s.pcap &" % timestamp)

    h1.cmd("iperf -s -e &")
    s1.cmd("tc qdisc")


    time.sleep(1)

    for i in range(num_flows):
        h2.cmd("iperf -c 10.0.0.1 -e -t %s &"% (iperf_time) ) 
    
    h2.cmd("iperf -c 10.0.0.1 -e -t %s -i 0.1 > %s" % (iperf_time, outfile))

    if tcpdump:
        h1.cmd("killall tcpdump")
        h2.cmd("killall tcpdump")

    h2.cmd("killall iperf")
    h1.cmd("killall iperf")
    net.stop()

if __name__ == "__main__":
    run_experiment(get_dualpi2_params())
