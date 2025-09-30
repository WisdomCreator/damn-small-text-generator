# Damn Small Text Generator (dstg)

`dstg` provides a clean REST API to use LLMs with async task processing. It perfect for **chatbots**, **content generation services**, **AI assistants** and many other use cases.

## ⭐ Features

- **Lightweight API** - built with FastAPI
- **Dynamic model managment** - load/unload models at runtime
- **Task queue with Celery** - non-blocking generation
- **Database integration** - stores prompts, outputs and metadata for later use

## ⚒️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/WisdomCreator/damn-small-text-generator.git
cd damn-small-text-generator
```

### 2. Install dependences
Before building and runnig the project, make sure you have:
- **[Docker](https://docs.docker.com/get-started/get-docker)** & **[Docker compose](https://docs.docker.com/compose)**
- **[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)**

Then build the images:
```bash
docker compose build
```

### 3. Configure environment
Copy the example environment file and rename it to `.env`:
```
cp .env.example .env
```
Then open `.env` in your editor and adjust the values.

### 4. Start Docker
```bash
docker compose up -d
```
Check logs:
```bash
docker compose logs -f
```
Open the API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📖 API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/text-generations` | Create a new text generation task |
| `GET`  | `/v1/text-generations/{gen_id}` | Get generation status and result |
| `GET` | `/v1/models` | List all available models |
| `GET` | `/v1/models/{model_name}` | Get model status |
| `POST` | `/v1/loaded-models/{model_name}` | Load a model into memory (requires `provider_type` parameter; currently only `torch` is supported) |
| `DELETE` | `/v1/loaded-models/{model_name}` | Unload a specific model |
| `DELETE` | `/v1/loaded-models` | Unload all models |

## 🖥️ Example request
Create a new generation task:
```bash
curl -X POST "http://localhost:8000/v1/text-generations/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Example prompt",
    "model_name": "Qwen3-0.6B",
    "max_new_tokens": 100,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.0,
    "do_sample": true
  }'
```
Response:
```json
{
  "generation_id": 50
}
```

## 📩 Download models
`dstg` expects models to be stored inside the `./models/` directory.
### 1. Install Git LFS (if not installed)
```bash
git lfs install
```

### 2. Clone a model from Hugging Face
```bash
cd models/
git clone https://huggingface.co/Qwen/Qwen3-8B
```
You can clone any other model that is supported by the `transformers` library.  
Make sure that the folder name matches the `model_name` you plan to use in API requests.
