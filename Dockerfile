# Python tabanlı bir resmi imajı kullanın
FROM python:3.8

# Çalışma dizinini ayarlayın
WORKDIR /app

# Bağımlılıkları kopyalayın ve yükleyin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyalayın
COPY . .

# Uygulamayı çalıştıracak komutu belirtin
CMD ["python", "./main.py"]
