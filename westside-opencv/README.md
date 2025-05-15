# Westside-W Detector (OpenCV + MediaPipe)

## Overview
This project is a real-time computer vision application that detects the iconic "Westside W" hand gesture using your webcam. When the gesture is detected, the app celebrates by displaying a bold message and (on first detection) opening Ice Cube's classic track "It Was A Good Day" on YouTube.

## Features
- **Real-time hand gesture detection** using OpenCV and MediaPipe
- **Recognizes the 'Westside W' sign** (index and pinky up, middle and ring intertwined)
- **Fun integration:** Automatically opens Ice Cube's music video the first time the gesture is detected
- **Customizable message and color**

## Why?
Because I'm from the West Coast of America and grew up loving the music of Ice Cube, Tupac, and Snoop Dogg. This project is a playful tribute to Westside hip-hop culture and the legendary artists who shaped it.

## How It Works
- The app uses your webcam to track your hand in real time.
- When you flash the 'Westside W' (index and pinky up, middle and ring intertwined), it displays a celebratory message in the center of the screen.
- On the first detection, it opens Ice Cube's "It Was A Good Day" in your browser.

## Installation
1. **Clone the repository and enter the folder:**
   ```bash
   cd westside-opencv
   ```
2. **(Recommended) Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install opencv-python mediapipe
   ```

## Usage
1. **Run the script:**
   ```bash
   python main.py
   ```
2. **Show your hand in front of the webcam and make the 'Westside W' sign.**
3. **Enjoy the message and the music!**
4. **Press ESC to quit.**

## Notes
- This project is for fun and learning. Tweak the detection logic or message as you like!
- Works on macOS, Windows, and Linux (no Windows-only dependencies).

## Credits
- Inspired by the music and culture of the West Coast.
- Shoutout to [Ice Cube - It Was A Good Day](https://www.youtube.com/watch?v=rzRqEWJYwX4&ab_channel=IceCubeVEVO), Tupac, and Snoop Dogg.

---

*"Westside!"* ✌️ 