# Smart Coffee Web Kiosk

This UI is based on the provided Smart Coffee Ordering HTML design. It runs at 1280x720 and receives real-time cursor/gesture events from the Python computer-vision bridge over WebSocket.

Swipe up or down to scroll screens when their content overflows. On the drink customization screen, those gestures adjust quantity instead.

When the Python backend is running, the UI shows a live, mirrored camera preview with the tracked hand and gesture overlay. Hover over the preview with a mouse or the hand cursor to move it to the next screen corner.
