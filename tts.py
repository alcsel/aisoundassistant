import torch
import torchaudio
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import soundfile as sf

# Model bileşenlerini yükle
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# Cihaz belirleme
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
vocoder = vocoder.to(device)

# Speaker embedding yükle (zorunlu)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[0]["xvector"]).unsqueeze(0).to(device)  # Cihaza taşı

# Metni oku (cevap.txt)
with open("cevap.txt", "r", encoding="utf-8") as f:
    text = f.read().strip()

# İşleme ve ses üretimi
inputs = processor(text=text, return_tensors="pt").to(device)
speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

# WAV dosyasına yaz
sf.write("english_output.wav", speech.cpu().numpy(), samplerate=16000)

print("İngilizce ses başarıyla 'english_output.wav' olarak kaydedildi.")
