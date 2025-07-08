/*
 * Copyright (c) 2025 Cynthia Ma, Helena Zhang
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module hamming_decoder (
    input  wire [7:0] code_in,         // Dedicated inputs
    output wire [7:0] code_out,        // Dedicated outputs
    output wire [2:0] error_location,  // Syndrome bits: 3 bits for error location, 0 for no error or uncorrectable error
    output wire [1:0] error_flag       // Error flag: 00 = no error, 01 = single-bit error, 10 = double-bit error
);

    // declare temporary signals for calculated check bits and syndrome bits
    wire c_all, c2, c1, c0;
    wire [3:0] syndrome;

    //code_in = [c_all, d3, d2, d1, c2, d0, c1, c0]

    assign c0 = code_in[2] ^ code_in[4] ^ code_in[6]; // d0, d1, d3
    assign c1 = code_in[2] ^ code_in[5] ^ code_in[6]; // d0, d2, d3
    assign c2 = code_in[4] ^ code_in[5] ^ code_in[6]; // d1, d2, d3
    // assign c_all = c0 ^ c1 ^ c2 ^ code_in[2] ^ code_in[4] ^ code_in[5] ^ code_in[6]; // all data and calculated parity bits
    assign c_all = ^code_in[6:0];

    assign syndrome[0] = c0 ^ code_in[0];
    assign syndrome[1] = c1 ^ code_in[1];
    assign syndrome[2] = c2 ^ code_in[3];
    assign syndrome[3] = c_all ^ code_in[7];

    assign error_location = syndrome[2:0];

    // assign error_flag = (syndrome[3] == 1'b1) ? 2'b01 :  // single-bit error 
    //                 (syndrome[3] == 1'b1 && syndrome[2:0] == 3'b000) ? 2'b10 : // double-bit error
    //                                                                      2'b00; // no error

    assign error_flag = (syndrome[3] == 1'b1)                            ? 2'b01 :  // single-bit error 
                        (syndrome[3] == 1'b0 && syndrome[2:0] != 3'b000) ? 2'b10 : // double-bit error
                                                                           2'b00; // no error


    wire [7:0] correction_mask;
    assign correction_mask = (syndrome[2:0] != 3'b000) ?
                         (8'b00000001 << (syndrome[2:0] - 1)) :
                         8'b00000000;

    assign code_out = (error_flag == 2'b01) ?
                        ((syndrome[2:0] == 3'b000) ?
                         (code_in ^ 8'b10000000) : 
                         (code_in ^ correction_mask)
                        ) :
                      code_in;

endmodule