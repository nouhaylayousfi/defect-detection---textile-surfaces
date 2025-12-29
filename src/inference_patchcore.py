from anomalib.models import Patchcore
import cv2
import torch

# Chemin vers ton checkpoint
CKPT_PATH = "../notebooks/results/Patchcore/textile_anomaly_model2/latest/weights/lightning/model.ckpt"

# Chargement du modèle avec l'argument obligatoire input_size
model = Patchcore.load_from_checkpoint(
    CKPT_PATH,
    input_size=(256, 256),   # <-- Obligatoire ici (taille utilisée à l'entraînement)
    backbone="resnet18",    
    layers=["layer2", "layer3"],       
    num_neighbors=3,
    coreset_sampling_ratio=0.01,
    strict=False 
)

model.eval()
model.freeze()  # Important pour PatchCore

# Device
device = torch.device("cpu")  # ou "cuda" si tu as un GPU
model.to(device)

def predict_defect(image_path: str, threshold: float = 60):
    """
    Retourne : ("OK" ou "KO", score, heatmap_numpy)
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de lire l'image : {image_path}")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (256, 256))
    
    # Conversion en tensor + normalisation ImageNet
    tensor = torch.from_numpy(image_resized).float().permute(2, 0, 1) / 255.0
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    tensor = (tensor - mean) / std
    tensor = tensor.unsqueeze(0).to(device)  # batch

    # Inférence
    with torch.no_grad():
        output = model(tensor)

    # PatchCore retourne généralement un dict
    if isinstance(output, dict):
        score = float(output["pred_score"])
        heatmap = output["anomaly_map"].cpu().numpy().squeeze()
    else:
        # Parfois tuple (anomaly_map, pred_score)
        heatmap = output[0].cpu().numpy().squeeze()
        score = float(output[1])

    status = "KO" if score > threshold else "OK"

    return status, score, heatmap