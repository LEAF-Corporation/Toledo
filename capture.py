import cv2
import numpy as np

class BirdsEyeView:
    def __init__(self, camera_indices, pts_camera, pts_topview, width, height):
        self.camera_indices = camera_indices
        self.pts_camera = pts_camera
        self.pts_topview = pts_topview
        self.width = width
        self.height = height
        self.M_transforms = [cv2.getPerspectiveTransform(pts, self.pts_topview) for pts in pts_camera]
        self.captures = [cv2.VideoCapture(idx) for idx in camera_indices]

    def get_topview_images(self):
        topview_images = []
        for idx, cap in enumerate(self.captures):
            ret, frame = cap.read()
            if not ret:
                topview_images.append(None)
                continue
            topview_frame = cv2.warpPerspective(frame, self.M_transforms[idx], (self.width, self.height))
            topview_images.append(topview_frame)
        return topview_images
    
    def create_birdseye_view(self):
        while True:
            topview_images = self.get_topview_images()
            if all(image is None for image in topview_images):
                break

            final_topview = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for topview_frame in topview_images:
                if topview_frame is not None:
                    final_topview = cv2.add(final_topview, topview_frame)

            # Adicionar coordenadas dos vértices das câmeras
            for pts, idx in zip(self.pts_camera, self.camera_indices):
                for pt in pts:
                    pt_tuple = tuple(map(int, pt))  # Certifique-se de que as coordenadas são números inteiros
                    cv2.circle(final_topview, pt_tuple, 5, (0, 0, 255), -1)
                    cv2.putText(final_topview, f'({pt[0]:.1f}, {pt[1]:.1f})', pt_tuple,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Adicionar coordenadas dos vértices da vista de cima
            for pt_top in self.pts_topview:
                pt_top_tuple = tuple(map(int, pt_top))  # Certifique-se de que as coordenadas são números inteiros
                cv2.circle(final_topview, pt_top_tuple, 5, (0, 255, 0), -1)
                cv2.putText(final_topview, f'({pt_top[0]:.1f}, {pt_top[1]:.1f})', pt_top_tuple,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow('Bird\'s Eye View', final_topview)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release_resources()

    def release_resources(self):
        for cap in self.captures:
            cap.release()
        cv2.destroyAllWindows()
        
def main():
    camera_indices = [0, 1, 2, 3]  # Substitua pelos índices das câmeras
    pts_camera = [
        np.float32([[0, 600], [800, 600], [200, 450], [600, 450]]),
        np.float32([[0, 600], [200, 450], [0, 0], [200, 150]]),
        np.float32([[600, 450], [800, 600], [600, 150], [800, 0]]),
        np.float32([[200,150], [600, 150], [0, 0], [800, 0]])
    ]
    pts_topview = np.float32([
       [100, 75],  # Vértice superior esquerdo
       [700, 75],  # Vértice superior direito
       [700, 525],  # Vértice inferior direito
       [100, 525]   # Vértice inferior esquerdo
    ])
    
    width = 800
    height = 600

    bev = BirdsEyeView(camera_indices, pts_camera, pts_topview, width, height)
    bev.create_birdseye_view()

if __name__ == "__main__":
    main()