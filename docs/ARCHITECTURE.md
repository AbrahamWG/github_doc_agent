# System Architecture

## Overview

Smart Documentation Agent is a multi-agent system that generates adaptive documentation for GitHub repositories. The system consists of three specialized AI agents orchestrated through a central coordinator, with MCP (Model Context Protocol) servers providing external data access.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                       │
│  - User interface for input and documentation display       │
│  - Handles state management and API communication           │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
┌───────────────────────────▼─────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  - Request validation and routing                           │
│  - Error handling and response formatting                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│              Agent Orchestrator                             │
│  - Coordinates agent execution flow                         │
│  - Manages parallel processing                              │
│  - Handles error recovery                                   │
└──┬────────────────────────┬─────────────────────────────┬───┘
   │                        │                             │
┌──▼──────────┐   ┌────────▼──────────┐   ┌─────────────▼───┐
│  Agent 1    │   │     Agent 2       │   │    Agent 3      │
│Code Analyzer│   │Context Gatherer   │   │Doc Generator    │
│             │   │                   │   │                 │
│- Structure  │   │- Best practices   │   │- Beginner docs  │
│- Complexity │   │- Standards        │   │- Intermediate   │
│- Metrics    │   │                   │   │- Advanced       │
└──┬──────────┘   └────────┬──────────┘   └─────────────┬───┘
   │                       │                            │
   └───────────────────────┼────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    MCP Servers (Tools)                      │
│  ┌────────────┐                                             │
│  │ GitHub MCP │    - Repository access                      │
│  │            │    - File content fetching                  │
│  │            │    - README extraction                      │
│  └────────────┘                                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Frontend Layer
**Technology:** React + Vite + Tailwind CSS

**Responsibilities:**
- Collect GitHub repository URL from user
- Display real-time generation progress
- Render multi-level documentation with tabbed interface
- Handle error states gracefully
- Provide download functionality

**Key Design Decisions:**
- Vite for faster development builds
- Tailwind for rapid UI development
- No state management library (React hooks sufficient for MVP)

### API Layer
**Technology:** FastAPI + Python 3.11

**Responsibilities:**
- Validate incoming requests
- Route requests to orchestrator
- Format responses
- Handle CORS for local development
- Provide health check endpoints

**Key Design Decisions:**
- FastAPI chosen over Flask for async support (critical for agent coordination)
- Pydantic models for request/response validation
- CORS middleware for security without compromising local dev experience

### Agent Orchestration Layer

**Orchestrator Pattern:**
The orchestrator coordinates all agents and manages the execution flow:

1. **Sequential Dependencies:** Some steps must complete before others begin
2. **Parallel Execution:** Independent steps run simultaneously for speed
3. **Error Isolation:** Agent failures don't crash the entire system

**Execution Flow:**
```
Step 1: Fetch Repo Data (GitHub MCP)
           ↓
Step 2: Code Analysis (Agent 1) ──┐
                                   ├─→ Step 4: Generate Docs (Agent 3)
Step 3: Context Gathering (Agent 2)┘
```

### Agent Layer

#### Agent 1: Code Analyzer
**Purpose:** Analyze repository structure and code complexity

**Responsibilities:**
- Compute statistical metrics (files, lines, languages)
- Identify project structure patterns
- Detect frameworks and project types
- Assess complexity using LLM analysis

**Key Insights Generated:**
- Project size and scope
- Testing infrastructure presence
- Documentation status
- Framework-specific patterns

#### Agent 2: Context Gatherer
**Purpose:** Gather external context and best practices

**Responsibilities:**
- Retrieve documentation standards for detected framework
- Identify language-specific best practices
- Gather relevant context for documentation generation

**Design Decision:**
- Uses LLM to generate current best practices (avoids hardcoding outdated standards)
- Focuses on project-specific recommendations

#### Agent 3: Documentation Generator
**Purpose:** Generate multi-level documentation

**Responsibilities:**
- Generate beginner-friendly documentation (What/Why/How)
- Generate intermediate documentation (Architecture/Integration)
- Generate advanced documentation (Technical deep-dive)

**Key Design Principle:**
- **Distinct Prompting Strategies:** Each level uses dramatically different prompts
- **Parallel Generation:** All three levels generated simultaneously
- **Tone Variation:** Beginner (friendly), Intermediate (professional), Advanced (technical)

### MCP Server Layer

#### GitHub MCP
**Purpose:** Provide abstraction over GitHub API

**Responsibilities:**
- Fetch repository metadata
- Retrieve file tree with depth limits
- Extract README content
- Handle rate limiting gracefully

**Key Design Decisions:**
- Depth-limited tree traversal (prevents timeout on large repos)
- File filtering (code files only, skip binaries)
- Size limits (skip files > 1MB)
- Rate limit checking before operations

## Data Flow

### Request Flow
```
1. User enters GitHub URL
2. Frontend validates URL format
3. POST /api/v1/generate sent to backend
4. Backend validates request
5. Orchestrator coordinates agents:
   a. GitHub MCP fetches repo data
   b. Agent 1 analyzes code (parallel with Agent 2)
   c. Agent 2 gathers context (parallel with Agent 1)
   d. Agent 3 generates docs (uses outputs from 1 & 2)
6. Backend formats response
7. Frontend displays documentation
```

### Error Handling Flow
```
Error Occurs
    ↓
Agent catches exception
    ↓
Returns error in structured format
    ↓
Orchestrator logs error
    ↓
Returns partial results if possible
    ↓
Backend formats error response
    ↓
Frontend displays user-friendly error
```

## Design Patterns Used

### 1. Orchestrator Pattern
- Central coordinator manages agent lifecycle
- Enables parallel execution where possible
- Provides single point of failure handling

### 2. MCP (Model Context Protocol) Pattern
- External services abstracted as "servers"
- Agents interact with MCPs, not APIs directly
- Easy to swap implementations

### 3. Multi-Agent Pattern
- Specialized agents for different concerns
- Each agent has single responsibility
- Agents don't communicate directly (only through orchestrator)

### 4. Async/Await Pattern
- Non-blocking I/O for API calls
- Parallel execution of independent tasks
- Better resource utilization

## Scalability Considerations

### Current MVP Limitations
- Synchronous request processing (one request at a time)
- In-memory state (no caching)
- Rate limits from free-tier APIs

### Future Enhancements
1. **Job Queue:** Use Celery or RQ for background processing
2. **Caching:** Redis for caching GitHub API responses
3. **Database:** Store generated documentation
4. **Load Balancing:** Multiple backend instances
5. **Streaming:** Stream documentation as it's generated

## Security Considerations

### API Key Management
- Never commit `.env` files
- Use environment variables for secrets
- Rotate keys regularly

### Rate Limiting
- Implement request throttling
- Queue requests during high load
- Monitor API usage

### Input Validation
- Validate GitHub URLs
- Sanitize user input
- Prevent injection attacks

## Technology Choices Rationale

| Technology | Alternative Considered | Why Chosen |
|------------|----------------------|------------|
| FastAPI | Flask | Async support, auto-docs, Pydantic validation |
| React | Vue/Svelte | Large ecosystem, job market demand |
| Tailwind | Bootstrap | More customizable, smaller bundle |
| Gemini | OpenAI GPT | Free tier, good performance |
| PyGithub | requests | Higher-level abstraction, rate limit handling |

## Performance Optimizations

1. **Parallel Agent Execution:** Agents 1 & 2 run simultaneously
2. **Depth-Limited Traversal:** Avoid fetching entire large repos
3. **File Filtering:** Skip non-code files early
4. **Truncated Context:** Limit README length sent to LLM
5. **Async I/O:** Non-blocking API calls

## Monitoring & Observability

### Logging Strategy
- Structured logging at each layer
- Log levels: INFO for flow, ERROR for exceptions
- Include request IDs for tracing

### Metrics to Track
- Request latency
- Agent execution time
- API call success rate
- Error frequency by type

## Conclusion

This architecture prioritizes:
1. **Modularity:** Easy to swap components
2. **Scalability:** Can add more agents or MCPs
3. **Maintainability:** Clear separation of concerns
4. **Performance:** Parallel execution where possible
