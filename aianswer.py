import requests

API_TOKEN = "api_keyiniz"  # Hugging Face API anahtarını buraya yaz
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def ask_question(question):
    prompt = f"<|system|>Sen kibar ve Türkçe cevaplar veren bir asistansın.<|user|>{question}<|assistant|>"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data[0]["generated_text"].split("<|assistant|>")[-1].strip()
    else:
        return f"[API Hatası: {response.status_code} - {response.text}]"

# Soruları oku
with open("kayit_metni.txt", "r", encoding="utf-8") as f:
    questions = [line.strip() for line in f if line.strip()]

# Sadece cevapları yaz
with open("cevap.txt", "w", encoding="utf-8") as f:
    for q in questions:
        answer = ask_question(q)
        f.write(f"{answer}\n\n")

print("Yalnızca cevaplar cevap.txt dosyasına yazıldı.")
