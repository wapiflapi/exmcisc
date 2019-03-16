#!/bin/sh

ghdl -a *.vhdl
ghdl -e Test_Flip_Flop
timeout 1 ghdl -r Test_Flip_Flop --vcd=test_flip_flop.vcd
echo "To see results do 'gtkwave test_flip_flop.vcd'"
