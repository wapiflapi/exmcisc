library IEEE;
use IEEE.std_logic_1164.all;

entity Test_reg_16b is
end Test_reg_16b; 

architecture Testbench_reg_16b of Test_reg_16b is

  component reg_16b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       v1: in std_logic := '0';
       v2: in std_logic := '0';
       v3: in std_logic := '0';
       v4: in std_logic := '0';
       v5: in std_logic := '0';
       v6: in std_logic := '0';
       v7: in std_logic := '0';
       v8: in std_logic := '0';
       v9: in std_logic := '0';
       v10: in std_logic := '0';
       v11: in std_logic := '0';
       v12: in std_logic := '0';
       v13: in std_logic := '0';
       v14: in std_logic := '0';
       v15: in std_logic := '0';
       v16: in std_logic := '0';
       q1: out std_logic := '0';
       q2: out std_logic := '0';
       q3: out std_logic := '0';
       q4: out std_logic := '0';
       q5: out std_logic := '0';
       q6: out std_logic := '0';
       q7: out std_logic := '0';
       q8: out std_logic := '0';
       q9: out std_logic := '0';
       q10: out std_logic := '0';
       q11: out std_logic := '0';
       q12: out std_logic := '0';
       q13: out std_logic := '0';
       q14: out std_logic := '0';
       q15: out std_logic := '0';
       q16: out std_logic := '0');
  end component;
  
  signal clk, set : std_logic := '0';
  signal v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16 : std_logic := '0';
  signal q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16 : std_logic := '0';
  constant CLK_PERIOD : time := 10 ns;

begin
  uut : reg_16b port map (
    clk => clk,
    set => set,
    v1 => v1,
    v2 => v2,
    v3 => v3, 
    v4 => v4,
    v5 => v5,
    v6 => v6,
    v7 => v7, 
    v8 => v8,
    v9 => v9,
    v10 => v10,
    v11 => v11, 
    v12 => v12,
    v13 => v13,
    v14 => v14,
    v15 => v15, 
    v16 => v16,
    q1 => q1,
    q2 => q2,
    q3 => q3,
    q4 => q4,
    q5 => q5,
    q6 => q6,
    q7 => q7,
    q8 => q8,
    q9 => q9,
    q10 => q10,
    q11 => q11,
    q12 => q12,
    q13 => q13,
    q14 => q14,
    q15 => q15,
    q16 => q16
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
      v5 <= '0';
      v6 <= '1';
      v7 <= '0';
      v8 <= '1';            
      v9 <= '0';
      v10 <= '1';
      v11 <= '0';
      v12 <= '1';            
      v13 <= '0';
      v14 <= '1';
      v15 <= '0';
      v16 <= '1';            
      wait for CLK_PERIOD;
      assert (q1 = '0' and q2 = '1' and q3 = '0' and q4 = '1' and q5 = '0' and q6 = '1' and q7 = '0' and q8 = '1' and q9 = '0' and q10 = '1' and q11 = '0' and q12 = '1' and q13 = '0' and q14 = '1' and q15 = '0' and q16 = '1')
        report "flip flop test 1 faillure" severity error;
      
      set <= '0';
      v1 <= '1';
      v2 <= '0';
      v3 <= '1';
      v4 <= '0';            
      v5 <= '1';
      v6 <= '0';
      v7 <= '1';
      v8 <= '0';            
      v9 <= '1';
      v10 <= '0';
      v11 <= '1';
      v12 <= '0';            
      v13 <= '1';
      v14 <= '0';
      v15 <= '1';
      v16 <= '0';            
      wait for CLK_PERIOD;
      assert (q1 = '0' and q2 = '1' and q3 = '0' and q4 = '1' and q5 = '0' and q6 = '1' and q7 = '0' and q8 = '1' and q9 = '0' and q10 = '1' and q11 = '0' and q12 = '1' and q13 = '0' and q14 = '1' and q15 = '0' and q16 = '1')
        report "flip flop test 2 faillure" severity error;
      
      set <= '1';
      wait for CLK_PERIOD;
      assert (q1 = '1' and q2 = '0' and q3 = '1' and q4 = '0' and q5 = '1' and q6 = '0' and q7 = '1' and q8 = '0' and q9 = '1' and q10 = '0' and q11 = '1' and q12 = '0' and q13 = '1' and q14 = '0' and q15 = '1' and q16 = '0')
        report "flip flop test 3 faillure" severity error;
      
      set <= '0';
      v1 <= '0';
      v2 <= '0';
      v3 <= '0';
      v4 <= '0';            
      v5 <= '0';
      v6 <= '0';
      v7 <= '0';
      v8 <= '0';            
      v9 <= '0';
      v10 <= '0';
      v11 <= '0';
      v12 <= '0';            
      v13 <= '0';
      v14 <= '0';
      v15 <= '0';
      v16 <= '0';            
      wait for CLK_PERIOD;
      assert (q1 = '1' and q2 = '0' and q3 = '1' and q4 = '0' and q5 = '1' and q6 = '0' and q7 = '1' and q8 = '0' and q9 = '1' and q10 = '0' and q11 = '1' and q12 = '0' and q13 = '1' and q14 = '0' and q15 = '1' and q16 = '0')
        report "flip flop test 4 faillure" severity error;
      
      wait;
    end process;
    
end Testbench_reg_16b;
