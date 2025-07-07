/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_hamming_top (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.

  // state macros
  localparam
    IDLE      = 3'b000,
    IN1       = 3'b010,
    IN2       = 3'b011,
    CALCULATE = 3'b100,
    OUT1      = 3'b101,
    OUT2      = 3'b110;

  // resgisters used in state machine
  reg [2:0] curr_state;
  reg [2:0] next_state;
  reg       mode_select;
  reg [7:0] data_in;
  reg [7:0] data_out;

  assign uo_out = data_out;

  // declare signals for outputs
  wire [7:0] encoded_code;
  wire [7:0] decoded_data;
  wire [2:0] syndrome;
  wire [1:0] errors;

  hamming_encoder hamming_encoder_inst (
      .data_in(data_in[3:0]),    // 4-bit dataword input
      .code_out(encoded_code) // Output encoded code
  );

  hamming_decoder hamming_decoder_inst (
      .code_in(data_in[7:0]),   // 8-bit codeword input
      .code_out(decoded_data),  // Output decoded data
      .error_location(syndrome),    // Output syndrome bits
      .error_flag(errors)     // Output error bits
  );

  // State machine to control the operation
  wire start = ui_in[0];

  always @(posedge clk or negedge rst_n) 
  begin
    if (!rst_n) begin
      curr_state <= IDLE;
    end else begin
      curr_state <= next_state;
    end
  end

  always @(*) 
  begin
    case (curr_state)
      IDLE: begin
        if (start) next_state = IN1;
        else next_state = IDLE;
      end
      IN1: begin
        next_state = IN2;
      end
      IN2: begin
        next_state = OUT1; //CALCULATE;
      end
      OUT1: begin
        next_state = OUT2;
      end
      OUT2: begin
        next_state = IDLE;
      end
      default: begin
        next_state = IDLE; // Default to IDLE state
      end
    endcase
  end

  // Input data handling
  always @(posedge clk or negedge rst_n) 
  begin
    if (!rst_n) begin
      data_in <= 8'b0;
      mode_select <= 0;
    end else begin
      case (curr_state)
        IN1: begin
          mode_select <= ui_in[0]; // 0 for encode, 1 for decode
        end
        IN2: begin
          // Load input data for encoding or decoding
          if (mode_select == 0) begin
            data_in <= {4'b0, ui_in[3:0]}; // 4-bit data for encoding
          end else begin
            data_in <= ui_in[7:0]; // 8-bit code for decoding
          end
        end
      endcase
      // $display("Time=%0t | State=%b | mode_select=%b | data_in=%b | encoded_code=%b | decoded_data=%b | syndrome=%b | errors=%b | data_out=%b", $time, curr_state, mode_select, data_in, encoded_code, decoded_data, syndrome, errors, data_out);
    end
  end

  // Output handling
  always @(posedge clk or negedge rst_n) 
  begin
    if (!rst_n) begin
      data_out <= 8'b0;
    end else begin
      case (curr_state)
        OUT1: begin
          if (mode_select == 0) begin
            data_out <= encoded_code;
          end else begin
            data_out <= decoded_data;
          end
        end
        OUT2: begin
          if (mode_select == 0) begin
            data_out <= encoded_code;
          end else begin
            data_out <= {3'b0, syndrome, errors};
          end
        end
      endcase
            // $display("Time=%0t | State=%b | mode_select=%b | data_in=%b | encoded_code=%b | decoded_data=%b | syndrome=%b | errors=%b | data_out=%b", $time, curr_state, mode_select, data_in, encoded_code, decoded_data, syndrome, errors, data_out);
    end
  end


  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, uio_out, uio_oe, 1'b0};
  assign uio_oe = 8'b0;
  assign uio_out = 8'b0;
  assign uio_in = 8'b0; // Assign unused IO inputs to 0 to prevent warnings

endmodule
