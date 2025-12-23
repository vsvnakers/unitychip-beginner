module SyncFIFO (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        we_i, // 写使能信号，高有效
    input  wire        re_i, // 读使能信号，高有效
    input  wire [31:0] data_i,
    output reg  [31:0] data_o,
    output wire        full_o, // 表示FIFO是否满
    output wire        empty_o // 表示FIFO是否空
);

  reg [31:0] ram[16];

  reg [3:0] wptr; // 写指针 仅在时钟上升沿更新
  reg [3:0] rptr; // 读指针
  reg [4:0] counter;
  // counter为0且empty_o=1表示FIFO为空
  // counter为16时full_o=1表示FIFO已满

  wire rvalid, wvalid;

  assign rvalid = re_i && !empty_o;
  assign wvalid = we_i && !full_o;

  always @(posedge clk) begin : PTR_UPDATE
    if (!rst_n) begin
      wptr   <= 0;
      rptr   <= 0;
      data_o <= 0;
    end else begin
      if (rvalid) begin
        rptr   <= rptr + 1;
        data_o <= ram[rptr];
      end
      if (wvalid) begin
        wptr      <= wptr + 1;
        ram[wptr] <= data_i;
      end
    end
  end

  always @(posedge clk) begin : COUNTER_UPDATE
    if (!rst_n) counter <= 0;
    else if (rvalid ^ wvalid) begin
      if (rvalid) counter <= counter - 1;
      if (wvalid) counter <= counter + 1;
    end
  end

  assign full_o  = counter == 5'd16;
  assign empty_o = counter == 0;

endmodule
