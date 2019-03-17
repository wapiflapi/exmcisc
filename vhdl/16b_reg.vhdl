Library IEEE;
USE IEEE.Std_logic_1164.all;

-- 16 bits register
entity reg_16b is
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
end reg_16b;

architecture reg_16b of reg_16b is
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

begin
  flip_flop_1 : Flip_Flop_4b port map (
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
  flip_flop_2 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    v1 => v5, 
    v2 => v6,
    v3 => v7,
    v4 => v8, 
    q1 => q5, 
    q2 => q6, 
    q3 => q7,  
    q4 => q8  
  ); 
  flip_flop_3 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    v1 => v9, 
    v2 => v10,
    v3 => v11,
    v4 => v12, 
    q1 => q9, 
    q2 => q10, 
    q3 => q11,  
    q4 => q12  
  ); 
  flip_flop_4 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    v1 => v13, 
    v2 => v14,
    v3 => v15,
    v4 => v16, 
    q1 => q13, 
    q2 => q14, 
    q3 => q15,  
    q4 => q16  
  ); 
end  reg_16b;

