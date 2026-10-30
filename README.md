# ☕ Smart Coffee Ordering System

A touchless coffee ordering kiosk that allows customers to browse a menu, customize drinks, manage their cart, and place orders using hand gestures. The system combines computer vision, hand tracking, a Python backend, and a web-based kiosk interface to create an interactive ordering experience.

## ✨ Project Overview

Smart Coffee is a gesture-controlled coffee ordering application designed to make self-service ordering more interactive and accessible. Instead of relying entirely on a touchscreen or mouse, customers can use hand movements to navigate the interface and interact with products.

The application uses OpenCV to process camera input, MediaPipe to track hand landmarks, and a gesture recognition system to translate hand movements into interface actions. A Python backend communicates with the HTML, CSS, and JavaScript frontend through WebSockets.

## 🚀 Features

### 🖐️ Gesture-Based Interaction
- Real-time hand tracking using MediaPipe.
- Camera-based gesture recognition.
- Virtual cursor for interacting with the kiosk.
- Swipe gestures for navigating interface elements.
- Pinch-and-hold interaction for confirming selections.
- Visual feedback for cursor position and interactive elements.

### ☕ Coffee Ordering
- Browse products by category.
- Explore hot coffee, iced coffee, non-coffee drinks, and bakery items.
- View product details and images.
- Customize available product options.
- Adjust item quantities.
- Add products to the shopping cart.
- Review and confirm an order.
- Generate an order ticket after confirmation.

### 🛒 Cart and Order Management
- Review selected products before ordering.
- Update quantities and manage cart items.
- Calculate the order total.
- Confirm orders through the kiosk interface.
- Send confirmed orders to the kitchen queue.

### 🍳 Kitchen Queue
- Display incoming orders.
- Organize orders for kitchen staff.
- Provide an overview of orders waiting to be prepared.

### 🎨 Interactive Kiosk Interface
- Modern coffee-shop-inspired visual design.
- Responsive HTML, CSS, and JavaScript interface.
- Product cards and image-based menu browsing.
- Hover and selection feedback.
- Camera and hand-tracking status indicators.
- Error messages and interaction timeout handling.
- Help and welcome screens.

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend logic and application coordination |
| OpenCV | Camera access and image processing |
| MediaPipe | Real-time hand landmark detection |
| HTML5 | Kiosk interface structure |
| CSS3 | Styling, layout, and animations |
| JavaScript | Frontend interactions and interface updates |
| WebSockets | Real-time communication between frontend and backend |
| JSON | Menu and product data storage |

## 🏗️ System Architecture

The application follows a camera-to-interface workflow:

1. **Camera input:** OpenCV captures frames from the camera.
2. **Hand tracking:** MediaPipe detects and tracks hand landmarks.
3. **Gesture recognition:** The gesture engine interprets hand movements.
4. **Backend processing:** Python handles application state, menu interactions, cart operations, and order management.
5. **Real-time communication:** A WebSocket connection transfers relevant events and state updates.
6. **Frontend rendering:** HTML, CSS, and JavaScript display the kiosk interface, virtual cursor, products, cart, and order information.
7. **Order processing:** Confirmed orders are added to the kitchen queue.

## 📁 Project Structure

```text
smart-coffee-ordering/
├── assets/
│   ├── coffee/              # Coffee and product images
│   └── sounds/              # Interaction sound effects, if included
├── data/
│   └── menu.json            # Menu and product data
├── docs/                    # Project documentation
├── frontend/
│   ├── index.html           # Main kiosk interface
│   ├── css/                 # Stylesheets, if organized separately
│   └── js/
│       └── products.js      # Product data, if used by the frontend
├── models/
│   └── hand_landmarker.task # MediaPipe hand-landmark model
├── tests/                   # Automated tests
├── README.md
└── requirements.txt         # Python dependencies, if included
```

*The tree above illustrates the main project areas. Actual filenames and folders may vary according to the current repository.*

## ⚙️ Requirements

Before running the project, make sure you have:

- Windows, Linux, or another supported Python environment.
- Python compatible with the installed project dependencies.
- A working webcam.
- A modern web browser.
- The required Python packages.
- The MediaPipe hand-landmark model file.
- The project's frontend assets and product data.

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd smart-coffee-ordering
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

If the repository includes `requirements.txt`, run:

```bash
python -m pip install -r requirements.txt
```

### 4. Check the project files

Make sure the hand-landmark model, menu data, product images, and other required assets are available in their expected locations.

## ▶️ Running the Application

1. Activate your Python virtual environment.
2. Start the Python application using its configured entry-point script.
3. Open the kiosk interface through the local URL provided by the application, if it does not open automatically.
4. Allow camera access when prompted.
5. Wait for the camera and hand-tracking system to initialize.
6. Use the supported gestures to browse the menu and place an order.

**Note:** Use the actual backend startup command and local URL defined in your project. They should be verified against the current source files before publishing this README.

## 🧪 Testing

The project includes automated tests. To run tests using Python's unittest framework, execute:

```bash
python -m unittest discover -q
```

On a Windows installation where Python 3.13 is installed through the Python launcher, you can also run:

```bash
py -3.13 -m unittest discover -q
```

## 📷 Camera and Gesture Troubleshooting

- **Camera does not open:** Check Windows camera privacy settings and allow camera access for the Python application.
- **Hand tracking does not work:** Check lighting, camera positioning, and the availability of the required model file.
- **Gestures are not recognized consistently:** Keep your hand within the camera frame and avoid obstructing the hand from view.
- **Kiosk cannot communicate with the backend:** Confirm that the Python server is running and the WebSocket connection is configured correctly.
- **Product images are missing:** Check the image paths referenced by the product data and ensure the required files exist in the assets directory.

## 🎯 Project Objectives

- Explore practical applications of computer vision.
- Implement real-time hand tracking and gesture recognition.
- Connect a Python backend to a web-based user interface.
- Develop an interactive, touchless ordering workflow.
- Practice software architecture, testing, and modular development.
- Improve the customer ordering experience through natural interaction.

## 🔮 Future Improvements

Potential improvements include:
- More robust gesture recognition in different lighting conditions.
- Better camera-processing performance.
- Expanded product customization.
- Improved kitchen order status tracking.
- More detailed order history and reporting.
- Packaging the application for easier installation and deployment.

## 👨‍💻 Development

This project is developed as a practical software project combining computer vision, frontend development, and backend application logic.

Contributions, feedback, and suggestions for improvement are welcome.

## 📄 License

Add the appropriate license for this project before distributing or publishing it.
