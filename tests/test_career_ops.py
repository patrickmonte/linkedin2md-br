from pathlib import Path
from unittest.mock import patch

from linkedin2md.career_ops import (
    _format_iso_date,
    _yaml_escape,
    export_career_ops,
    generate_career_ops_applications_md,
    generate_career_ops_cv_markdown,
    generate_career_ops_profile_yaml,
    generate_career_ops_readme,
)
from linkedin2md.cli import _parse_args, main
from linkedin2md.protocols import MultilingualText


class TestCareerOpsYamlGeneration:
    """Tests for YAML profile configuration generation."""

    def test_yaml_escaping(self):
        """Test escaping quotes, newlines, and backslashes."""
        assert _yaml_escape('hello "world"') == r'"hello \"world\""'
        assert _yaml_escape("line1\nline2") == r'"line1\nline2"'
        assert _yaml_escape(r"path\to\file") == r'"path\\to\\file"'

    def test_profile_yaml_generation(self):
        """Test generation of config/profile.yml."""
        data = {
            "profile": {
                "name": "Alex Doe",
                "title": "Senior AI Engineer",
                "email": "alex@example.com",
                "phone": "+1 555 0100",
                "location": "San Francisco, CA, United States",
                "profile_meta": {
                    "public_profile_url": "https://www.linkedin.com/in/alexdoe",
                    "twitter": "alexdoe",
                    "websites": ["https://github.com/alexdoe", "https://alexdoe.dev"],
                },
            },
            "experience": [
                {
                    "company": "Tech Corp",
                    "role": "Staff Engineer",
                    "start": "2020",
                    "end": None,
                }
            ],
            "skills": ["Python", "PyTorch", "Kubernetes", "Docker", "Go"],
        }
        yaml_content = generate_career_ops_profile_yaml(data, lang="en")
        assert 'full_name: "Alex Doe"' in yaml_content
        assert 'email: "alex@example.com"' in yaml_content
        assert 'title: "Senior AI Engineer"' in yaml_content
        assert 'linkedin: "linkedin.com/in/alexdoe"' in yaml_content
        assert 'github: "github.com/alexdoe"' in yaml_content
        assert 'twitter: "https://x.com/alexdoe"' in yaml_content
        assert 'output: "en"' in yaml_content
        assert 'currency: "USD"' in yaml_content
        assert 'name: "Staff Engineer"' in yaml_content
        assert '- "Python"' in yaml_content

    def test_profile_yaml_portuguese_defaults(self):
        """Test Portuguese language produces pt-BR and BRL defaults."""
        data = {
            "profile": {
                "name": "Maria Silva",
                "title": "Desenvolvedora Backend",
                "location": "São Paulo, SP, Brazil",
            },
            "skills": ["Python", "FastAPI"],
        }
        yaml_content = generate_career_ops_profile_yaml(data, lang="pt")
        assert 'output: "pt-BR"' in yaml_content
        assert 'currency: "BRL"' in yaml_content
        assert 'country: "Brazil"' in yaml_content

    def test_profile_yaml_empty_data(self):
        """Test empty profile does not fail and generates safe placeholders."""
        yaml_content = generate_career_ops_profile_yaml({}, lang="en")
        assert 'full_name: ""' in yaml_content
        assert "target_roles:" in yaml_content
        assert "superpowers:" in yaml_content


class TestCareerOpsCvGeneration:
    """Tests for cv.md (Master CV) generation."""

    def test_cv_markdown_full_structure(self):
        """Test complete cv.md generation with all sections."""
        data = {
            "profile": {
                "name": "Jane Smith",
                "title": "Principal Architect",
                "email": "jane@example.com",
                "location": "London, UK",
                "summary": "Experienced distributed systems architect.",
            },
            "experience": [
                {
                    "company": "Big Cloud",
                    "role": "Lead Architect",
                    "start": "Jan 2021",
                    "end": None,
                    "location": "Remote",
                    "achievements": [
                        {"text": "Scaled architecture to 10M users"},
                        {"text": "Cut latency by 50%"},
                    ],
                }
            ],
            "education": [
                {
                    "institution": "MIT",
                    "degree": "B.S. in Computer Science",
                    "start": "2015",
                    "end": "2019",
                }
            ],
            "skills": ["Cloud Architecture", "Go", "Kubernetes"],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date": "2022",
                    "url": "https://aws.amazon.com/verify/123",
                }
            ],
            "languages": [
                {"name": "English", "proficiency": "Native"},
            ],
            "projects": [
                {
                    "title": "Open Router",
                    "start": "2023",
                    "end": None,
                    "description": "High performance LLM proxy.",
                    "url": "https://github.com/example/router",
                }
            ],
        }
        cv_md = generate_career_ops_cv_markdown(data, lang="en")
        assert "# Jane Smith" in cv_md
        assert "**Principal Architect**" in cv_md
        assert "London, UK | jane@example.com" in cv_md
        assert "## Summary" in cv_md
        assert "Experienced distributed systems architect." in cv_md
        assert "## Experience" in cv_md
        assert "### Lead Architect — Big Cloud" in cv_md
        assert "*Jan 2021 – Present* | *Remote*" in cv_md
        assert "- Scaled architecture to 10M users" in cv_md
        assert "## Education" in cv_md
        assert "### B.S. in Computer Science — MIT" in cv_md
        assert "## Skills" in cv_md
        assert "Cloud Architecture, Go, Kubernetes" in cv_md
        assert "## Certifications" in cv_md
        assert "AWS Certified Solutions Architect" in cv_md
        assert "## Languages" in cv_md
        assert "- English (Native)" in cv_md
        assert "## Projects" in cv_md
        assert "### Open Router" in cv_md

    def test_cv_markdown_portuguese(self):
        """Test cv.md translations when lang is pt."""
        data = {
            "profile": {
                "name": "Carlos Lima",
                "title": MultilingualText(pt="Especialista em TI", en="IT Specialist"),
                "summary": MultilingualText(
                    pt="Resumo profissional.", en="Professional summary."
                ),
            },
            "experience": [
                {
                    "company": "Empresa BR",
                    "role": "Engenheiro SRE",
                    "start": "jan 2020",
                    "end": None,
                    "achievements": [
                        {
                            "text": MultilingualText(
                                pt="Otimizou infraestrutura.",
                                en="Optimized infra.",
                            )
                        },
                    ],
                }
            ],
            "certifications": [
                {
                    "name": "Certificado Linux",
                    "issuer": "LPI",
                    "date": "jul 2021",
                    "url": "https://example.com/cert",
                }
            ],
            "languages": [
                {"name": "English", "proficiency": "Full professional proficiency"},
            ],
        }
        cv_md = generate_career_ops_cv_markdown(data, lang="pt")
        assert "# Carlos Lima" in cv_md
        assert "**Especialista em TI**" in cv_md
        assert "## Resumo" in cv_md
        assert "Resumo profissional." in cv_md
        assert "## Experiência" in cv_md
        assert "*jan de 2020 – Atual*" in cv_md
        assert "- Otimizou infraestrutura." in cv_md
        assert "## Licenças e Certificados" in cv_md
        assert "[Ver certificado]" in cv_md
        assert "## Idiomas" in cv_md
        assert "- Inglês (Proficiência profissional completa)" in cv_md

    def test_cv_markdown_empty_data(self):
        """Test cv.md handles completely empty dictionary gracefully."""
        cv_md = generate_career_ops_cv_markdown({}, lang="en")
        assert cv_md == "\n" or cv_md == ""


class TestCareerOpsApplicationsTracker:
    """Tests for data/applications.md tracking table."""

    def test_applications_table_structure(self):
        """Test tracker table header and rows."""
        data = {
            "job_applications": [
                {
                    "date": "10/14/2026",
                    "company": "Anthropic",
                    "title": "Systems Engineer",
                    "status": "Applied",
                    "url": "https://anthropic.com/jobs/1",
                },
                {
                    "date": "08/01/2026, 10:30 AM",
                    "company": "Vercel",
                    "title": "Staff Engineer",
                    "status": "Applied",
                    "withdraw_date": "08/15/2026",
                    "url": "https://vercel.com/jobs/2",
                },
            ]
        }
        apps_md = generate_career_ops_applications_md(data)
        assert (
            "| # | Date | Company | Role | Status | Score | PDF | Report | Notes |"
            in apps_md
        )
        assert "2026-10-14 | Anthropic | Systems Engineer | Applied" in apps_md
        assert "2026-08-01 | Vercel | Staff Engineer | Withdrawn" in apps_md
        assert "[Link](https://anthropic.com/jobs/1)" in apps_md

    def test_empty_applications_table(self):
        """Test empty job applications list produces header only."""
        apps_md = generate_career_ops_applications_md({"job_applications": []})
        assert (
            "| # | Date | Company | Role | Status | Score | PDF | Report | Notes |"
            in apps_md
        )
        assert "| 1 |" not in apps_md

    def test_format_iso_date_formats(self):
        """Test date conversion helper."""
        assert _format_iso_date("12/31/2025") == "2025-12-31"
        assert _format_iso_date("2025-12-31") == "2025-12-31"
        assert _format_iso_date("7/10/26, 7:53 AM") == "2026-07-10"
        assert _format_iso_date("") == "-"
        assert _format_iso_date("Unknown Date") == "Unknown Date"


class TestCareerOpsExport:
    """Tests for export_career_ops file creation."""

    def test_export_creates_expected_files(self, tmp_path):
        """Test export_career_ops creates all package files."""
        data = {
            "profile": {"name": "Test User"},
            "job_applications": [],
        }
        files = export_career_ops(data, tmp_path, lang="pt")
        assert len(files) == 4
        assert (tmp_path / "cv.md").exists()
        assert (tmp_path / "config" / "profile.yml").exists()
        assert (tmp_path / "data" / "applications.md").exists()
        assert (tmp_path / "README.md").exists()

        readme_content = generate_career_ops_readme("pt")
        assert "Pacote de Dados para Career-Ops" in readme_content


class TestCareerOpsCli:
    """Tests for CLI --career-ops integration."""

    def test_parse_career_ops_flag_default(self):
        """Test --career-ops flag without argument sets default sentinel."""
        args = _parse_args(["export.zip", "--career-ops"])
        assert args.career_ops == Path("__DEFAULT__")

    def test_parse_career_ops_custom_path(self):
        """Test --career-ops with explicit destination path."""
        args = _parse_args(["export.zip", "--career-ops", "my_ops"])
        assert args.career_ops == Path("my_ops")

    def test_main_career_ops_export(self, tmp_path):
        """Test running main() with --career-ops."""
        zip_path = tmp_path / "test.zip"
        import zipfile

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("Profile.csv", "First Name,Last Name\nJohn,Doe\n")

        out_dir = tmp_path / "output"
        cop_dir = tmp_path / "ops"

        with patch(
            "sys.argv",
            [
                "linkedin2md",
                str(zip_path),
                "-o",
                str(out_dir),
                "--career-ops",
                str(cop_dir),
                "-q",
            ],
        ):
            code = main()

        assert code == 0
        assert (cop_dir / "cv.md").exists()
        assert (cop_dir / "config" / "profile.yml").exists()
        assert (cop_dir / "data" / "applications.md").exists()
        assert (cop_dir / "README.md").exists()
