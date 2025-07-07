# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

### expected progress
### evaluation dates


from timeit import Timer
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

test_cases_encoder_data = [0b00000000, 0b00000001, 0b00000010, 0b00000011, 0b00000100, 0b00000101, 0b00000110, 
                      0b00000111, 0b00001000, 0b00001001, 0b00001010, 0b00001011, 0b00001100, 0b00001101,
                      0b00001110, 0b00001111]


test_cases_codeword = [0b00000000, 0b10000111, 0b10011001, 0b00011110, 0b10101010, 0b00101101, 0b00110011, 
                               0b10110100, 0b01001011, 0b11001100, 0b11010010, 0b01010101, 0b11100001, 0b01100110, 0b01111000, 0b11111111]

    # assign c0 = data_in[0] ^ data_in[1] ^ data_in[3]; // d0, d1, d3
    # assign c1 = data_in[0] ^ data_in[2] ^ data_in[3]; // d0, d2, d3
    # assign c2 = data_in[1] ^ data_in[2] ^ data_in[3]; // d1, d2, d3
    # assign c_all = c0 ^ c1 ^ c2 ^ data_in[3] ^ data_in[2] ^ data_in[1] ^ data_in[0]; // all data and calculated parity bits
    
    # assign code_out = {c_all, data_in[3], data_in[2], data_in[1], c2, data_in[0], c1, c0};

@cocotb.test()
async def test_project(dut):
    # max clock period = 50 mHz
    # Set the clock period to 50 us (20 KHz)
    clock = Clock(dut.clk, 50, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Test project behavior")
    dut._log.info("=========================================================")
    dut._log.info("Test encoder functionality")
    
    for i in range(len(test_cases_encoder_data)):
        dut.ui_in.value = 1 # start
        await ClockCycles(dut.clk, 1)

        # IN1 (mode = 0)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)
        print(f"input1: {dut.ui_in.value}")
        # print(dut.uo_out.value)

        # IN2
        dut.ui_in.value = test_cases_encoder_data[i]
        await ClockCycles(dut.clk, 1)
        print(f"input2: {dut.ui_in.value}")
        # print(dut.uo_out.value)

        # OUT1
        await ClockCycles(dut.clk, 2)
        print(f"Encoded output: {dut.uo_out.value}")
        print("Encoded testcase: " + bin(test_cases_codeword[i]))
        assert dut.uo_out.value == test_cases_codeword[i]
        # await ClockCycles(dut.clk, 1)
        # assert dut.uo_out.value == 0b10110100

        ClockCycles(dut.clk, 3)
        
    # dut._log.info("Start")

    # dut.ui_in.value = 1 # start
    # await ClockCycles(dut.clk, 1)

    # # IN1 (mode = 0)
    # dut.ui_in.value = 0
    # await ClockCycles(dut.clk, 1)
    # # print(f"input1: {dut.ui_in.value}")
    # # print(dut.uo_out.value)

    # # IN2 (dataword = 0111)
    # dut.ui_in.value = 0b0111
    # await ClockCycles(dut.clk, 1)
    # # print(f"input2: {dut.ui_in.value}")
    # # print(dut.uo_out.value)

    # # OUT1
    # await ClockCycles(dut.clk, 2)
    # # print(f"Encoded output: {dut.uo_out.value}")
    # assert dut.uo_out.value == 0b10110100
    # await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == 0b10110100

    # ClockCycles(dut.clk, 3)

    # print("=========================================================")
    # ## test decoding
    # dut._log.info("Test decoding functionality -- no error")
    # dut.ui_in.value = 0b1 # start
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT: {dut.uo_out.value}")
    # dut.ui_in.value = 0b1 # mode = 1
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT: {dut.uo_out.value}")
    # dut.ui_in.value = 0b10110101
    # await ClockCycles(dut.clk, 1)
    # # assert dut.uo_out.value == 0b10110100 # should match the original dataword
    # print(f"OUT1: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # # assert dut.uo_out.value == 0b00000000 # no error, 0's expected
    # print(f"OUT2: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1) # return to idle state
    # print(f"OUT3: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT4: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT5: {dut.uo_out.value}")

    # await ClockCycles(dut.clk, 3) # return to idle state

    # dut._log.info("Test decoding functionality -- 1 bit error correction")
    
    # dut._log.info("Reset")
    # dut.ena.value = 1
    # dut.ui_in.value = 0
    # dut.uio_in.value = 0
    # dut.rst_n.value = 0
    # await ClockCycles(dut.clk, 10)
    # dut.rst_n.value = 1
    # await ClockCycles(dut.clk, 1)
    
    # dut.ui_in.value = 0b1 # start = 1
    # await ClockCycles(dut.clk, 1)
    # dut.ui_in.value = 1 # mode = 1
    # await ClockCycles(dut.clk, 1)
    
    # print(f"OUT6: {dut.uo_out.value}")
    # dut.ui_in.value = 0b11110100 # introduce a 1-bit error in the dataword
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT7: {dut.uo_out.value}")
    # # assert dut.uo_out.value == 0b10110100 # should correct the 1-bit error
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT8: {dut.uo_out.value}")
    # # assert dut.uo_out.value == 0b00011101 # error_location = 7, error_flag = 1
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT9: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT10: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT11: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT11: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT11: {dut.uo_out.value}")
    # await ClockCycles(dut.clk, 1)
    # print(f"OUT11: {dut.uo_out.value}")




