from __future__ import annotations

import json
import sys

from src.collector.service import BaseTickerCollectorService


def main() -> int:
    """Executa o coletor base via linha de comando."""

    if len(sys.argv) < 2:
        print("Uso: python -m src.main <TICKER>")
        return 1

    ticker = sys.argv[1].upper().strip()
    service = BaseTickerCollectorService()
    result = service.run(ticker)
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
