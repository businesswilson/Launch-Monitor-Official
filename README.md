# Golf Swing Analysis Space

## Features
- REST API (`/analyze-video`) for pose and ball detection
- Gradio UI for visual uploads and feedback

## Deploy on Hugging Face Spaces

1. Create a new Space (choose "Gradio" or "Custom" for FastAPI).
2. Upload all files from this repo.
3. For REST API: set `app.py` as the entrypoint.
4. For Gradio UI: set `gradio_app.py` as the entrypoint.
5. Wait for build, then use the API or UI!

## API Example

POST `/analyze-video` with a video file (form field `video`).

Response:
```json
{
  "pose_keypoints": { ... },
  "ball": { "x": 123, "y": 456, "radius": 17 }
}
```
```

---

**Once you have these files, zip the folder and upload to Hugging Face Spaces, or push to GitHub and link your Space.**

If you need any more help, or want to see a more advanced version, just ask!
