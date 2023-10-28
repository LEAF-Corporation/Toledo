import cv2
import numpy as np

def main():
    # Inicializa o VideoCapture
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        exit(0)

    # Cria a janela de controles
    cv2.namedWindow("Controles")

    # Cria as trackbars
    cv2.createTrackbar("x", "Controles", 0, frame.shape[0], lambda x: None)
    cv2.createTrackbar("y", "Controles", 0, frame.shape[1], lambda x: None)

    # Inicializa a linha
    start_point = (0, 0)
    end_point = (frame.shape[0], frame.shape[1])
    color = (255, 0, 0)
    line_thickness = 2

    # Inicializa o estado da linha
    is_dragging = False
    drag_start_point = None

    while True:
        # Captura um novo frame
        ret, frame = cap.read()

        # Desenha a linha
        if is_dragging:
            cv2.line(frame, drag_start_point, (cv2.getTrackbarPos("x", "Controles"), cv2.getTrackbarPos("y", "Controles")), color, line_thickness)
        else:
            cv2.line(frame, start_point, end_point, color, line_thickness)

        # Exibe o frame
        cv2.imshow("Frame", frame)

        # Processa os eventos
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # Verifica se o usuário está clicando para iniciar o arrastamento
        if key == ord("m"):
            if is_dragging:
                is_dragging = False
            else:
                is_dragging = True
                drag_start_point = cv2.getTrackbarPos("x", "Controles"), cv2.getTrackbarPos("y", "Controles")

        # Atualiza as posições da linha
        if is_dragging:
            start_point = (cv2.getTrackbarPos("x", "Controles"), cv2.getTrackbarPos("y", "Controles"))
            end_point = (cv2.getTrackbarPos("x", "Controles"), cv2.getTrackbarPos("y", "Controles"))

    # Libera o VideoCapture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
