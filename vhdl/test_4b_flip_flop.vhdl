library IEEE;
use IEEE.std_logic_1164.all;

entity Test_Flip_Flop_4b is
end Test_Flip_Flop_4b; 

architecture Testbench_Flip_Flop_4b of Test_Flip_Flop_4b is

  component Flip_Flop_4b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       v1: in std_logic := '0';
       v2: in std_logic := '0';
       v3: in std_logic := '0';
       v4: in std_logic := '0';
       q1: out std_logic := '0';
       q2: out std_logic := '0';
       q3: out std_logic := '0';
       q4: out std_logic := '0');
  end component;
  
  signal clk, set : std_logic := '0';
  signal v1, v2, v3, v4 : std_logic := '0';
  signal q1, q2, q3, q4 : std_logic := '0';
  constant CLK_PERIOD : time := 10 ns;

begin
  uut : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    v1 => v1,
    v2 => v2,
    v3 => v3, 
    v4 => v4,
    q1 => q1,
    q2 => q2,
    q3 => q3,
    q4 => q4
    );
  
  Clk_process :process
    begin
        Clk <= '0';
        wait for CLK_PERIOD/2;
        Clk <= '1';
        wait for CLK_PERIOD/2; 
    end process;

    Tests :process
    begin      
      wait for CLK_PERIOD / 2; -- init

      set <= '1';
      v1 <= '0';
      v2 <= '1';
      v3 <= '0';
      v4 <= '1';            
      wait for CLK_PERIOD;
      assert (q1 = '0' and q2 = '1' and q3 = '0' and q4 = '1')
        report "flip flop test 1 faillure" severity error;
      
      set <= '0';
      v1 <= '1';
      v2 <= '0';
      v3 <= '1';
      v4 <= '0';            
      wait for CLK_PERIOD;
      assert (q1 = '0' and q2 = '1' and q3 = '0' and q4 = '1')
        report "flip flop test 2 faillure" severity error;
      
      set <= '1';
      wait for CLK_PERIOD;
      assert (q1 = '1' and q2 = '0' and q3 = '1' and q4 = '0')
        report "flip flop test 3 faillure" severity error;
      
      set <= '0';
      v1 <= '0';
      v2 <= '0';
      v3 <= '0';
      v4 <= '0';            
      wait for CLK_PERIOD;
      assert (q1 = '1' and q2 = '0' and q3 = '1' and q4 = '0')
        report "flip flop test 4 faillure" severity error;
      
      wait;
    end process;
    
end Testbench_Flip_Flop_4b;
