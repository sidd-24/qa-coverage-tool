# 🧪 AI-Assisted QA Coverage Analysis & Regression Testing Tool

> Accelerating test creation and systematically identifying coverage gaps across features using AI — built with Python, TypeScript, Groq, and GitHub Actions.

---

## 📌 Project Overview

Manual test writing is slow, inconsistent, and rarely keeps pace with feature development. This project solves that by using AI to generate test scenarios directly from feature descriptions, while maintaining a structured regression layer and a live coverage gap tracker — all wired into a CI/CD pipeline.

The goal was not to replace human judgment in testing, but to eliminate the repetitive scaffolding work so engineers can focus on what actually needs thinking.

---

## 🎯 Objectives

- Use AI tools to accelerate test creation from feature descriptions
- Build a reusable regression testing layer in both Python and TypeScript
- Systematically track and close coverage gaps across features
- Translate newly released features into automated regression tests quickly
- Deploy the full suite in a CI/CD pipeline ready for production

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Test Generation | Groq API (`openai/gpt-oss-120b`, configurable with `GROQ_MODEL`) |
| Python Testing | `pytest`, `pytest-cov` |
| TypeScript Testing | `Jest`, `ts-jest` |
| Coverage Analysis | `pytest --cov`, Jest `--coverage` |
| Gap Tracking | Custom Python CLI + JSON store |
| CI/CD | GitHub Actions |
| Environment | Python 3.11, Node 20, Linux (Ubuntu in CI) |

---

## 📁 Project Structure

```
qa-coverage-tool/
├── .github/
│   └── workflows/
│       └── regression.yml          # CI/CD pipeline — runs on every push/PR
├── features/
│   └── sample_feature.md           # Feature descriptions fed to AI
├── scripts/
│   ├── generate_tests.py           # AI test generation via Groq
│   └── coverage_gap_tracker.py     # Gap analysis CLI
├── tests/
│   ├── python/
│   │   ├── conftest.py             # Shared pytest fixtures
│   │   ├── test_patterns.py        # Reusable assertion patterns
│   │   └── test_regression.py      # Hand-written regression baseline
│   └── typescript/
│       ├── patterns.ts             # Reusable TS test utilities
│       └── regression.test.ts      # TS regression tests
├── coverage_gaps.json              # Tracked coverage gaps
├── requirements.txt
├── package.json
├── tsconfig.json
└── .env                            # Local only — never committed
```

---

## 🚀 How It Works

### 1. Write a Feature Description

Drop a plain markdown file into `features/` describing what the feature does and its acceptance criteria. No special format required — just write it like you would for a ticket.

```markdown
# Feature: User Authentication
## Acceptance Criteria
- User can register with email and password
- Password must be at least 8 characters
- User receives error on duplicate email
...
```

### 2. AI Generates the Tests

Run the generation script and point it at your feature file:

```bash
python scripts/generate_tests.py features/sample_feature.md python
```

The script sends the feature description to Groq's LLM and gets back a complete pytest file covering happy paths, edge cases, and error cases. The output is saved to `tests/python/` automatically.

You review it, adjust anything that doesn't fit, and commit it.

### 3. Regression Layer Runs

The hand-written `test_regression.py` and `regression.test.ts` files form the permanent baseline — tests that must always pass, representing known-good behavior. These are never auto-generated; they are authored once and protected.

```bash
# Python
pytest tests/python/ -v --cov=tests/python --cov-report=term-missing

# TypeScript
npm test
```

### 4. Track Coverage Gaps

Anything not yet covered gets logged in `coverage_gaps.json` and managed via CLI:

```bash
# See all open gaps
python scripts/coverage_gap_tracker.py open

# Close a gap once covered
python scripts/coverage_gap_tracker.py close GAP-001

# Add a newly discovered gap
python scripts/coverage_gap_tracker.py add "Payments" "Refund flow" "high" "Not yet automated"

# Full report — tests + open gaps together
python scripts/coverage_gap_tracker.py report
```

### 5. CI/CD Runs Automatically

Every push to `main` or `develop` triggers GitHub Actions, which:
- Runs Python tests with coverage report
- Runs TypeScript tests with coverage
- Prints all open coverage gaps as a pipeline summary

```yaml
# .github/workflows/regression.yml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 20+
- A free [Groq API key](https://console.groq.com) (no credit card required)

### 1. Clone the repo

```bash
git clone https://github.com/sidd-24/qa-coverage-tool.git
cd qa-coverage-tool
```

### 2. Set up Python environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 3. Set up Node

```bash
npm install
```

### 4. Configure environment

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Never commit `.env` — it's in `.gitignore`. Add `GROQ_API_KEY` as a GitHub Secret for CI.

---

## 📋 Usage

### Generate tests from a feature

```bash
python scripts/generate_tests.py features/sample_feature.md python
python scripts/generate_tests.py features/sample_feature.md typescript
```

### Run Python tests with coverage

```bash
pytest tests/python/ -v --cov=tests/python --cov-report=term-missing --import-mode=importlib
```

### Run TypeScript tests

```bash
npm test
npm run test:coverage
```

### Manage coverage gaps

```bash
python scripts/coverage_gap_tracker.py list
python scripts/coverage_gap_tracker.py open
python scripts/coverage_gap_tracker.py close GAP-002
python scripts/coverage_gap_tracker.py add "Feature" "Area" "high" "Notes"
python scripts/coverage_gap_tracker.py report
```

---

## 📊 Sample Output

```
collected 8 items

test_regression.py::TestAuthRegistration::test_valid_registration_payload_shape PASSED
test_regression.py::TestAuthRegistration::test_password_minimum_length PASSED
test_regression.py::TestAuthRegistration::test_valid_password_length PASSED
test_regression.py::TestAuthTokens::test_token_structure PASSED
test_regression.py::TestAuthTokens::test_empty_token_rejected PASSED
test_regression.py::TestResponsePatterns::test_success_response_shape PASSED
test_regression.py::TestResponsePatterns::test_unauthorized_response_shape PASSED
test_regression.py::TestResponsePatterns::test_duplicate_email_response_shape PASSED

---------- coverage ----------
TOTAL    100%

==================================================
COVERAGE GAPS (2 found)
==================================================
[GAP-002] User Authentication — Token invalidation on logout
  Status  : open
  Priority: medium

[GAP-003] Payments — Refund flow
  Status  : open
  Priority: high
```

---

## 🔄 Day-to-Day Workflow

```
New feature arrives
       ↓
Write features/my_feature.md
       ↓
python scripts/generate_tests.py features/my_feature.md python
       ↓
Review & edit the generated test file
       ↓
pytest tests/python/ -v --cov=tests/python
       ↓
python scripts/coverage_gap_tracker.py report
       ↓
git push  →  GitHub Actions runs everything automatically
```

---

## 💡 Key Design Decisions

**Why Groq?** Free tier with no credit card, fast inference, and generous rate limits (14,400 requests/day). Ideal for a dev tooling project where you're running generation frequently.

**Why separate generated vs hand-written tests?** AI-generated tests are a starting point — they get reviewed and adjusted. The regression baseline (`test_regression.py`) is always hand-authored and represents ground truth that must never break.

**Why a JSON gap tracker instead of a proper database?** Simplicity. The gaps file lives in the repo, gets committed alongside code, and is visible in PRs. No external tooling needed.

**Why both Python and TypeScript?** Real projects have mixed stacks. Demonstrating reusable patterns in both languages makes the test infrastructure more broadly applicable.

---

## 🔐 Security Notes

- API keys are stored in `.env` locally and as GitHub Secrets in CI
- `.env` is in `.gitignore` and must never be committed
- Rotate keys immediately if accidentally exposed in git history

---

## 📄 License

MIT
