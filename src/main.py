from camera_capture import capture_image
from inference_patchcore import predict_defect
from thingsboard_client import send_telemetry
from send_to_arduino import send_to_arduino



IMAGE_PATH = "captured.jpg"

if __name__ == "__main__":
    print("=== Système de détection de défauts textiles ===\n")

    # 1. Capture d'image
    saved_path = capture_image(save_path=IMAGE_PATH)

    if saved_path is None:
        print("Aucune image capturée. Fin du programme.")
        exit()

    try:
        # 2. Prédiction avec le modèle PatchCore
        print("Analyse en cours...")
        status, score, heatmap = predict_defect(saved_path, threshold=18)

        print(f"Résultat : {status}")
        print(f"Score d'anomalie : {score:.4f}")

        # 3. Envoi à ThingsBoard + arduino
        send_telemetry(status, score)
        send_to_arduino(status) 

        # Optionnel : Afficher la heatmap
        import cv2
        heatmap_colored = cv2.applyColorMap((heatmap * 255).astype("uint8"), cv2.COLORMAP_JET)
        heatmap_resized = cv2.resize(heatmap_colored, (640, 480))
        cv2.imshow(f"Heatmap - {status}", heatmap_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Erreur : {e}")