library IEEE;
use IEEE.std_logic_1164.all;

entity Test_Flip_Flop_4b is
end Test_Flip_Flop_4b; 

architecture Testbench_Flip_Flop_4b of Test_Flip_Flop_4b is

  component Flip_Flop_4b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic_vector(3 downto 0);
       q: out std_logic_vector(3 downto 0));
  end component;
  
  signal clk, set : std_logic := '0';
  signal val: std_logic_vector(3 downto 0);
  signal q: std_logic_vector(3 downto 0);
  constant CLK_PERIOD : time := 10 ns;

begin
  uut : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    val => val,
    q => q
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
      val <= "0101";
      wait for CLK_PERIOD;
      assert (q = "0101")
        report "flip flop test 1 faillure" severity error;
      
      set <= '0';
      val <= "1010";
      wait for CLK_PERIOD;
      assert (q = "0101")
        report "flip flop test 2 faillure" severity error;
      
      set <= '1';
      wait for CLK_PERIOD;
      assert (q = "1010")
        report "flip flop test 3 faillure" severity error;
      
      set <= '0';
      val <= "0000";
      wait for CLK_PERIOD;
      assert (q = "1010")
        report "flip flop test 4 faillure" severity error;
      
      wait;
    end process;
    
end Testbench_Flip_Flop_4b;
