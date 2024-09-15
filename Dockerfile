FROM python:3.12-alpine
WORKDIR /app
COPY . .
WORKDIR /app/src
CMD ["python", "main.py"]
EXPOSE 5000/udp
