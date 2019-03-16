Library IEEE;
USE IEEE.Std_logic_1164.all;

-- flip flop storing 1 bit
entity Flip_Flop is
  port(clk: in std_logic;
       set: in std_logic := '0';
       val: in std_logic := '0';
       Q: out std_logic := '0');
end Flip_Flop;

architecture Falling_Flip_Flop of Flip_Flop is
begin
  process(clk)
  begin
    if(falling_edge(clk)) then
      if (set = '1') then
        Q <= val;
      end if;
    end if;
  end process;
end  Falling_Flip_Flop;
