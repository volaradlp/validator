FROM python:3.12-slim

# Install any Python dependencies your application needs, e.g.:
# RUN pip install --no-cache-dir cryptography

RUN mkdir /sealed && chmod 777 /sealed

WORKDIR /app

COPY . /app

CMD ["python", "-m", "my_proof"]