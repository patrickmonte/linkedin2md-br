# linkedin2md — v0.8.0

[![PyPI version](https://img.shields.io/pypi/v/linkedin2md?style=flat-square&label=PyPI)](https://pypi.org/project/linkedin2md/)
[![Python versions](https://img.shields.io/pypi/pyversions/linkedin2md)](https://pypi.org/project/linkedin2md/)
[![License](https://img.shields.io/pypi/l/linkedin2md)](https://github.com/juanmanueldaza/linkedin2md/blob/main/LICENSE)
[![PyPI Downloads](https://img.shields.io/pypi/dm/linkedin2md?style=flat-square)](https://pypi.org/project/linkedin2md/)
[![GitHub stars](https://img.shields.io/github/stars/juanmanueldaza/linkedin2md?style=flat-square)](https://github.com/juanmanueldaza/linkedin2md)
[![CI](https://github.com/juanmanueldaza/linkedin2md/actions/workflows/ci.yml/badge.svg)](https://github.com/juanmanueldaza/linkedin2md/actions/workflows/ci.yml)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/juanmanueldaza/linkedin2md/issues)
[![Good First Issues](https://img.shields.io/github/issues/juanmanueldaza/linkedin2md/good%20first%20issue?style=flat-square&label=good%20first%20issues)](https://github.com/juanmanueldaza/linkedin2md/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

Convert LinkedIn data exports to clean Markdown files - the ideal format for LLM analysis.

## Why Markdown?

Markdown is the lingua franca of AI tools. Once your LinkedIn data is in `.md` format, you can:

- **Upload to [NotebookLM](https://notebooklm.google.com/)** and have conversations about your career history
- **Use [Claude Projects](https://claude.ai)** to analyze patterns across your professional journey
- **Feed to [Obsidian](https://obsidian.md/)** with AI plugins for a personal career knowledge base
- **Run local LLMs** (Ollama, LM Studio) for completely private analysis

### Example Prompts

Once your LinkedIn data is in an LLM, try asking:

| Question | Data Used |
|----------|-----------|
| "What patterns do you see in my career transitions?" | experience.md |
| "What skills have I developed over time?" | skills.md, experience.md |
| "Group my connections by industry" | connections.md |
| "What themes appear in my recommendations?" | recommendations.md |
| "Summarize my job applications and outcomes" | job_applications.md |
| "What qualities do people consistently mention about me?" | recommendations.md, endorsements.md |
| "Based on my experience, what roles should I target?" | All files |

## System Requirements

`linkedin2md` has a **zero-dependency core** (pure Python standard library) for core Markdown conversion and Career-Ops export.

| Platform | Supported Versions | Notes |
|----------|-------------------|-------|
| **Windows** | Windows 10, 11, Windows Server | PowerShell 5.1+, PowerShell 7+, Command Prompt, Windows Terminal |
| **Linux** | Debian, Ubuntu 20.04+, Fedora, Arch, Alpine | All distributions with Python 3.10+ |
| **macOS** | macOS 12 (Monterey) or later | Apple Silicon (M1/M2/M3/M4) & Intel (x86_64) |
| **Python** | 3.10, 3.11, 3.12, 3.13, 3.14 | Standard CPython |

### Optional Feature Requirements

*   **PDF Resume Generation (`--pdf`)**: Requires `weasyprint` and `markdown`:
    *   **Windows**: Wheels bundle all native libraries automatically (`pip install weasyprint markdown`).
    *   **Linux (Ubuntu/Debian)**: `sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b` then `pip install weasyprint markdown`.
    *   **macOS**: `brew install pango` then `pip install weasyprint markdown`.
*   **Career-Ops Integration (`--career-ops`)**:
    *   Exporting the package requires only `linkedin2md` (**zero external dependencies**).
    *   Executing the AI search agent in the exported folder requires **Node.js 18+** (for `npx @santifer/career-ops init`) and an AI coding CLI (Claude Code, OpenCode, Codex, Cursor, etc.).

## Installation

### Recommended (All Platforms via pipx)

Installs `linkedin2md` in an isolated environment and exposes it globally:

```bash
pipx install linkedin2md
```

### Windows

Open **PowerShell** or **Command Prompt**:

```powershell
# Using pip:
pip install linkedin2md

# Or using uv tool (fastest):
uv tool install linkedin2md
```

### Linux (Ubuntu, Debian, Fedora, Arch)

```bash
# Using pipx (recommended, prevents PEP 668 externally-managed-environment errors):
sudo apt install pipx  # on Debian/Ubuntu
pipx ensurepath
pipx install linkedin2md

# Or using uv:
uv tool install linkedin2md
```

### macOS

Open **Terminal**:

```bash
# Using Homebrew + pipx:
brew install pipx
pipx ensurepath
pipx install linkedin2md

# Or using uv:
uv tool install linkedin2md
```

## Usage & Parameter Reference

### Quick Examples

```bash
# Standard conversion (creates linkedin_export/ with 40+ clean markdown files)
linkedin2md Complete_LinkedInDataExport.zip

# Custom output directory
linkedin2md export.zip -o ./my-profile

# Export in Brazilian Portuguese
linkedin2md export.zip --lang pt

# Export in Spanish
linkedin2md export.zip --lang es

# Export ready-to-use package for career-ops AI agent
linkedin2md export.zip --career-ops ./my-career-ops --lang pt

# Generate elegant A4 PDF resume alongside Markdown files
linkedin2md export.zip --lang pt --pdf

# CI/CD / Automated audit mode: fail on omissions and generate private JSON diagnostics
linkedin2md export.zip --strict --report diagnostics.json -q
```

### Parameter Reference

| Parameter | Type / Format | Default | Description |
|-----------|---------------|---------|-------------|
| `source` | `Path` (Positional) | *Required* | Path to LinkedIn data ZIP file (`Complete_LinkedInDataExport_*.zip` or `Basic_LinkedInDataExport_*.zip`). |
| `-o`, `--output` | `Directory Path` | `linkedin_export` | Destination directory for converted Markdown files. Created automatically if it does not exist. |
| `--lang` | `Choice` | `en` | Target prose language for headings, tables, labels, and dates. Supported values: `en`, `pt` (or `pt-BR`, `pt_BR`, `portuguese`), `es` (or `spanish`). |
| `--career-ops [DIR]` | `Directory Path` (Optional) | `None` | Exports master CV (`cv.md`), configuration (`config/profile.yml`), applications tracker (`data/applications.md`), and instructions for [career-ops](https://github.com/career-ops-hq/career-ops). Defaults to `<output>/career-ops` if passed without path. |
| `--pdf` | `Flag` | `False` | Renders a print-ready A4 executive PDF resume (`profile.pdf`) from your profile and experience data. Fully localized according to `--lang`. |
| `--strict` | `Flag` | `False` | Enforces strict conversion integrity; exits with status code `1` if diagnostics report unconsumed CSV files or extraction anomalies. |
| `--report PATH` | `File Path` | `None` | Writes a private JSON diagnostics report with timing per section, CSV key coverage, and integrity verification. |
| `-q`, `--quiet` | `Flag` | `False` | Suppresses stdout progress and file listing messages. Ideal for scripts and background processing. |
| `--version` | `Flag` | - | Displays installed version (`linkedin2md 0.8.0`) and exits. |
| `-h`, `--help` | `Flag` | - | Displays command-line help and usage reference. |

## How to Export Your LinkedIn Data

Follow these steps to download your LinkedIn data:

1. **Go to Settings**: Log into LinkedIn, click your profile photo in the top right, then select **"Settings & Privacy"**

2. **Navigate to Data Privacy**: In the left sidebar, click **"Data privacy"**

3. **Request your data**: Click **"Get a copy of your data"**

4. **Select data to download**: 
   - Choose **"Download larger data archive"** for complete data
   - Or select specific categories if you only need certain data

5. **Request archive**: Click **"Request archive"**

6. **Wait for email**: LinkedIn will process your request and send an email when ready (usually within 24 hours, sometimes up to 72 hours for large archives)

7. **Download the ZIP file**: Click the download link in the email. The file will be named something like `Complete_LinkedInDataExport_01-20-2025.zip`

> **Note**: The download link expires after a few days. Download it promptly and store it safely.

## LLM Tools That Work Great With This

| Tool | Type | Best For |
|------|------|----------|
| [NotebookLM](https://notebooklm.google.com/) | Cloud | Conversational analysis, audio summaries |
| [Claude Projects](https://claude.ai) | Cloud | Deep analysis, long context |
| [ChatGPT](https://chat.openai.com) | Cloud | General analysis, quick insights |
| [Obsidian](https://obsidian.md/) + AI plugins | Local | Personal knowledge base, linked notes |
| [Open Notebook](https://github.com/Open-Notebook/Open-Notebook) | Local/Cloud | 16+ AI models, open source |
| [Ollama](https://ollama.ai/) | Local | Private, offline analysis |

## Output

Creates 40+ markdown files in the output directory, organized by category:

### Core Profile
- `profile.md` - Name, title, contact, summary
- `experience.md` - Work history with achievements
- `education.md` - Educational background
- `skills.md` - Professional skills
- `certifications.md` - Certifications and licenses
- `languages.md` - Language proficiencies
- `projects.md` - Personal and professional projects

### Recommendations & Endorsements
- `recommendations.md` - Recommendations received
- `endorsements.md` - Skill endorsements received

### Learning
- `learning.md` - LinkedIn Learning courses
- `learning_reviews.md` - Course reviews and ratings

### Network
- `connections.md` - Your connections
- `companies_followed.md` - Companies you follow
- `members_followed.md` - People you follow
- `invitations.md` - Connection invitations sent/received
- `imported_contacts.md` - Contacts imported from address book

### Content & Activity
- `posts.md` - Your posts and shares
- `comments.md` - Comments you made
- `reactions.md` - Likes and reactions
- `reposts.md` - Content you reposted
- `votes.md` - Poll votes
- `saved_items.md` - Bookmarked content
- `events.md` - Events attended

### Job Search
- `job_applications.md` - All job applications
- `saved_jobs.md` - Jobs you saved
- `job_preferences.md` - Job seeker preferences
- `saved_job_answers.md` - Saved application answers
- `screening_responses.md` - Screening question responses
- `saved_job_alerts.md` - Job alert settings

### Activity History
- `search_queries.md` - Search history
- `logins.md` - Login history
- `security_challenges.md` - Security verification events

### Advertising & Privacy
- `ads_clicked.md` - Ads you clicked
- `ad_targeting.md` - How LinkedIn targets ads to you
- `lan_ads.md` - LinkedIn Audience Network engagement
- `inferences.md` - LinkedIn's inferences about you

### Payments
- `receipts.md` - Premium subscription receipts

### Services Marketplace
- `service_engagements.md` - Service provider engagements
- `service_opportunities.md` - Service opportunities

### Identity
- `verifications.md` - Identity verifications
- `identity_assets.md` - Uploaded documents (resumes, etc.)

## 📄 PDF Resume Generation

With the `--pdf` flag, `linkedin2md` converts your parsed structured data into an elegant, print-ready, professional A4 PDF Resume (`profile.pdf`):

*   **Design**: Hand-crafted executive layout with pristine typography, clean margins, and print-friendly stylesheets.
*   **Prerequisites**: Requires `weasyprint` and `markdown` libraries to be installed locally:
    ```bash
    pip install weasyprint markdown
    ```
    *(If not installed, `linkedin2md` will continue to generate your Markdown folder safely, omitting the PDF and providing setup instructions).*

## 🎯 Export for Career-Ops

With the `--career-ops` flag, `linkedin2md` exports your LinkedIn history directly into a package ready for [career-ops](https://github.com/career-ops-hq/career-ops) — the open-source AI job search agent:

```bash
# Export into ./career-ops directory
linkedin2md export.zip --career-ops

# Or specify a custom target directory
linkedin2md export.zip --career-ops ./my-career-ops

# Localized for Brazilian Portuguese
linkedin2md export.zip --career-ops --lang pt
```

This generates:
- `cv.md`: Master Curriculum Vitae in Markdown used by career-ops to evaluate job matches and tailor ATS resumes.
- `config/profile.yml`: Candidate configuration with your contact details, target roles, superpowers, location policies, and language settings (`output: pt-BR` when `--lang pt` is used).
- `data/applications.md`: Flat-file application tracker pre-populated with your past LinkedIn job applications.
- `README.md`: Setup and quick-start instructions for initializing career-ops via `npx @santifer/career-ops init`.

## 🤖 Agentic Development ([N3RV](https://github.com/juanmanueldaza/n3rv) Framework)

This repository is fully configured for **Agentic Development** using [opencode](https://opencode.ai) and the [N3RV](https://github.com/juanmanueldaza/n3rv) orchestration framework. N3RV coordinates specialized autonomous subagents to design, program, test, and audit code changes.

### Install N3RV

```bash
git clone https://github.com/juanmanueldaza/n3rv.git ~/n3rv
cd ~/n3rv && uv tool install .
cd /path/to/linkedin2md
n3rv init
```

### Quick Commands (Inside Opencode/Claude Code TUI):

*   **SDD Pipeline (`/sdd-new <change>`)**: Starts the 8-phase Spec-Driven Development workflow (explore ➔ propose ➔ spec ➔ design ➔ tasks ➔ apply ➔ verify ➔ archive) utilizing custom subagents in `.opencode/agents/` and `.opencode/skills/`.
*   **Adversarial Review (`/judgment-day`)**: Triggers a dual-model adversarial code review (e.g. Claude vs. Copilot) to stress-test pull requests against `AGENTS.md` standards.
*   **Standards Audit (`/review`)**: Automatically audits files against strict linting and universal code standards.

We welcome PRs developed and verified using your own AI agent setups!

## Contributing

We welcome contributions from everyone! Whether it's a bug fix, new feature, improved documentation, or a translation — we'd love your help.

- See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, coding standards, and PR workflow.
- Look for [good first issues](https://github.com/juanmanueldaza/linkedin2md/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) for beginner-friendly tasks.
- Be respectful, inclusive, and constructive in all interactions.

## License

GPL-2.0 - see [LICENSE](LICENSE) for details.
