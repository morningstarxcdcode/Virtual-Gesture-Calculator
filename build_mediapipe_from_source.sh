#!/bin/bash

# Step 1: Clone the mediapipe repository
if [ ! -d "mediapipe" ]; then
  git clone https://github.com/google/mediapipe.git
else
  echo "mediapipe directory already exists, skipping clone."
fi

cd mediapipe

# Step 2: Checkout a stable release tag (optional)
# git checkout v0.9.0

# Step 3: Use the correct Bazel binary version 6.5.0 to build the mediapipe Python package
HERMETIC_PYTHON_VERSION=3.12 /opt/homebrew/Cellar/bazel/8.2.1/libexec/bin/bazel-6.5.0-darwin-arm64 build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/python:mediapipe_pip_package

# Step 4: Build the wheel file
bazel-bin/mediapipe/python/mediapipe_pip_package --output_dir ../mediapipe_wheel

cd ..

# Step 5: Install the built mediapipe wheel
pip3 install mediapipe_wheel/*.whl

echo "Mediapipe build and installation complete."
