# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for MVP. All endpoints are public.

## Endpoints

### 1. Generate Documentation

Generate multi-level documentation for a GitHub repository.

**Endpoint:** `POST /api/v1/generate`

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repository"
}
```

**Response (Success):**
```json
{
  "success": true,
  "repo_name": "repository",
  "documentation": {
    "beginner": "# Beginner Documentation\n\n...",
    "intermediate": "# Intermediate Documentation\n\n...",
    "advanced": "# Advanced Documentation\n\n..."
  },
  "metadata": {
    "analysis": {
      "statistics": {
        "total_files": 42,
        "estimated_lines": 5000,
        "languages": {
          "py": 30,
          "js": 10,
          "md": 2
        },
        "primary_language": "Python"
      },
      "structure": {
        "has_tests": true,
        "has_documentation": false,
        "has_config_files": true,
        "detected_framework": "Python",
        "project_type": "Application"
      },
      "complexity": {
        "complexity_analysis": "..."
      },
      "key_insights": [
        "Small project - documentation can cover all components in detail",
        "Framework detected: Python - leverage framework conventions"
      ]
    },
    "rate_limit_remaining": 4998
  }
}
```

**Response (Error):**
```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200 OK` - Documentation generated successfully
- `400 Bad Request` - Invalid GitHub URL
- `500 Internal Server Error` - Server error during generation

**Example Usage:**

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/expressjs/express"}'
```

```javascript
// JavaScript/Frontend
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    repo_url: 'https://github.com/expressjs/express'
  }),
});

const data = await response.json();
console.log(data.documentation.beginner);
```

```python
# Python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/generate',
    json={'repo_url': 'https://github.com/expressjs/express'}
)

data = response.json()
print(data['documentation']['beginner'])
```

### 2. Health Check

Check if the API is running.

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "smart-docs-agent"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

**Example Usage:**

```bash
curl http://localhost:8000/api/v1/health
```

### 3. Root Endpoint

Get API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Smart Documentation Agent API",
  "docs_url": "/docs",
  "health_check": "/api/v1/health"
}
```

**Status Codes:**
- `200 OK` - Always successful

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test endpoints directly in the browser
- Download OpenAPI specification

## Rate Limits

### GitHub API Limits
- **Without authentication:** 60 requests/hour
- **With authentication:** 5000 requests/hour

The API response includes `rate_limit_remaining` in metadata.

### Server Limits
- **MVP:** No rate limiting implemented
- **Production:** Consider implementing rate limiting per IP

## Error Responses

All errors follow this structure:

```json
{
  "detail": "Error description"
}
```

### Common Errors

**Invalid GitHub URL**
```json
{
  "detail": "Invalid GitHub URL"
}
```

**GitHub API Rate Limit**
```json
{
  "detail": "GitHub API rate limit exceeded. Please try again later or add a GitHub token."
}
```

**Repository Not Found**
```json
{
  "detail": "404 {\"message\": \"Not Found\", ...}"
}
```

**Gemini API Error**
```json
{
  "detail": "Error generating documentation: ..."
}
```

## Request/Response Models

### DocumentationRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| repo_url | string | Yes | GitHub repository URL |

**Validation Rules:**
- Must start with `https://github.com/`
- Must match pattern: `https://github.com/{owner}/{repo}`

### DocumentationResponse

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether generation succeeded |
| repo_name | string | Repository name |
| documentation | object | Contains beginner, intermediate, advanced docs |
| metadata | object | Analysis results and rate limit info |

## CORS Configuration

The API allows requests from:
- `http://localhost:5173` (default Vite dev server)
- Configurable via `FRONTEND_URL` environment variable

All HTTP methods and headers are allowed for development.

## Performance Considerations

### Typical Response Times
- Small repos (< 50 files): 20-40 seconds
- Medium repos (50-200 files): 40-70 seconds
- Large repos (200+ files): 60-90 seconds

### Factors Affecting Performance
1. **Repository Size:** More files = longer processing
2. **GitHub API:** Network latency and rate limits
3. **LLM Generation:** 3 levels generated in parallel
4. **README Length:** Longer READMEs take more time to analyze

### Optimization Tips
1. **Use GitHub Token:** Increases rate limit
2. **Cache Results:** Implement caching for repeated requests
3. **Queue System:** Process requests in background

## Versioning

Current API version: `v1`

All endpoints are prefixed with `/api/v1/`.

Future versions will use `/api/v2/`, etc., allowing backwards compatibility.

## Testing

### Manual Testing

Use the Swagger UI at http://localhost:8000/docs to test endpoints interactively.

### Automated Testing

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_documentation():
    response = client.post(
        "/api/v1/generate",
        json={"repo_url": "https://github.com/expressjs/express"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "beginner" in data["documentation"]
```

## Security

### Input Validation
- GitHub URLs are validated before processing
- Invalid URLs return 400 Bad Request

### API Keys
- Never expose `GEMINI_API_KEY` in responses
- Store in environment variables only

### CORS
- Production should restrict CORS origins
- Development allows localhost only

## Future Enhancements

1. **Authentication:** Add API key authentication
2. **Rate Limiting:** Implement per-user rate limits
3. **Webhooks:** Notify when generation completes
4. **Streaming:** Stream documentation as it's generated
5. **Caching:** Cache results for popular repositories
6. **Batch Processing:** Generate docs for multiple repos
