# Dockerized Sample Web App

A small Flask web app packaged with a `Dockerfile` and `docker-compose.yml`. Runs with **one command**.
No secrets in this repo; the only settings are non-secret environment variables.

## Prerequisites
Docker Engine 24+ with the Compose plugin (`docker compose version` should work). Use your own machine or VM only.

## Run (one command)
```bash
docker compose up -d --build
```
Open http://localhost:8000. Check it:
```bash
curl http://localhost:8000/health      # {"status":"ok"}
curl http://localhost:8000/api/info    # JSON with container hostname, env, uptime
docker compose ps                      # STATUS should become "healthy"
```
Stop and remove: `docker compose down`

## Endpoints
| Path | Returns |
|------|---------|
| `/` | HTML status page (container hostname, environment, Python version, uptime) |
| `/health` | `{"status":"ok"}` used by the container healthcheck |
| `/api/info` | Same details as JSON |

## Configuration
Copy `.env.example` to `.env` (git-ignored) to change defaults:

| Variable | Default | Meaning |
|----------|---------|---------|
| `HOST_PORT` | `8000` | Port on your machine |
| `APP_NAME` | `TechAbout Docker Demo` | Title shown on the page |
| `APP_ENV` | `development` | Environment label |

Example: `HOST_PORT=9090 docker compose up -d --build` then open http://localhost:9090.

## What the Dockerfile does
- Base `python:3.12-slim` (small image).
- Copies `requirements.txt` first and installs it, so the dependency layer is cached between code changes.
- Runs as a **non-root** user (`appuser`).
- Serves with **gunicorn** (2 workers), not the Flask dev server.
- `HEALTHCHECK` calls `/health` using Python's standard library (no curl needed).

## What docker-compose.yml does
One service, `web`: builds the image, maps `HOST_PORT:8000`, passes the env variables, restarts unless stopped.

## Runbook
| Task | Command |
|------|---------|
| Start | `docker compose up -d --build` |
| Status / health | `docker compose ps` |
| Logs (follow) | `docker compose logs -f web` |
| Shell inside | `docker compose exec web sh` |
| Rebuild after code change | `docker compose up -d --build` |
| Stop and remove | `docker compose down` |

## Troubleshooting
| Symptom | Fix |
|---------|-----|
| `port is already allocated` | Port 8000 is taken. Use `HOST_PORT=9090 docker compose up -d --build` |
| `permission denied` on the Docker socket (Linux) | `sudo usermod -aG docker $USER`, then log out and in |
| Status stays `starting` or `unhealthy` | `docker compose logs web` and look for a Python error |
| Old page after editing code | Rebuild: `docker compose up -d --build` |

## Files
```
app/app.py            Flask app
requirements.txt      pinned dependencies
Dockerfile            image definition
docker-compose.yml    one-command run
.env.example          non-secret settings
.dockerignore         keeps junk out of the image
screenshots/          proof (add your own Docker screenshots here)
```
