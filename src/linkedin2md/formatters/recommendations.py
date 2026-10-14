"""Recommendations and endorsements formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class RecommendationsFormatter(BaseFormatter):
    """Format recommendations received section."""

    @property
    def section_key(self) -> str:
        return "recommendations"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Recommendations', lang)}", ""]
        from_label = self._t("From", lang)
        at_label = self._t("at", lang)

        for rec in data:
            author = self._escape_heading(rec.get("author", ""))
            lines.append(f"## {from_label} {author}")

            meta_parts = []
            if rec.get("title"):
                title = self._escape_inline(rec["title"]).replace("\n", " ")
                meta_parts.append(f"**{title}**")
            if rec.get("company"):
                company = self._escape_inline(rec["company"]).replace("\n", " ")
                meta_parts.append(f"{at_label} {company}")
            if rec.get("date"):
                date = self._escape_inline(
                    self._localize_date(rec["date"], lang)
                ).replace("\n", " ")
                meta_parts.append(f"| {date}")
            if meta_parts:
                lines.append(" ".join(meta_parts))

            text = self._get_text(rec.get("text"), lang)
            if text:
                lines.append("")
                lines.append(self._blockquote(text))

            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class RecommendationsGivenFormatter(BaseFormatter):
    """Format recommendations given section."""

    @property
    def section_key(self) -> str:
        return "recommendations_given"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Recommendations Given', lang)}", ""]
        to_label = self._t("To", lang)
        at_label = self._t("at", lang)

        for rec in data:
            recipient = self._escape_heading(rec.get("recipient", ""))
            lines.append(f"## {to_label} {recipient}")

            meta_parts = []
            if rec.get("title"):
                title = self._escape_inline(rec["title"]).replace("\n", " ")
                meta_parts.append(f"**{title}**")
            if rec.get("company"):
                company = self._escape_inline(rec["company"]).replace("\n", " ")
                meta_parts.append(f"{at_label} {company}")
            if rec.get("date"):
                date = self._escape_inline(
                    self._localize_date(rec["date"], lang)
                ).replace("\n", " ")
                meta_parts.append(f"| {date}")
            if meta_parts:
                lines.append(" ".join(meta_parts))

            text = self._get_text(rec.get("text"), lang)
            if text:
                lines.append("")
                lines.append(self._blockquote(text))

            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class EndorsementsFormatter(BaseFormatter):
    """Format endorsements received section."""

    @property
    def section_key(self) -> str:
        return "endorsements"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Endorsements', lang)}", ""]
        lines.append(self._table_header(["Skill", "Endorsed By", "Date"], lang))
        lines.append("|-------|-------------|------|")

        for end in data:
            skill = self._escape_table_cell(end.get("skill", ""))
            endorser = self._escape_table_cell(end.get("endorser", ""))
            date = self._escape_table_cell(
                self._localize_date(end.get("date", ""), lang)
            )
            lines.append(f"| {skill} | {endorser} | {date} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class EndorsementsGivenFormatter(BaseFormatter):
    """Format endorsements given section."""

    @property
    def section_key(self) -> str:
        return "endorsements_given"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Endorsements Given', lang)}", ""]
        lines.append(self._table_header(["Skill", "Endorsed", "Date"], lang))
        lines.append("|-------|----------|------|")

        for end in data:
            skill = self._escape_table_cell(end.get("skill", ""))
            endorsee = self._escape_table_cell(end.get("endorsee", ""))
            date = self._escape_table_cell(
                self._localize_date(end.get("date", ""), lang)
            )
            lines.append(f"| {skill} | {endorsee} | {date} |")

        lines.append("")
        return "\n".join(lines)
