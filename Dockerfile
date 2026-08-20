FROM python:3.10-slim

ENV TERRAFORM_VERSION=1.15.8

# Terraform CLI so the /generate validation loop runs real `terraform validate`
# instead of the heuristic fallback. ca-certificates stays: terraform init needs TLS.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl unzip ca-certificates \
    && ARCH="$(dpkg --print-architecture)" \
    && curl -fsSL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip" -o /tmp/terraform.zip \
    && unzip /tmp/terraform.zip -d /usr/local/bin \
    && rm /tmp/terraform.zip \
    && apt-get purge -y curl unzip \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY static/ static/

# main.py writes terraform_output/main.tf and assumes the dir exists
RUN mkdir -p terraform_output

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
