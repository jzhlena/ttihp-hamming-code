# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

### expected progress
### evaluation dates


from timeit import Timer
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

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
    
    ## test encoding
    dut._log.info("Test basic encoding functionality")

    dut.ui_in.value = 1 # start
    await ClockCycles(dut.clk, 1)

    # IN1 (mode = 0)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)
    # print(f"input1: {dut.ui_in.value}")
    # print(dut.uo_out.value)

    # IN2 (dataword = 0111)
    dut.ui_in.value = 0b0111
    await ClockCycles(dut.clk, 1)
    # print(f"input2: {dut.ui_in.value}")
    # print(dut.uo_out.value)

    # OUT1
    await ClockCycles(dut.clk, 2)
    # print(f"Encoded output: {dut.uo_out.value}")
    assert dut.uo_out.value == 0b10110100
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b10110100

    ClockCycles(dut.clk, 3)

    ## test only encoder

    # print("=========================================================")
    # ## test decoding
    # dut._log.info("Test decoding functionality -- no error")
    # dut.ui_in.value = 0b1 # start
    # await ClockCycles(dut.clk, 1)
    # dut.ui_in.value = 0b1 # mode = 1
    # await ClockCycles(dut.clk, 1)
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
    # dut.ui_in.value = 0b11 # start = 1, mode = 1
    # await ClockCycles(dut.clk, 1)
    # dut.ui_in.value = 0b11110100 # introduce a 1-bit error in the dataword
    # await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == 0b10110100 # should correct the 1-bit error
    # await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == 0b00011101 # error_location = 7, error_flag = 1




