# Fly_High
complete guide form ground based tracking to autonomous areal based drone tracking.
## Overview

Camera calibration is the process of estimating the parameters of a camera's lens and image sensor. These parameters can be used to correct for lens distortion, measure the size of an object in world units, or determine the location of the camera in the scene.

This toolkit includes:

1. **Image Capture Tool**: Capture calibration images from your camera
2. **Calibration Tool**: Process the calibration images to compute camera parameters

## Requirements

- Python 3.6+
- OpenCV 4.5+
- NumPy 1.20+
- Matplotlib 3.4+ (for visualization)

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Capture Calibration Images

You need multiple images of a chessboard pattern from different angles and positions. The script `capture_images.py` helps you capture these images:

```bash
python capture_images.py
```

Controls:
- Press `c` to capture an image
- Press `q` or Escape to quit

The images will be saved in the `calibration_images` directory.

### Step 2: Run Camera Calibration

Process the calibration images to compute the camera matrix and distortion coefficients:

```bash
python camera_calibration.py
```

The calibration results will be saved in the `output` directory:
- `calibration_data.pkl`: Complete calibration data in pickle format
- `camera_matrix.txt`: Camera matrix in text format
- `distortion_coefficients.txt`: Distortion coefficients in text format
- Undistorted versions of the calibration images (if enabled)
