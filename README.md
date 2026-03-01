# Task API – Agile & DevOps Prototype

Small REST API for tasks: create, list, get by ID, update, delete. Built over two sprints with CI/CD, tests, and monitoring.

## Quick start

```bash
pip install -r requirements.txt
pytest tests/ -v
python app.py
```

- API: http://localhost:5000  
- Health: http://localhost:5000/health  
- Tasks: http://localhost:5000/tasks (GET list, POST create)

## Project structure

- `app.py` – Flask app and all endpoints  
- `tests/test_app.py` – Unit/integration tests (run in CI)  
- `.github/workflows/ci.yml` – CI pipeline (GitHub Actions)  
- `BACKLOG_AND_SPRINT_PLANS.md` – Backlog, DoD, sprint plans  
- `SPRINT_REVIEW_Sprint1.md`, `SPRINT_REVIEW_Sprint2.md` – Sprint reviews  



<img width="1918" height="711" alt="image" src="https://github.com/user-attachments/assets/a14dd96c-f781-4325-963f-311d9073683e" />

- `RETROSPECTIVE_Sprint1.md`, `RETROSPECTIVE_Sprint2.md` – Retrospectives  

## CI/CD

On push/PR to `main` or `master`, the workflow installs dependencies and runs `pytest tests/ -v`. See `.github/workflows/ci.yml`.

