# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

### expected progress
### evaluation dates


from timeit import Timer
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge

test_cases_encoder_data = [0b00000000, 0b00000001, 0b00000010, 0b00000011, 0b00000100, 0b00000101, 0b00000110, 
                      0b00000111, 0b00001000, 0b00001001, 0b00001010, 0b00001011, 0b00001100, 0b00001101,
                      0b00001110, 0b00001111]


test_cases_codeword = [0b00000000, 0b10000111, 0b10011001, 0b00011110, 0b10101010, 0b00101101, 0b00110011, 
                               0b10110100, 0b01001011, 0b11001100, 0b11010010, 0b01010101, 0b11100001, 0b01100110, 0b01111000, 0b11111111]

@cocotb.test()
async def test_project(dut):
    print(dir(dut))
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
        dut._log.info("Start")
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

        
    dut._log.info("=========================================================")
    dut._log.info("Test decoder functionality -- no error")
    
    for i in range(len(test_cases_codeword)):
        
        # Reset
        await reset(dut)
        
        dut._log.info("Start")
        
        #START 
        dut.ui_in.value = 0b1 # start
        await ClockCycles(dut.clk, 1)
        
        #IN1
        dut.ui_in.value = 0b1 # mode = 1
        await ClockCycles(dut.clk, 1)
        
        #IN2
        dut.ui_in.value = test_cases_codeword[i] 
        await ClockCycles(dut.clk, 1)
        
        print(f"input2: {dut.ui_in.value}")
        
        await ClockCycles(dut.clk, 2)
        
        
        #OUT1
        # await ClockCycles(dut.clk, 1)
        print("Encoded testcase: " + bin(test_cases_codeword[i]))
        print(f"OUT5: {dut.uo_out.value}")
        assert dut.uo_out.value == test_cases_codeword[i]
        
        #OUT2
        await ClockCycles(dut.clk, 1)
        print(f"OUT6: {dut.uo_out.value}")
        assert dut.uo_out.value == 0b00000000
        
    await reset(dut)

    dut._log.info("=========================================================")
    dut._log.info("Test decoder functionality -- single bit error correction")

    for i in range(len(test_cases_codeword)):
        await ClockCycles(dut.clk, 1)

        codeword = test_cases_codeword[i]
        bit_position = i % 8
        corrupted_cw = flip_bit(codeword, bit_position)
        syndrome = (bit_position + 1)
        if (syndrome >= 8): syndrome = 0
        expected_out2 = syndrome << 2 | 0b01

        print(f"Codeword: {bin(codeword)}")
        
        #START 
        dut.ui_in.value = 0b1 # start
        await ClockCycles(dut.clk, 1)
        
        #IN1
        dut.ui_in.value = 0b1 # mode = 1
        await ClockCycles(dut.clk, 1)
        print(f"input1: {dut.ui_in.value}")
        
        #IN2
        dut.ui_in.value = corrupted_cw
        await ClockCycles(dut.clk, 1)
        print(f"input2: {dut.ui_in.value}")
        
        #OUT1
        await ClockCycles(dut.clk, 2)
        print(f"OUT1: {dut.uo_out.value}")
        assert dut.uo_out.value == codeword
        
        #OUT2
        await ClockCycles(dut.clk, 1)
        print(f"OUT2: {dut.uo_out.value}")
        assert dut.uo_out.value == expected_out2

        await reset(dut)

    
    await reset(dut)

    dut._log.info("=========================================================")
    dut._log.info("Test decoder functionality -- double bit error detection")

    await ClockCycles(dut.clk, 1)

    codeword = test_cases_codeword[2]
    corrupted_cw = flip_bit(codeword, 2)
    corrupted_cw = flip_bit(corrupted_cw, 5)
    
    #START 
    dut.ui_in.value = 0b1 # start
    await ClockCycles(dut.clk, 1)
    
    #IN1
    dut.ui_in.value = 0b1 # mode = 1
    await ClockCycles(dut.clk, 1)
    
    #IN2
    dut.ui_in.value = corrupted_cw
    await ClockCycles(dut.clk, 1)
    print(f"input2: {dut.ui_in.value}")
    print(f"Original codeword: {bin(codeword)}")
    
    #OUT1
    await ClockCycles(dut.clk, 2)
    print(f"OUT1: {dut.uo_out.value}")
    assert dut.uo_out.value == corrupted_cw
    
    #OUT2
    await ClockCycles(dut.clk, 1)
    print(f"OUT2: {dut.uo_out.value}")
    assert dut.uo_out.value == 0b00000010



        
async def reset(dut, timeout=10):
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    # raise TimeoutError("Timeout: did not reach IDLE state")

def flip_bit(value, position):
    return value ^ (1 << position)