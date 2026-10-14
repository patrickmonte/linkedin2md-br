"""Content section formatters.

Each formatter handles ONE section (SRP).
"""

from linkedin2md.formatters.base import BaseFormatter
from linkedin2md.registry import register_formatter


@register_formatter
class PostsFormatter(BaseFormatter):
    """Format posts section."""

    @property
    def section_key(self) -> str:
        return "posts"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Posts', lang)}", ""]

        for post in data:
            date = self._escape_heading(self._localize_date(post.get("date", ""), lang))
            lines.append(f"## {date}")

            content = self._get_text(post.get("content"), lang)
            if content:
                lines.append("")
                lines.append(self._escape_block(content))

            link = self._render_link(self._t("View Post", lang), post.get("url"))
            if link:
                lines.append("")
                lines.append(link)

            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class CommentsFormatter(BaseFormatter):
    """Format comments section."""

    @property
    def section_key(self) -> str:
        return "comments"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Comments', lang)}", ""]

        for comment in data:
            date = self._escape_inline(
                self._localize_date(comment.get("date", ""), lang)
            ).replace("\n", " ")
            message = self._get_text(comment.get("message"), lang)
            link = self._render_link(self._t("View", lang), comment.get("url", ""))

            lines.append(f"**{date}**")
            if message:
                lines.append(self._blockquote(message))
            if link:
                lines.append(link)
            lines.append("")

        return "\n".join(lines)


@register_formatter
class ReactionsFormatter(BaseFormatter):
    """Format reactions section."""

    @property
    def section_key(self) -> str:
        return "reactions"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Reactions', lang)}", ""]
        lines.append(self._table_header(["Date", "Type", "Link"], lang))
        lines.append("|------|------|------|")

        view = self._t("View", lang)
        for reaction in data:
            date = self._escape_table_cell(
                self._localize_date(reaction.get("date", ""), lang)
            )
            rtype = self._escape_table_cell(reaction.get("type", ""))
            link = self._render_table_link(view, reaction.get("url", ""))
            lines.append(f"| {date} | {rtype} | {link} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class RepostsFormatter(BaseFormatter):
    """Format reposts section."""

    @property
    def section_key(self) -> str:
        return "reposts"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Reposts', lang)}", ""]
        lines.append(self._table_header(["Date", "Link"], lang))
        lines.append("|------|------|")

        view = self._t("View", lang)
        for repost in data:
            date = self._escape_table_cell(
                self._localize_date(repost.get("date", ""), lang)
            )
            link = self._render_table_link(view, repost.get("url", ""))
            lines.append(f"| {date} | {link} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class VotesFormatter(BaseFormatter):
    """Format votes section."""

    @property
    def section_key(self) -> str:
        return "votes"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Poll Votes', lang)}", ""]
        lines.append(self._table_header(["Date", "Option", "Link"], lang))
        lines.append("|------|--------|------|")

        view = self._t("View", lang)
        for vote in data:
            date = self._escape_table_cell(
                self._localize_date(vote.get("date", ""), lang)
            )
            option = self._escape_table_cell(vote.get("option", ""))
            link = self._render_table_link(view, vote.get("url", ""))
            lines.append(f"| {date} | {option} | {link} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class SavedItemsFormatter(BaseFormatter):
    """Format saved items section."""

    @property
    def section_key(self) -> str:
        return "saved_items"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Saved Items', lang)}", ""]
        lines.append(self._table_header(["Saved At", "Link"], lang))
        lines.append("|----------|------|")

        view = self._t("View", lang)
        for item in data:
            saved_at = self._escape_table_cell(
                self._localize_date(item.get("saved_at", ""), lang)
            )
            link = self._render_table_link(view, item.get("url", ""))
            lines.append(f"| {saved_at} | {link} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class EventsFormatter(BaseFormatter):
    """Format events section."""

    @property
    def section_key(self) -> str:
        return "events"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Events', lang)}", ""]
        lines.append(self._table_header(["Name", "Time", "Status"], lang))
        lines.append("|------|------|--------|")

        for event in data:
            name = self._escape_table_cell(event.get("name", ""))
            time = self._escape_table_cell(
                self._localize_date(event.get("time", ""), lang)
            )
            status = self._escape_table_cell(event.get("status", ""))
            lines.append(f"| {name} | {time} | {status} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class MediaFormatter(BaseFormatter):
    """Format uploaded media section."""

    @property
    def section_key(self) -> str:
        return "media"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Uploaded Media', lang)}", ""]
        lines.append(self._table_header(["Date", "Description", "Link"], lang))
        lines.append("|------|-------------|------|")

        view = self._t("View", lang)
        for m in data:
            date = self._escape_table_cell(self._localize_date(m.get("date", ""), lang))
            desc = self._escape_table_cell(m.get("description", ""))
            link = self._render_table_link(view, m.get("url", ""))
            lines.append(f"| {date} | {desc} | {link} |")

        lines.append("")
        return "\n".join(lines)


@register_formatter
class MessagesFormatter(BaseFormatter):
    """Format messages section."""

    @property
    def section_key(self) -> str:
        return "messages"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Messages', lang)}", ""]
        from_label = self._t("From", lang)
        to_label = self._t("To", lang)
        subject_label = self._t("Subject", lang)

        for msg in data:
            date = self._escape_heading(self._localize_date(msg.get("date", ""), lang))
            from_name = self._escape_inline(msg.get("from_name", "")).replace("\n", " ")
            to_name = self._escape_inline(msg.get("to_name", "")).replace("\n", " ")
            subject = self._escape_inline(msg.get("subject", "") or "").replace(
                "\n", " "
            )
            content = msg.get("content", "") or ""

            lines.append(f"## {date}")
            lines.append(f"**{from_label}:** {from_name} → **{to_label}:** {to_name}")
            if subject:
                lines.append(f"**{subject_label}:** {subject}")
            if content:
                lines.append("")
                truncated = self._truncate_text(content, 500, "message.content")
                lines.append(self._blockquote(truncated))
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class ScriptFormatter(BaseFormatter):
    """Format scripts section."""

    @property
    def section_key(self) -> str:
        return "scripts"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Scripts', lang)}", ""]

        for script in data:
            name = self._escape_heading(script.get("name", ""))
            date = self._escape_inline(
                self._localize_date(script.get("date", ""), lang)
            ).replace("\n", " ")
            content = script.get("content", "") or ""

            lines.append(f"## {name}")
            if date:
                lines.append(f"**{self._t('Date', lang)}:** {date}")
            if content:
                lines.append("")
                lines.append(self._escape_block(content))
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


@register_formatter
class ArticlesFormatter(BaseFormatter):
    """Format published articles section."""

    @property
    def section_key(self) -> str:
        return "articles"

    def _format_content(self, data: list, lang: str) -> str:
        lines = [f"# {self._t('Published Articles', lang)}", ""]

        for article in data:
            title = self._escape_heading(article.get("title", ""))
            date = self._escape_inline(
                self._localize_date(article.get("date", ""), lang)
            ).replace("\n", " ")
            author = self._escape_inline(article.get("author", "")).replace("\n", " ")
            summary = article.get("summary", "")

            lines.append(f"## {title}")
            if date:
                lines.append(f"**{self._t('Date', lang)}:** {date}")
            if author:
                lines.append(f"**{self._t('Author', lang)}:** {author}")
            if summary:
                lines.append("")
                lines.append(self._escape_block(summary))
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
