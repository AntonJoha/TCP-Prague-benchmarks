
PATH=$PATH:/sbin
# some preparations for having better paced traffic and reduce bursts for each network interface $NETIF that sends L4S traffic
# Avoid processing 64K packets in the kernel, which will send those packets in a burst independent of the pacing (lro only for newer NICS and kernels that support it):
sudo ethtool -K enp0s3 tso off gso off gro off lro off
# fq qdisc needs to be configured on clients and server NICS (instead of fq_codel; fq is the only one that supports the pacing)
sudo tc qdisc replace dev enp0s3 root handle 1: fq limit 20480 flow_limit 10240
# Enable Accurate ECN (only needed for BBR2 and DCTCP, not needed for Prague)
sysctl -w net.ipv4.tcp_ecn=3
# set Prague congestion control system wide (or in the application with socket options)
sysctl -w net.ipv4.tcp_congestion_control=prague
