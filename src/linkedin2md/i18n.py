"""Localization of generated output labels.

Single Responsibility: translate fixed UI strings (headings, table headers,
field labels, CLI/PDF messages) and canonical dates to the output language.

Design notes:
- English strings are used as message ids (gettext style). English output
  is therefore always the identity transformation, which keeps the default
  output byte-for-byte stable.
- Catalogs only need to list the strings they translate; anything missing
  falls back to the English message id.
- Language codes are normalized so ``pt``, ``pt-BR``, ``pt_br`` and
  ``PT-BR`` all resolve to the canonical internal code ``pt``.
"""

import re

DEFAULT_LANGUAGE = "en"

#: Canonical internal language codes (ISO 639-1).
SUPPORTED_LANGUAGES: tuple[str, ...] = ("en", "es", "pt")

#: BCP 47 tags used in documents that declare a language (e.g. PDF/HTML).
LANGUAGE_TAGS: dict[str, str] = {"en": "en", "es": "es", "pt": "pt-BR"}

_LANGUAGE_ALIASES: dict[str, str] = {
    "en": "en",
    "en-us": "en",
    "en-gb": "en",
    "english": "en",
    "es": "es",
    "es-es": "es",
    "es-ar": "es",
    "es-mx": "es",
    "es-419": "es",
    "spanish": "es",
    "español": "es",
    "pt": "pt",
    "pt-br": "pt",
    "ptbr": "pt",
    "brazilian": "pt",
    "portuguese": "pt",
    "português": "pt",
    "portugues": "pt",
}


def normalize_language(code: str | None, *, strict: bool = False) -> str:
    """Return the canonical internal language code for ``code``.

    Args:
        code: Language code or alias (e.g. ``"pt-BR"``, ``"pt_br"``, ``"es"``).
        strict: When True, raise ``ValueError`` for unknown codes. When False,
            unknown codes are returned lower-cased so custom languages keep
            working with ``MultilingualText`` content lookups.

    Returns:
        Canonical code such as ``"en"``, ``"es"`` or ``"pt"``.
    """
    if not code:
        return DEFAULT_LANGUAGE
    key = code.strip().lower().replace("_", "-")
    canonical = _LANGUAGE_ALIASES.get(key)
    if canonical is not None:
        return canonical
    if strict:
        supported = ", ".join((*SUPPORTED_LANGUAGES, "pt-BR"))
        raise ValueError(
            f"Unsupported language {code!r}. Supported languages: {supported}"
        )
    return key


def language_tag(lang: str) -> str:
    """Return the BCP 47 tag for a language (``pt`` -> ``pt-BR``)."""
    canonical = normalize_language(lang)
    return LANGUAGE_TAGS.get(canonical, canonical)


# ============================================================================
# Brazilian Portuguese catalog
# ============================================================================

_PT_BR: dict[str, str] = {
    # --- Profile ----------------------------------------------------------
    "Summary": "Resumo",
    "Profile Details": "Detalhes do Perfil",
    "Industry": "Setor",
    "Maiden Name": "Nome de Solteiro(a)",
    "Profile URL": "URL do Perfil",
    "Address": "Endereço",
    "Twitter": "Twitter",
    "Website": "Site",
    "Birth Date": "Data de Nascimento",
    "Member Since": "Membro desde",
    "Connections": "Conexões",
    # --- Professional -----------------------------------------------------
    "Skills": "Competências",
    "Experience": "Experiência",
    "Present": "Atual",
    "Education": "Formação Acadêmica",
    "Field of Study": "Área de Estudo",
    "Grade": "Nota",
    "Activities": "Atividades",
    "Certifications": "Licenças e Certificados",
    "View Certificate": "Ver certificado",
    "Languages": "Idiomas",
    "Projects": "Projetos",
    "View Project": "Ver projeto",
    # --- Content ----------------------------------------------------------
    "Posts": "Posts",
    "View Post": "Ver post",
    "Comments": "Comentários",
    "View": "Ver",
    "Reactions": "Reações",
    "Reposts": "Compartilhamentos",
    "Poll Votes": "Votos em Enquetes",
    "Option": "Opção",
    "Saved Items": "Itens Salvos",
    "Saved At": "Salvo em",
    "Events": "Eventos",
    "Uploaded Media": "Mídias Enviadas",
    "Messages": "Mensagens",
    "From": "De",
    "To": "Para",
    "Subject": "Assunto",
    "Scripts": "Scripts",
    "Published Articles": "Artigos Publicados",
    "Author": "Autor",
    # --- Common column / field labels ---------------------------------------
    "Date": "Data",
    "Type": "Tipo",
    "Link": "Link",
    "Name": "Nome",
    "Time": "Data e Hora",
    "Status": "Status",
    "Description": "Descrição",
    "Company": "Empresa",
    "Position": "Cargo",
    "Title": "Título",
    "Location": "Localização",
    "Details": "Detalhes",
    "Email": "E-mail",
    "URL": "URL",
    "Unknown": "Desconhecido",
    "(not specified)": "(não informado)",
    "Yes": "Sim",
    # --- Jobs -------------------------------------------------------------
    "Job Applications": "Candidaturas a Vagas",
    "Resume": "Currículo",
    "Saved Jobs": "Vagas Salvas",
    "Job Seeker Preferences": "Preferências de Busca de Emprego",
    "Locations": "Localidades",
    "Job Titles": "Cargos",
    "Job Types": "Tipos de Vaga",
    "Industries": "Setores",
    "Open to Recruiters": "Aberto a Recrutadores",
    "Dream Companies": "Empresas dos Sonhos",
    "Saved Job Application Answers": "Respostas Salvas de Candidaturas",
    "Q": "P",
    "A": "R",
    "Screening Question Responses": "Respostas a Perguntas de Triagem",
    "Response": "Resposta",
    "Saved Job Alerts": "Alertas de Vagas Salvos",
    "Alert ID": "ID do Alerta",
    "Query": "Consulta",
    "Job Descriptions": "Descrições de Vagas",
    "Date Applied": "Data da Candidatura",
    # --- Recommendations --------------------------------------------------
    "Recommendations": "Recomendações Recebidas",
    "Recommendations Given": "Recomendações Feitas",
    "at": "em",
    "Endorsements": "Validações de Competências",
    "Endorsements Given": "Validações Feitas",
    "Skill": "Competência",
    "Endorsed By": "Validado por",
    "Endorsed": "Validado",
    # --- Network ----------------------------------------------------------
    "Connected": "Conectado em",
    "Companies Followed": "Empresas Seguidas",
    "Members Followed": "Pessoas Seguidas",
    "Connection Invitations": "Convites de Conexão",
    "Direction": "Direção",
    "Imported Contacts": "Contatos Importados",
    "Groups": "Grupos",
    "Group": "Grupo",
    # --- Activity ---------------------------------------------------------
    "Search History": "Histórico de Pesquisas",
    "Login History": "Histórico de Logins",
    "IP Address": "Endereço IP",
    "Security Challenges": "Desafios de Segurança",
    "Country": "País",
    # --- Advertising ------------------------------------------------------
    "Ads Clicked": "Anúncios Clicados",
    "Ad ID": "ID do Anúncio",
    "Ad Targeting Criteria": "Critérios de Segmentação de Anúncios",
    "LinkedIn Audience Network Ads": "Anúncios da LinkedIn Audience Network",
    "Action": "Ação",
    "Page/App": "Página/App",
    "LinkedIn's Inferences About You": "Inferências do LinkedIn sobre Você",
    "Category": "Categoria",
    "Inference": "Inferência",
    # --- Identity ---------------------------------------------------------
    "Identity Verifications": "Verificações de Identidade",
    "Document": "Documento",
    "Provider": "Provedor",
    "Verified": "Verificado em",
    "Expires": "Expira em",
    "Uploaded Documents": "Documentos Enviados",
    "(with content)": "(com conteúdo)",
    "(no content)": "(sem conteúdo)",
    # --- Learning ---------------------------------------------------------
    "LinkedIn Learning": "LinkedIn Learning",
    "Completed": "Concluído",
    "In Progress": "Em andamento",
    "Learning Reviews": "Avaliações do LinkedIn Learning",
    "Content": "Conteúdo",
    "Rating": "Avaliação",
    # --- Payments / services ----------------------------------------------
    "Payment Receipts": "Recibos de Pagamento",
    "Amount": "Valor",
    "Currency": "Moeda",
    "Service Marketplace Engagements": "Contratações no Marketplace de Serviços",
    "Service Marketplace Opportunities": "Oportunidades no Marketplace de Serviços",
    # --- Privacy / account ------------------------------------------------
    "Contact Settings": "Configurações de Contato",
    "Setting": "Configuração",
    "Value": "Valor",
    "Data Export History": "Histórico de Exportação de Dados",
    "Requested At": "Solicitado em",
    "Completed At": "Concluído em",
    "Deletion History": "Histórico de Exclusões",
    "Who Viewed Your Profile": "Quem Viu seu Perfil",
    "Viewer": "Visitante",
    "LinkedIn Salary": "Salários no LinkedIn",
    "Salary": "Salário",
    "Profile for Business": "Perfil para Empresas",
    "Profile Summary": "Resumo do Perfil",
    # --- Profile extensions -----------------------------------------------
    "Causes": "Causas",
    "Cause": "Causa",
    "Interests": "Interesses",
    "Interest": "Interesse",
    "Courses": "Cursos",
    "Course": "Curso",
    "School": "Instituição de Ensino",
    "Honors & Awards": "Prêmios e Reconhecimentos",
    "Issuer": "Emissor",
    "Test Scores": "Resultados de Exames",
    "Test": "Exame",
    "Score": "Pontuação",
    "Patents": "Patentes",
    "Number": "Número",
    "Organizations": "Organizações",
    "Organization": "Organização",
    "Publications": "Publicações",
    "Publisher": "Editora",
    "Volunteer Experience": "Trabalho Voluntário",
    "Role": "Função",
    "Start": "Início",
    "End": "Fim",
    # --- CLI / PDF ------------------------------------------------------------
    "Extracting and converting export...": "Extraindo e convertendo a exportação...",
    "Created {count} files in {path}/": "{count} arquivos criados em {path}/",
    "Generating PDF Resume...": "Gerando currículo em PDF...",
    "Created PDF Resume: {path}": "Currículo em PDF criado: {path}",
    "LinkedIn Export Resume": "Currículo - Exportação do LinkedIn",
    "Page": "Página",
    "of": "de",
}

# LinkedIn language proficiency levels (exact values found in Languages.csv).
_PT_BR_PROFICIENCY: dict[str, str] = {
    "elementary proficiency": "Nível básico",
    "limited working proficiency": "Proficiência limitada",
    "professional working proficiency": "Proficiência profissional",
    "full professional proficiency": "Proficiência profissional completa",
    "native or bilingual proficiency": "Proficiência nativa ou bilíngue",
}

# Language names (LanguagesParser normalizes known names to English).
_PT_BR_LANGUAGE_NAMES: dict[str, str] = {
    "english": "Inglês",
    "spanish": "Espanhol",
    "french": "Francês",
    "german": "Alemão",
    "italian": "Italiano",
    "portuguese": "Português",
    "chinese": "Chinês",
    "mandarin": "Mandarim",
    "japanese": "Japonês",
    "korean": "Coreano",
    "arabic": "Árabe",
    "russian": "Russo",
    "hindi": "Hindi",
    "dutch": "Holandês",
}

_CATALOGS: dict[str, dict[str, str]] = {
    "pt": _PT_BR,
}

_PROFICIENCY_CATALOGS: dict[str, dict[str, str]] = {
    "pt": _PT_BR_PROFICIENCY,
}

_LANGUAGE_NAME_CATALOGS: dict[str, dict[str, str]] = {
    "pt": _PT_BR_LANGUAGE_NAMES,
}


def translate(message: str, lang: str) -> str:
    """Translate an English message id into ``lang``.

    Unknown languages and untranslated messages return ``message`` unchanged.
    """
    catalog = _CATALOGS.get(normalize_language(lang))
    if catalog is None:
        return message
    return catalog.get(message, message)


def _translate_value(value: str, lang: str, catalogs: dict[str, dict[str, str]]) -> str:
    """Case-insensitively translate a data value; unknown values pass through."""
    catalog = catalogs.get(normalize_language(lang))
    if catalog is None or not value:
        return value
    return catalog.get(value.strip().lower(), value)


def translate_proficiency(value: str, lang: str) -> str:
    """Translate a LinkedIn language proficiency level into ``lang``."""
    return _translate_value(value, lang, _PROFICIENCY_CATALOGS)


def translate_language_name(value: str, lang: str) -> str:
    """Translate an (English) language name into ``lang``."""
    return _translate_value(value, lang, _LANGUAGE_NAME_CATALOGS)


def get_catalog(lang: str) -> dict[str, str]:
    """Return a copy of the translation catalog for ``lang`` (may be empty)."""
    return dict(_CATALOGS.get(normalize_language(lang), {}))


# ============================================================================
# Date localization
# ============================================================================

#: Canonical English month abbreviations produced by the parsers.
ENGLISH_MONTHS: tuple[str, ...] = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)

_PT_BR_MONTHS: tuple[str, ...] = (
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
)

_CANONICAL_DATE = re.compile(r"(" + "|".join(ENGLISH_MONTHS) + r") (\d{4})")


def localize_date(value: str, lang: str) -> str:
    """Localize a canonical ``"Mon YYYY"`` date (e.g. ``"Jan 2024"``).

    Brazilian Portuguese follows LinkedIn's pt-BR style: ``"jan de 2024"``.
    Values that are not canonical month/year dates are returned unchanged.
    """
    if normalize_language(lang) != "pt" or not value:
        return value
    trimmed = value.strip()
    match = re.fullmatch(r"([A-Za-z]{3}) (\d{4})", trimmed)
    if match is None:
        return value
    month_name = match.group(1).capitalize()
    if month_name in ENGLISH_MONTHS:
        month = _PT_BR_MONTHS[ENGLISH_MONTHS.index(month_name)]
        return f"{month} de {match.group(2)}"
    month_lower = match.group(1).lower()
    if month_lower in _PT_BR_MONTHS:
        return f"{month_lower} de {match.group(2)}"
    return value
