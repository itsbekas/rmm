# Microservices that make up the backend of the website

## Running

### Python Services

```sh
# Setup venv and install service
uv venv
source .venv/bin/activate
uv pip install .

# Initial setup:
rmm-setup-<service-name>
# Run the API:
rmm-api-<service-name>
# Run the task scheduler:
celery -A rmm.<service-name>.tasks worker --loglevel=info
celery -A rmm.<service-name>.tasks beat --loglevel=info
