# Virtual Gesture Calculator

A virtual calculator application that uses hand gesture recognition via MediaPipe Hands and OpenCV to allow users to interact with a calculator UI through pinch gestures detected by a webcam.

## Features

- Real-time hand tracking using MediaPipe Hands
- Virtual calculator UI with buttons controlled by pinch gestures
- Simple and intuitive interaction with the calculator using hand gestures

## Installation

### Prerequisites

- Python 3.12
- Bazel 6.5.0
- pip

### Build and install MediaPipe from source

Run the provided build script to build and install MediaPipe:

```bash
./build_mediapipe_from_source.sh
```

### Install other dependencies

```bash
pip install opencv-python numpy
```

## Usage

Run the virtual gesture calculator script:

```bash
python gesture_calculator.py
```

Press `q` to quit the application.

## License

This project is licensed under the MIT License.
