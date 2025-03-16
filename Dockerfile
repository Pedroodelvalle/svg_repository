# Usa a imagem oficial do Python 3.9
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do seu projeto para o contêiner
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080 para o Fly.io
EXPOSE 8080

# Comando para rodar a aplicação Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
