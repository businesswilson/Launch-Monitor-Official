import gradio as gr
import cv2
import numpy as np
from utils import analyze_pose, detect_ball

def analyze_video_ui(video):
    # Read first frame
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None, 'Could not read video'

    pose = analyze_pose(frame)
    ball = detect_ball(frame)

    # Draw results
    out = frame.copy()
    if pose:
        for k, (x, y) in pose.items():
            h, w = out.shape[:2]
            cv2.circle(out, (int(x * w), int(y * h)), 8, (0, 255, 0), -1)
    if ball is not None:
        cv2.circle(out, (ball[0], ball[1]), ball[2], (0, 0, 255), 2)

    return out, str({'pose_keypoints': pose, 'ball': ball})

iface = gr.Interface(
    fn=analyze_video_ui,
    inputs=gr.Video(),
    outputs=[gr.Image(type='numpy'), gr.Textbox()],
    title='Golf Swing Pose & Ball Detection',
    description='Upload a golf swing video. The first frame will be analyzed for pose and ball detection.'
)

if __name__ == '__main__':
    iface.launch()
