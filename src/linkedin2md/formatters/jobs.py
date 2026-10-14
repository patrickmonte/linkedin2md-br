"""Job-related section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class JobApplicationsFormatter(BaseFormatter):
    """Format job applications section."""

    @property
    def section_key(self) -> str:
        return "job_applications"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Job Applications', lang)}", ""]
        lines.append(
            self._table_header(
                ["Date", "Company", "Position", "Status", "Resume"], lang
            )
        )
        lines.append("|------|---------|----------|--------|--------|")

        for app in data:
            date = self._escape_table_cell(
                self._localize_date(app.get("date", ""), lang)
            )
            company = self._escape_table_cell(app.get("company", ""))
            title = self._escape_table_cell(app.get("title", ""))
            status = self._escape_table_cell(app.get("status", ""))
            resume = self._escape_table_cell(app.get("resume_used", ""))
            lines.append(f"| {date} | {company} | {title} | {status} | {resume} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class SavedJobsFormatter(BaseFormatter):
    """Format saved jobs section."""

    @property
    def section_key(self) -> str:
        return "saved_jobs"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Saved Jobs', lang)}", ""]
        lines.append(self._table_header(["Date", "Company", "Position"], lang))
        lines.append("|------|---------|----------|")

        for job in data:
            date = self._escape_table_cell(
                self._localize_date(job.get("date", ""), lang)
            )
            company = self._escape_table_cell(job.get("company", ""))
            title = self._escape_table_cell(job.get("title", ""))
            lines.append(f"| {date} | {company} | {title} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class JobPreferencesFormatter(BaseFormatter):
    """Format job preferences section."""

    @property
    def section_key(self) -> str:
        return "job_preferences"

    def _format_content(self, data: dict, lang: str) -> str:
        lines = [f"# {self._t('Job Seeker Preferences', lang)}", ""]

        if data.get("locations"):
            loc_label = self._t("Locations", lang)
            loc_val = self._escape_joined(data["locations"])
            lines.append(f"**{loc_label}:** {loc_val}")
            lines.append("")

        if data.get("job_titles"):
            titles_label = self._t("Job Titles", lang)
            titles_val = self._escape_joined(data["job_titles"])
            lines.append(f"**{titles_label}:** {titles_val}")
            lines.append("")

        if data.get("job_types"):
            types_label = self._t("Job Types", lang)
            types_val = self._escape_joined(data["job_types"])
            lines.append(f"**{types_label}:** {types_val}")
            lines.append("")

        if data.get("industries"):
            ind_label = self._t("Industries", lang)
            ind_val = self._escape_joined(data["industries"])
            lines.append(f"**{ind_label}:** {ind_val}")
            lines.append("")

        if data.get("open_to_recruiters"):
            open_label = self._t("Open to Recruiters", lang)
            yes_val = self._t("Yes", lang)
            lines.append(f"**{open_label}:** {yes_val}")
            lines.append("")

        if data.get("dream_companies"):
            dream_label = self._t("Dream Companies", lang)
            dream_val = self._escape_joined(data["dream_companies"])
            lines.append(f"**{dream_label}:** {dream_val}")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class SavedJobAnswersFormatter(BaseFormatter):
    """Format saved job answers section."""

    @property
    def section_key(self) -> str:
        return "saved_job_answers"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Saved Job Application Answers', lang)}", ""]
        q_label = self._t("Q", lang)
        a_label = self._t("A", lang)

        for answer in data:
            question = self._escape_inline(answer.get("question", "")).replace(
                "\n", " "
            )
            ans = self._escape_inline(answer.get("answer", "") or "").replace("\n", " ")
            lines.append(f"**{q_label}:** {question}")
            lines.append(f"**{a_label}:** {ans}")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class ScreeningResponsesFormatter(BaseFormatter):
    """Format screening responses section."""

    @property
    def section_key(self) -> str:
        return "screening_responses"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Screening Question Responses', lang)}", ""]
        response_label = self._t("Response", lang)

        for i, response in enumerate(data, 1):
            lines.append(f"## {response_label} {i}")
            for key, value in response.items():
                formatted_key = self._escape_inline(
                    str(key).replace("_", " ").title()
                ).replace("\n", " ")
                formatted_value = self._escape_list_item(value)
                lines.append(f"- **{formatted_key}:** {formatted_value}")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class SavedJobAlertsFormatter(BaseFormatter):
    """Format saved job alerts section."""

    @property
    def section_key(self) -> str:
        return "saved_job_alerts"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Saved Job Alerts', lang)}", ""]

        for alert in data:
            search_id = self._escape_inline(alert.get("search_id", "")).replace(
                "\n", " "
            )
            query = self._escape_inline(alert.get("query_context", "") or "").replace(
                "\n", " "
            )
            lines.append(f"**{self._t('Alert ID', lang)}:** {search_id}")
            if query:
                lines.append(f"**{self._t('Query', lang)}:** {query}")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class JobDescriptionFormatter(BaseFormatter):
    """Format job descriptions section."""

    @property
    def section_key(self) -> str:
        return "job_descriptions"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Job Descriptions', lang)}", ""]

        for job in data:
            company = job.get("company", "")
            title = job.get("title", "")
            description = job.get("description", "") or ""
            date_applied = self._localize_date(job.get("date_applied", "") or "", lang)
            status = job.get("status", "") or ""

            heading = self._escape_heading(company or title or self._t("Unknown", lang))
            lines.append(f"## {heading}")
            if company and title:
                title_value = self._escape_inline(title).replace("\n", " ")
                lines.append(f"**{self._t('Title', lang)}:** {title_value}")
            elif not company and title:
                co_label = self._t("Company", lang)
                not_spec = self._t("(not specified)", lang)
                lines.append(f"**{co_label}:** {not_spec}")
            if company and not title:
                ti_label = self._t("Title", lang)
                not_spec = self._t("(not specified)", lang)
                lines.append(f"**{ti_label}:** {not_spec}")
            if description:
                desc_label = self._t("Description", lang)
                desc_block = self._escape_block(description)
                lines.append(f"**{desc_label}:** {desc_block}")
            if date_applied:
                date_value = self._escape_inline(date_applied).replace("\n", " ")
                lines.append(f"**{self._t('Date Applied', lang)}:** {date_value}")
            if status:
                status_value = self._escape_inline(status).replace("\n", " ")
                lines.append(f"**{self._t('Status', lang)}:** {status_value}")
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
