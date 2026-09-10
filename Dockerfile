FROM python:3.12-slim

WORKDIR /app

# Create the output directory inside the image
RUN mkdir -p output

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY validation/ ./validation/
COPY data/ ./data/

CMD ["python", "validation/validate.py"]