Library IEEE;
USE IEEE.Std_logic_1164.all;

-- flip flop storing 1 bit
entity 4b_Flip_Flop is
  port(clk: in std_logic;
       set: in std_logic;
       val: in BIT_VECTOR(0, 3);
       Q: out  BIT_VECTOR(0, 3));
end 4b_Flip_Flop;

architecture 4b_Flip_Flop of 4b_Flip_Flop is
  component Flip_Flop is
  port(clk: in std_logic;
       set: in std_logic;
       val: in std_logic;
       Q: out std_logic);
  end component;

  signal v1, v2, v3, v4 : std_logic;
  signal q1, q2, q3, q4 : std_logic;

begin
  fli_flop_1 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v1,
    Q => q1
    );
  fli_flop_2 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v2,
    Q => q2
    );
  fli_flop_3 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v3,
    Q => q3
    );
  fli_flop_4 : Flip_Flop port map (
    clk => clk,
    set => set,
    val => v4,
    Q => q4
    );

  process(clk)
  begin
    if(falling_edge(clk)) then
      v1 <= val and '1';
      v2 <= shift_right(unsigned(val and "10"), 1);  
      v3 <= shift_right(unsigned(val and "100"), 2);  
      v4 <= shift_right(unsigned(val and "1000"), 3);

      Q <= q1 or shift_left(unsigned(q2), 1) or shift_left(unsigned(q3), 2) or shift_left(unsigned(q4), 3)
  end process
  
end  4b_Flip_Flop;

