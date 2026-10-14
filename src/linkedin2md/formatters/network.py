"""Network section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class ConnectionsFormatter(BaseFormatter):
    """Format connections section."""

    @property
    def section_key(self) -> str:
        return "connections"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Connections', lang)}", ""]
        lines.append(
            self._table_header(["Name", "Company", "Position", "Connected"], lang)
        )
        lines.append("|------|---------|----------|-----------|")

        for conn in data:
            name = self._escape_table_cell(conn.get("name", ""))
            company = self._escape_table_cell(conn.get("company", ""))
            position = self._escape_table_cell(conn.get("position", ""))
            connected = self._escape_table_cell(
                self._localize_date(conn.get("connected_on", ""), lang)
            )
            lines.append(f"| {name} | {company} | {position} | {connected} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class CompaniesFollowedFormatter(BaseFormatter):
    """Format companies followed section."""

    @property
    def section_key(self) -> str:
        return "companies_followed"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Companies Followed', lang)}", ""]
        for company in data:
            name = self._escape_list_item(company.get("name", ""))
            lines.append(f"- {name}")
        lines.append("")
        return "\n".join(lines)


@register_formatter
class MembersFollowedFormatter(BaseFormatter):
    """Format members followed section."""

    @property
    def section_key(self) -> str:
        return "members_followed"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Members Followed', lang)}", ""]
        lines.append(self._table_header(["Name", "Date", "Status"], lang))
        lines.append("|------|------|--------|")

        for member in data:
            name = self._escape_table_cell(member.get("name", ""))
            date = self._escape_table_cell(
                self._localize_date(member.get("date", ""), lang)
            )
            status = self._escape_table_cell(member.get("status", ""))
            lines.append(f"| {name} | {date} | {status} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class InvitationsFormatter(BaseFormatter):
    """Format invitations section."""

    @property
    def section_key(self) -> str:
        return "invitations"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Connection Invitations', lang)}", ""]
        lines.append(self._table_header(["From", "To", "Date", "Direction"], lang))
        lines.append("|------|-----|------|-----------|")

        for inv in data:
            from_name = self._escape_table_cell(inv.get("from", ""))
            to_name = self._escape_table_cell(inv.get("to", ""))
            date = self._escape_table_cell(
                self._localize_date(inv.get("sent_at", ""), lang)
            )
            direction = self._escape_table_cell(inv.get("direction", ""))
            lines.append(f"| {from_name} | {to_name} | {date} | {direction} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class ImportedContactsFormatter(BaseFormatter):
    """Format imported contacts section."""

    @property
    def section_key(self) -> str:
        return "imported_contacts"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Imported Contacts', lang)}", ""]
        lines.append(self._table_header(["Name", "Email", "Title"], lang))
        lines.append("|------|-------|-------|")

        for contact in data:
            name = self._escape_table_cell(contact.get("name", ""))
            emails = self._escape_table_cell(contact.get("emails", ""))
            title = self._escape_table_cell(contact.get("title", ""))
            lines.append(f"| {name} | {emails} | {title} |")

        lines.append("")
        return "\n".join(lines)
