"""Tests for Brazilian Portuguese (pt-BR) support and internationalization."""

import pytest

from linkedin2md.formatters.jobs import (
    JobApplicationsFormatter,
    JobPreferencesFormatter,
)
from linkedin2md.formatters.network import ConnectionsFormatter
from linkedin2md.formatters.payments import ReceiptsFormatter
from linkedin2md.formatters.privacy import (
    ContactSettingsFormatter,
    WhoViewedProfileFormatter,
)
from linkedin2md.formatters.professional import (
    CertificationsFormatter,
    EducationFormatter,
    ExperienceFormatter,
    LanguagesFormatter,
    ProjectsFormatter,
    SkillsFormatter,
)
from linkedin2md.formatters.profile import ProfileFormatter
from linkedin2md.formatters.profile_ext import (
    CausesFormatter,
    CoursesFormatter,
    InterestsFormatter,
)
from linkedin2md.i18n import (
    language_tag,
    localize_date,
    normalize_language,
    translate,
    translate_language_name,
    translate_proficiency,
)
from linkedin2md.language import PortugueseSpanishEnglishDetector
from linkedin2md.protocols import MultilingualText


class TestLanguageNormalization:
    """Tests for language code normalization and aliases."""

    def test_portuguese_aliases_normalize_to_pt(self) -> None:
        """Test variations of pt-BR map to canonical 'pt'."""
        for alias in (
            "pt",
            "pt-BR",
            "pt-br",
            "pt_BR",
            "ptbr",
            "brazilian",
            "portuguese",
            "português",
        ):
            assert normalize_language(alias) == "pt"

    def test_spanish_aliases_normalize_to_es(self) -> None:
        """Test variations of Spanish map to canonical 'es'."""
        for alias in ("es", "es-ES", "es-AR", "spanish", "español"):
            assert normalize_language(alias) == "es"

    def test_english_aliases_normalize_to_en(self) -> None:
        """Test variations of English map to canonical 'en'."""
        for alias in ("en", "en-US", "en-GB", "english"):
            assert normalize_language(alias) == "en"

    def test_empty_or_none_defaults_to_en(self) -> None:
        """Test empty or None returns default language."""
        assert normalize_language(None) == "en"
        assert normalize_language("") == "en"

    def test_strict_rejects_unsupported_language(self) -> None:
        """Test strict mode raises ValueError for unknown language."""
        with pytest.raises(ValueError, match="Unsupported language 'fr'"):
            normalize_language("fr", strict=True)

    def test_non_strict_preserves_custom_code(self) -> None:
        """Test non-strict mode lowercases arbitrary language code."""
        assert normalize_language("FR") == "fr"

    def test_language_tag_for_documents(self) -> None:
        """Test BCP 47 document language tags."""
        assert language_tag("pt") == "pt-BR"
        assert language_tag("pt-BR") == "pt-BR"
        assert language_tag("es") == "es"
        assert language_tag("en") == "en"


class TestCatalogAndTranslations:
    """Tests for translation lookup functions."""

    def test_translate_known_keys_pt(self) -> None:
        """Test Brazilian Portuguese translation catalog lookup."""
        assert translate("Skills", "pt") == "Competências"
        assert translate("Experience", "pt-BR") == "Experiência"
        assert translate("Education", "pt") == "Formação Acadêmica"
        assert translate("Present", "pt") == "Atual"
        assert translate("Summary", "pt") == "Resumo"
        assert translate("Job Applications", "pt") == "Candidaturas a Vagas"

    def test_translate_unknown_key_falls_back(self) -> None:
        """Test unknown message id returns original string."""
        assert translate("Unknown Key 123", "pt") == "Unknown Key 123"

    def test_translate_english_is_identity(self) -> None:
        """Test English language lookup returns the message id itself."""
        assert translate("Skills", "en") == "Skills"
        assert translate("Experience", "en") == "Experience"

    def test_translate_proficiency(self) -> None:
        """Test translating LinkedIn proficiency levels to pt-BR."""
        assert (
            translate_proficiency("Professional working proficiency", "pt")
            == "Proficiência profissional"
        )
        assert (
            translate_proficiency("Native or bilingual proficiency", "pt-BR")
            == "Proficiência nativa ou bilíngue"
        )
        assert (
            translate_proficiency("Full professional proficiency", "pt")
            == "Proficiência profissional completa"
        )
        assert translate_proficiency("Elementary proficiency", "pt") == "Nível básico"
        assert (
            translate_proficiency("Limited working proficiency", "pt")
            == "Proficiência limitada"
        )
        # English pass-through
        assert (
            translate_proficiency("Professional working proficiency", "en")
            == "Professional working proficiency"
        )

    def test_translate_language_name(self) -> None:
        """Test translating language names to pt-BR."""
        assert translate_language_name("English", "pt") == "Inglês"
        assert translate_language_name("Spanish", "pt-BR") == "Espanhol"
        assert translate_language_name("French", "pt") == "Francês"
        assert translate_language_name("German", "pt") == "Alemão"
        assert translate_language_name("Portuguese", "pt") == "Português"
        assert translate_language_name("Chinese", "pt") == "Chinês"
        assert translate_language_name("Dutch", "pt") == "Holandês"
        # English pass-through
        assert translate_language_name("English", "en") == "English"


class TestDateLocalization:
    """Tests for month/year date localization."""

    def test_localize_date_pt(self) -> None:
        """Test formatting dates to Brazilian Portuguese style ('jan de 2024')."""
        assert localize_date("Jan 2024", "pt") == "jan de 2024"
        assert localize_date("Feb 2023", "pt-BR") == "fev de 2023"
        assert localize_date("Mar 2022", "pt") == "mar de 2022"
        assert localize_date("Apr 2021", "pt") == "abr de 2021"
        assert localize_date("May 2020", "pt") == "mai de 2020"
        assert localize_date("Jun 2019", "pt") == "jun de 2019"
        assert localize_date("Jul 2018", "pt") == "jul de 2018"
        assert localize_date("Aug 2017", "pt") == "ago de 2017"
        assert localize_date("Sep 2016", "pt") == "set de 2016"
        assert localize_date("Oct 2015", "pt") == "out de 2015"
        assert localize_date("Nov 2014", "pt") == "nov de 2014"
        assert localize_date("Dec 2013", "pt") == "dez de 2013"

    def test_localize_date_english_pass_through(self) -> None:
        """Test English dates pass through unchanged."""
        assert localize_date("Jan 2024", "en") == "Jan 2024"

    def test_localize_date_edge_cases(self) -> None:
        """Test empty, None, and arbitrary text dates pass through safely."""
        assert localize_date("", "pt") == ""
        assert localize_date("2024", "pt") == "2024"
        assert localize_date("Present", "pt") == "Present"


class TestDetectorTrilingual:
    """Tests for PortugueseSpanishEnglishDetector."""

    def test_detect_portuguese_text(self) -> None:
        """Test detecting natural Brazilian Portuguese sentences."""
        detector = PortugueseSpanishEnglishDetector()
        assert detector.supported_languages == ["en", "es", "pt"]

        samples = [
            (
                "Sou um desenvolvedor de software com bastante "
                "experiência em backend e Python."
            ),
            (
                "Trabalho na área de tecnologia com desenvolvimento "
                "de soluções em nuvem."
            ),
            (
                "Atuação em projetos de arquitetura de microsserviços "
                "e liderança de equipe."
            ),
            (
                "Formação acadêmica com graduação em Ciência da "
                "Computação e pós-graduação."
            ),
        ]
        for sample in samples:
            assert detector.detect(sample) == "pt", (
                f"Failed to detect Portuguese for: {sample}"
            )

    def test_detect_spanish_text(self) -> None:
        """Test detecting natural Spanish sentences."""
        detector = PortugueseSpanishEnglishDetector()
        samples = [
            (
                "Soy un desarrollador de software con mucha "
                "experiencia en desarrollo backend."
            ),
            ("Trabajo en equipo en proyectos de ingeniería de datos y desarrollo web."),
            (
                "Ingeniero en sistemas con experiencia laboral "
                "en empresas multinacionales."
            ),
        ]
        for sample in samples:
            assert detector.detect(sample) == "es", (
                f"Failed to detect Spanish for: {sample}"
            )

    def test_detect_english_text(self) -> None:
        """Test detecting English text."""
        detector = PortugueseSpanishEnglishDetector()
        samples = [
            (
                "Senior software engineer with 10 years of experience "
                "in distributed systems."
            ),
            (
                "Led cross-functional teams to build cloud native "
                "platforms with Python and Go."
            ),
        ]
        for sample in samples:
            assert detector.detect(sample) == "en", (
                f"Failed to detect English for: {sample}"
            )

    def test_detect_empty_or_special(self) -> None:
        """Test empty text and numbers default to English."""
        detector = PortugueseSpanishEnglishDetector()
        assert detector.detect("") == "en"
        assert detector.detect("12345 67890") == "en"


class TestPortugueseSectionFormatters:
    """Tests that formatters render Portuguese headings, labels and dates."""

    def test_format_profile_portuguese(self) -> None:
        """Test ProfileFormatter produces pt-BR headings and labels."""
        formatter = ProfileFormatter()
        data = {
            "name": "Maria Oliveira",
            "title": MultilingualText(pt="Engenheira de Dados"),
            "email": "maria@example.com",
            "phone": "+55 11 99999-9999",
            "location": "São Paulo, Brasil",
            "summary": MultilingualText(
                pt="Especialista em pipelines de dados e big data."
            ),
            "profile_meta": {
                "industry": "Tecnologia",
                "registered_at": "Jan 2018",
                "connections_count": "500+",
            },
        }
        output = formatter.format(data, "pt-BR")
        assert "# Maria Oliveira" in output
        assert "Engenheira de Dados" in output
        assert "## Resumo" in output
        assert "Especialista em pipelines" in output
        assert "## Detalhes do Perfil" in output
        assert "- **Setor:** Tecnologia" in output
        assert "- **Membro desde:** jan de 2018" in output
        assert "- **Conexões:** 500+" in output

    def test_format_experience_portuguese(self) -> None:
        """Test ExperienceFormatter produces pt-BR headings, 'Atual' and dates."""
        formatter = ExperienceFormatter()
        data = [
            {
                "company": "Tech Corp",
                "role": MultilingualText(pt="Desenvolvedora Sênior"),
                "location": "Remoto",
                "start": "Mar 2021",
                "end": None,
                "achievements": [
                    {
                        "text": MultilingualText(
                            pt="Liderou migração para Kubernetes com sucesso."
                        )
                    }
                ],
            }
        ]
        output = formatter.format(data, "pt")
        assert "# Experiência" in output
        assert "## Tech Corp" in output
        assert "**Desenvolvedora Sênior**" in output
        assert "mar de 2021 - Atual" in output
        assert "- Liderou migração para Kubernetes com sucesso." in output

    def test_format_education_portuguese(self) -> None:
        """Test EducationFormatter produces pt-BR labels."""
        formatter = EducationFormatter()
        data = [
            {
                "institution": "Universidade de São Paulo",
                "degree": MultilingualText(pt="Bacharelado em Engenharia"),
                "field": "Engenharia de Software",
                "start": "2015",
                "end": "2019",
                "grade": "9.5",
                "notes": MultilingualText(pt="Destaque acadêmico."),
                "activities": "Empresa Júnior",
            }
        ]
        output = formatter.format(data, "pt-BR")
        assert "# Formação Acadêmica" in output
        assert "## Universidade de São Paulo" in output
        assert "**Bacharelado em Engenharia**" in output
        assert "**Área de Estudo:** Engenharia de Software" in output
        assert "**Nota:** 9.5" in output
        assert "> Destaque acadêmico." in output
        assert "Atividades: Empresa Júnior" in output

    def test_format_skills_portuguese(self) -> None:
        """Test SkillsFormatter produces pt-BR heading."""
        formatter = SkillsFormatter()
        data = ["Python", "Docker", "PostgreSQL", "Kubernetes"]
        output = formatter.format(data, "pt")
        assert "# Competências" in output
        assert "Python, Docker, PostgreSQL, Kubernetes" in output

    def test_format_certifications_portuguese(self) -> None:
        """Test CertificationsFormatter produces pt-BR heading and link."""
        formatter = CertificationsFormatter()
        data = [
            {
                "name": "AWS Solutions Architect",
                "issuer": "Amazon Web Services",
                "date": "Jun 2022",
                "url": "https://aws.amazon.com/cert/123",
            }
        ]
        output = formatter.format(data, "pt")
        assert "# Licenças e Certificados" in output
        assert "## AWS Solutions Architect" in output
        assert "jun de 2022" in output
        assert "[Ver certificado](https://aws.amazon.com/cert/123)" in output

    def test_format_languages_portuguese(self) -> None:
        """Test LanguagesFormatter translates language names and proficiency levels."""
        formatter = LanguagesFormatter()
        data = [
            {"name": "English", "proficiency": "Professional working proficiency"},
            {"name": "Portuguese", "proficiency": "Native or bilingual proficiency"},
        ]
        output = formatter.format(data, "pt-BR")
        assert "# Idiomas" in output
        assert "- **Inglês**: Proficiência profissional" in output
        assert "- **Português**: Proficiência nativa ou bilíngue" in output

    def test_format_projects_portuguese(self) -> None:
        """Test ProjectsFormatter produces pt-BR heading and dates."""
        formatter = ProjectsFormatter()
        data = [
            {
                "title": "Open Source Project",
                "start": "Jan 2023",
                "end": "Dec 2023",
                "description": MultilingualText(
                    pt="Projeto open source de alta performance."
                ),
                "url": "https://github.com/example/project",
            }
        ]
        output = formatter.format(data, "pt")
        assert "# Projetos" in output
        assert "jan de 2023 - dez de 2023" in output
        assert "[Ver projeto](https://github.com/example/project)" in output

    def test_format_job_applications_portuguese(self) -> None:
        """Test JobApplicationsFormatter produces pt-BR table headers."""
        formatter = JobApplicationsFormatter()
        data = [
            {
                "date": "Aug 2023",
                "company": "Empresa X",
                "title": "Arquiteta de Software",
                "status": "Em análise",
                "resume_used": "cv_2023.pdf",
            }
        ]
        output = formatter.format(data, "pt-BR")
        assert "# Candidaturas a Vagas" in output
        assert "| Data | Empresa | Cargo | Status | Currículo |" in output
        assert "ago de 2023" in output

    def test_format_job_preferences_portuguese(self) -> None:
        """Test JobPreferencesFormatter produces pt-BR labels."""
        formatter = JobPreferencesFormatter()
        data = {
            "locations": ["Brasil", "Remoto"],
            "job_titles": ["Engenheiro de Software"],
            "open_to_recruiters": True,
        }
        output = formatter.format(data, "pt")
        assert "# Preferências de Busca de Emprego" in output
        assert "**Localidades:** Brasil, Remoto" in output
        assert "**Cargos:** Engenheiro de Software" in output
        assert "**Aberto a Recrutadores:** Sim" in output

    def test_format_connections_portuguese(self) -> None:
        """Test ConnectionsFormatter produces pt-BR table headers."""
        formatter = ConnectionsFormatter()
        data = [
            {
                "name": "Carlos Souza",
                "company": "Startup Y",
                "position": "CTO",
                "connected_on": "May 2021",
            }
        ]
        output = formatter.format(data, "pt")
        assert "# Conexões" in output
        assert "| Nome | Empresa | Cargo | Conectado em |" in output
        assert "mai de 2021" in output

    def test_format_simple_list_subclasses_portuguese(self) -> None:
        """Test SimpleListFormatter subclasses render translated titles and columns."""
        causes = CausesFormatter().format([{"name": "Educação"}], "pt")
        assert "# Causas" in causes
        assert "| Causa |" in causes

        interests = InterestsFormatter().format(
            [{"name": "Inteligência Artificial"}], "pt"
        )
        assert "# Interesses" in interests
        assert "| Interesse |" in interests

        courses = CoursesFormatter().format(
            [{"name": "Algoritmos", "school": "USP"}], "pt"
        )
        assert "# Cursos" in courses
        assert "| Curso | Instituição de Ensino |" in courses

        contact = ContactSettingsFormatter().format(
            [{"setting": "Email", "value": "Visível"}], "pt"
        )
        assert "# Configurações de Contato" in contact
        assert "| Configuração | Valor |" in contact

        who = WhoViewedProfileFormatter().format(
            [{"date": "2024-01-01", "viewer": "Recrutador"}], "pt"
        )
        assert "# Quem Viu seu Perfil" in who
        assert "| Data | Visitante |" in who

        receipts = ReceiptsFormatter().format(
            [
                {
                    "date": "Jan 2024",
                    "description": "LinkedIn Premium",
                    "amount": "89.90",
                    "currency": "BRL",
                }
            ],
            "pt",
        )
        assert "# Recibos de Pagamento" in receipts
        assert "| Data | Descrição | Valor | Moeda |" in receipts
        assert "jan de 2024" in receipts
