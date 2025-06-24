/*
 * Copyright (c) 2025 Cynthia Ma, Helena Zhang
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module hamming_encoder (
    input  wire [3:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    // input  wire [7:0] uio_in,   // IOs: Input path
    // output wire [7:0] uio_out,  // IOs: Output path
    // output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    // input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    // input  wire       clk,      // clock
    // input  wire       rst_n     // reset_n - low to reset
);

    // declare temporary signals for calculated check bits
    wire c_all, c2, c1, c0;

    assign c0 = ui_in[0] ^ ui_in[1] ^ ui_in[3]; // d0, d1, d3
    assign c1 = ui_in[0] ^ ui_in[2] ^ ui_in[3]; // d0, d2, d3
    assign c2 = ui_in[1] ^ ui_in[2] ^ ui_in[3]; // d1, d2, d3
    assign c_all = c0 ^ c1 ^ c2 ^ ui_in[3] ^ ui_in[2] ^ ui_in[1] ^ ui_in[0]; // all data and calculated parity bits
    
    // 8 7 6 5 4 3 2 1
    assign uo_out = {c_all, ui_in[3], ui_in[2], ui_in[1], c2, ui_in[0], c1, c0,}

endmodule;