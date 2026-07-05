# Deploy DocStruct (2 minutes)

## Option A — Streamlit Cloud (recommended, free)

1. Push this folder to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. **New app** → select repo → main file: `app.py`
4. Deploy. Demo login: `demo` / `demo123`

Optional: add `GEMINI_API_KEY` in **App settings → Secrets**.

## Option B — Render (free tier)

1. Push to GitHub
2. [render.com](https://render.com) → **New → Blueprint**
3. Connect repo — `render.yaml` is included
4. Deploy

## Option C — Instant public link (tunnel)

While running locally:

```bash
npx localtunnel --port 8501
```

Share the `https://....loca.lt` URL (adds a quick tunnel to your local app).