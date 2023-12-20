
tc qdisc replace dev s1-eth2 root handle 1: dualpi2 target 5ms tupdate 16ms alpha 0.156250 beta 3.195312 l4s_ect coupling_factor 2 drop_on_overload step_thresh 1ms drop_dequeue split_gso classic_protection 10% limit 100
tc qdisc replace dev s1-eth1 root handle 1: dualpi2 target 5ms tupdate 16ms alpha 0.156250 beta 3.195312 l4s_ect coupling_factor 2 drop_on_overload step_thresh 1ms drop_dequeue split_gso classic_protection 10% limit 100
