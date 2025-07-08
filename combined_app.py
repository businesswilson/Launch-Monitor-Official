import gradio as gr
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import tempfile
from utils import analyze_pose, detect_ball

# Create FastAPI app
app = FastAPI()

# FastAPI endpoint
@app.post('/analyze-video')
async def analyze_video(video: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(await video.read())
        temp_path = temp_file.name

    cap = cv2.VideoCapture(temp_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return JSONResponse(content={'error': 'Could not read video'}, status_code=400)

    pose = analyze_pose(frame)
    ball = detect_ball(frame)

    return {
        'pose_keypoints': pose,
        'ball': {'x': int(ball[0]), 'y': int(ball[1]), 'radius': int(ball[2])} if ball is not None else None
    }

# Gradio UI function
def analyze_video_ui(video):
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None, 'Could not read video'

    pose = analyze_pose(frame)
    ball = detect_ball(frame)

    out = frame.copy()
    if pose:
        for k, (x, y) in pose.items():
            h, w = out.shape[:2]
            cv2.circle(out, (int(x * w), int(y * h)), 8, (0, 255, 0), -1)
    if ball is not None:
        cv2.circle(out, (ball[0], ball[1]), ball[2], (0, 0, 255), 2)

    return out, str({'pose_keypoints': pose, 'ball': ball})

# Create Gradio interface
iface = gr.Interface(
    fn=analyze_video_ui,
    inputs=gr.Video(),
    outputs=[gr.Image(type='numpy'), gr.Textbox()],
    title='Golf Swing Pose & Ball Detection',
    description='Upload a golf swing video. The first frame will be analyzed for pose and ball detection.'
)

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, iface, path="/")
