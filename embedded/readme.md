## Prerequisites

- STM32Cube & STM32CubeIDE installed
- stm32 nucleo h743zi2 board
- 3 Microphones
- 1 Sound emitter

## Usage

This directory matches the Core directory of the STM32CubeIDE, so all included binaries are omitted out here,
to use this code, copy it to the IDE core directory.

when opening a new project using Cube, select the board `NUCLEO-H743ZI2` and the project type `STM32CubeIDE`.
enabled ADC1 and connect 3 channels of the microphones to it.
copy the code from the `Core` directory to the `Src` directory in the generated project.

when the code is uploaded to the board, the board will start to listen to the sound and fill up the buffer with the sound data, while also sending the buffers over UART to the connected PC.

open a Putty terminal and connect to the board using the correct COM port and baud rate, there you can see the resulted sound data.
