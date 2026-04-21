# Usamos a imagem oficial do Node.js (LTS)
FROM node:20-slim

# Define a pasta de trabalho
WORKDIR /app

# Copia apenas os arquivos de dependências primeiro (otimiza o cache do Docker)
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código
COPY . .

# Expõe a porta padrão do Vite
EXPOSE 5173

# Comando para rodar o Vite com acesso externo (--host)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]