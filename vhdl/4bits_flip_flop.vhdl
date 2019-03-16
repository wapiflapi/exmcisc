Library IEEE;
USE IEEE.Std_logic_1164.all;

-- flip flop storing 1 bit
entity Flip_Flop_4b is
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
end Flip_Flop_4b;

architecture Flip_Flop_4b of Flip_Flop_4b is
  component Flip_Flop is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic := '0';
       Q: out std_logic := '0');
  end component;

begin
  fli_flop_1 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v1,
    q => q1
    );
  fli_flop_2 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v2,
    q => q2
    );
  fli_flop_3 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v3,
    q => q3
    );
  fli_flop_4 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v4,
    q => q4
    );  
end  Flip_Flop_4b;

