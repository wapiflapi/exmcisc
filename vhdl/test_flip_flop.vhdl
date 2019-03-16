library IEEE;
use IEEE.std_logic_1164.all;

entity Test_Flip_Flop is
end Test_Flip_Flop; 

architecture Testbench_Flip_Flop of Test_Flip_Flop is

  component Flip_Flop is
  port(clk: in std_logic;
       set: in std_logic;
       val: in std_logic;
       Q: out std_logic);
  end component;
  
  signal clk, set, val : std_logic;
  signal Q : std_logic;
  constant CLK_PERIOD : time := 10 ns;

begin
  uut : Flip_Flop port map (
    clk => clk,
    set => set,
    val => val,
    Q => Q
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
      set <= '0';
      val <= '0';
      wait for CLK_PERIOD / 2; -- init

      set <= '1';
      val <= '1';
      wait for CLK_PERIOD;
      assert (Q = '1')
        report "flip flop test 1 faillure" severity error;
      
      set <= '0';
      val <= '0';
      wait for CLK_PERIOD;
      assert (Q = '1')
        report "flip flop test 2 faillure" severity error;
      
      set <= '1';
      val <= '0';
      wait for CLK_PERIOD;
      assert (Q = '0')
        report "flip flop test 3 faillure" severity error;
      
      set <= '0';
      val <= '1';
      wait for CLK_PERIOD;
      assert (Q = '0')
        report "flip flop test 4 faillure" severity error;
      
      wait;
    end process;
    
end Testbench_Flip_Flop;
