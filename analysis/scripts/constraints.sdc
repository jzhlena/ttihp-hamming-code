set period 10
create_clock -period $period [get_ports clk]

set clk_period_factor .2
set delay [expr $period * $clk_period_factor]
set_input_delay $delay -clock clk [all_inputs]
set_output_delay $delay -clock clk [all_outputs]

set_input_transition .1 [all_inputs]
