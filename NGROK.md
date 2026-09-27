## Remote demos with ngrok

EarthLens includes an optional ngrok Docker profile for sharing the app during judging or a remote demo. It creates two tunnels: one for the Vite frontend and one for the FastAPI API.

### Requirements

- Docker Desktop with Compose
- An ngrok account and authentication token
- The repository checked out locally

### Start the tunnels

```bash
cp .env.example .env
# Edit .env and set NGROK_AUTHTOKEN
./start-ngrok.sh
```

Windows:

```bat
copy .env.example .env
REM Edit .env and set NGROK_AUTHTOKEN
start-ngrok.bat
```

The ngrok inspection dashboard is available at `http://localhost:4040`. It shows the generated public URLs for both tunnels. Open the frontend URL to view the app and use the backend URL to inspect the API at `/docs`.

### Important Vite limitation

Vite injects `VITE_API_URL` when the frontend bundle is built. The default Docker demo uses `http://localhost:8000`, which is correct for local use but not for a remote viewer. For a fully remote demo:

1. Start the stack once and copy the public backend URL from `http://localhost:4040`.
2. Set `VITE_API_URL` in `.env` to that backend URL, without a trailing slash.
3. Rebuild the frontend: `docker compose --profile tunnel build frontend`.
4. Restart the stack: `docker compose --profile tunnel up`.
5. Open the public frontend tunnel URL.

The frontend and backend URLs can change when ngrok restarts unless you configure reserved domains. Never commit `.env` or an ngrok token.

### Security note

The development CORS configuration permits wildcard origins to make ephemeral ngrok demos easier. For staging or production, set `EARTHLENS_ENV=production` and explicitly set `EARTHLENS_ALLOWED_ORIGINS` to the exact frontend origin.
