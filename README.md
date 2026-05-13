# 📷 Camera Projection Model

> Assignment 1 — Computer Vision 2026/1 | UFES

Python application for visualizing and interacting with the **Rigid Body Motion and Perspective Projection Model**.

The program allows the user to manipulate the camera pose and intrinsic parameters, while observing the corresponding changes in both the 3D scene and the projected 2D image.

---

## 🚀 Features

- 3D visualization of an object and the camera reference frame
- Interactive control of camera **extrinsic parameters**
  - Translation along X, Y and Z
  - Rotation around X, Y and Z
- Support for camera motion in two different reference frames:
  - **World frame**
  - **Camera's own reference frame**
- Real-time perspective projection of the 3D object onto the image plane
- Interactive control of camera **intrinsic parameters**
  - Image width and height in pixels
  - CCD/sensor dimensions
  - Focal distance
  - Skew factor
- Automatic update of the principal point based on image dimensions
- Synchronized update of the 2D projection and 3D visualization after each parameter change

---

## 🛠️ Requirements

All project dependencies are listed in the `requirements.txt` file.

It is recommended to create and activate a virtual environment before installing the dependencies.

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

After installing the dependencies, run the application from the project root directory:

```bash
python main.py
```

---

## 📁 Project Structure

```text
camera-projection-model/
├── assets/
│   └── models/
│       └── bulbasaur.STL
│
├── src/
│   ├── camera.py           # Camera projection
│   ├── draw.py             # Plot configuration and reference frame drawing
│   ├── gui_template.py     # Main graphical interface
│   ├── object.py           # STL loading and object processing
│   └── transformations.py  # Translation and rotation matrices
│
├── main.py                 # Application entry point
├── README.md
└── requirements.txt
```

---

## 👤 Author

Gustavo Nunes Lopes

---

## 📚 Course

**Computer Vision 2026/1**  
Prof. Raquel Frizera Vassallo  
Universidade Federal do Espírito Santo — UFES
