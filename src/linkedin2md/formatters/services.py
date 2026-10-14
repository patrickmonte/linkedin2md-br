"""Services marketplace section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class ServiceEngagementsFormatter(BaseFormatter):
    """Format service engagements section."""

    @property
    def section_key(self) -> str:
        return "service_engagements"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Service Marketplace Engagements', lang)}", ""]
        lines.append(self._table_header(["Date", "Type", "Amount", "Currency"], lang))
        lines.append("|------|------|--------|----------|")

        for e in data:
            date = self._escape_table_cell(self._localize_date(e.get("date", ""), lang))
            mtype = self._escape_table_cell(e.get("marketplace_type", ""))
            amount = self._escape_table_cell(e.get("amount", ""))
            currency = self._escape_table_cell(e.get("currency", ""))
            lines.append(f"| {date} | {mtype} | {amount} | {currency} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class ServiceOpportunitiesFormatter(BaseFormatter):
    """Format service opportunities section."""

    @property
    def section_key(self) -> str:
        return "service_opportunities"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Service Marketplace Opportunities', lang)}", ""]

        for opp in data:
            raw_date = opp.get("date", "") or ""
            date = self._escape_inline(self._localize_date(raw_date, lang)).replace(
                "\n", " "
            )
            category = self._escape_heading(opp.get("category", "") or "")
            location = self._escape_inline(opp.get("location", "") or "").replace(
                "\n", " "
            )
            status = self._escape_inline(opp.get("status", "") or "").replace("\n", " ")

            lines.append(f"## {category}")
            lines.append(f"**{self._t('Date', lang)}:** {date}")
            if location:
                lines.append(f"**{self._t('Location', lang)}:** {location}")
            if status:
                lines.append(f"**{self._t('Status', lang)}:** {status}")

            qa = opp.get("questions_answers", "")
            if qa:
                lines.append("")
                lines.append(f"**{self._t('Details', lang)}:**")
                lines.append(self._blockquote(qa))

            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
