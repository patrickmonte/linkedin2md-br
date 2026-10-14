"""Identity section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class VerificationsFormatter(BaseFormatter):
    """Format verifications section."""

    @property
    def section_key(self) -> str:
        return "verifications"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Identity Verifications', lang)}", ""]

        for v in data:
            name_parts = [
                v.get("first_name", ""),
                v.get("middle_name", ""),
                v.get("last_name", ""),
            ]
            name = self._escape_joined(
                " ".join(p for p in name_parts if p and p != "N/A")
            )

            lines.append(f"## {name}")
            if v.get("verification_type"):
                value = self._escape_inline(v["verification_type"]).replace("\n", " ")
                lines.append(f"**{self._t('Type', lang)}:** {value}")
            if v.get("document_type"):
                value = self._escape_inline(v["document_type"]).replace("\n", " ")
                lines.append(f"**{self._t('Document', lang)}:** {value}")
            if v.get("provider"):
                value = self._escape_inline(v["provider"]).replace("\n", " ")
                lines.append(f"**{self._t('Provider', lang)}:** {value}")
            if v.get("verified_date"):
                verified = self._localize_date(v["verified_date"], lang)
                value = self._escape_inline(verified).replace("\n", " ")
                lines.append(f"**{self._t('Verified', lang)}:** {value}")
            if v.get("expiry_date") and v.get("expiry_date") != "N/A":
                expires = self._localize_date(v["expiry_date"], lang)
                value = self._escape_inline(expires).replace("\n", " ")
                lines.append(f"**{self._t('Expires', lang)}:** {value}")

            lines.append("")

        return "\n".join(lines)


@register_formatter
class IdentityAssetsFormatter(BaseFormatter):
    """Format identity assets section."""

    @property
    def section_key(self) -> str:
        return "identity_assets"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Uploaded Documents', lang)}", ""]

        for asset in data:
            name = self._escape_list_item(asset.get("name", ""))
            has_content = asset.get("has_content", False)
            status_text = (
                self._t("(with content)", lang)
                if has_content
                else self._t("(no content)", lang)
            )
            lines.append(f"- {name} {status_text}")

        lines.append("")
        return "\n".join(lines)
