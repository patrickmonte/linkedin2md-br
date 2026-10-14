"""Learning section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class LearningFormatter(BaseFormatter):
    """Format LinkedIn Learning section."""

    @property
    def section_key(self) -> str:
        return "learning"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('LinkedIn Learning', lang)}", ""]

        for course in data:
            title = self._escape_list_item(course.get("title", ""))
            completed = course.get("completed_at")
            status = (
                self._t("Completed", lang)
                if completed
                else self._t("In Progress", lang)
            )
            lines.append(f"- **{title}** ({status})")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class LearningReviewsFormatter(BaseFormatter):
    """Format learning reviews section."""

    @property
    def section_key(self) -> str:
        return "learning_reviews"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Learning Reviews', lang)}", ""]
        lines.append(self._table_header(["Content", "Rating", "Date"], lang))
        lines.append("|---------|--------|------|")

        for review in data:
            content = self._escape_table_cell(review.get("content", ""))
            rating = self._escape_table_cell(review.get("rating", ""))
            date = self._escape_table_cell(
                self._localize_date(review.get("date", ""), lang)
            )
            lines.append(f"| {content} | {rating} | {date} |")

        lines.append("")
        return "\n".join(lines)
