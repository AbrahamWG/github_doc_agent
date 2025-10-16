# Getting Started with Smart Documentation Agent

This is a quick guide to get you up and running in 5 minutes.

## 🚀 Quick Setup (Automated)

**If you want automated setup, just run:**

```bash
./setup.sh
```

This script will:
- Create `.env` file from template
- Prompt for your API keys
- Install all dependencies (backend + frontend)
- Set everything up automatically

Then skip to "Step 5: Test It Out!" below.

---

## 📋 Manual Setup (Step-by-Step)

### Prerequisites Check

Before you begin, verify you have:

```bash
# Check Python version (need 3.11+)
python3 --version

# Check Node.js version (need 18+)
node --version

# Check npm
npm --version
```

If any are missing, install them first:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

### Step 1: Get Your API Key (2 minutes)

1. Open https://aistudio.google.com/apikey in your browser
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AI...`)

**Important:** Keep this key secret! Never commit it to Git.

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies (this may take 1-2 minutes)
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
# Use your favorite editor (nano, vim, vscode, etc.)
nano .env
```

In the `.env` file, replace `your_gemini_api_key_here` with your actual key:

```env
GEMINI_API_KEY=AIza...your_actual_key_here
GITHUB_TOKEN=
ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173
BACKEND_PORT=8000
```

Save and close.

## Step 3: Start Backend (30 seconds)

```bash
# Still in backend directory with venv activated
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend is now running.

## Step 4: Frontend Setup (2 minutes)

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (this may take 1-2 minutes)
npm install

# Start development server
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

## Step 5: Test It Out!

1. Open your browser to http://localhost:5173
2. You should see "Smart Documentation Generator"
3. Try one of the example repositories:
   - Click on `https://github.com/expressjs/express`
4. Click "Generate Documentation"
5. Wait 30-60 seconds
6. View the three levels of documentation!

## Troubleshooting Quick Fixes

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Error:** `ValidationError: GEMINI_API_KEY field required`

**Fix:**
- Check that `backend/.env` exists
- Verify the API key is correctly pasted (no extra spaces)
- Make sure the line is: `GEMINI_API_KEY=your_key` (no quotes)

### Frontend won't start

**Error:** `Cannot find module 'react'`

**Fix:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "Backend is not reachable" error

**Fix:**
1. Check backend terminal - is it still running?
2. Visit http://localhost:8000/api/v1/health in your browser
3. Should return: `{"status":"healthy","service":"smart-docs-agent"}`
4. If not, restart the backend

### "Rate limit exceeded" error

**Fix:**
- You've hit GitHub's 60 requests/hour limit
- Generate a GitHub token:
  1. Go to https://github.com/settings/tokens
  2. Click "Generate new token (classic)"
  3. Give it a name like "doc-agent"
  4. No scopes needed for public repos
  5. Click "Generate token"
  6. Copy the token
  7. Add to `backend/.env`:
     ```env
     GITHUB_TOKEN=ghp_your_token_here
     ```
  8. Restart backend

## Next Steps

Once everything is working:

1. **Read the architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. **Explore the API:** http://localhost:8000/docs
3. **Try different repos:** Experiment with various projects
4. **Customize prompts:** Edit `backend/app/agents/doc_generator.py`
5. **Add features:** See README.md for enhancement ideas

## Using the Quick Start Script (Alternative)

If you're on macOS/Linux, you can use the convenience script:

```bash
# From project root
./start.sh
```

This will:
- Check for `.env` file
- Create virtual environment if needed
- Install dependencies
- Start both backend and frontend
- Show you the URLs

Press Ctrl+C to stop both services.

## Video Walkthrough

(If you create a video walkthrough, link it here)

## Common Mistakes

1. **Forgetting to activate virtual environment**
   - Always run `source venv/bin/activate` before running backend
   - Your prompt should show `(venv)` when activated

2. **Not setting API key**
   - The app cannot work without `GEMINI_API_KEY`
   - Get yours from https://aistudio.google.com/apikey

3. **Using private repos without token**
   - Private repos require `GITHUB_TOKEN`
   - Generate at https://github.com/settings/tokens

4. **Not restarting after .env changes**
   - After editing `.env`, restart the backend server
   - Ctrl+C in backend terminal, then run uvicorn again

## Getting Help

If you're still stuck:

1. Check [COMMON_PITFALLS.md](docs/COMMON_PITFALLS.md)
2. Read the full [SETUP.md](docs/SETUP.md)
3. Check error messages carefully
4. Open an issue on GitHub

## Success Indicators

You know everything is working when:

✅ Backend terminal shows "Application startup complete"
✅ Frontend shows "Smart Documentation Generator"
✅ http://localhost:8000/api/v1/health returns healthy status
✅ You can generate documentation for a sample repo

Happy documenting! 🚀
