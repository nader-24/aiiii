import time
import numpy as np
from picamera2 import Picamera2
from libcamera import controls

class Camera:
    def __init__(self, resolution=(640, 480), framerate=30):
        self.width, self.height = resolution
        self.camera = self._init_camera(resolution, framerate)
        self.last_frame_time = time.time()
        self.frame_count = 0
        self.fps = 0
        
    def _init_camera(self, resolution, framerate):
        # Initialize and configure camera
        camera = Picamera2()
        
        # Configure preview settings
        config = camera.create_preview_configuration(
            main={"size": resolution, "format": "RGB888"},
            controls={"FrameRate": framerate}
        )
        camera.configure(config)
        
        # Optional: Set advanced controls
        camera.set_controls({
            "AwbEnable": True,         # Auto white balance
            "AeEnable": True,          # Auto exposure
            "NoiseReductionMode": 2,   # Enhanced noise reduction
        })
        
        camera.start()
        time.sleep(2.0)  # Allow sensor to adjust
        return camera
    
    def get_frame(self):
        # Capture frame as numpy array
        frame = self.camera.capture_array()
        
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
        self.camera.stop()
        self.camera.close()