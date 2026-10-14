"""Activity history section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class SearchQueriesFormatter(BaseFormatter):
    """Format search queries section."""

    @property
    def section_key(self) -> str:
        return "search_queries"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Search History', lang)}", ""]
        lines.append(self._table_header(["Time", "Query"], lang))
        lines.append("|------|-------|")

        for q in data:
            time = self._escape_table_cell(self._localize_date(q.get("time", ""), lang))
            query = self._escape_table_cell(q.get("query", ""))
            lines.append(f"| {time} | {query} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class LoginsFormatter(BaseFormatter):
    """Format logins section."""

    @property
    def section_key(self) -> str:
        return "logins"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Login History', lang)}", ""]
        lines.append(self._table_header(["Date", "IP Address", "Type"], lang))
        lines.append("|------|------------|------|")

        for login in data:
            date = self._escape_table_cell(
                self._localize_date(login.get("date", ""), lang)
            )
            ip = self._escape_table_cell(login.get("ip_address", ""))
            login_type = self._escape_table_cell(login.get("login_type", ""))
            lines.append(f"| {date} | {ip} | {login_type} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class SecurityChallengesFormatter(BaseFormatter):
    """Format security challenges section."""

    @property
    def section_key(self) -> str:
        return "security_challenges"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Security Challenges', lang)}", ""]
        lines.append(
            self._table_header(["Date", "IP Address", "Country", "Type"], lang)
        )
        lines.append("|------|------------|---------|------|")

        for c in data:
            date = self._escape_table_cell(self._localize_date(c.get("date", ""), lang))
            ip = self._escape_table_cell(c.get("ip_address", ""))
            country = self._escape_table_cell(c.get("country", ""))
            ctype = self._escape_table_cell(c.get("challenge_type", ""))
            lines.append(f"| {date} | {ip} | {country} | {ctype} |")

        lines.append("")
        return "\n".join(lines)
