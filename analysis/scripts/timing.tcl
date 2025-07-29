read_liberty analysis/pdk_files/sky130_fd_sc_hd__tt_025C_1v80.lib
read_verilog analysis/netlist.v
link_design tt_um_hamming_top

read_sdc analysis/scripts/constraints.sdc

report_checks -path_delay max -fields {startpoint endpoint arrival required slack} -digits 4 > analysis/report.txt
report_wns > analysis/report_wns.txt
report_tns > analysis/report_tns.txt