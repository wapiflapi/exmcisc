library ieee;
use ieee.std_logic_1164.all;

entity MUX is port(
  E0, E1, E2, E3: in std_logic_vector(15 downto 0);
  SEL: in std_logic(2 downto 0);
  S: out std_logic_vector(15 downto 0));
end;

architecture FLOT_MUX of MUX is
begin
  with SEL select
    S <= E0 when "00",
         E1 when "01",
         E2 when "10",
         E3 when others;
end FLOT_MUX;
