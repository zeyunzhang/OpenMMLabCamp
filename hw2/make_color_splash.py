from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import cv2
from pathlib import Path
from PIL import Image

def last_n_parts(filepath: Path, n: int = 2) -> Path:
    return Path(*filepath.parts[-abs(n):])

config_file = "configs/mask_rcnn/balloon.py"
checkpoint_file = "work_dirs/balloon/latest.pth"
frames_dir = "video/frames"
segmented_frames_dir = "video/segmented"

model = init_detector(config_file, checkpoint_file)

video_reader = mmcv.VideoReader("./test_video.mp4")
video_reader.cvt2frames(frames_dir)

for img in Path(frames_dir).iterdir():
    print(img)
    print(last_n_parts(Path(img), 1))
    result = inference_detector(model, img)

    frame = model.show_result(img, result, 0.5)
    image_pil = Image.fromarray(frame)
    image_pil.save(Path(segmented_frames_dir) / last_n_parts(img, 1))

mmcv.video.frames2video(segmented_frames_dir, "./test_video_color_splash.mp4")

"""
img_org = Image.open(img_url)
img_gray= img_org.convert('L')
img_gray.save(img_out)
"""
