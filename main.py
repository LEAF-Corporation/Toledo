"""
ESTE É O CÓDIGO PRINCIPAL, TODA A MÁGICA ACONTECE AQUI :)
DEIXEI AS FUNÇÕES COMENTADAS PARA CONSCIENTIZAR PARA O QUE CADA UMA SERVE.
*TENHA PARA NÃO SUBIR ALTERAÇÕES INDEVIDAMENTE*
"""


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


def carregar_cameras(index: int) -> cv2.VideoCapture:
    """
    :param index: Índice da câmera (Qual "porta" a câmera é utilizada)
    :return: VideoCapture
    """

    # Inicia a captura
    cap = cv2.VideoCapture(index)

    # Define a resolução da janela da câmera (800x600)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    # Caso a câmera não abrir ou não ser detectada, ele encerrará o programa
    if cap is None or not cap.isOpened():
        print(f'AVISO: Não foi possível carregar a câmera {index}')
        exit(0)

    return cap


# Inicia as duas câmeras
cap1 = carregar_cameras(0)
cap2 = carregar_cameras(1)

# Verifica se núcleos CUDA estão disponíveis e carrega o dataset YOLOv5
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load("ultralytics/yolov5", "yolov5x")
model.names = {0: 'person', 7: 'truck'}  # NÃO MEXER, o dicionário serve para apontar a classe de detecção no dataset.

# Comprimento e Largura do caminhão que é obtido durante a execução
comp = []
larg = []


# Função para processar a detecção
def processar_deteccao(frame, results, device, model):
    """
    :param frame: Frame de captura da câmera
    :param results: Resultado do processamento de imagem
    :param device: Dispositivo (CUDA/CPU)
    :param model: Dataset YOLOv5
    :return:
    """

    frame_height, frame_width, _ = frame.shape

    # Enviar o modelo para a GPU
    model.to(device)

    # Obter as previsões de detecção
    pred = results.pred[0]

    # Iterar sobre cada detecção
    for det in pred:
        if int(det[5]) not in [0, 7]:  # Se não tiver caminhão/pessoa, pula a detecção do frame.
            continue

        bbox = det[:4]  # Bounding box: (x1, y1, x2, y2)
        bbox = [int(i) for i in bbox]  # Converter para inteiros

        classe = model.names[int(det[5])]  # Classificações

        if classe == "truck":
            cor = (0, 255, 0)  # Cor verde para caminhão
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), cor, 2)

            c1, c2 = [(bbox[0] + 17, bbox[1] + 180), (bbox[2] - 95, bbox[3])]
            l1, l2 = [(bbox[0] + 446, bbox[1] + 433), (bbox[2] - 30, bbox[3] - 85)]

            # Câmera 1: Linha de demarcação da pista
            cv2.line(frame, (56, 187), (500, 453), (0, 0, 255), 2)
            cv2.line(frame, (500, 453), (570, 350), (0, 0, 255), 2)

            # Câmera 2: Linha de demarcação da pista
            cv2.line(frame, (690, 190), (1137, 453), (0, 0, 255), 2)
            cv2.line(frame, (1137, 453), (1205, 350), (0, 0, 255), 2)

            # Algoritmo de cálculo do comprimento e largura do caminhão
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


# Tira a distorção (Olho de Peixe) da câmera
def tirar_distorcao(frame) -> cv2.VideoCapture:
    """
    :param frame: Frame de captura da câmera
    :return: VideoCapture
    """
    w, h = frame.shape[:2]
    cameraMatrix = pickle.load(open("config/cameraMatrix.pkl", "rb"))
    dist = pickle.load(open("config/dist.pkl", "rb"))

    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))

    dst = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
    # x, y, w, h = roi
    # dst = dst[y:y + h, x:x + w]

    return dst


# Dados gerados do caminhão (Modelo, Placa e Peso)
def mock_dados() -> tuple:
    """
    :return: Tupla de dados do caminhão
    """
    modelos = ['Volvo', 'DAF', 'Volkswagen', 'Scania', 'Mercedes-Benz', 'Iveco', 'Ford']
    caracteres = [x for x in str(string.ascii_uppercase + string.digits)]
    shuffle(modelos)
    shuffle(caracteres)

    modelo = choice(modelos)
    placa = ''.join([choice(caracteres) for i in range(7)])
    peso = f'{round(uniform(250.00, 600.00), 2)}g'

    return modelo, placa, peso


# Relatório pós-execução com os dados obtidos na execução
def relatorio(date, brand, plate, weight, length, width, time):
    """
    :param date: Data da execução do código (Datetime)
    :param brand: Marca do caminhão
    :param plate: Número da placa
    :param weight: Peso do caminhão
    :param length: Comprimento do caminhão
    :param width: Largura do caminhão
    :param time: Tempo de execução do código
    :return:
    """
    save_date = datetime.strftime(date, '%d_%m_%Y')
    date = datetime.strftime(date, '%d/%m/%Y %H:%M:%S')
    path = fr'C:\Users\kmuvi\Documents\Toledo\Relatorio_{save_date}.xlsx'

    dataframe = pd.DataFrame(
        columns=['Data', 'Modelo', 'Placa', 'Peso', 'Comprimento', 'Largura', 'Tempo decorrido'],
        data={'Data': date, 'Modelo': brand, 'Placa': plate, 'Peso': weight, 'Comprimento': length,
              'Largura': width, 'Tempo decorrido': time},
        index=[0])

    if os.path.exists(path):
        dataframe_old = pd.read_excel(path)
        dataframe = pd.concat([dataframe_old, dataframe], join='inner', ignore_index=True)

    dataframe.to_excel(path, index=False)


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

        # Concatena os frames horizontalmente
        combined_frame = np.hstack((frame1, frame2))

        # Executa a detecção no frame combinado
        results = model(combined_frame)

        # Processa a detecção e desenha as bounding boxes
        processar_deteccao(combined_frame, results, "cuda", model)

        # Exibe o frame com as bounding boxes
        cv2.imshow('Deteccao em Tempo Real', combined_frame)

        # Verifica se o usuário pressionou a tecla 'esc' para sair
        if cv2.waitKey(1) & 0xFF == 27:
            end = t.time()
            tempo = f'{round(end - start, 2)}s'

            modelo, placa, peso = mock_dados()
            comprimento = f'{round(sum(comp) / len(comp), 2)}cm'
            largura = f'{round(sum(larg) / len(larg), 2)}cm'

            relatorio(data, modelo, placa, peso, comprimento, largura, tempo)
            break

# Libera a captura de vídeo e fecha a janela
cap1.release()
cap2.release()
cv2.destroyAllWindows()
print('Fim do programa.')
