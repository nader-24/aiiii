import cv2
import numpy as np
from camera_module import Camera

def main():
    # Initialize camera with optional parameters
    camera = Camera(resolution=(640, 480), framerate=30)
    
    try:
        print("Starting camera preview. Press 'q' to exit.")
        while True:
            frame = camera.get_frame()
            
            # Display FPS on frame
            fps_text = f"FPS: {camera.fps:.1f}"
            cv2.putText(frame, fps_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow("Raspberry Pi Camera (picamera2)", frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # Cleanup resources
        camera.release()
        cv2.destroyAllWindows()
        print("Camera resources released")

if __name__ == "__main__":
    main()