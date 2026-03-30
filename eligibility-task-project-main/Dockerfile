FROM python:3.11-slim

# Set environment variables to suppress debconf warnings
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm
ENV DEBCONF_NONINTERACTIVE_SEEN=true

WORKDIR /app

# Install system dependencies without interactive prompts
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Reset DEBIAN_FRONTEND
ENV DEBIAN_FRONTEND=

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
