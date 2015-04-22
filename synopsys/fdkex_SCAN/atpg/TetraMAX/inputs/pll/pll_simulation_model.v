
module pll(refclk, clk1x, clk2x, reset);
    input  refclk;
    output clk1x;
    output clk2x;
    input reset;

    reg clk1x;
    reg clk2x;

always
  begin
    clk1x = #2 refclk;
    clk2x = #2 refclk;
  end

endmodule

