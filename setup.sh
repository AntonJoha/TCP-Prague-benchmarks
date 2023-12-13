git clone https://github.com/L4STeam/iproute2.git
cd iproute2
./configure
make
tc/tc qdisc replace dev eth0 root dualpi2 ...
# You can optionally install (!potentially overwrite) the new
# iproute2 utils with `make install`
