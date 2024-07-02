# OMRON CompoWay/F protocol on Temperature Controller E5AC
This software shows OMRON CompoWay/F protocol typical sample on Temperature Controller like E5AC, using Python.
## Overview
XXXXX
### Function
1. Image View: Still or Live image is displayed at 1/2 scaled image viewer.
2. Camera Selector: Select Webcam or Microscope cam.
3. Camera setting: Change the exposure etc. using the driver provided by the camera manufacture.
4. Scale-Bar: Show and hide the Scale-Bar.
5. Scale-Bar length: Change between 1um and 1000um to fit the objective lens magnification.
6. Scale-Bar color: white, black, green, light blue, red
7. Scale-Bar location: Move Scale-Bar where to mouse click.
8. Save file: Save as jpg file.

## Development Environment
#### Hardware Environment
  1. Camera: 1/2inch color CMOS,   1600x1200pixels,  4.2um/pixel,  10fps(max) (material(4))
  2. Relay Lens (Eyepiece): 0.7x (material(3))
  3. Objective Lens: 5x, 10x, 20x, 50x, 100x (material(1))
#### Software Environment
  1. OS: Windows11
  2. Python: Version 3.9.10
  3. Libraries: PySerial, Pillow
#### Known issue
  1. None
#### Related material
  1. [FCS module](https://github.com/TurBoss/TurBoHostLink)
  2. [FCS and BCC](https://github.com/TurBoss/TurBoHostLink)

