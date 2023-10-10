import cv2
import torch
import numpy as np
import pickle
import pandas as pd
import string
import os

from random import choice, shuffle, uniform
from datetime import datetime
import time as t


print('Bem-vindo à ferramenta MSQTRS\nToledo do Brasil - Indústria de Balanças Ltda.\nCopyright ©2023')


def carregar_cameras(index):
    # Configuração da câmera
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    if cap is None or not cap.isOpened():
        print(f'AVISO: Não foi possível carregar a câmera {index}')
        exit(0)

    return cap


cap1 = carregar_cameras(0)
cap2 = carregar_cameras(2)

# Inicializar o modelo
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load("ultralytics/yolov5", "yolov5x")
model.names = {0: 'person', 7: 'truck'}


comp = []
larg = []
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

            c1, c2 = [(bbox[0] + 17, bbox[1] + 180), (bbox[2] - 95, bbox[3])]
            l1, l2 = [(bbox[0] + 446, bbox[1] + 433), (bbox[2] - 30, bbox[3] - 85)]

            # Câmera 1
            cv2.line(frame, (56, 187), (500, 453), (0, 0, 255), 2)
            cv2.line(frame, (500, 453), (570, 350), (0, 0, 255), 2)

            # Câmera 2
            cv2.line(frame, (690, 190), (1137, 453), (0, 0, 255), 2)
            cv2.line(frame, (1137, 453), (1205, 350), (0, 0, 255), 2)

            comprimento, largura = [(cv2.norm(np.array(c1) - np.array(c2))) * 0.048975,
                                    (cv2.norm(np.array(l1) - np.array(l2))) * 0.043975]

            if largura > 6.00:
                if largura > 7.00:
                    largura -= 0.5
                largura -= 1.20

            comp.append(comprimento)
            larg.append(largura)

            cv2.putText(frame,
                        f"Caminhao C: {comprimento:.2f}cm L: {largura:.2f}cm {bbox}",
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
    # x, y, w, h = roi
    # dst = dst[y:y + h, x:x + w]

    return dst


def mock_dados():
    modelos = ['Volvo', 'DAF', 'Volkswagen', 'Scania', 'Mercedes-Benz', 'Iveco', 'Ford']
    caracteres = [x for x in str(string.ascii_uppercase + string.digits)]
    shuffle(modelos)
    shuffle(caracteres)

    modelo = choice(modelos)
    placa = ''.join([choice(caracteres) for i in range(7)])
    peso = f'{round(uniform(250.00, 600.00), 2)}g'

    return modelo, placa, peso


def relatorio(date, model, plate, weight, length, width, time):
    save_date = datetime.strftime(date, '%d_%m_%Y')
    date = datetime.strftime(date, '%d/%m/%Y %H:%M:%S')
    path = fr'C:\Users\kmuvi\Documents\Toledo\Relatorio_{save_date}.xlsx'

    dataframe = pd.DataFrame(
        columns=['Data', 'Modelo', 'Placa', 'Peso', 'Comprimento', 'Largura', 'Tempo decorrido'],
        data={'Data': date, 'Modelo': model, 'Placa': plate, 'Peso': weight, 'Comprimento': length,
              'Largura': width, 'Tempo decorrido': time},
        index=[0])

    if not os.path.exists(path):
        dataframe.to_excel(path, index=False)
    else:
        dataframe_old = pd.read_excel(path)
        dataframe_new = pd.concat([dataframe_old, dataframe], join='inner', ignore_index=True)
        dataframe_new.to_excel(path, index=False)


data = datetime.now()
start = t.time()
# Inicializar a detecção
with (torch.no_grad()):
    while True:
        # Ler um frame de cada câmera
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1:
            print('A conexão com a câmera 1 foi perdida.')
            break
        if not ret2:
            print('A conexão com a câmera 2 foi perdida.')
            break

        frame1 = tirar_distorcao(frame1)
        frame2 = tirar_distorcao(frame2)

        cv2.putText(frame1, 'CAM-1', (20, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 6, cv2.LINE_4)
        cv2.putText(frame1, 'CAM-1', (20, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2, cv2.LINE_4)

        cv2.putText(frame2, 'CAM-2', (20, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 6, cv2.LINE_4)
        cv2.putText(frame2, 'CAM-2', (20, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2, cv2.LINE_4)

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
            end = t.time()
            tempo = f'{round(end - start,2)}s'

            modelo, placa, peso = mock_dados()
            comprimento = f'{round(sum(comp) / len(comp),2)}cm'
            largura = f'{round(sum(larg) / len(larg),2)}cm'

            relatorio(data, modelo, placa, peso, comprimento, largura, tempo)
            break

# Liberar a captura de vídeo e fechar a janela
cap1.release()
cap2.release()
cv2.destroyAllWindows()
print('Fim do programa.')
