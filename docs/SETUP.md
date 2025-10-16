# Setup Instructions

This guide will help you set up and run the Smart Documentation Agent locally.

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd github_doc_agent
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=optional_for_private_repos
ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173
BACKEND_PORT=8000
```

**Getting a Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into your `.env` file

**GitHub Token (Optional):**
- Only needed for private repositories or to increase rate limits
- Generate at: https://github.com/settings/tokens
- Required scopes: `repo` (for private repos)

#### Run the Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at http://localhost:8000
API docs will be available at http://localhost:8000/docs

### 3. Frontend Setup

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

## Testing the Application

1. Open your browser to http://localhost:5173
2. Enter a GitHub repository URL (e.g., https://github.com/expressjs/express)
3. Click "Generate Documentation"
4. Wait 30-60 seconds for the documentation to be generated
5. View the three levels of documentation (Beginner, Intermediate, Advanced)

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError"**
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

**"Invalid API Key"**
- Check that your `GEMINI_API_KEY` is correct in `.env`
- Verify the key works at https://aistudio.google.com/apikey

**"GitHub API rate limit exceeded"**
- Add a `GITHUB_TOKEN` to your `.env` file
- Without a token, you're limited to 60 requests/hour

### Frontend Issues

**"Backend is not reachable"**
- Make sure the backend is running on port 8000
- Check that no other application is using port 8000
- Try restarting the backend

**"npm install" fails**
- Update Node.js to version 18 or higher
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then run `npm install` again

## Development Tips

### Backend Development

- Use `--reload` flag with uvicorn for auto-reload on code changes
- Check logs in the terminal for debugging
- Use the interactive API docs at http://localhost:8000/docs

### Frontend Development

- Vite provides hot module replacement (HMR)
- Check browser console for errors
- Use React DevTools extension for debugging

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GEMINI_API_KEY | Yes | - | Google Gemini API key |
| GITHUB_TOKEN | No | "" | GitHub personal access token |
| ENVIRONMENT | No | development | Environment mode |
| FRONTEND_URL | No | http://localhost:5173 | Frontend URL for CORS |
| BACKEND_PORT | No | 8000 | Backend server port |

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system design
- See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for API details
- Check [COMMON_PITFALLS.md](./COMMON_PITFALLS.md) for common issues
