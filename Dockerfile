FROM python:3.12-slim
WORKDIR /app

COPY . .
COPY wait-for-it.sh /wait-for-it.sh

RUN chmod +x /wait-for-it.sh
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["python", "main.py"]