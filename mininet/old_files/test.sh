tc qdisc add dev s1-eth2 root handle 1: tbf rate 50mbit burst 1514 limit 1000000
