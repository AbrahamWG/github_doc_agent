# Smart Documentation Agent

A multi-agent AI system that automatically generates adaptive, multi-level documentation for GitHub repositories. Built with Google's Gemini API and a three-agent architecture, it produces beginner, intermediate, and advanced documentation tailored to different experience levels.

## 📺 Video Demo

**[Watch the Full Demo on YouTube](https://www.youtube.com/watch?v=XXXrGy6r0c8&feature=youtu.be)**

See the system in action: generating documentation for Express.js, exploring the three levels (Beginner/Intermediate/Advanced), and showcasing the dark mode feature!

## Features

- **Multi-Level Documentation:** Generates three distinct documentation levels:
  - **Beginner:** Friendly explanations with examples and troubleshooting
  - **Intermediate:** Architecture overviews and integration patterns
  - **Advanced:** Technical deep-dives and contribution guidelines

- **Intelligent Analysis:** Uses AI agents to:
  - Analyze code structure and complexity
  - Gather relevant context and best practices
  - Generate tailored documentation for each level

- **Fast & Efficient:**
  - Parallel agent execution
  - Smart repository traversal (depth-limited)
  - File filtering to skip binaries

- **Free to Run:**
  - Uses free Gemini API tier
  - Works with GitHub's public API (60 requests/hour)
  - Optional GitHub token for higher rate limits

## Architecture

```
Frontend (React) → Backend (FastAPI) → Agent Orchestrator
                                            ↓
                    ┌───────────────────────┼───────────────────────┐
                    ↓                       ↓                       ↓
            Code Analyzer           Context Gatherer       Doc Generator
                    ↓                       ↓                       ↓
                    └───────────────────────┴───────────────────────┘
                                            ↓
                                    GitHub MCP Server
```

### Multi-Agent System

1. **Code Analyzer Agent:** Analyzes repository structure, detects frameworks, computes metrics
2. **Context Gatherer Agent:** Retrieves documentation standards and best practices
3. **Documentation Generator Agent:** Generates three levels of documentation in parallel

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Gemini API Key (free from [Google AI Studio](https://aistudio.google.com/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/github_doc_agent.git
cd github_doc_agent
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

**Get your Gemini API key:**
1. Visit https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy and paste into `backend/.env`

```bash
# Run the backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### 3. Frontend Setup

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:5173

### 4. Try It Out

1. Open http://localhost:5173
2. Enter a GitHub repository URL (e.g., `https://github.com/expressjs/express`)
3. Click "Generate Documentation"
4. Wait 30-60 seconds
5. View three levels of documentation!

## Usage Examples

### Web Interface

Simply paste any public GitHub repository URL:
- `https://github.com/facebook/react`
- `https://github.com/microsoft/vscode`
- `https://github.com/django/django`

### API Usage

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/expressjs/express"}'
```

See [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full API reference.

## Documentation

- [SETUP.md](docs/SETUP.md) - Detailed setup instructions
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture and design
- [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - API endpoints and usage
- [COMMON_PITFALLS.md](docs/COMMON_PITFALLS.md) - Troubleshooting guide

## Project Structure

```
github_doc_agent/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── agents/            # Three AI agents
│   │   │   ├── code_analyzer.py
│   │   │   ├── context_gatherer.py
│   │   │   ├── doc_generator.py
│   │   │   └── orchestrator.py
│   │   ├── mcp_servers/       # MCP servers (GitHub integration)
│   │   ├── models/            # Pydantic models
│   │   ├── routes/            # API routes
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/                       # Documentation
└── docker-compose.yml          # Docker setup
```

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework with async support
- **Google Gemini API** - LLM for documentation generation
- **PyGithub** - GitHub API wrapper
- **Pydantic** - Data validation

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Configuration

### Environment Variables

Create `backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=optional_for_private_repos
ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173
BACKEND_PORT=8000
```

See [SETUP.md](docs/SETUP.md) for detailed configuration options.

## Docker Deployment

Run with Docker Compose:

```bash
# Set environment variables
export GEMINI_API_KEY=your_key_here
export GITHUB_TOKEN=your_token_here  # Optional

# Start services
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

### Frontend Development

```bash
cd frontend
npm run dev
```

Hot module replacement enabled.

### Running Tests

```bash
cd backend
pytest
```

## System Design Highlights

### Multi-Agent Architecture
- **Orchestrator Pattern:** Central coordinator manages agent lifecycle
- **Parallel Execution:** Agents 1 & 2 run simultaneously
- **Error Isolation:** Agent failures don't crash the system

### Performance Optimizations
- Depth-limited repository traversal
- File filtering (code files only)
- Parallel documentation generation
- Async I/O throughout

### Scalability Considerations
- Stateless design (easy to horizontally scale)
- Ready for job queue integration
- Cacheable results

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for comprehensive design documentation.

## Common Issues

### "GitHub API rate limit exceeded"
- Add a GitHub token to `.env` for 5000 requests/hour
- Generate at: https://github.com/settings/tokens

### "Backend is not reachable"
- Verify backend is running: `curl http://localhost:8000/api/v1/health`
- Check that port 8000 is not in use

### "Invalid API Key"
- Verify `GEMINI_API_KEY` in `backend/.env`
- Test at https://aistudio.google.com/apikey

See [COMMON_PITFALLS.md](docs/COMMON_PITFALLS.md) for comprehensive troubleshooting.

## Limitations (MVP)

- **Public Repos Only:** Requires GitHub token for private repos
- **Rate Limits:** 60 GitHub requests/hour without token
- **Processing Time:** 30-90 seconds per repository
- **No Caching:** Each request regenerates documentation
- **Synchronous:** Processes one request at a time

## Future Enhancements

1. **Background Processing:** Job queue for async processing
2. **Caching Layer:** Redis for storing results
3. **Streaming:** Real-time documentation streaming
4. **Database:** Persist generated documentation
5. **Authentication:** User accounts and API keys
6. **Webhooks:** Notify when generation completes
7. **More Agents:** Code quality, security analysis

## Contributing

This is an MVP project built for demonstration purposes. To extend it:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request

Key areas for contribution:
- Additional agents (security analyzer, code quality checker)
- More MCP servers (GitLab, Bitbucket support)
- UI improvements
- Performance optimizations

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/)
- Uses [PyGithub](https://github.com/PyGithub/PyGithub) for GitHub integration
- Inspired by multi-agent AI system design patterns

## Contact

For issues or questions:
- Open an issue on GitHub
- Check [COMMON_PITFALLS.md](docs/COMMON_PITFALLS.md) for solutions
- Review [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

---

**Note:** This is an MVP (Minimum Viable Product) designed to demonstrate multi-agent AI system design. It runs completely locally and uses free-tier APIs. Perfect for learning, experimentation, and portfolio projects.
