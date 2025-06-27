<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The project is an implementation of an (8,4) Hamming Code encoder/decoder. A start signal is sent sent (1 to bit 0 of input) to activate the state machine. A select value is then read in from bit 0 of the input, before 8 bits of the input are read in on the next clock cycle.

**SELECT == 0 - ENCODER**

Bits [4:0] of the input are passed in. 4 parity bits are generated, consisting of 3 check and 1 overall parity bit. The bits are passed to the output in the order [O_ALL, D3, D2, D1, C2, D0, C1, C0], with D0 and C0 representing the least significant bits of the data and check bits respectively.

**SELECT == 1 - DECODER**

Bits [7:0] of the input are passed in. 4 parity bits are recalculated and compared to the received bits. If the program detects a single-bit error, the bit at that position is flipped. Else, the corrected codeword is passed to bits [7:0] of the output. 

In the next clock cycle, the 5 bits consisting of error information are passed. Bits [3:2] consist of bits [2:0] of the calculated syndrome, highlighting the corrected bit position. Bits [1:0] display the total number of errors detected.

## How to test

A start signal must be sent (1 to bit 0 of input) to activate the state machine. Testing can then be done selecting a mode (0 or 1) and then supplying a known data input. 

The encoder can be verified by ensuring that the output matches the expected codeword value. The decoder can be similarly verified by modifying known encoder values and determining the expected output.


## External hardware

n/a
