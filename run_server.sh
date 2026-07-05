#!/bin/bash
# Run DocStruct for team access on your network (Cisco UCS / internal server)
# Team opens: http://<SERVER-IP>:8501

cd "$(dirname "$0")"

export PYTHONUNBUFFERED=1

python3 -m streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true \
  --browser.gatherUsageStats false