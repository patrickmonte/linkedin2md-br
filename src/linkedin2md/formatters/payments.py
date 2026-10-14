"""Payment section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class ReceiptsFormatter(BaseFormatter):
    """Format receipts section."""

    @property
    def section_key(self) -> str:
        return "receipts"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Payment Receipts', lang)}", ""]
        lines.append(
            self._table_header(["Date", "Description", "Amount", "Currency"], lang)
        )
        lines.append("|------|-------------|--------|----------|")

        for receipt in data:
            date = self._escape_table_cell(
                self._localize_date(receipt.get("date", ""), lang)
            )
            desc = self._escape_table_cell(receipt.get("description", ""))
            amount = self._escape_table_cell(receipt.get("amount", ""))
            currency = self._escape_table_cell(receipt.get("currency", ""))
            lines.append(f"| {date} | {desc} | {amount} | {currency} |")

        lines.append("")
        return "\n".join(lines)
