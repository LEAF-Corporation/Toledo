import cv2
import torch
import numpy as np
import pickle

#from CameraCalibration.calibration import calibration

# Inicializar o modelo
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load("ultralytics/yolov5", "yolov5x")
model.names = {0: 'person', 7: 'truck'}


# Função para processar a detecção

def processar_detecao(frame, results, device, model):
    frame_height, frame_width, _ = frame.shape

    # Enviar o modelo para a GPU
    model.to(device)

    # Obter as previsões de detecção
    pred = results.pred[0]


    # Iterar sobre cada detecção
    for det in pred:
        if int(det[5]) not in [0, 7]:
            continue

        bbox = det[:4]  # Bounding box: (x1, y1, x2, y2)
        bbox = [int(i) for i in bbox]  # Converter para inteiros

        classe = model.names[int(det[5])]  # Classificações

        # Frente do caminão

        if classe == "truck":
            cor = (0, 255, 0)  # Cor verde para caminhão
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), cor, 2)

            c1, c2 = [(bbox[0]+17, bbox[1]+180), (bbox[2]-95, bbox[3])]
            l1, l2 = [(bbox[2]-95, bbox[3]), (bbox[2]-30, bbox[3]-85)]

            # Câmera 1
            cv2.line(frame, (60, 190), (500, 453), (0, 0, 255), 2)
            cv2.line(frame, (500, 453), (570, 350), (0, 0, 255), 2)

            # Câmera 2
            cv2.line(frame, (690, 187), (1133, 453), (0, 0, 255), 2)
            cv2.line(frame, (1133, 453), (1203, 347), (0, 0, 255), 2)

            comprimento, largura = [(cv2.norm(np.array(c1) - np.array(c2))) * 0.048975,
                                    (cv2.norm(np.array(l1) - np.array(l2))) * 0.048975]
            cv2.putText(frame,
                        f"Caminhao C: {comprimento:.2f}cm L: {largura:.2f}cm",  # {c1, c2, l1, l2}
                        (bbox[0] + 20, bbox[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

        elif classe == "person":
            # Exibir alerta e desenhar uma bounding box vermelha caso uma pessoa seja detectada
            cor = (0, 0, 255)  # Cor vermelha para pessoa
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), cor, 2)
            cv2.putText(frame, f"ALERTA: Pessoa detectada!", (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

        # print(f'Class: {classe} - Accuracy: {det[4] * 100:.2f}%')


def tirar_distorcao(frame):
    w, h = frame.shape[:2]
    cameraMatrix = pickle.load(open("cameraMatrix.pkl", "rb"))
    dist = pickle.load(open("dist.pkl", "rb"))

    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))

    dst = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    #dst = dst[y:y + h, x:x + w]

    return dst


cap1 = cv2.VideoCapture(0)  # Câmera 1
cap2 = cv2.VideoCapture(2)  # Câmera 2

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# Inicializar a detecção
with torch.no_grad():
    while True:
        # Ler um frame de cada câmera
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        frame1 = tirar_distorcao(frame1)
        frame2 = tirar_distorcao(frame2)

        # Concatenar horizontalmente os frames
        combined_frame = np.hstack((frame1, frame2))

        # Executar a detecção no frame combinado
        results = model(combined_frame)

        # Processar a detecção e desenhar as bounding boxes
        processar_detecao(combined_frame, results, "cuda", model)

        # Exibir o frame com as bounding boxes
        cv2.imshow('Deteccao em Tempo Real', combined_frame)

        # Verificar se o usuário pressionou a tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar a captura de vídeo e fechar a janela
cap1.release()
cap2.release()
cv2.destroyAllWindows()
