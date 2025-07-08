from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import tempfile
from utils import analyze_pose, detect_ball

app = FastAPI()

@app.post('/analyze-video')
async def analyze_video(video: UploadFile = File(...)):
    # Save video to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(await video.read())
        temp_path = temp_file.name

    # Open video and analyze first frame (for demo)
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
