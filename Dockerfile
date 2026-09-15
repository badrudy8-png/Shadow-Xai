FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

ENV SHADOW_MODEL_PROVIDER=echo
EXPOSE 8080
CMD ["shadow-xai", "serve", "--host", "0.0.0.0", "--port", "8080"]
