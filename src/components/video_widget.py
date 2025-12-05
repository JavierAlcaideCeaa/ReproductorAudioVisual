class VideoWidget:
    def __init__(self):
        self.video_path = None

    def load_video(self, path):
        self.video_path = path
        # Logic to load the video file

    def render(self):
        if self.video_path:
            # Logic to render the video on the UI
            pass
        else:
            raise ValueError("No video loaded. Please load a video first.")