# Project File Structure

```
github_doc_agent/
│
├── 📄 README.md                      # Main project documentation
├── 📄 GETTING_STARTED.md             # Quick start guide (5 minutes)
├── 📄 PROJECT_STATUS.md              # Current status and roadmap
├── 📄 PROJECT_TREE.md                # This file
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
└── 📁 docs/                          # Comprehensive Documentation
    ├── 📄 SETUP.md                   # Detailed setup instructions
    ├── 📄 ARCHITECTURE.md            # System architecture & design
    ├── 📄 API_DOCUMENTATION.md       # API reference guide
    └── 📄 COMMON_PITFALLS.md         # Troubleshooting guide
```

## File Count Summary

- **Backend Python Files:** 13 files
- **Frontend React Files:** 7 files
- **Configuration Files:** 8 files
- **Documentation Files:** 8 files
- **Total Files:** 36 files

## Key Files to Start With

### For Users
1. 📄 **GETTING_STARTED.md** - Start here (5-minute setup)
2. 📄 **README.md** - Full project overview
3. 📄 **docs/SETUP.md** - Detailed setup guide

### For Developers
1. 📄 **docs/ARCHITECTURE.md** - Understand the system design
2. 📄 **backend/app/agents/orchestrator.py** - See agent coordination
3. 📄 **backend/app/agents/doc_generator.py** - Modify prompts here
4. 📄 **frontend/src/App.jsx** - Main React application logic

### For DevOps
1. 📄 **docker-compose.yml** - Multi-container setup
2. 📄 **backend/Dockerfile** - Backend container
3. 📄 **frontend/Dockerfile** - Frontend container
4. 📄 **.env.example** - Environment variables template

## Important Directories

### `/backend/app/agents/` 🤖
The heart of the system. Three specialized AI agents:
- **code_analyzer.py** - Analyzes repository structure
- **context_gatherer.py** - Gathers best practices
- **doc_generator.py** - Generates 3 levels of docs
- **orchestrator.py** - Coordinates everything

### `/backend/app/mcp_servers/` 🔌
External data sources abstracted as servers:
- **github_mcp.py** - GitHub API wrapper

### `/frontend/src/components/` ⚛️
React UI components:
- **RepoInput.jsx** - User input form
- **LoadingState.jsx** - Progress indicator
- **DocumentationViewer.jsx** - Tabbed doc display
- **ErrorBoundary.jsx** - Error handling

### `/docs/` 📚
Comprehensive system documentation:
- **SETUP.md** - Installation guide
- **ARCHITECTURE.md** - System design (⭐ Read this!)
- **API_DOCUMENTATION.md** - API reference
- **COMMON_PITFALLS.md** - Troubleshooting

## Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `package.json` | Node.js dependencies |
| `docker-compose.yml` | Multi-container orchestration |
| `vite.config.js` | Frontend build tool config |
| `tailwind.config.js` | CSS framework config |
| `.gitignore` | Git exclusion rules |

## Entry Points

### Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Entry: `backend/app/main.py`

### Frontend
```bash
cd frontend
npm run dev
```
Entry: `frontend/src/main.jsx` → `frontend/src/App.jsx`

### Docker
```bash
docker-compose up --build
```
Entry: `docker-compose.yml`

## Testing Files

- `backend/app/tests/test_api.py` - API endpoint tests
- More tests can be added to `/backend/app/tests/`

## Missing Files (Intentionally)

These files are generated/created by users:
- `.env` - Contains secrets (never commit!)
- `node_modules/` - Installed by npm
- `venv/` - Created by Python
- `dist/` - Frontend build output
- `__pycache__/` - Python bytecode cache

## Code Statistics

```
Language      Files   Lines   Code    Comments
---------------------------------------------
Python        13      ~1200   ~900    ~300
JavaScript    7       ~600    ~500    ~100
Markdown      8       ~2500   ~2500   N/A
Config        8       ~200    ~200    ~0
---------------------------------------------
Total         36      ~4500   ~4100   ~400
```

## Dependency Graph

```
main.py
  ↓
orchestrator.py
  ├── code_analyzer.py
  ├── context_gatherer.py
  ├── doc_generator.py
  └── github_mcp.py
```

## Data Flow

```
User Input (Frontend)
  ↓
RepoInput.jsx
  ↓
api.js (Axios)
  ↓
FastAPI (main.py)
  ↓
documentation.py (Route)
  ↓
orchestrator.py
  ├── github_mcp.py → GitHub API
  ├── code_analyzer.py → Gemini API
  ├── context_gatherer.py → Gemini API
  └── doc_generator.py → Gemini API
  ↓
Response (JSON)
  ↓
DocumentationViewer.jsx
  ↓
User sees docs!
```

## How to Navigate This Project

1. **Understanding the System:**
   - Read: `README.md` → `docs/ARCHITECTURE.md`
   - Explore: `backend/app/agents/orchestrator.py`

2. **Setting Up:**
   - Follow: `GETTING_STARTED.md` (5 min)
   - Or: `docs/SETUP.md` (detailed)

3. **Modifying Behavior:**
   - Prompts: `backend/app/agents/doc_generator.py`
   - UI: `frontend/src/components/`
   - Logic: `backend/app/agents/`

4. **Troubleshooting:**
   - Check: `docs/COMMON_PITFALLS.md`
   - Logs: Backend terminal output
   - Errors: Browser console (F12)

5. **Deploying:**
   - Local: `./start.sh` or `docker-compose up`
   - Cloud: See `docs/SETUP.md` (future enhancement)

## Next Steps

After reviewing this structure:

1. ✅ Verify all files exist
2. ✅ Read GETTING_STARTED.md
3. ✅ Set up .env file
4. ✅ Install dependencies
5. ✅ Run the application
6. ✅ Generate your first documentation!

---

**Pro Tip:** Open this project in VS Code and install these extensions:
- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Docker
