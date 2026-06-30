from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS_FILE = ROOT / "mcp_tools.yaml"


def parse_tools(text: str) -> list[dict[str, str]]:
    tools: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in text.splitlines():
        name_match = re.match(r'^-\s+name:\s+"?([^"]+)"?\s*$', line)
        if name_match:
            current = {"name": name_match.group(1)}
            tools.append(current)
            continue

        if current is None:
            continue

        field_match = re.match(r'^\s+(category|description):\s+"?([^"]+)"?\s*$', line)
        if field_match:
            current[field_match.group(1)] = field_match.group(2)

    return tools


def main() -> int:
    tools = parse_tools(TOOLS_FILE.read_text(encoding="utf-8"))
    if not tools:
        print("No tools found in mcp_tools.yaml", file=sys.stderr)
        return 1

    for tool in tools:
        print(
            f"{tool.get('name', '')}\t"
            f"{tool.get('category', '')}\t"
            f"{tool.get('description', '')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
