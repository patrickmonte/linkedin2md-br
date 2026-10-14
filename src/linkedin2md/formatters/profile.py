"""Profile section formatter.

Single Responsibility: Format profile data to Markdown.
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class ProfileFormatter(BaseFormatter):
    """Format complete profile section."""

    @property
    def section_key(self) -> str:
        return "profile"

    def _format_content(self, data: dict, lang: str) -> str:
        """Format profile data from composed profile section dict."""
        lines = []

        name = data.get("name", "")
        if name:
            lines.append(f"# {self._escape_heading(name)}")
            lines.append("")

        title = self._get_text(data.get("title"), lang)
        if title:
            title_value = self._escape_inline(title).replace("\n", " ")
            lines.append(f"**{title_value}**")
            lines.append("")

        contact_parts = []
        if data.get("location"):
            contact_parts.append(data["location"])
        if data.get("email"):
            contact_parts.append(data["email"])
        if data.get("phone"):
            contact_parts.append(data["phone"])
        if contact_parts:
            lines.append(
                " | ".join(
                    self._escape_inline(part).replace("\n", " ")
                    for part in contact_parts
                )
            )
            lines.append("")

        summary = self._get_text(data.get("summary"), lang)
        if summary:
            lines.append(f"## {self._t('Summary', lang)}")
            lines.append("")
            lines.append(self._escape_block(summary))
            lines.append("")

        meta = data.get("profile_meta", {})
        if meta:
            detail_lines: list[str] = []

            def add_detail(label: str, value: str) -> None:
                detail_lines.append(f"- **{self._t(label, lang)}:** {value}")

            if meta.get("industry"):
                industry = self._escape_inline(meta["industry"]).replace("\n", " ")
                add_detail("Industry", industry)
            if meta.get("maiden_name"):
                maiden_name = self._escape_inline(meta["maiden_name"]).replace(
                    "\n", " "
                )
                add_detail("Maiden Name", maiden_name)
            if meta.get("public_profile_url"):
                link = self._render_link(
                    meta["public_profile_url"], meta["public_profile_url"]
                )
                if link:
                    add_detail("Profile URL", link)
            if meta.get("address"):
                address = self._escape_inline(meta["address"]).replace("\n", " ")
                add_detail("Address", address)
            if meta.get("twitter"):
                twitter = self._escape_inline(meta["twitter"]).replace("\n", " ")
                add_detail("Twitter", twitter)
            if meta.get("websites"):
                for site in meta["websites"]:
                    website = self._render_plain_url(site)
                    if website:
                        add_detail("Website", website)
            if meta.get("birth_date"):
                birth_date = self._escape_inline(meta["birth_date"]).replace("\n", " ")
                add_detail("Birth Date", birth_date)
            if meta.get("registered_at"):
                registered = self._localize_date(meta["registered_at"], lang)
                registered_at = self._escape_inline(registered).replace("\n", " ")
                add_detail("Member Since", registered_at)
            if meta.get("connections_count"):
                connections = self._escape_inline(meta["connections_count"]).replace(
                    "\n", " "
                )
                add_detail("Connections", connections)
            if detail_lines:
                lines.append(f"## {self._t('Profile Details', lang)}")
                lines.append("")
                lines.extend(detail_lines)
                lines.append("")

        return "\n".join(lines)
