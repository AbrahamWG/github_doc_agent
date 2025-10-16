# Common Pitfalls and Solutions

This document covers common issues you might encounter and how to solve them.

## GitHub API Issues

### Pitfall 1: Rate Limit Exceeded

**Problem:**
```
GitHub API rate limit exceeded. Please try again later or add a GitHub token.
```

**Why It Happens:**
- Without authentication: 60 requests/hour
- Each repo analysis uses 5-15 requests
- You can only analyze ~4-12 repos per hour

**Solution:**
1. Add a GitHub Personal Access Token to `.env`:
   ```env
   GITHUB_TOKEN=ghp_your_token_here
   ```
2. Generate token at: https://github.com/settings/tokens
3. Required scopes: None for public repos, `repo` for private repos
4. With token: 5000 requests/hour

### Pitfall 2: Repository Not Found

**Problem:**
```
404 {"message": "Not Found"}
```

**Why It Happens:**
- Repository doesn't exist
- Repository is private and you don't have access
- Typo in URL

**Solution:**
1. Verify the repository exists by visiting the URL in your browser
2. For private repos, add a GitHub token with `repo` scope
3. Double-check the URL format: `https://github.com/owner/repo`

### Pitfall 3: Large Repository Timeout

**Problem:**
Request takes >2 minutes and times out.

**Why It Happens:**
- Repository has thousands of files
- GitHub API is slow
- LLM generation is taking too long

**Solution:**
1. The system limits depth to 3 levels (prevents full traversal)
2. For production, implement:
   - Background job queue
   - Streaming responses
   - Result caching

## Gemini API Issues

### Pitfall 4: Invalid API Key

**Problem:**
```
google.api_core.exceptions.PermissionDenied: 400 API key not valid
```

**Why It Happens:**
- `GEMINI_API_KEY` is missing or incorrect
- API key was revoked
- API key has no quota remaining

**Solution:**
1. Verify your key at https://aistudio.google.com/apikey
2. Generate a new key if needed
3. Update `.env` file:
   ```env
   GEMINI_API_KEY=your_new_key_here
   ```
4. Restart the backend server

### Pitfall 5: Quota Exceeded

**Problem:**
```
Resource has been exhausted (e.g. check quota)
```

**Why It Happens:**
- Free tier has daily limits
- Too many requests in short time

**Solution:**
1. Wait 24 hours for quota reset
2. Implement caching to reduce API calls
3. For production, upgrade to paid tier

### Pitfall 6: Token Limit Exceeded

**Problem:**
```
Request payload size exceeds the limit
```

**Why It Happens:**
- Sending too much code to Gemini
- README is extremely long

**Solution:**
Already handled in code:
```python
# Truncate to avoid token limits
truncated_readme = readme_content[:3000]
```

If still occurring, reduce truncation limit further.

## Backend Issues

### Pitfall 7: Module Import Errors

**Problem:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Why It Happens:**
- Virtual environment not activated
- Dependencies not installed

**Solution:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Pitfall 8: Port Already in Use

**Problem:**
```
ERROR: [Errno 48] Address already in use
```

**Why It Happens:**
- Another process is using port 8000
- Previous backend instance didn't shut down

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use a different port
uvicorn app.main:app --port 8001
```

### Pitfall 9: CORS Errors

**Problem:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:5173'
has been blocked by CORS policy
```

**Why It Happens:**
- CORS middleware not configured
- Frontend URL not in allowed origins

**Solution:**
Already configured in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    ...
)
```

If using different port, update `FRONTEND_URL` in `.env`.

## Frontend Issues

### Pitfall 10: npm Install Fails

**Problem:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Why It Happens:**
- Dependency version conflicts
- Old npm/Node version
- Corrupted cache

**Solution:**
```bash
# Update Node.js to v18+
node --version

# Clear npm cache
npm cache clean --force

# Delete and reinstall
rm -rf node_modules package-lock.json
npm install

# Or use --legacy-peer-deps
npm install --legacy-peer-deps
```

### Pitfall 11: Vite Build Errors

**Problem:**
```
Failed to resolve import "react"
```

**Why It Happens:**
- Dependencies not installed
- Wrong Node version

**Solution:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Pitfall 12: Backend Not Reachable

**Problem:**
Red banner: "Backend is not reachable"

**Why It Happens:**
- Backend not running
- Backend on wrong port
- Network firewall

**Solution:**
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
2. Check backend logs for errors
3. Verify port in `vite.config.js` proxy matches backend

## Code Issues

### Pitfall 13: Documentation Quality Issues

**Problem:**
- All three levels sound similar
- Documentation is too generic
- Hallucinated features

**Why It Happens:**
- LLM prompt not specific enough
- Not enough context provided

**Solution:**
Adjust prompts in `doc_generator.py`:
- Make level differences more explicit
- Add `temperature=0.3` for consistency
- Include more analysis context

### Pitfall 14: Slow Performance

**Problem:**
Documentation takes >90 seconds to generate

**Why It Happens:**
- Large repository
- Sequential processing
- Network latency

**Solution:**
Already optimized:
- Parallel agent execution
- Depth-limited tree traversal
- File filtering

Further optimizations:
- Implement caching
- Use faster LLM model
- Background job processing

## Environment Issues

### Pitfall 15: .env Not Loaded

**Problem:**
```
ValidationError: GEMINI_API_KEY field required
```

**Why It Happens:**
- `.env` file not in correct location
- Virtual environment not activated
- Typo in variable name

**Solution:**
1. Verify `.env` location: `backend/.env`
2. Check file contents:
   ```bash
   cat backend/.env
   ```
3. Verify no spaces around `=`:
   ```env
   GEMINI_API_KEY=abc123  # Correct
   GEMINI_API_KEY = abc123  # Wrong!
   ```

### Pitfall 16: Python Version Issues

**Problem:**
```
SyntaxError: invalid syntax
```

**Why It Happens:**
- Python version < 3.11
- Using incompatible features

**Solution:**
```bash
python --version  # Should be 3.11+

# Use correct Python version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Testing Issues

### Pitfall 17: Tests Fail Locally

**Problem:**
```
pytest FAILED tests/test_agents.py
```

**Why It Happens:**
- Missing environment variables
- API keys not set in test environment

**Solution:**
Create `backend/.env.test`:
```env
GEMINI_API_KEY=test_key_here
GITHUB_TOKEN=test_token_here
```

Use in tests:
```python
from dotenv import load_dotenv
load_dotenv('.env.test')
```

## Deployment Issues

### Pitfall 18: Docker Build Fails

**Problem:**
```
ERROR [build 3/5] RUN pip install -r requirements.txt
```

**Why It Happens:**
- Missing dependencies in requirements.txt
- Wrong Python version in Dockerfile

**Solution:**
Ensure Dockerfile uses Python 3.11:
```dockerfile
FROM python:3.11-slim
```

### Pitfall 19: Environment Variables in Production

**Problem:**
Application works locally but fails in production

**Why It Happens:**
- `.env` file not deployed (correct behavior!)
- Environment variables not set in production

**Solution:**
Set environment variables in deployment platform:
- Cloud Run: Use Secret Manager
- Heroku: Use Config Vars
- Docker: Use `--env-file` or `-e` flags

## Best Practices to Avoid Issues

1. **Always use virtual environments**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Never commit `.env` files**
   - Use `.env.example` instead
   - Add `.env` to `.gitignore`

3. **Check logs first**
   - Backend: Terminal output
   - Frontend: Browser console
   - GitHub: Check repository is public

4. **Use health check endpoint**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

5. **Test with small repos first**
   - Start with repos < 50 files
   - Verify everything works
   - Then try larger repos

6. **Monitor rate limits**
   - Check `rate_limit_remaining` in response
   - Add GitHub token early
   - Implement caching

7. **Read error messages carefully**
   - Most errors are self-explanatory
   - Check the specific line number
   - Google the exact error message

## Getting Help

If you encounter an issue not listed here:

1. Check the GitHub Issues page
2. Read the full error stack trace
3. Verify your setup matches SETUP.md
4. Check API documentation
5. Enable debug logging:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

## Summary

Most issues fall into these categories:
- **API Keys:** Missing or invalid
- **Rate Limits:** Too many requests
- **Environment:** Wrong Python/Node version
- **Network:** Backend not reachable
- **Configuration:** .env file issues

Always start by:
1. Checking `.env` file
2. Verifying backend is running
3. Testing with a small, public repository
4. Reading the error message carefully
