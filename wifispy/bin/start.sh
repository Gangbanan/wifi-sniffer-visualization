service network-manager stop
ifconfig wlp2s0 down
iw dev wlp2s0 set type monitor
ifconfig wlp2s0 up


