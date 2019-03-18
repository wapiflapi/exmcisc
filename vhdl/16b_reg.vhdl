Library IEEE;
USE IEEE.Std_logic_1164.all;

-- 16 bits register
entity reg_16b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic_vector(15 downto 0);
       q: out std_logic_vector(15 downto 0));
end reg_16b;

architecture reg_16b of reg_16b is
  component Flip_Flop_4b is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic_vector(3 downto 0);
       q: out std_logic_vector(3 downto 0));
  end component;

begin
  flip_flop_1 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    val => val(15 downto 12),
    q => q(15 downto 12)
  ); 
  flip_flop_2 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    val => val(11 downto 8),
    q => q(11 downto 8)
  ); 
  flip_flop_3 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    val => val(7 downto 4),
    q => q(7 downto 4)
  ); 
  flip_flop_4 : Flip_Flop_4b port map (
    clk => clk,
    set => set,
    val => val(3 downto 0),
    q => q(3 downto 0)
  ); 
end  reg_16b;

