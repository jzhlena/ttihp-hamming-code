/*
 * Copyright (c) 2025 Cynthia Ma, Helena Zhang
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module hamming_decoder (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    // input  wire [7:0] uio_in,   // IOs: Input path
    // output wire [7:0] uio_out,  // IOs: Output path
    // output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    // input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    // input  wire       clk,      // clock
    // input  wire       rst_n     // reset_n - low to reset
);

    // declare temporary signals for calculated check bits and syndrome bits
    wire c_
    wire s_all, s2, s1, s0;

endmodule