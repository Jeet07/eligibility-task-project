FROM python:3.11-slim


ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm
ENV DEBCONF_NONINTERACTIVE_SEEN=true

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean


ENV DEBIAN_FRONTEND=


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
