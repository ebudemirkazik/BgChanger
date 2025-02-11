# Python resmi imajını temel al
FROM python:3.8-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Uygulama bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Gerekli klasörleri oluştur
RUN mkdir -p static/images/uploads static/images/results

# Port ayarı
EXPOSE 5000

# Çalıştırma komutu
CMD ["python", "app.py"] 