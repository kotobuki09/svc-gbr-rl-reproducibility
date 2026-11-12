#!/usr/bin/env python3
"""Generate the committed synthetic demonstration sample."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from svc_release.demo_data import generate_demo_frame


OUTPUT = ROOT / "data" / "sample" / "svc_demo_synthetic.csv"


def main() -> None:
    frame = generate_demo_frame()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)
    print(f"wrote {len(frame)} synthetic rows to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
