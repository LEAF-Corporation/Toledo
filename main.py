import cv2
import numpy as np


# Coordenadas na imagem da câmera 1
x1_cam1, y1_cam1 = 100, 100
x2_cam1, y2_cam1 = 300, 100
x3_cam1, y3_cam1 = 300, 300
x4_cam1, y4_cam1 = 100, 300

# Coordenadas na imagem da vista de cima para o ponto correspondente na câmera 1
x_top1, y_top1 = 200, 200

# Coordenadas na imagem da câmera 2
x1_cam2, y1_cam2 = 400, 100
x2_cam2, y2_cam2 = 600, 100
x3_cam2, y3_cam2 = 600, 300
x4_cam2, y4_cam2 = 400, 300

# Coordenadas na imagem da vista de cima para o ponto correspondente na câmera 2
x_top2, y_top2 = 500, 200

# Coordenadas na imagem da câmera 3
x1_cam3, y1_cam3 = 100, 400
x2_cam3, y2_cam3 = 300, 400
x3_cam3, y3_cam3 = 300, 600
x4_cam3, y4_cam3 = 100, 600

# Coordenadas na imagem da vista de cima para o ponto correspondente na câmera 3
x_top3, y_top3 = 200, 500

# Coordenadas na imagem da câmera 4
x1_cam4, y1_cam4 = 400, 400
x2_cam4, y2_cam4 = 600, 400
x3_cam4, y3_cam4 = 600, 600
x4_cam4, y4_cam4 = 400, 600

# Coordenadas na imagem da vista de cima para o ponto correspondente na câmera 4
x_top4, y_top4 = 500, 500

# Defina os pontos de correspondência manualmente para cada câmera
pts_camera1 = np.float32([[x1_cam1, y1_cam1], [x2_cam1, y2_cam1], [x3_cam1, y3_cam1], [x4_cam1, y4_cam1]])
pts_camera2 = np.float32([[x1_cam2, y1_cam2], [x2_cam2, y2_cam2], [x3_cam2, y3_cam2], [x4_cam2, y4_cam2]])
pts_camera3 = np.float32([[x1_cam3, y1_cam3], [x2_cam3, y2_cam3], [x3_cam3, y3_cam3], [x4_cam3, y4_cam3]])
pts_camera4 = np.float32([[x1_cam4, y1_cam4], [x2_cam4, y2_cam4], [x3_cam4, y3_cam4], [x4_cam4, y4_cam4]])

# Defina os pontos correspondentes na vista de cima para cada câmera
pts_topview = np.float32([[x_top1, y_top1], [x_top2, y_top2], [x_top3, y_top3], [x_top4, y_top4]])

# Matrizes de transformação para cada câmera
M1 = cv2.getPerspectiveTransform(pts_camera1, pts_topview)
M2 = cv2.getPerspectiveTransform(pts_camera2, pts_topview)
M3 = cv2.getPerspectiveTransform(pts_camera3, pts_topview)
M4 = cv2.getPerspectiveTransform(pts_camera4, pts_topview)

# Defina as dimensões da imagem resultante da vista de cima
width = 800
height = 600

# Inicialize as capturas de vídeo para cada câmera
cap_camera1 = cv2.VideoCapture(0)
cap_camera2 = cv2.VideoCapture(1)
cap_camera3 = cv2.VideoCapture(2)
cap_camera4 = cv2.VideoCapture(3)


while True:
    ret1, frame1 = cap_camera1.read()
    ret2, frame2 = cap_camera2.read()
    ret3, frame3 = cap_camera3.read()
    ret4, frame4 = cap_camera4.read()

    if not (ret1 and ret2 and ret3 and ret4):
        break

    topview_camera1 = cv2.warpPerspective(frame1, M1, (width, height))
    topview_camera2 = cv2.warpPerspective(frame2, M2, (width, height))
    topview_camera3 = cv2.warpPerspective(frame3, M3, (width, height))
    topview_camera4 = cv2.warpPerspective(frame4, M4, (width, height))

    final_topview = cv2.add(topview_camera1, topview_camera2)
    final_topview = cv2.add(final_topview, topview_camera3)
    final_topview = cv2.add(final_topview, topview_camera4)

    cv2.imshow("Bird's Eye View", final_topview)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere os recursos e feche as janelas
cap_camera1.release()
cap_camera2.release()
cap_camera3.release()
cap_camera4.release()
cv2.destroyAllWindows()