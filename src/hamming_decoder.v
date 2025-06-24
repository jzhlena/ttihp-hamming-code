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

    
    // 432, error location, 10, error flag
    // wire [7:0] error_out;
    // wire [2:0] error_location;
    // wire [1:0] error_flag;

    //code_in = [c_all, d3, d2, d1, c2, d0, c1, c0]

    assign c0 = code_in[2] ^ code_in[4] ^ code_in[6]; // d0, d1, d3
    assign c1 = code_in[2] ^ code_in[5] ^ code_in[6]; // d0, d2, d3
    assign c2 = code_in[4] ^ code_in[5] ^ code_in[6]; // d1, d2, d3
    assign c_all = c0 ^ c1 ^ c2 ^ code_in[2] ^ code_in[4] ^ code_in[5] ^ code_in[6]; // all data and calculated parity bits

    assign syndrome[0] = c0 ^ code_in[0];
    assign syndrome[1] = c1 ^ code_in[1];
    assign syndrome[2] = c2 ^ code_in[3];
    assign syndrome[3] = c_all ^ code_in[7];

    assign error_location = syndrome[2:0];
    assign error_flag = (syndrome[3] && syndrome[2:0] != 3'b000) ? 2'b01 :  // single-bit error
                        (syndrome[3] && syndrome[2:0] == 3'b000) ? 2'b10 : // double-bit error
                                                                   2'b0;   // no error

    // single bit error correction
    assign code_out = (syndrome[2:0] != 3'b000) ?
                      (code_in ^ (8'b00000001 << (7 - syndrome[2:0]))) : 
                      code_in;


    // assign error_out = {3'b000, error_location, error_flag};

    // // output selector toggle
    // reg toggle;

    // // switches between code_out and error_out every cycle
    // always @(posedge clk or negedge rst_n) begin
    //     if (!rst_n) begin
    //         toggle <= 1'b0;
    //         uo_out <= 8'b0;
    //     end else begin
    //         toggle <= ~toggle;
    //         if (toggle)
    //             uo_out <= code_out;   // output corrected code on one cycle
    //         else
    //             uo_out <= error_out;  // output error info on next cycle
    //     end
    // end

endmodule