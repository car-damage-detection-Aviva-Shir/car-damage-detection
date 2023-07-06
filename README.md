
# Car Damage Detection

This project implements car damage detection using Convolutional Neural Networks (CNNs) and  VGG16 architecture. It provides a frontend interface built with Django and Atom framework, allowing users to upload an image of a damaged car and receive the detection report from the trained model.


## Features

- Utilizes the VGG16 architecture for car damage detection.
- Provides a user-friendly frontend interface built with Django and Atom framework.
- Allows users to upload car images and receive the detection report.
- Returns the detection report, indicating whether there is damage, and if so, the location of the damage (front, sides,rear) and its severity(minor, moderate, severe).
- Supports multiple image formats (e.g., JPEG, PNG).


## Prerequisites
Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- Django==1.10
- TensorFlow==1.14.0
- Keras==2.2.4
- Atom
- Pillow==6.2.0


## Example for Minor damage in the Rear side 
<h3>The system receives a picture of a damaged car</h3>
<img src="https://github.com/aviva997/Car-Damage-Detection/assets/73630522/cf92cceb-2f7c-43be-9dc5-459e3ded5b66" width="400" alt="Damaged Car">
<h3>after click on "click to start Assessment":</h3>
<img src="https://github.com/aviva997/Car-Damage-Detection/assets/73630522/5b21da1b-ed67-4b82-a64c-a29b6759fd04" width="400" alt="Damaged Car">

## Example for Moderate damage in the Rear side
<h3>The system receives a picture of a damaged car</h3>
<img src="https://github.com/aviva997/Car-Damage-Detection/assets/73630522/5df183bf-ef19-4671-a93a-008eb0c84318" width="400" alt="Damaged Car">
<h3>after click on "click to start Assessment":</h3>
<img src="https://github.com/aviva997/Car-Damage-Detection/assets/73630522/18eb880f-51a8-4360-ac5e-dda0db8ce2e5" width="400" alt="Damaged Car">

## Example for Severe damage in the Front side
<h3>The system receives a picture of a damaged car</h3>
<img src="https://github.com/aviva997/Car-Damage-Detection/assets/73630522/774528c2-45ea-47e1-97b1-1f6a750a1a6d" width="400" alt="Damaged Car">
<h3>after click on "click to start Assessment":</h3>
<img src="https://github.com/aviva997/Car-Damage-Detection/assets/73630522/95f4d9fc-6980-4d78-a3a3-5be4a026a601" width="400" alt="Damaged Car">


## Installation

1. Clone this repository to your local machine.
```bash
https://github.com/car-damage-detection-Aviva-Shir/car-damage-detection.git
```
2. Clone this repository to your local machine.
```bash
 cd car-damage-detection
 cd carcare
 cd cardamage
```
3. Run
```bash
python manage.py runserver
```

    
