# Self-Hosting asciinema-server

Guide for deploying and operating a private, on-premises or cloud instance of `asciinema-server`.

## Architecture & Requirements

- **Application Stack**: Elixir / Phoenix framework with WebAssembly terminal playback.
- **Image**: `ghcr.io/asciinema/asciinema-server:latest`.
- **Database**: PostgreSQL 14.0 or newer.
- **Storage**: Local filesystem volume or AWS S3 / MinIO / GCS object storage.
- **Email**: SMTP relay for magic login links (optional for initial admin setup).
- **Compute**: Minimum 512 MB RAM (1 GB recommended).

---

## Docker Compose Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: asciinema
      POSTGRES_PASSWORD: asciinema_db_password
      POSTGRES_DB: asciinema_prod
    volumes:
      - pgdata:/var/lib/postgresql/data

  asciinema:
    image: ghcr.io/asciinema/asciinema-server:latest
    restart: always
    depends_on:
      - postgres
    ports:
      - "4000:4000"
    environment:
      # Generate with: openssl rand -hex 32
      SECRET_KEY_BASE: "78cf196238b97587bcba29381640a92cd86b240182470984cfb7eef2009234ae"
      DATABASE_URL: "ecto://asciinema:asciinema_db_password@postgres:5432/asciinema_prod"
      SERVER_URL: "https://asciinema.corp.internal"
      SERVER_NAME: "Internal asciinema"
      
      # Admin & Access Control
      ADMIN_PANEL_ON_MAIN_ENDPOINT: "1"
      SIGN_UP_DISABLED: "false" # Set to "true" after creating the initial admin account
      
      # SMTP Configuration for magic login links
      SMTP_HOST: "smtp.mailgun.org"
      SMTP_PORT: "587"
      SMTP_USERNAME: "postmaster@mail.corp.internal"
      SMTP_PASSWORD: "smtp_secret_password"
      SMTP_FROM_ADDRESS: "asciinema@corp.internal"
      
      # Optional: S3 Object Storage for .cast assets
      # FS_STORE: "s3"
      # S3_BUCKET: "internal-asciinema-casts"
      # S3_REGION: "us-east-1"
      # S3_AWS_ACCESS_KEY_ID: "..."
      # S3_AWS_SECRET_ACCESS_KEY: "..."
    volumes:
      - uploads:/opt/app/uploads

volumes:
  pgdata:
  uploads:
```

---

## Administration & Bootstrap Workflow

1. **Launch Containers**:
   ```bash
   docker compose up -d
   ```
   *The container automatically runs Ecto database migrations on startup.*

2. **Bootstrap the First Admin Account**:
   Open `https://asciinema.corp.internal` in your browser and register. The first registered account automatically receives administrator privileges.

3. **Lock Down Signups**:
   Once initial users/admins have registered, edit `docker-compose.yml` to set:
   ```yaml
   SIGN_UP_DISABLED: "true"
   ```
   Apply changes with `docker compose up -d`.

---

## Client CLI Configuration

To direct terminal recordings and uploads to your private instance:

### Option A: Environment Variable
```bash
export ASCIINEMA_SERVER_URL="https://asciinema.corp.internal"
```

### Option B: Global Configuration File (`~/.config/asciinema/config.toml`)
```toml
[api]
server_url = "https://asciinema.corp.internal"
```

### Authenticate Client Installation
```bash
asciinema auth
```
The CLI outputs an authentication link:
`https://asciinema.corp.internal/connect/<uuid>`

Visiting the link in your browser associates all future uploads from that machine with your private user account.
