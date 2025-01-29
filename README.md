# Kinect smanetting

## Hardware

- Kinect XBOX 360 KINECT MODEL 1414
- USB Adapter for Kinect XBOX 360 KINECT MODEL 1414 (Kinect to USB) [amazon](https://www.amazon.it/s?k=adapter+kinect+to+usb)

## Software

- [libfreenect](https://github.com/OpenKinect/libfreenect)

## Install

Clone the repository

```bash
git clone https://github.com/OpenKinect/libfreenect.git
```

Install the dependencies

```bash
brew install libusb cmake
```

> If you don't have brew installed, you can install it from the documentation [here](https://brew.sh/)

Compile the library

```bash
cd libfreenect
mkdir build
cd build
cmake ..
make
sudo make install
```

> Note: If you have a problem with the permissions, you can use `sudo` before the command

## Test

Connect the Kinect to the USB adapter and the USB adapter to the computer.

Run the test

```bash
./bin/freenect-glview
```

> Note: the bin folder is in the build folder

You can use the following keys to interact with the test:

- 'w' - tilt up
- 's' - level
- 'x' - tilt down
- '0'-'6' - select LED mode
- '+' & '-' - change IR intensity 
- 'f' - change video format
- 'm' - mirror video
- 'o' - rotate video with accelerometer 
- 'e' - auto exposure
- 'b' - white balance
- 'r' - raw color
- 'n' - near mode (K4W only) 

## Python library

To use the Kinect with Python, you can use the library `freenect` that is a wrapper of the library `libfreenect`.

Navigate to the python folder in the libfreenect repository `cd wrappers/python`

Install dependencies

```bash
pip install cython
```

Regenerate the cython file freenect.c

```bash
cython freenect.pyx
```


Compile the python library

```bash
python setup.py build_ext --inplace
```