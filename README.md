# Random Numbers Testing Module2

This is created as a part of masters thesis, working jointly at DRDO, IIIT Delhi and University of Delhi. This module is by-product of [Random Numbers Testing Module](https://github.com/MayankKharbanda/random_number_testing_module), which is used for testing random files, rather than [source testing](https://github.com/MayankKharbanda/random_number_testing_module). Parts of code are from [Randomness Statistics Batteries](https://github.com/crocs-muni/rtt-statistical-batteries).


## Installation

- clone random\_number\_testing\_module.
- run Install.
- run multi\_process.py

## Description(Parameters)
 
- [-n] Number of random files to test (Required).
- [-t] Path of tests file (Required).
- [-d] Destination to store results (Default - results/).
- [-c] Number of cores to be allocated to the module.(Default - 4).
- [-m] Random files location, to test.

For example, if n=3 and m=files/random_file.
It will test
- file/random\_file\_0.bin
- file/random\_file\_1.bin
- file/random\_file\_2.bin
