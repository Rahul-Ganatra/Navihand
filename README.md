# NaviHand - Hand Gesture Controlled Cursor

NaviHand is a Python-based application that allows you to control your computer's cursor using hand gestures captured through your webcam. The project uses OpenCV and MediaPipe for hand detection and tracking, making it an intuitive and hands-free way to interact with your computer.

## Features

- **Cursor Movement**: Control your mouse cursor using your index finger
- **Gesture Controls**:
  - ✌️ Peace Sign (Index + Middle Finger): Left Click
  - 3️⃣ Three Fingers (Index + Middle + Ring): Right Click
  - ✊ Fist: Drag and Drop
  - 🤚 Both Hands Open: Lock Screen
- **Real-time Hand Tracking**: Smooth and responsive cursor movement
- **Customizable Settings**: Adjustable parameters for sensitivity and gesture detection

## Tech Stack

- **Python**: Core programming language
- **OpenCV**: For webcam access and image processing
- **MediaPipe**: For real-time hand detection and landmark tracking
- **PyAutoGUI**: For controlling mouse movements and clicks
- **NumPy**: For numerical operations

## Prerequisites

- Python 3.7 or higher
- Webcam
- Windows operating system

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Rahul-Ganatra/NaviHand.git
cd NaviHand
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python hand_control.py
```

2. Position your hand in front of the webcam:
   - Use your index finger to move the cursor
   - Make a peace sign (✌️) for left click
   - Show three fingers (3️⃣) for right click
   - Make a fist (✊) for drag and drop
   - Show both hands open (🤚) to lock the screen

3. To exit the application, press 'q' in the terminal window.

## How It Works

The application uses:
- OpenCV for webcam capture and image processing
- MediaPipe for hand detection and landmark tracking
- PyAutoGUI for mouse control

The system tracks 21 hand landmarks and uses specific combinations of these landmarks to detect different gestures. The cursor movement is mapped to the position of your index finger, while other gestures trigger specific mouse actions.

## Customization

You can adjust the following parameters in the code:
- `frameR`: Frame reduction for smoother cursor movement
- `smoothening`: Smoothing factor for cursor movement
- `wCam` and `hCam`: Camera resolution
- `wScr` and `hScr`: Screen resolution

## Troubleshooting

- If the cursor movement is too sensitive, increase the `smoothening` value
- If gestures are not being detected properly, ensure good lighting and clear hand visibility
- Make sure your webcam is properly connected and accessible

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe for the hand tracking model
- OpenCV for computer vision capabilities
- PyAutoGUI for mouse control functionality

---

Made with ❤️ by Rahul Jignesh Ganatra

