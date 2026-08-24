# Cattle and Buffalo Breed Classification

The FastAPI backend serves the existing trained PyTorch checkpoint for inference only. Training code remains isolated in `DL/`.

## Configuration

Copy `.env.example` to `.env`, retain the Supabase values already used by the project, and set `MODEL_PATH` if the checkpoint is stored elsewhere. The repository defaults to the existing `DL/models/cattle_breed_model.pth` checkpoint.

## Run the backend

```powershell
cd cattle-buffalo-breed-classification
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`. `GET /api/v1/health` reports database and model readiness. Submit a JPEG or PNG as multipart field `image` to `POST /api/v1/predict`.

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/v1/predict -F "image=@path\to\animal.jpg"
```

## Run the frontend

```powershell
cd cattle-buffalo-breed-classification\frontend
npm run dev
```

The frontend calls `http://127.0.0.1:8000/api/v1/predict` by default. Set `VITE_API_BASE_URL` to change it.
