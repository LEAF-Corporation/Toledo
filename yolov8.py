from ultralytics import YOLO
import numpy as np

model = YOLO("yolov8x-seg.pt")

results = model.predict(source='2', show=True, stream=True, classes=[0, 7])  # , show_labels=False)
names = model.names

for r in results:
    for c in r.boxes.cls:
        tag = names[int(c)]
        if tag == 'person':
            print('Alerta, pessoa!')
        elif tag == 'truck':
            print('Alerta, caminhão!')

# Process results list
#for result in results:
#    box = result.boxes[0]
#    class_id = result.names[box.cls[0].item()]
#    if class_id == 'person':
#        print('Alerta, pessoa detectada!')
