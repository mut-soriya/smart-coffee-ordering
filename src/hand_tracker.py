import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path="models/hand_landmarker.task", max_hands=1, detection_confidence=.5, tracking_confidence=.5):
        base=python.BaseOptions(model_asset_path=model_path)
        options=vision.HandLandmarkerOptions(base_options=base, running_mode=vision.RunningMode.VIDEO, num_hands=max_hands, min_hand_detection_confidence=detection_confidence, min_hand_presence_confidence=detection_confidence, min_tracking_confidence=tracking_confidence)
        self.detector=vision.HandLandmarker.create_from_options(options); self.timestamp_ms=0
    def process(self,frame):
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB); image=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb); self.timestamp_ms+=33
        return self.detector.detect_for_video(image,self.timestamp_ms)
    def draw_landmarks(self,frame,results):
        if results.hand_landmarks:
            for hand in results.hand_landmarks:
                h,w,_=frame.shape; pts=[(int(p.x*w),int(p.y*h)) for p in hand]
                for x,y in pts: cv2.circle(frame,(x,y),4,(0,210,120),-1)
                for c in vision.HandLandmarksConnections.HAND_CONNECTIONS:
                    cv2.line(frame,pts[c.start],pts[c.end],(0,180,100),2)
        return frame
    def close(self): self.detector.close()
