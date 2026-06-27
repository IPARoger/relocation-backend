"""Shared Playwright helpers for settings smokes (WEB2 final QA prep)."""

from __future__ import annotations


def open_settings_minor_aspects_details(page) -> None:
    """Minor aspect controls live inside a closed <details> on the astrology subpage."""
    page.evaluate(
        "()=>{const d=document.getElementById('rm-settings-minor-aspects-advanced');"
        "if(d && !d.open) d.open=true;}"
    )


def wait_for_minor_aspects(page, timeout: int = 15000) -> None:
    open_settings_minor_aspects_details(page)
    page.wait_for_selector("#rm-settings-minor-aspects", state="attached", timeout=timeout)
