import cv2

def capture_image(save_path="captured.jpg"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Impossible d'ouvrir la caméra")

    print("Appuie sur 'c' pour capturer, 'q' pour quitter")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera - Appuie 'c' pour capturer", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cv2.imwrite(save_path, frame)
            print(f"Image capturée et sauvegardée : {save_path}")
            break
        elif key == ord('q'):
            print("Capture annulée")
            save_path = None
            break

    cap.release()
    cv2.destroyAllWindows()
    return save_path