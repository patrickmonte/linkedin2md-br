"""Career-Ops export module for linkedin2md.

Generates data packages compatible with career-ops
(https://github.com/career-ops-hq/career-ops):
- cv.md: Master CV in structured Markdown.
- config/profile.yml: Candidate profile and targeting configuration.
- data/applications.md: Job application tracker table.
- README.md: Usage instructions.

Zero external dependencies: uses Python standard library only.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from linkedin2md.i18n import (
    localize_date,
    normalize_language,
    translate,
    translate_language_name,
    translate_proficiency,
)
from linkedin2md.protocols import MultilingualText

logger = logging.getLogger(__name__)


def _yaml_escape(val: str) -> str:
    """Escape and quote a string for YAML output."""
    escaped = (
        val.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "")
        .replace("\n", "\\n")
    )
    return f'"{escaped}"'


def _get_text(val: Any, lang: str) -> str:
    """Extract text in preferred language."""
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    if isinstance(val, MultilingualText):
        return val.get(normalize_language(lang))
    if isinstance(val, dict):
        norm = normalize_language(lang)
        sub = (
            val.get(norm)
            or val.get("en")
            or val.get("pt")
            or val.get("es")
            or val.get("text")
            or ""
        )
        return _get_text(sub, lang)
    return str(val)


def _format_iso_date(date_str: str) -> str:
    """Format diverse date inputs into ISO YYYY-MM-DD if possible."""
    if not date_str:
        return "-"
    clean = date_str.strip()
    date_part = clean.split(",")[0].strip()
    formats = [
        "%m/%d/%Y",
        "%m/%d/%y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%Y/%m/%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_part, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return clean


def _extract_primary_roles(
    headline: str, experiences: list[dict[str, Any]], lang: str
) -> list[str]:
    """Infer 1-3 primary target roles from headline and recent positions."""
    roles: list[str] = []
    seen: set[str] = set()

    def add_role(role_name: str) -> None:
        cleaned = re.sub(r"[\r\n\t]+", " ", role_name).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        # Avoid excessively long compound strings
        if cleaned and len(cleaned) <= 60:
            lower = cleaned.lower()
            if lower not in seen:
                roles.append(cleaned)
                seen.add(lower)

    # 1. Check recent positions in experience
    for exp in experiences[:3]:
        role_text = _get_text(exp.get("role"), lang)
        if role_text:
            add_role(role_text)

    # 2. Check headline segments (often separated by |, /, or -)
    if headline:
        segments = re.split(r"[\s]*[|/•][\s]*", headline)
        for seg in segments:
            seg = seg.strip()
            # Exclude buzzword fragments like "+20 anos" or certifications
            if seg and not re.search(r"^\+?\d+\s*anos", seg, re.IGNORECASE):
                add_role(seg)

    if not roles and headline:
        add_role(headline)

    return roles[:3] if roles else ["Software Engineer"]


def _extract_location_details(location: str) -> tuple[str, str, str]:
    """Extract city, country, and currency from location string."""
    if not location:
        return "", "", "USD"

    parts = [p.strip() for p in location.split(",") if p.strip()]
    city = parts[0] if parts else ""
    country = parts[-1] if len(parts) > 1 else parts[0]

    country_lower = country.lower()
    if any(
        b in country_lower for b in ["brazil", "brasil", "ceará", "ceara", "sp", "rj"]
    ):
        currency = "BRL"
        if country_lower in ["ceará", "ceara", "sp", "rj"]:
            country = "Brazil"
    elif any(
        uk in country_lower for uk in ["united kingdom", "uk", "england", "scotland"]
    ):
        currency = "GBP"
    elif any(
        eu in country_lower
        for eu in [
            "spain",
            "españa",
            "germany",
            "deutschland",
            "france",
            "italy",
            "portugal",
            "netherlands",
        ]
    ):
        currency = "EUR"
    else:
        currency = "USD"

    return city, country, currency


def generate_career_ops_profile_yaml(data: dict[str, Any], lang: str = "en") -> str:
    """Generate config/profile.yml content for career-ops."""
    norm_lang = normalize_language(lang)
    lang_output = "pt-BR" if norm_lang == "pt" else norm_lang

    profile = data.get("profile", {})
    if not isinstance(profile, dict):
        profile = {}

    meta = profile.get("profile_meta", {})
    if not isinstance(meta, dict):
        meta = {}

    full_name = profile.get("name", "")
    headline = _get_text(profile.get("title"), lang)
    email = profile.get("email", "")
    phone = profile.get("phone", "")
    location = profile.get("location", "")

    city, country, currency = _extract_location_details(location)
    if norm_lang == "pt" and currency == "USD" and not country:
        currency = "BRL"

    # Social & Links
    linkedin_raw = meta.get("public_profile_url") or ""
    linkedin = re.sub(r"^https?://(www\.)?", "", linkedin_raw).rstrip("/")

    twitter_handle = meta.get("twitter") or ""
    twitter = f"https://x.com/{twitter_handle}" if twitter_handle else ""

    websites = meta.get("websites") or []
    github = ""
    portfolio_url = ""
    for w in websites:
        if "github.com" in w.lower() and not github:
            github = re.sub(r"^https?://(www\.)?", "", w).rstrip("/")
        elif not portfolio_url:
            portfolio_url = w

    experiences = data.get("experience", [])
    if not isinstance(experiences, list):
        experiences = []

    primary_roles = _extract_primary_roles(headline, experiences, lang)

    # Superpowers from top skills
    skills = data.get("skills", [])
    if not isinstance(skills, list):
        skills = []
    superpowers = [s for s in skills[:5] if isinstance(s, str) and s.strip()]

    lines = [
        "# Career-Ops Profile Configuration",
        "# Generated by linkedin2md for career-ops (https://github.com/career-ops-hq/career-ops)",
        "",
        "candidate:",
        f"  full_name: {_yaml_escape(full_name)}",
        f"  title: {_yaml_escape(headline)}",
        f"  email: {_yaml_escape(email)}",
        f"  phone: {_yaml_escape(phone)}",
        f"  location: {_yaml_escape(location)}",
        f"  linkedin: {_yaml_escape(linkedin)}",
        f"  portfolio_url: {_yaml_escape(portfolio_url)}",
        f"  github: {_yaml_escape(github)}",
        f"  twitter: {_yaml_escape(twitter)}",
        '  photo: ""',
        "  photo_style: rounded",
        "",
        "target_roles:",
        "  primary:",
    ]
    for role in primary_roles:
        lines.append(f"    - {_yaml_escape(role)}")

    lines.extend(
        [
            "  archetypes:",
            f"    - name: {_yaml_escape(primary_roles[0])}",
            '      level: "Senior"',
            '      fit: "primary"',
            "",
            "narrative:",
            f"  headline: {_yaml_escape(headline)}",
            '  exit_story: ""',
            "  superpowers:",
        ]
    )
    if superpowers:
        for p in superpowers:
            lines.append(f"    - {_yaml_escape(p)}")
    else:
        lines.append('    - "Problem Solving"')

    lines.extend(
        [
            "  proof_points: []",
            "",
            "compensation:",
            '  target_range: ""',
            f"  currency: {_yaml_escape(currency)}",
            '  minimum: ""',
            '  location_flexibility: "Remote preferred"',
            "",
            "location:",
            f"  country: {_yaml_escape(country)}",
            f"  city: {_yaml_escape(city)}",
            '  timezone: ""',
            '  visa_status: "No sponsorship needed"',
            "  authorized_in:",
        ]
    )
    if country:
        lines.append(f"    - {_yaml_escape(country)}")
    else:
        lines.append('    - "United States"')

    lines.extend(
        [
            "  needs_sponsorship: false",
            "",
            "language:",
            f"  output: {_yaml_escape(lang_output)}",
            "",
            "spend_tier: standard",
            "",
        ]
    )

    return "\n".join(lines)


def generate_career_ops_cv_markdown(data: dict[str, Any], lang: str = "en") -> str:
    """Generate cv.md (Master CV) for career-ops."""
    lines: list[str] = []

    profile = data.get("profile", {})
    if not isinstance(profile, dict):
        profile = {}

    meta = profile.get("profile_meta", {})
    if not isinstance(meta, dict):
        meta = {}

    name = profile.get("name", "")
    if name:
        lines.append(f"# {name}")
        lines.append("")

    title = _get_text(profile.get("title"), lang)
    if title:
        lines.append(f"**{title}**")
        lines.append("")

    # Contact line
    contacts: list[str] = []
    if profile.get("location"):
        contacts.append(str(profile["location"]))
    if profile.get("email"):
        contacts.append(str(profile["email"]))
    if profile.get("phone"):
        contacts.append(str(profile["phone"]))
    if meta.get("public_profile_url"):
        contacts.append(str(meta["public_profile_url"]))
    elif meta.get("twitter"):
        contacts.append(f"x.com/{meta['twitter']}")
    websites = meta.get("websites") or []
    for w in websites:
        if w not in contacts:
            contacts.append(w)

    if contacts:
        lines.append(" | ".join(contacts))
        lines.append("")

    # Summary
    summary = _get_text(profile.get("summary"), lang)
    if summary:
        lines.append(f"## {translate('Summary', lang)}")
        lines.append("")
        lines.append(summary)
        lines.append("")

    # Experience
    experiences = data.get("experience", [])
    if isinstance(experiences, list) and experiences:
        lines.append(f"## {translate('Experience', lang)}")
        lines.append("")
        for exp in experiences:
            role = _get_text(exp.get("role"), lang) or "Role"
            company = exp.get("company", "Company")
            lines.append(f"### {role} — {company}")

            start = localize_date(str(exp.get("start", "")), lang)
            end = exp.get("end")
            end_str = (
                localize_date(str(end), lang) if end else translate("Present", lang)
            )
            dates = f"*{start} – {end_str}*" if start else f"*{end_str}*"
            location = exp.get("location")
            if location:
                dates += f" | *{location}*"
            lines.append(dates)
            lines.append("")

            achievements = exp.get("achievements", [])
            if isinstance(achievements, list) and achievements:
                for ach in achievements:
                    ach_text = _get_text(ach, lang)
                    if ach_text:
                        lines.append(f"- {ach_text}")
                lines.append("")
            elif exp.get("description"):
                desc = _get_text(exp.get("description"), lang)
                if desc:
                    lines.append(desc)
                    lines.append("")

    # Education
    educations = data.get("education", [])
    if isinstance(educations, list) and educations:
        lines.append(f"## {translate('Education', lang)}")
        lines.append("")
        for edu in educations:
            inst = edu.get("institution", "University")
            degree = _get_text(edu.get("degree"), lang)
            field = edu.get("field")
            if degree and field:
                header = f"{degree} ({field}) — {inst}"
            elif degree:
                header = f"{degree} — {inst}"
            else:
                header = inst

            lines.append(f"### {header}")
            start = edu.get("start", "")
            end = edu.get("end", "")
            if start and end:
                lines.append(f"*{start} – {end}*")
            elif start or end:
                lines.append(f"*{start or end}*")

            notes = _get_text(edu.get("notes"), lang)
            if notes:
                lines.append(f"- {notes}")
            activities = edu.get("activities")
            if activities:
                lines.append(f"- {activities}")
            lines.append("")

    # Skills
    skills = data.get("skills", [])
    if isinstance(skills, list) and skills:
        lines.append(f"## {translate('Skills', lang)}")
        lines.append("")
        clean_skills = [s.strip() for s in skills if isinstance(s, str) and s.strip()]
        if clean_skills:
            lines.append(
                f"- **{translate('Skills', lang)}:** {', '.join(clean_skills)}"
            )
            lines.append("")

    # Certifications
    certs = data.get("certifications", [])
    if isinstance(certs, list) and certs:
        lines.append(f"## {translate('Certifications', lang)}")
        lines.append("")
        for c in certs:
            c_name = c.get("name", "")
            issuer = c.get("issuer", "")
            date_raw = c.get("date", "")
            c_date = localize_date(date_raw, lang) if date_raw else ""
            url = c.get("url")

            item = f"- **{c_name}**"
            if issuer:
                item += f" — {issuer}"
            if c_date:
                item += f" (*{c_date}*)"
            if url:
                label = translate("View Certificate", lang)
                item += f" [{label}]({url})"
            lines.append(item)
        lines.append("")

    # Languages
    langs = data.get("languages", [])
    if isinstance(langs, list) and langs:
        lines.append(f"## {translate('Languages', lang)}")
        lines.append("")
        for l_item in langs:
            l_name = l_item.get("name", "")
            l_name_tr = translate_language_name(l_name, lang)
            prof = l_item.get("proficiency")
            prof_tr = translate_proficiency(prof, lang) if prof else ""
            if prof_tr:
                lines.append(f"- {l_name_tr} ({prof_tr})")
            else:
                lines.append(f"- {l_name_tr}")
        lines.append("")

    # Projects
    projects = data.get("projects", [])
    if isinstance(projects, list) and projects:
        lines.append(f"## {translate('Projects', lang)}")
        lines.append("")
        for p in projects:
            p_title = p.get("title", "")
            lines.append(f"### {p_title}")
            start = localize_date(str(p.get("start", "")), lang)
            end = localize_date(str(p.get("end", "")), lang) if p.get("end") else ""
            if start and end:
                lines.append(f"*{start} – {end}*")
            elif start or end:
                lines.append(f"*{start or end}*")

            desc = _get_text(p.get("description"), lang)
            if desc:
                lines.append(desc)
            url = p.get("url")
            if url:
                label = translate("View project", lang)
                lines.append(f"[{label}]({url})")
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def generate_career_ops_applications_md(data: dict[str, Any]) -> str:
    """Generate data/applications.md tracking table for career-ops."""
    lines = [
        "# Applications Tracker",
        "",
        "| # | Date | Company | Role | Status | Score | PDF | Report | Notes | URL |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]

    apps = data.get("job_applications", [])
    if isinstance(apps, list):
        for idx, a in enumerate(apps, start=1):
            date_raw = a.get("date", "")
            date_str = _format_iso_date(date_raw)
            company = str(a.get("company", "-")).replace("|", "\\|")
            role = str(a.get("title", "-")).replace("|", "\\|")

            if a.get("withdraw_date"):
                status = "Withdrawn"
            else:
                status = str(a.get("status") or "Applied").replace("|", "\\|")

            url_raw = a.get("url")
            if url_raw and isinstance(url_raw, str) and url_raw.startswith("http"):
                url_cell = f"[Link]({url_raw})"
            else:
                url_cell = "-"

            notes = "Imported from LinkedIn"

            row = (
                f"| {idx} | {date_str} | {company} | {role} | {status} |"
                f" - | no | - | {notes} | {url_cell} |"
            )
            lines.append(row)

    lines.append("")
    return "\n".join(lines)


def generate_career_ops_readme(lang: str = "en") -> str:
    """Generate instructions README.md for the career-ops package."""
    norm_lang = normalize_language(lang)
    if norm_lang == "pt":
        return (
            "# Pacote de Dados para Career-Ops\n\n"
            "Este pacote foi gerado pelo "
            "[linkedin2md](https://github.com/juanmanueldaza/linkedin2md) "
            "para uso com o "
            "[career-ops](https://github.com/career-ops-hq/career-ops) "
            "— o agente de busca e candidatura profissional com IA.\n\n"
            "## Arquivos inclusos\n\n"
            "- `cv.md`: Seu Currículo Mestre (Master CV) em formato "
            "Markdown estruturado. O career-ops utiliza este arquivo como "
            "verdade imutável para avaliar vagas e gerar currículos ATS "
            "sob medida.\n"
            "- `config/profile.yml`: Configurações do candidato, objetivos de "
            "carreira, competências principais (superpowers), faixas salariais "
            "e regras de localização.\n"
            "- `data/applications.md`: Tabela rastreadora de candidaturas (Tracker) "
            "preenchida com o histórico importado do LinkedIn.\n\n"
            "## Como usar no Career-Ops\n\n"
            "### Opção 1: Inicializar o Career-Ops diretamente nesta pasta\n"
            "Se você possui uma CLI de programação com IA "
            "(como Claude Code, OpenCode ou Codex):\n"
            "```bash\n"
            "npx @santifer/career-ops init\n"
            "```\n"
            "O career-ops reconhecerá automaticamente seus arquivos `cv.md` e "
            "`config/profile.yml`.\n\n"
            "### Opção 2: Copiar para um projeto existente do Career-Ops\n"
            "Caso já tenha um repositório configurado:\n"
            "1. Copie `cv.md` para a raiz do seu repositório `career-ops`.\n"
            "2. Copie `config/profile.yml` para a pasta `config/`.\n"
            "3. Copie `data/applications.md` para a pasta `data/`.\n\n"
            "Para documentação completa, visite: "
            "https://github.com/career-ops-hq/career-ops\n"
        )
    elif norm_lang == "es":
        return (
            "# Paquete de Datos para Career-Ops\n\n"
            "Este paquete fue generado por "
            "[linkedin2md](https://github.com/juanmanueldaza/linkedin2md) "
            "para usar con "
            "[career-ops](https://github.com/career-ops-hq/career-ops) "
            "— el agente de búsqueda y postulación laboral con IA.\n\n"
            "## Archivos incluidos\n\n"
            "- `cv.md`: Tu CV Maestro (Master CV) en formato Markdown estructurado.\n"
            "- `config/profile.yml`: Configuración de perfil, objetivos de puesto y "
            "políticas de postulación.\n"
            "- `data/applications.md`: Tabla de seguimiento de postulaciones "
            "importadas de LinkedIn.\n\n"
            "## Cómo usar en Career-Ops\n\n"
            "```bash\n"
            "npx @santifer/career-ops init\n"
            "```\n\n"
            "Más información en: https://github.com/career-ops-hq/career-ops\n"
        )
    return (
        "# Career-Ops Data Package\n\n"
        "This directory was generated by "
        "[linkedin2md](https://github.com/juanmanueldaza/linkedin2md) "
        "for use with "
        "[career-ops](https://github.com/career-ops-hq/career-ops) "
        "— the open-source AI job search agent.\n\n"
        "## Included Files\n\n"
        "- `cv.md`: Master Curriculum Vitae in structured Markdown. "
        "Career-ops uses this file as the baseline to evaluate job postings "
        "and dynamically tailor ATS-friendly resumes.\n"
        "- `config/profile.yml`: Candidate configuration containing contact "
        "information, target roles, narrative superpowers, compensation, and "
        "location policies.\n"
        "- `data/applications.md`: Application tracking table pre-populated "
        "with your past LinkedIn job applications.\n\n"
        "## How to Use with Career-Ops\n\n"
        "### Option 1: Initialize Career-Ops in this directory\n"
        "Run the initializer in your AI coding CLI (Claude Code, OpenCode, Codex):\n"
        "```bash\n"
        "npx @santifer/career-ops init\n"
        "```\n\n"
        "### Option 2: Copy to an existing Career-Ops repository\n"
        "1. Copy `cv.md` to your career-ops project root.\n"
        "2. Copy `config/profile.yml` into your `config/` directory.\n"
        "3. Copy `data/applications.md` into your `data/` directory.\n\n"
        "For more details, visit: https://github.com/career-ops-hq/career-ops\n"
    )


def export_career_ops(
    data: dict[str, Any], output_dir: Path, lang: str = "en"
) -> list[Path]:
    """Export LinkedIn parsed data package for career-ops.

    Creates:
    - <output_dir>/cv.md
    - <output_dir>/config/profile.yml
    - <output_dir>/data/applications.md
    - <output_dir>/README.md

    Args:
        data: Parsed data dictionary from LinkedInToMarkdownConverter
        output_dir: Target directory for the career-ops package
        lang: Language for text generation (en, es, pt)

    Returns:
        List of generated file Paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    config_dir = output_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    created_files: list[Path] = []

    # 1. cv.md
    cv_path = output_dir / "cv.md"
    cv_content = generate_career_ops_cv_markdown(data, lang=lang)
    cv_path.write_text(cv_content, encoding="utf-8")
    created_files.append(cv_path)

    # 2. config/profile.yml
    profile_path = config_dir / "profile.yml"
    profile_content = generate_career_ops_profile_yaml(data, lang=lang)
    profile_path.write_text(profile_content, encoding="utf-8")
    created_files.append(profile_path)

    # 3. data/applications.md
    apps_path = data_dir / "applications.md"
    apps_content = generate_career_ops_applications_md(data)
    apps_path.write_text(apps_content, encoding="utf-8")
    created_files.append(apps_path)

    # 4. README.md
    readme_path = output_dir / "README.md"
    readme_content = generate_career_ops_readme(lang=lang)
    readme_path.write_text(readme_content, encoding="utf-8")
    created_files.append(readme_path)

    return created_files
