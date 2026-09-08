## Plan: BookWorm FastAPI + React MVP

TL;DR: Convert the terminal application into a full-stack web app by exposing the existing business logic through a FastAPI backend (REST routes for auth, library, and AI chat) and building a React frontend that consumes those routes. Keep the existing text-file storage temporarily behind a storage layer, and migrate to SQLite once the MVP works end-to-end.

**How to use this plan:** Each step lists what to build AND what to learn first. If you already know a topic, skim it and move on — the goal is to never hit a step and be stuck on a concept you've never seen before.

---

### Phase 1: Stabilize the foundation

**1. Confirm the current Python environment and document the supported run commands from the repository root and `backend/`.**
- *Study first:* Nothing new — this is just re-familiarization with your own project (venv activation, `pip install -r requirements.txt`, running `main.py` from different directories).

**2. Reconcile the AI model configuration: the code uses `qwen2`, while the README documents `phi3:mini`; make the chosen model configurable rather than hard-coded.**
- *Study first:* Python environment variables (`os.environ`, `.env` files) and the `python-dotenv` package. This is how config values get read at runtime instead of hard-coded — a pattern you'll reuse constantly in FastAPI (API keys, DB URLs, model names all come from `.env`).

**3. Move shared paths and settings into a small configuration module so the API, the CLI, and vector code resolve data files consistently regardless of the launch directory.**
- *Study first:* Basic Python module organization — what makes a file importable as a module, relative vs. absolute imports, and `__init__.py` basics if you organize `backend/` into a package.

**4. Define simple domain structures for a user and book/library entry. Preserve the existing file formats during this phase.**
- *Study first:* **Pydantic models** (`BaseModel`, field types, optional fields). This is the single most important new concept for this whole rebuild — FastAPI uses Pydantic for request/response validation everywhere, so a `User` and `Book` model you define here gets reused almost unchanged as your API schemas in Phase 2.

---

### Phase 2: Build the FastAPI backend

**5. Set up a FastAPI project skeleton (`backend/app/main.py`) with a single health-check route, and confirm it runs with `uvicorn`.**
- *Study first:* What FastAPI actually is (an ASGI web framework), what `uvicorn` does (the server that runs it), and the absolute basics of HTTP — methods (GET/POST/PUT/DELETE), status codes (200, 401, 404, 422), and what a JSON request/response body looks like. FastAPI's own "First Steps" tutorial is the fastest way to get this.

**6. Split `backend/main.py`'s logic into reusable service functions for authentication, library operations, and recommendations — pure Python functions with no `input()`/`print()`, so routes and the AI chain can both call them.**
- *Study first:* Separation of concerns / service-layer pattern (routes should be thin, business logic should live elsewhere and be testable without a running server). No new syntax here, just a design habit — this is the same extraction your original plan called for, it just now feeds API routes instead of Streamlit widgets.

**7. Build authentication routes: `POST /signup`, `POST /login`, and a way to protect other routes so only logged-in users can reach them.**
- *Study first:* **JWTs (JSON Web Tokens)** and how stateless auth works — since there's no server-side session/global variable anymore, the frontend must send proof of identity (a token) with every request. Look at FastAPI's official security tutorial (OAuth2PasswordBearer + JWT) and the `python-jose` or `PyJWT` library. Also study **password hashing with `passlib`/`bcrypt`** now rather than later — you're building auth from scratch here, so do it right the first time instead of migrating unsalted SHA-256 afterward.

**8. Create a storage service around `profiles.txt`, `{username}_books.txt`, `{username}_tbr.txt`, and `{username}_reading.txt`. Validate usernames before using them in filenames, handle missing files, and centralize parsing/writing.**
- *Study first:* Nothing new conceptually — this is the same file I/O you already know, just organized behind functions the routes call.

**9. Build library routes: `GET /library/{status}`, `POST /library`, `PATCH /library/{book_id}` (to move a book between Finished/TBR/Currently Reading).**
- *Study first:* **RESTful API design conventions** — resource-based URLs, using the right HTTP verb for the right action, path parameters vs. query parameters vs. request bodies. This is a core "corporate world" skill — nearly every backend job expects you to know REST conventions even if the company uses GraphQL instead.

**10. Extract the Ollama/Chroma recommendation chain from `chatbot()` into a callable service, and expose it as `POST /chat` (accepts a message + returns the model's response).**
- *Study first:* Nothing new in the RAG logic itself (you already understand `vector.py` and the chain). New concept: **how to structure a request/response body for a chat endpoint** — typically `{"message": str}` in, `{"response": str}` out, sometimes with the chat history included in the request since the API is stateless between calls (no more Python `while True` loop holding history in memory).

**11. Decide and document whether recommendations exclude only finished books or also account for TBR/currently-reading books. Keep catalog grounding limited to titles present in `books.csv`.**
- *Study first:* Nothing new — this is a product/logic decision, not a technical one.

**12. Add CORS configuration so a React app running on a different port (e.g. `localhost:3000`) can call your API (`localhost:8000`) during development.**
- *Study first:* **CORS (Cross-Origin Resource Sharing)** — why browsers block cross-origin requests by default and how `CORSMiddleware` in FastAPI allowlists your frontend's origin. This trips up almost everyone the first time they connect a separate frontend and backend — worth understanding *why* it exists, not just pasting the fix.

---

### Phase 3: Build the React frontend

**13. Set up a React project (Vite is the modern standard — faster and simpler than Create React App) and confirm the default page runs.**
- *Study first:* **JavaScript fundamentals** if rusty: `const`/`let`, arrow functions, template literals, destructuring, `async`/`await`, and the `fetch` API (or `axios`) for making HTTP requests. Then **JSX syntax** and what a **functional component** is. The Odin Project's JavaScript path or javascript.info are solid, and React's own official "Quick Start" tutorial is short and hands-on.

**14. Learn and apply React state and effects: `useState` for local component state, `useEffect` for running code when a component loads (e.g. fetching data).**
- *Study first:* This IS the study step — `useState`/`useEffect` are the two hooks you'll use constantly. Don't skip building a couple of tiny throwaway components (a counter, a fetch-and-display list) before wiring up real BookWorm screens, so the mental model is solid before the stakes are real.

**15. Build a login/signup page that calls your FastAPI `/login` and `/signup` routes, and store the returned JWT (in memory via React state, or `localStorage` for persistence across refreshes).**
- *Study first:* How to send a `POST` request with a JSON body using `fetch`/`axios`, how to read the response, and basic **client-side routing** — look at `react-router-dom` (`BrowserRouter`, `Routes`, `Route`) so you can have distinct pages/URLs (`/login`, `/library`, `/chat`) instead of one giant component.

**16. Build the library pages (Finished, TBR, Currently Reading) that fetch data from your `/library/{status}` route and render it as a list, plus a form to add a new book (`POST /library`).**
- *Study first:* Rendering **lists with `.map()`** in JSX and why React needs a unique `key` prop on each list item. Also **controlled form inputs** (`value` + `onChange` tied to state) — this replaces the `input()` calls in your old `addbook()` function.

**17. Build the AI chat page: a message list, a text input, and a send button that calls `POST /chat` and appends the response to the conversation.**
- *Study first:* Managing an **array in state** (appending new messages immutably, e.g. `setMessages([...messages, newMessage])`), and basic UX patterns for chat UIs (auto-scroll to newest message, disabling the send button while waiting for a response, showing a loading indicator).

**18. Attach the JWT to every authenticated request (as an `Authorization: Bearer <token>` header), and handle token expiry/401 responses by redirecting to login.**
- *Study first:* How HTTP headers work in `fetch`/`axios` calls, and a first look at **React Context** (`createContext`/`useContext`) as a way to share the logged-in user/token across every component without passing it down manually through props at every level ("prop drilling").

**19. Style the app — plain CSS to start, or a component library (e.g. Tailwind CSS or MUI) if you want to move faster.**
- *Study first:* Whichever you pick — if Tailwind, learn utility-class basics; if MUI, learn how to import and customize pre-built components. Not urgent to master, just enough to make the app presentable.

---

### Phase 4: Connect, harden, and finish

**20. Run the FastAPI backend and React frontend together locally and walk through the full flow: signup → login → add books → get AI recommendations → logout.**
- *Study first:* Nothing new — this is integration testing by hand.

**21. Add input validation (Pydantic already helps a lot here), handle malformed legacy `.txt` files gracefully, and add proper HTTP error responses (401 for bad auth, 404 for missing resources, 422 for bad input) instead of silent failures.**
- *Study first:* FastAPI's `HTTPException` and how Pydantic validation errors automatically become 422 responses — understanding this now saves confusion later when the frontend needs to handle these error shapes.

**22. Add graceful handling for missing Ollama, missing models, unavailable Chroma data, and empty catalogs, surfaced as real error responses the frontend can display (not a crashed request).**
- *Study first:* Basic `try`/`except` around the Ollama/Chroma calls, translated into an appropriate HTTP status code (e.g. 503 Service Unavailable) rather than letting the exception bubble up as a generic 500.

**23. Once the MVP behavior is stable, migrate storage from per-user text files to a real database.**
- *Study first:* **SQL basics** (tables, primary/foreign keys, basic `SELECT`/`INSERT`/`UPDATE`) and an **ORM** — SQLAlchemy is the standard for FastAPI, paired with SQLite as the file-based database to start (no separate DB server needed) and Alembic for migrations if you want to go further. This is one of the highest-value corporate skills in this whole plan — SQL + ORM knowledge shows up in nearly every backend job description.

**24. Add focused backend tests for authentication, file/DB operations, recommendation exclusion logic, and route status codes.**
- *Study first:* **`pytest`** basics and FastAPI's `TestClient` (built on `httpx`), which lets you call your routes in tests without running a live server.

**25. Update `README.md` with environment setup, Ollama model pulls, vector-index preparation, exact commands to run both the API and the frontend, and known limitations.**
- *Study first:* Nothing new — documentation writing.

---

**Relevant files (updated for this architecture)**
- `backend/app/main.py` — FastAPI app instance, router includes, CORS config.
- `backend/app/routers/` — `auth.py`, `library.py`, `chat.py` — route definitions per domain.
- `backend/app/services/` — auth, library, and recommendation business logic (no HTTP-specific code).
- `backend/app/models.py` — Pydantic request/response schemas (and SQLAlchemy models once Phase 4 migrates to a DB).
- `backend/vector.py` — Chroma catalog initialization; wrap in a function with caching so it doesn't rebuild on every import.
- `frontend/src/pages/` — `Login.jsx`, `Signup.jsx`, `Library.jsx`, `Chat.jsx`.
- `frontend/src/context/AuthContext.jsx` — shared auth/token state.
- `backend/requirements.txt` — add `fastapi`, `uvicorn`, `python-jose`/`pyjwt`, `passlib[bcrypt]`, `python-dotenv`, `pytest`, `httpx`, and later `sqlalchemy`.
- `frontend/package.json` — React, `react-router-dom`, and your chosen styling library.

**Decisions**
- Backend framework: **FastAPI** (over Flask) for built-in Pydantic validation, automatic OpenAPI docs, and async support — all strong resume signals.
- Frontend framework: **React** (via Vite) for the strongest job-market relevance.
- Auth strategy: JWT-based stateless auth from the start, rather than migrating from the old global-variable session later.
- Short-term storage: keep text files behind a storage abstraction through the MVP; SQLite + SQLAlchemy is the Phase 4 milestone.
- Include: authentication, personal reading history, status management, AI recommendations/chat, a responsive React UI, and graceful error handling.
- Exclude from the first MVP: public profiles, social following, ratings/reviews, cover-image integrations, deployment, and persistent multi-device chat history.

**Further Considerations**
1. Build and test the backend routes independently first (using FastAPI's auto-generated `/docs` page, or a tool like Postman/Insomnia/Thunder Client) before writing any React code — this isolates backend bugs from frontend bugs.
2. Treat the current file storage as local-development storage only; concurrent hosted use should wait for the SQLite migration.
3. Do not rebuild the Chroma index on every backend restart. Cache it and add a deliberate rebuild step when `books.csv` changes.
4. If FastAPI + React ends up feeling like too much at once, it's reasonable to build the backend fully first and test it via `/docs`/Postman, then tackle React as a distinct second project phase — you don't have to learn both simultaneously.
