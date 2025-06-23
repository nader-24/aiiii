import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

class Camera:
    def __init__(self, resolution=(640, 480), framerate=30):
        self.width, self.height = resolution
        self.camera = self._init_camera(resolution, framerate)
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        self.last_frame_time = time.time()
        self.frame_count = 0
        self.fps = 0
        # Warm-up camera and auto-adjust settings
        time.sleep(2.0)
        
    def _init_camera(self, resolution, framerate):
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = framerate
        # Optional: Configure camera settings (e.g., rotation, brightness)
        # camera.rotation = 180
        # camera.brightness = 60
        return camera
    
    def get_frame(self):
        # Clear stream for fresh capture
        self.raw_capture.truncate(0)
        self.camera.capture(self.raw_capture, format='bgr', use_video_port=True)
        frame = self.raw_capture.array
        
        # Calculate FPS
        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.last_frame_time = current_time
            
        return frame
    
    def release(self):
        self.camera.close()
        self.raw_capture.close()