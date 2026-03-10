# Deploying AITA 3201 on Fly.io

## Prerequisites

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login
```

## First-Time Setup

```bash
# 1. Create the app (run from AITA_3201 directory)
fly apps create aita-3201

# 2. Create persistent volume in Chicago region (1 GB is plenty)
fly volumes create aita_data --region ord --size 1

# 3. Set secrets (env vars — never stored in fly.toml)
fly secrets set \
  OPENAI_API_KEY="sk-..." \
  ADMIN_PASSWORD="..." \
  GOOGLE_COOKIE_KEY="..." \
  GOOGLE_REDIRECT_URI="https://aita-3201.fly.dev"

# 4. Update Google OAuth console
#    Add https://aita-3201.fly.dev to authorized redirect URIs
#    in Google Cloud Console > APIs & Services > Credentials

# 5. Build the aita-core wheel and copy it here
cd ../aita-core
python -m build --wheel
cp dist/aita_core-*.whl ../AITA_3201/
cd ../AITA_3201

# 6. Deploy
fly deploy
```

## Updating

```bash
# Rebuild wheel if aita-core changed
cd ../aita-core
python -m build --wheel
cp dist/aita_core-*.whl ../AITA_3201/
cd ../AITA_3201

# Deploy
fly deploy
```

## Re-ingesting Documents

Run ingestion locally, then copy the updated index:

```bash
# Local ingestion
python add_document.py

# Copy to Fly volume via SSH
fly ssh console -C "rm /app/faiss_db/index.faiss /app/faiss_db/metadata.pkl"
fly sftp shell
put faiss_db/index.faiss /app/faiss_db/index.faiss
put faiss_db/metadata.pkl /app/faiss_db/metadata.pkl
```

Or just redeploy (the index is baked into the Docker image):
```bash
fly deploy
```

## Useful Commands

```bash
fly status              # Check app status
fly logs                # Stream logs
fly ssh console         # SSH into the machine
fly volumes list        # Check volumes
fly scale show          # Check VM size
fly scale memory 2048   # Increase memory if needed
```

## Architecture Notes

- **VM**: shared-cpu-1x, 1 GB RAM (sufficient for 66 students)
- **Volume**: 1 GB at `/app/data` for SQLite DB + config overrides
- **Region**: ord (Chicago) for low latency to UMN
- **Auto-stop**: Machine stops after idle period, starts on first request (~2-3s cold start)
- **FAISS index**: Baked into Docker image (rebuilt on each deploy)
- **TLS**: Handled by Fly's edge proxy (app serves HTTP on port 8501)
- Set `min_machines_running = 1` in fly.toml to avoid cold starts (costs ~$3-5/month)

## Cost Estimate

- shared-cpu-1x, 1 GB RAM: ~$5-7/month (with auto-stop)
- 1 GB volume: $0.15/month
- Outbound bandwidth: included (first 100 GB free)
- **Total: ~$5-7/month**
