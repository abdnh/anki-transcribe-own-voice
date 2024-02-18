from __future__ import annotations

from concurrent.futures import Future
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from asr.providers import Provider

from importlib import import_module
from types import ModuleType

from aqt.addons import AddonManager
from aqt.main import AnkiQt

from .config import config


def get_asr_addon(addon_manager: AddonManager) -> ModuleType | None:
    for meta in addon_manager.all_addon_meta():
        if meta.ankiweb_id() == 411601849 or meta.human_name() in (
            "Speech Recognition for Anki",
            "asr",
        ):
            return import_module(meta.dir_name)
    return None


def transcribe(
    mw: AnkiQt,
    path: str,
    on_done: Callable[[Future], None] | None = None,
) -> Future | None:
    asr = get_asr_addon(mw.addonManager)
    if not asr:
        return None
    providers: list[type[Provider]] = asr.providers.PROVIDERS
    provider_class = next(
        (provider for provider in providers if provider.name == config["provider"]),
        providers[-1],
    )
    provider: Provider = asr.providers.init_provider(provider_class)
    return provider.transcribe_in_background(
        path, config["language"], mw.taskman, on_done
    )
