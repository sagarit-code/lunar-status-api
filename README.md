🌙 Lunar Status API

A small FastAPI service that returns **live lunar status** based on the user’s IP.
Built for **SeismoTech** to show real-time reaction angle, direction, and moon horizon position.

### Endpoint

```
GET /lunar-status
```

### Run Locally

```
pip install -r requirements.txt
uvicorn api:app --reload
```

### Env Vars

```
OPENCAGE_KEY=your_key
IPGEO_KEY=your_key
```


