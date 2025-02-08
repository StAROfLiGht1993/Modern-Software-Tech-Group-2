import torch
import torch.nn as nn
from torchvision import transforms, models
import pytesseract
import requests
import cv2
from PIL import Image
import os
from torchvision.models import ResNet18_Weights

# ✅ Define API Key for Pokémon TCG API
API_KEY = "67652158-5942-474b-bcef-653249bba035"
BASE_URL = "https://api.pokemontcg.io/v2/cards"

# ✅ Set Up Path to Tesseract (Ensure This is Correct on Your Machine)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Load CNN Model for Real vs. Fake Classification
class PokemonCardClassifier(nn.Module):
    def __init__(self):
        super(PokemonCardClassifier, self).__init__()
        self.model = models.resnet18(weights=ResNet18_Weights.DEFAULT)
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)  # 2 classes (Real, Fake)

    def forward(self, x):
        return self.model(x)

# ✅ Load the Pretrained Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PokemonCardClassifier().to(device)
model.load_state_dict(torch.load("pokemon_card_classifier.pth", map_location=device))
model.eval()

# ✅ Define Image Preprocessing for CNN
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# ✅ Function to Preprocess Image for OCR
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # Resize for better OCR
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # Improve contrast
    return img

# ✅ Function to Extract Text from Pokémon Card (OCR)
def extract_text(image_path):
    img = preprocess_image(image_path)
    extracted_text = pytesseract.image_to_string(img, config="--psm 6")  # OCR
    extracted_text = extracted_text.replace("\n", " ").strip()
    print(f"🔍 Extracted Text: {extracted_text}")
    return extracted_text

# ✅ Function to Validate Pokémon Name via API
def validate_pokemon_card(pokemon_name):
    params = {"q": f'name:"{pokemon_name}"'}
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        cards = response.json()["data"]
        return len(cards) > 0  # Return True if the card exists in database
    return False

# ✅ Function to Predict Image Authenticity (Real or Fake)
def predict_card(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    return "Real Pokémon Card" if predicted.item() == 0 else "Fake Pokémon Card"

# ✅ Main Function to Authenticate Pokémon Cards
def authenticate_card(image_path):
    extracted_text = extract_text(image_path)  # Step 1: Extract OCR text
    pokemon_name = extracted_text.split()[0]  # Assume first word is Pokémon name
    
    valid = validate_pokemon_card(pokemon_name)  # Step 2: Check if name is valid in API
    image_result = predict_card(image_path)  # Step 3: Run CNN model

    # ✅ Final Decision
    if valid and image_result == "Real Pokémon Card":
        return {"result": "Authentic", "pokemon_name": pokemon_name}
    else:
        return {"result": "Fake", "pokemon_name": pokemon_name}
