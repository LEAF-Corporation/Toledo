from ultralytics import YOLO
import torch

model = YOLO("models/yolov8s-seg.pt")


def model_training():
    model.predict(source="0", show=True)


if __name__ == '__main__':
    if torch.__version__.split('+')[1].startswith('cu') and torch.cuda.is_available():
        model_training()
