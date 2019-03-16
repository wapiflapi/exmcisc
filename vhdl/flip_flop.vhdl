Library IEEE;
USE IEEE.Std_logic_1164.all;

-- flip flop storing 1 bit
entity Flip_Flop is
  port(clk: in std_logic;
       set: in std_logic;
       val: in std_logic;
       Q: out std_logic);
end Flip_Flop;

architecture Falling_Flip_Flop of Flip_Flop is
  signal state: std_logic := '0';
begin
  process(clk)
  begin
    if(rising_edge(clk)) then
      if (set = '1') then
        state <= val;
      end if;
    end if;
    if (falling_edge(clk)) then
      Q <= state;
    end if;
  end process;
end  Falling_Flip_Flop;
