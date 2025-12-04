FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 9000
CMD ["python", "app.py", "--host=0.0.0.0", "--port=9000"]