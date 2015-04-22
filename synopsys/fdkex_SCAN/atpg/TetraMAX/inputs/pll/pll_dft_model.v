
module pll(refclk, clk1x, clk2x, reset);
    input  refclk;
    output clk1x;
    output clk2x;
    input reset;

    reg clk1x;
    reg clk2x;

    buf tmp_buf1 ( .a(refclk), .o1(clk1x) );
    buf tmp_buf2 ( .a(refclk), .o1(clk2x) );

endmodule

