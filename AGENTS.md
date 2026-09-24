# Hello Agent project rules

These rules apply to the entire repository.

## Architecture

- Keep backend code in `backend/` and frontend code in `frontend/`.
- Build the backend with FastAPI and Python type hints.
- Build the frontend with Vue 3 Composition API and Vite.
- Keep API contracts explicit and document changes that affect both apps.

## Development

- Prefer small, focused modules and changes.
- Add or update tests when behavior changes.
- Never commit secrets, local environment files, virtual environments,
  dependency directories, or build output.
- Do not install or upgrade dependencies unless the task explicitly requires it.
- Update `README.md` when setup steps or the project structure change.

## Verification

- Run the relevant backend and frontend checks before handing off changes.
- Report checks that could not be run and explain why.
