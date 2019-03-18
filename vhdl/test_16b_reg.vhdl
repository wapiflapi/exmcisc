library IEEE;
use IEEE.std_logic_1164.all;

entity Test_reg_16b is
end Test_reg_16b; 

architecture Testbench_reg_16b of Test_reg_16b is

  component reg_16b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic_vector(15 downto 0);
       q: out std_logic_vector(15 downto 0));
  end component;
  
  signal clk, set : std_logic := '0';
  signal val: std_logic_vector(15 downto 0) := "0000000000000000";
  signal q: std_logic_vector(15 downto 0) := "0000000000000000";
  constant CLK_PERIOD : time := 10 ns;

begin
  uut : reg_16b port map (
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
      val <= "0101010101010101";
      wait for CLK_PERIOD;
      assert (q = "0101010101010101")
        report "flip flop test 1 faillure" severity error;
      
      set <= '0';
      val <= "1010101010101010";
      wait for CLK_PERIOD;
      assert (q = "0101010101010101") 
        report "flip flop test 2 faillure" severity error;
      
      set <= '1';
      wait for CLK_PERIOD;
      assert (q = "1010101010101010")
        report "flip flop test 3 faillure" severity error;
      
      set <= '0';
      val <= "0000000000000000";
      wait for CLK_PERIOD;
      assert (q = "1010101010101010")
        report "flip flop test 4 faillure" severity error;
      
      wait;
    end process;
    
end Testbench_reg_16b;
