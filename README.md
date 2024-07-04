# OMRON CompoWay/F protocol on Temperature Controller E5AC
Python , OMRON , CompoWay/F protocol , serial IF , Binary I/O comunication , Temperature Controller like E5AC ,　Digital Controller , without RS-485 communication IF model , Enable Manual Mode
## Overview
It helps to operate an OMRON digital controller from an external PC. The device used is an OMRON E5AC-TCX4ASM-000 digital controller without an RS-485 communication IF.

### Function
These functions are available as libraries for Omron Digital Controllers.
1. Allocate serial IF communication.
2. Typical CompoWay/F protocol command and response.
3. Enable Manual Mode
4. Read temperature 
5. Set output value

### Notes
1. CompoWay/F bautrates is 38400bps, not 9600bps.
2. BCC(Block Check Character) is 8-bit value that is the result of an EXCLUSIVE OR sequentially performed between each character in a transmission.
3. The EXCLUSIVE OR module was copied from rerated material(1) website.

### Hardware Environment
  1. Temperature Controller : OMRON E5AC-TCX4ASM-000 Digital Controller without RS-485 communication IF.
  2. USB: OMRON USB Serial Conversion Cable E58-CIFQ2
  3. PC: windows PC
### Software Environment
  1. OS: Windows11
  2. Python: Version 3.9.13
  3. Libraries: PySerial
### Known issue
  1. None
### Related material
  1. [FCS module](https://github.com/TurBoss/TurBoHostLink)
  2. [Frame Checksum (FCS)....EXCLUSIVE OR ...expressed in ASCII Character](https://www.manualslib.com/manual/1538556/Omron-Sysmac-Cv-Series.html?page=60)
  3. [Block Check Character(BCC)....EXCLUSIVE OR ...expressed in bytes.](https://www.manualslib.com/manual/1901904/Omron-E5c-T-Series.html?page=27)
  4. [OMRON Digital Temperature Controllers E5AC Catalog](https://www.fa.omron.co.jp/products/family/3157/download/catalog.html)
  5. [OMRON Digital Temperature Controllers User’s Manual E5@C](https://www.fa.omron.co.jp/data_pdf/mnu/h174-e1-18_e5_c.pdf?id=3157)
  6. [OMRON Digital Temperature Controllers Communications Manual E5@C](https://www.fa.omron.co.jp/data_pdf/mnu/h175-e1-17_e5_c.pdf?id=3157)
  7. [OMRON Conversion Cable E58-CIFQ Catalog](https://www.fa.omron.co.jp/data_pdf/cat/e58-cifq2_ds_e_1_6_csm1011536.pdf?id=3166)
