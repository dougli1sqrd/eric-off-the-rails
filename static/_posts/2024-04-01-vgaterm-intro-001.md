---
layout: authored-post
title: "Introduction to Vgaterm"
author: Eric
category: tech
tags: vgaterm
---

Over the past two years or so my friend [Seth](https://github.com/sethp) and I have been building a hardware [terminal](). Or at least, we started building something and it eventually became a terminal.

This pandemic project was a way for us to connect with each other and learn new technical skills while building something that would allow us to physically connect computers together.

A hardware terminal is an old-school way of connecting a user to a mainframe - or a multi-user computer. A terminal would have a keyboard and monitor and a "serial" connection to a computer that many other people could be using at the same time on their own terminals. It's the hardware equivalent to opening your favorite terminal program and typing the `ls` command to list all the files in the current directory. To learn about terminals and how they've shaped computing history, I'd absolutely reccomend [this blog post](http://www.linusakesson.net/programming/tty/)

Terminals are largely not in use any more because computers are cheap and everywhere and can just connect to each other over the internet. You may remember using a hardware terminal (up to the late 90s, perhaps) at your local library to browse the available books in the catalogue.

This is the start in a series of posts all about the planning, building, and philosphy of Seth and I making a hardware terminal in 2024.

This post will specifically be about the basic workings, pictures, and how we were inspired to make something like this.

# The Start

My technical background is mostly java, python, and the web. So a part of me has always wanted to learn more systems and lower-level programming. When Rust came around I was excited to learn a new systems language with an interesting type system. At some point many years back during a conversation over pizza, Seth and I decided to make a Github org for playing with Rust and learning low level programming. We called it [Rustbox](), as the original conceit was to make an operating system together in rust.

At some point I learned about [RISC-V](https://riscv.org/), an open source instruction set for CPUs, and decided I wanted to try programming rust for RISC-V, and Seth and I bought a few [HiFive](https://www.sifive.com/boards/hifive1-rev-b) boards. Inspired by [Ben Eater](https://www.youtube.com/@BenEater)'s youtube video ["Making the Worlds Worst Video Card"]() using a 6502 processor, I decided to make the hifive board into a "video card". It output a VGA signal in the 640x480 mode with 160x96 actual pixels (due to memory constraints) with 64 colors. After a year I had a set of breadboards and a RISC-V CPU displaying images and text (using my own font):

{% include figure.html image="/assets/images/hifive-vga-breadboards.jpg" caption="hifive board attached to breadboards outputing VGA" width=600 %}

{% include figure.html image="/assets/images/streetcar-red-hifive.jpg" caption="Red streetcar in SF converted for VGA hardware" width=600  %}

{% include figure.html image="/assets/images/green-text-hifive.jpg" caption="Text demo with highlighted characters included using my own custom font" width=600 %}

Code for this project can be [found here](https://github.com/rustbox/rustbox-hifive1-revb)

# Vgaterm

The hifive board video card was neat and I learned a lot but I wanted it to be useful somehow. In the hifive code I had also made some command line bare metal programs as well as having the characters update from keyboard input. I was also always a little sad that I needed a large computer to be attached to my small computer to run and interact with it (aka through screen or other terminal program). Thus I realized I wanted to make a physical terminal, and upgrade the VGA capabilities. So Seth and I embarked on making *Vgaterm*: a hardware terminal that would would output 640x400 pixels at 256 colors, connect to serial IO, recieve keyboard input, and display text updates to the screen. The goal was to be able to log in to a standard linux machine with the hardware and interact on the command line - and hopefully use any standard terminal programs like Vim, etc.

The final device uses an esp32c3 microcontroller and custom designed circuit boards hand soldered together.

{% include figure.html image="/assets/images/vgaterm-top.jpg" caption="Completed Vgaterm" width=750 %}

{% include figure.html image="/assets/images/vgaterm-front.jpg" caption="Vgaterm uses a four position rotary switch to select an IO port: USB, raw pin headers (pictured here bridged), RJ45, DSUB-9 serial (RS-232)" width=750 %}

{% include figure.html image="/assets/images/vgaterm-hello.jpg" caption="Hello World, this is the Vgaterm Terminal!" width=750 %}

## Technical Overview

Since the new device aspirationally would output VGA at the full 640x480 60Hz standard we would need a microcontroller that would:

* have at least 300 KB of fast memory for the video buffer (1 byte per pixel, giving us 256 colors)
* have some memory for coordinating IO and other tasks
* fast enough to output pixels for the VGA pixel clock at 25.175 MHz: 39.7 ns per byte

Additionally, part of the philosophy of the project was to celebrate and engage in open hardware and software. So keeping a RISC-V core felt crucial to our goals.

Finding the esp32c3 by Espressif seemed to fit the bill by the numbers:
* 400 KB SRAM
* 4 MB Flash Memory
* 160 MHz CPU
* 15 GPIO pins

However, it turned out that bit-banging 8 GPIO lines as fast as possible on the esp32c3 was not quite fast enough, additionally there wasn't an obvious way to match the VGA clock domain from the CPU.

To solve the clock domain issue we decided to use a FIFO memory (first in first out, like a queue) chip. So the CPU writes bytes into the FIFO, and the VGA clock domain reads from the FIFO, 

To solve the speed issue the esp32c3 comes equipped with a quad [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) module allowing 4 bits to be clocked out at up to 80 MHz - much faster than bit-banging.

So with these two pieces, we could design a circuit that collects two 4 bit [nibbles](https://en.wikipedia.org/wiki/Nibble) into a byte (representing the color of a single pixel) and load it into a FIFO memory. At the same time, the VGA timing hardware would read pixel bytes exactly when needed.

### Logical Components

There are five main components to Vgaterm:

* VGA Timing
* CPU Pixel Output
* Displaying a Pixel Byte
* Digital to Analog Converters (DAC)
* IO control and video buffer updates

{% include figure.html image="/assets/images/vgaterm-logical-diagram.jpg" caption="Vgaterm logical diagram. Details were omitted to show the high level units" width=800 %}

Repositories containing all our code and schematics:
* esp32c3 code: [https://github.com/rustbox/esp32c3-vgaterm](https://github.com/rustbox/esp32c3-vgaterm)
* VGA timing generation code and Programmable Logic Device code: [https://github.com/rustbox/cuddly-robot](https://github.com/rustbox/cuddly-robot)
* PCB schematics and CAD: [https://github.com/rustbox/vgaterm-schematics](https://github.com/rustbox/vgaterm-schematics)

### VGA Timing

VGA comes in several modes, and we target the 640x480, 60Hz frame rate mode - the base standard. VGA has 3 analog signals between 0 and 0.7 volts representing the amount of Red Green and Blue per pixel. There are also two timing signals `H_SYNC` and `V_SYNC` that tell the monitor what resolution mode to be in and when to sample the analog color signals to actually dispaly a pixel. When the monitor is actively sampling colors and displaying pixels we say that this portion of the frame is `visible`. There is time during a complete frame when this isn't the case and this is _blanking area_. Lastly, the _pixel clock_ speed is the rate at which pixels are shown, and in our case that's 25.175 MHz. In the diagram above, I've labeled a signal `CLK_VIS`, and this is the _pixel clock_ signal during the `visible` time. To see detailed VGA timing information, see [tiny vga](http://tinyvga.com/vga-timing/640x480@60Hz).

:----:|:-----:
![](/assets/images/vgaterm-timing-front.jpg) | ![](/assets/images/vgaterm-timing-back.jpg)
<span style="color: {{ site.caption_color }};">Vgaterm Timing circuit top</span> | <span style="color: {{ site.caption_color }};">Vgaterm Timing cicuit bottom</span>

VGA timing is controlled by the "timing board" circuit. This establishes the `H_SYNC` and `V_SYNC` signals that VGA requires, the `START` signal which alerts the CPU to begin  emitting pixels to the FIFO, and the `visible` flag, which is used to compute `CLK_VIS` to read pixel bytes out of the FIFO.

### Pixels Out
Every frame (60 times a second) the esp32c3 microcontroller needs to output 256,000 bytes (640x400 pixels, 1 byte per pixel) to hardware so they may be displayed. This is the most important software role as any jitter in timing can cause display artifacts.

To cross the clock domains, from the CPU SPI to VGA pixel clock, we used a FIFO memory chip. This lets us write bytes from the CPU while VGA hardware reads bytes exactly when it needs them.

This was clever, but there are a few constraints we had to consider when designing a circuit around the FIFO:
* The FIFO read and write setup and hold times had to be obeyed by the SPI clock and `CLK_VIS` signals
* The SPI Clock could be in only divisions by 2 of 80 MHz (80, 40, 20, 10, etc)
* If we emitted pixels too quickly, and VGA hardware could not read from the FIFO fast enough, we would blow the queue and drop pixels
    * This could be mitigated by adding more space in the FIFO, but at a steep dollar cost
* If we emitted pixels too slowly, and VGA hardware attempted to consume pixels faster than were being written then we'd also drop pixels
* VGA hardware does not read from the FIFO at the pixel clock rate across the entire duration of the frame. Since the visible portion of the frame is only about 73% of the total time spent per frame (because of the blanking times), the average read rate per frame is actually less than the pixel clock rate

The details in how we eneded up on our specific design will be elaberated on in another post, but suffice to say we had to coordinate design details across software, hardware, specific part choices, and part pricing.

### Displaying Pixels
To dispaly pixels, the `CLK_VIS` signal generated by the VGA timing hardware reads bytes from the FIFO and into a Programmable Logic Unit (PLU) which maps the 8 bits into 9 bits, 3 sets of 3 bits for each of the color channels - red, green, and blue. These 9 bits then get sent to the DAC, described in the following section.

An important consideration for this stage is how long it takes to shuttle a byte from the FIFO into the DAC and finally into the monitor. Since there is processing of the read bytes it's possible that the pixels become late compared to `H_SYNC` and `V_SYNC` and this will show up as a horizontal shift. I.E. the "first" pixel could actually show up on the 2nd or 3rd pixel position on the screen, instead of the actual 1st pixel.

{% include figure.html image="/assets/images/left-collum-timing-bug.jpg" caption="Notice the far left column of the screen in white next to the blue. It appears to wrap around from the far right side of the screen because the first pixel of the image is shifted over 2 or 3 positions" width=550 %}

So a method to handle this kind of pixel shifting makes the picture quality better.

### Digital to Analog Converter (DAC)
Once the pixel byte has been taken out of the FIFO memory it's on its way to being displayed by the monitor. To be displayed this pixel byte must be converted into three analog voltages between 0 and 0.7 volts corresponding to the Red, Green, and Blue color channels. This is accomplished with a [R2R Resistor Ladder DAC]().

An R2R Resistor Ladder DAC is traditionally connected into an op-amp to maintain the output voltage regardless of load. However in our case the load is just the 75 Ohm impedance of the analog color lines in the monitor, so we really only have the one load. One concern, however, is that the resistor ladder can consume a fair amount of current and the lines representing the color coming from an IC may not be rated to supply the amount of current the DAC would need to maintain the voltage.

In earlier versions of the DAC this is what we did (this is what Ben Eater did in his original "Worlds Worst Video Card" video). We did also try an op-amp but that seemed to create some weird artifacts in the colors in images. Lastly what seemed to work best is just feed the input bit lines into line drivers which _could_ supply the appropriate amount of current and now colors are quite vivid.

### IO Control
To actually function as a terminal Vgaterm must receive serial signals from a connected host on one of the four IO ports and update the video buffer accordingly. It also must handle keyboard input and forward those typed characters to the connected host.

{% include figure.html image="/assets/images/vgaterm-terminal-sequence.drawio.png" caption="Basic Keyboard input to terminal operation" %}

For keyboard input we went over several options including falling back on [PS/2 protocol over USB](https://en.wikipedia.org/wiki/PS/2_port#Conversion_between_PS/2_and_USB) and trying to write a basic USB host onto the esp32c3. But we settled on just using this [USB host to UART converter](https://www.tindie.com/products/matzelectronics/ch559-usb-host-to-uart-bridge-module/) by [MatzElectronics](https://www.tindie.com/stores/matzelectronics/).

Software, in a loop, waits for keyboard input or input by a connected host. When input is received on either, the CPU is interrupted. If receiving key presses, the character(s) are dequeued and passed along to the connected host. If receiving characters from the host, vgaterm updates the text buffer and cursor which updates the video memory. The updated video memory is then emitted in the next frame, showing the text to the user on screen.

Seth and I decided that this should _never_ interrupt the CPU from emitting pixel bytes as we wanted to prevent any visual artifacts as much as possible. However this means that we could end up more likely to drop characters if the CPU is overwhelmed with input. The CPU UART is configured to issue an `XOFF` character as a part of [Software Flow Control](https://en.wikipedia.org/wiki/Software_flow_control) to tell the host to stop sending input.


# Next Steps

This is only an overview of the operation and design of Vgaterm. My hope is that I can continue to make posts going into more detail about each of these major components. I learned so much working on this project and it gave me such joy to share it with a friend.

The project felt like it always had a perfectly moderate learning curve, where each new solution to solve a problem would reveal a new seemingly harder problem that we would have to tackle. But then with dedication, thought, community, and experimenting would reveal a way to solve it. I really believe that only with Seth's help could I have done this - that we could only have done this together. We each have different strengths and backgrounds and we complemented each other. Working on this made me understand what joy working with technology can really be like, that supporting and being supported by people can really make each other flourish. And it made me hopeful that professional work could be like this too.

Another aspect about this project that feels important is how we engaged with open source and open hardware. Seth and I wanted this to be open from the beginning, but I feel like I have a love for open source and open hardware like never before.

Engaging with the open hardware world helped me realize that electronics and hardware is just a skill that someone can learn, and that we, the community, can collectively own and build things that are important and useful - that we don't have to capitulate to huge corporations that want to collect our data, exploit workers, or monopolize the objects and services in our daily lives. It feels like a way to fight against the [enshittification](https://en.wikipedia.org/wiki/Enshittification) that represents our time in tech today. These are concepts I'm still thinking about and working through, and I have Vgaterm to thank for helping me engage with these ideas.


