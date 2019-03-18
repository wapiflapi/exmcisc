Library IEEE;
USE IEEE.Std_logic_1164.all;

-- flip flop storing 1 bit
entity Flip_Flop_4b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic_vector(3 downto 0);
       q: out std_logic_vector(3 downto 0));
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
    val => val(0),
    q => q(0)
    );
  fli_flop_2 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => val(1),
    q => q(1)
    );
  fli_flop_3 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => val(2),
    q => q(2)
    );
  fli_flop_4 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => val(3),
    q => q(3)
    );  
end  Flip_Flop_4b;

