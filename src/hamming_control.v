/*
 * Copyright (c) 2025 Cynthia Ma, Helena Zhang
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module hamming_top (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire [3:0] data_in = ui_in[3:0]; // 4-bit data for encoder
    wire [7:0] code_in = ui_in[7:0]; // 8-bit code for decoder

    // declare signals for outputs
    wire [7:0] encoded_code;
    wire [7:0] decoded_data;


    //

endmodule