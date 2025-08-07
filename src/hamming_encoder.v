/*
 * Copyright (c) 2025 Cynthia Ma, Helena Zhang
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module hamming_encoder (
    input  wire [3:0] data_in,    // Dedicated inputs
    output wire [7:0] code_out   // Dedicated outputs
);

    // declare temporary signals for calculated check bits
    wire c_all, c2, c1, c0;

    assign c0 = data_in[0] ^ data_in[1] ^ data_in[3]; // d0, d1, d3
    assign c1 = data_in[0] ^ data_in[2] ^ data_in[3]; // d0, d2, d3
    assign c2 = data_in[1] ^ data_in[2] ^ data_in[3]; // d1, d2, d3
    assign c_all = c0 ^ c1 ^ c2 ^ data_in[3] ^ data_in[2] ^ data_in[1] ^ data_in[0]; // all data and calculated parity bits
    
    // 8 7 6 5 4 3 2 1
    assign code_out = {c_all, data_in[3], data_in[2], data_in[1], c2, data_in[0], c1, c0};

endmodule