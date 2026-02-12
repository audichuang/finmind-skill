"""
FinMind client with automatic token loading and multi-token load balancing.

Usage:
    from finmind_client import get_loader

    dl = get_loader()
    df = dl.taiwan_stock_daily(stock_id="2330", start_date="2024-01-01")

Token config: Place finmind_tokens.json next to this file.
"""
import itertools
import json
from pathlib import Path
from FinMind.data import DataLoader

_CONFIG_PATH = Path(__file__).parent / "finmind_tokens.json"


class FinMindPool:
    """Round-robin token pool for load balancing across multiple FinMind accounts."""

    def __init__(self, tokens: list[str]):
        self._loaders: dict[str, DataLoader] = {}
        for token in tokens:
            dl = DataLoader()
            dl.login_by_token(api_token=token)
            self._loaders[token] = dl
        self._cycle = itertools.cycle(tokens)

    def get_loader(self) -> DataLoader:
        """Get next DataLoader in round-robin order."""
        return self._loaders[next(self._cycle)]


def _load_tokens() -> list[str]:
    """Load tokens from finmind_tokens.json. Returns empty list if file not found."""
    if not _CONFIG_PATH.exists():
        return []
    with open(_CONFIG_PATH) as f:
        return json.load(f)["tokens"]


# Module-level singleton
_tokens = _load_tokens()
_pool = FinMindPool(_tokens) if len(_tokens) > 1 else None
_single_loader = None


def get_loader() -> DataLoader:
    """
    Get a ready-to-use DataLoader with token authentication.

    - No config file   → anonymous DataLoader (~600 req/hr)
    - 1 token          → single authenticated DataLoader (~1,800 req/hr)
    - N tokens         → round-robin pool (N x 1,800 req/hr)
    """
    global _single_loader

    # Multi-token: round-robin
    if _pool:
        return _pool.get_loader()

    # Single token: reuse one loader
    if _tokens:
        if _single_loader is None:
            _single_loader = DataLoader()
            _single_loader.login_by_token(api_token=_tokens[0])
        return _single_loader

    # No token: anonymous
    if _single_loader is None:
        _single_loader = DataLoader()
    return _single_loader
