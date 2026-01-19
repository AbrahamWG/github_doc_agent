# Project File Structure

```
github_doc_agent/
│
├── 📄 README.md                      # Main project documentation
├── 📄 PROJECT_TREE.md                # This file - project structure guide
├── 📄 .gitignore                     # Git ignore rules
├── 📄 docker-compose.yml             # Multi-container Docker setup
├── 🔧 start.sh                       # Quick start script
│
├── 📁 backend/                       # Python FastAPI Backend
│   ├── 📄 requirements.txt           # Python dependencies
│   ├── 📄 .env.example               # Environment variable template
│   ├── 📄 Dockerfile                 # Backend container config
│   │
│   └── 📁 app/                       # Application code
│       ├── 📄 __init__.py
│       ├── 📄 main.py                # FastAPI app entry point
│       ├── 📄 config.py              # Environment configuration
│       │
│       ├── 📁 agents/                # AI Agents (Core Logic)
│       │   ├── 📄 __init__.py
│       │   ├── 📄 code_analyzer.py   # Agent 1: Code Analysis
│       │   ├── 📄 context_gatherer.py # Agent 2: Context Gathering
│       │   ├── 📄 doc_generator.py   # Agent 3: Doc Generation
│       │   └── 📄 orchestrator.py    # Agent Coordinator
│       │
│       ├── 📁 mcp_servers/           # MCP Servers (External Data)
│       │   ├── 📄 __init__.py
│       │   └── 📄 github_mcp.py      # GitHub API integration
│       │
│       ├── 📁 models/                # Request/Response Models
│       │   ├── 📄 __init__.py
│       │   ├── 📄 request_models.py  # Pydantic request models
│       │   └── 📄 response_models.py # Pydantic response models
│       │
│       ├── 📁 routes/                # API Routes
│       │   ├── 📄 __init__.py
│       │   └── 📄 documentation.py   # Documentation endpoints
│       │
│       ├── 📁 utils/                 # Utility functions
│       │   └── 📄 __init__.py
│       │
│       └── 📁 tests/                 # Test suite
│           ├── 📄 __init__.py
│           └── 📄 test_api.py        # API tests
│
├── 📁 frontend/                      # React Frontend
│   ├── 📄 package.json               # Node dependencies
│   ├── 📄 vite.config.js             # Vite configuration
│   ├── 📄 tailwind.config.js         # Tailwind CSS config
│   ├── 📄 postcss.config.js          # PostCSS config
│   ├── 📄 index.html                 # HTML entry point
│   ├── 📄 Dockerfile                 # Frontend container config
│   ├── 📄 nginx.conf                 # Production server config
│   │
│   └── 📁 src/                       # Source code
│       ├── 📄 main.jsx               # React entry point
│       ├── 📄 App.jsx                # Main application component
│       ├── 📄 index.css              # Global styles (Tailwind)
│       │
│       ├── 📁 components/            # React Components
│       │   ├── 📄 RepoInput.jsx      # Repository URL input
│       │   ├── 📄 LoadingState.jsx   # Loading indicator
│       │   ├── 📄 DocumentationViewer.jsx # Doc display
│       │   └── 📄 ErrorBoundary.jsx  # Error handling
│       │
│       └── 📁 services/              # API Integration
│           └── 📄 api.js             # Backend API client
│
└── 📁 docs/                          # Additional Documentation (legacy)
    └── (documentation files moved to README.md)
```

## File Count Summary

- **Backend Python Files:** 13 files
- **Frontend React Files:** 7 files
- **Configuration Files:** 8 files
- **Documentation Files:** 2 files (README.md, PROJECT_TREE.md)
- **Total Files:** ~36 files

## Key Files to Start With

### For Users
1. 📄 **README.md** - Start here! Complete project overview and quick start
2. 📄 **PROJECT_TREE.md** - This file - understand the structure

### For Developers

#### Understanding the System
1. **backend/app/main.py** - FastAPI application entry point
2. **backend/app/agents/orchestrator.py** - Agent coordination logic
3. **backend/app/agents/doc_generator.py** - Documentation generation prompts

#### Frontend Components
1. **frontend/src/App.jsx** - Main React application logic
2. **frontend/src/components/RepoInput.jsx** - User input handling
3. **frontend/src/components/DocumentationViewer.jsx** - Documentation display

#### Configuration
1. **backend/app/config.py** - Environment configuration
2. **backend/.env.example** - Environment variables template
3. **docker-compose.yml** - Docker setup

## Important Directories

### `/backend/app/agents/` 🤖
The heart of the system. Three specialized AI agents:

- **code_analyzer.py** - Analyzes repository structure, detects frameworks
  - Makes 1 LLM call: complexity analysis based on README
  - Computes stats and structure without LLM (faster)

- **context_gatherer.py** - Generates current best practices dynamically
  - Makes 2 LLM calls: documentation standards + language-specific best practices
  - **Not RAG**: Uses LLM to generate best practices on-the-fly (avoids hardcoding outdated standards)
  - Based on detected framework/language from code analyzer

- **doc_generator.py** - Generates 3 levels of documentation
  - Makes 3 LLM calls: beginner, intermediate, advanced (all in parallel)
  - Uses analysis + context to create tailored documentation

- **orchestrator.py** - Coordinates all agents
  - Manages parallel execution (agents 1 & 2 run simultaneously)
  - Handles dependencies and error isolation

**Key Functions:**
- `orchestrator.generate_documentation()` - Main entry point
- `code_analyzer.analyze_codebase()` - Structure analysis
- `context_gatherer.gather_context()` - Best practices generation
- `doc_generator.generate_documentation()` - Multi-level documentation generation

### `/backend/app/mcp_servers/` 🔌
External data sources abstracted as servers:
- **github_mcp.py** - GitHub API wrapper

**Key Functions:**
- `get_repository_data()` - Fetch repo metadata
- `get_file_tree()` - Get repository structure
- `get_readme()` - Extract README content

### `/frontend/src/components/` ⚛️
React UI components:
- **RepoInput.jsx** - User input form with URL validation
- **LoadingState.jsx** - Progress indicator during generation
- **DocumentationViewer.jsx** - Tabbed interface for 3 doc levels
- **ErrorBoundary.jsx** - Graceful error handling

### `/backend/app/models/` 📋
Request/Response data models:
- **request_models.py** - `DocumentationRequest` (validates GitHub URLs)
- **response_models.py** - `DocumentationResponse` (structured output)

### `/backend/app/routes/` 🛣️
API endpoints:
- **documentation.py** - `/api/v1/generate` endpoint

## Entry Points

### Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
**Entry:** `backend/app/main.py`
- Initializes FastAPI app
- Sets up CORS middleware
- Registers routes
- Starts server on port 8000

### Frontend
```bash
cd frontend
npm run dev
```
**Entry:** `frontend/src/main.jsx` → `frontend/src/App.jsx`
- React application bootstrap
- Renders main App component
- Sets up routing (if added)

### Docker
```bash
docker-compose up --build
```
**Entry:** `docker-compose.yml`
- Starts both backend and frontend containers
- Sets up networking between services

## Data Flow

**What this shows:** How data moves through the entire system from user input to final output, including all layers (frontend, API, backend, agents).

```
User Input (Frontend)
  ↓
RepoInput.jsx (URL validation)
  ↓
api.js (Axios HTTP client)
  ↓
POST /api/v1/generate (FastAPI)
  ↓
documentation.py (Route handler)
  ↓
orchestrator.py (Agent coordination)
  ├── github_mcp.py → GitHub API (fetch repo data)
  ├── code_analyzer.py → Gemini API (1 call: complexity analysis)
  ├── context_gatherer.py → Gemini API (2 calls: doc standards + best practices)
  └── doc_generator.py → Gemini API (3 calls: beginner/intermediate/advanced in parallel)
  
Total: ~6-8 LLM API calls per documentation generation
  ↓
Response (JSON with documentation)
  ↓
DocumentationViewer.jsx (Render tabs)
  ↓
User sees documentation!
```

**Key Point:** This shows the *path* data takes through different files and modules.

## Execution Flow

**What this shows:** The timing and sequencing of agent execution within the backend - which agents run in parallel vs sequentially, and their dependencies.

### Agent Orchestration Sequence

```
1. Fetch Repository Data (GitHub MCP)
   ↓
2. Code Analysis (Agent 1) ──┐
                             ├──→ 4. Generate Docs (Agent 3)
3. Context Gathering (Agent 2)┘
```

**Parallel Execution:**
- Agents 1 and 2 run simultaneously (both start after step 1)
- Agent 3 waits for both to complete before starting
- All 3 documentation levels generated in parallel by Agent 3

**Key Point:** This shows the *timing* and *dependencies* between agents, focusing on parallelization and execution order.

### Understanding Context Gatherer (Agent 2)

**Question:** Why do we need `context_gatherer.py`? Is it RAG?

**Answer:** No, it's **not RAG** (Retrieval-Augmented Generation). Here's what it does:

**What Context Gatherer Does:**
- Uses LLM to **generate** current best practices on-the-fly
- Based on detected framework/language (e.g., "React", "Python", "Django")
- Produces tailored documentation standards for that specific tech stack

**Why Not Just Hardcode Standards?**
- Documentation standards evolve (best practices change over time)
- Hardcoded standards become outdated quickly
- LLM provides current, framework-specific recommendations

**Example:**
```
Input: Framework detected = "React"
Context Gatherer LLM Prompt: "What are current React documentation best practices?"
Output: Modern React docs should include: hooks examples, TypeScript patterns, etc.
```

**Note:** The Context Gatherer results are passed to Doc Generator, which uses them to inform how documentation should be structured (e.g., "React projects should emphasize component examples").

## Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables (secrets - never commit!) |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `package.json` | Node.js dependencies and scripts |
| `docker-compose.yml` | Multi-container orchestration |
| `vite.config.js` | Frontend build tool config |
| `tailwind.config.js` | CSS framework config |
| `nginx.conf` | Production web server config |
| `.gitignore` | Git exclusion rules |

## Missing Files (Intentionally)

These files are generated/created by users:
- `.env` - Contains secrets (never commit!)
- `node_modules/` - Installed by npm
- `venv/` - Created by Python virtual environment
- `dist/` - Frontend build output
- `__pycache__/` - Python bytecode cache

## Code Statistics

```
Language      Files   Lines   Code    Comments
---------------------------------------------
Python        13      ~1200   ~900    ~300
JavaScript    7       ~600    ~500    ~100
Markdown      2       ~1000   ~1000   N/A
Config        8       ~200    ~200    ~0
---------------------------------------------
Total         30      ~3000   ~2600   ~400
```

## Dependency Graph

```
main.py (FastAPI App)
  ↓
routes/documentation.py
  ↓
orchestrator.py
  ├── code_analyzer.py
  │   └── github_mcp.py
  ├── context_gatherer.py
  │   └── github_mcp.py
  ├── doc_generator.py
  │   └── github_mcp.py
  └── github_mcp.py
```

## How to Navigate This Project

### 1. Understanding the System
   - Start with: `README.md` for overview
   - Read: `backend/app/agents/orchestrator.py` for agent flow
   - Explore: `backend/app/agents/doc_generator.py` for prompts

### 2. Setting Up
   - Follow: `README.md` Quick Start section
   - Configure: `backend/.env` file with API keys
   - Test: `curl http://localhost:8000/api/v1/health`

### 3. Modifying Behavior
   - **Prompts:** Edit `backend/app/agents/doc_generator.py`
   - **UI:** Modify `frontend/src/components/`
   - **Logic:** Update `backend/app/agents/`
   - **API:** Change `backend/app/routes/documentation.py`

### 4. Troubleshooting
   - Check: `README.md` Troubleshooting section
   - Logs: Backend terminal output
   - Errors: Browser console (F12)
   - API: http://localhost:8000/docs (Swagger UI)

### 5. Deploying
   - **Local:** `./start.sh` or `docker-compose up`
   - **Development:** Use `--reload` flag with uvicorn
   - **Production:** Build with Docker and deploy to cloud

## Next Steps

After reviewing this structure:

1. ✅ Read README.md for complete setup instructions
2. ✅ Set up `.env` file with API keys
3. ✅ Install dependencies (backend + frontend)
4. ✅ Run the application locally
5. ✅ Generate your first documentation!
6. ✅ Explore the code in `/backend/app/agents/`

---

**Pro Tip:** Open this project in VS Code and install these extensions:
- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Docker
