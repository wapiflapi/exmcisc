#!/bin/sh

ghdl -a *.vhdl
ghdl -e Test_Flip_Flop_4b
timeout 1 ghdl -r Test_Flip_Flop_4b --vcd=test_flip_flop_4b.vcd
echo "To see results do 'gtkwave test_flip_flop_4b.vcd'"
