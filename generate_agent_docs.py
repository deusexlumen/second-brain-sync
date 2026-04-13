#!/usr/bin/env python3
"""
Generiert eine menschenlesbare Markdown-Datei (docs/AGENTS.md)
aus der maschinenlesbaren agents.yaml.
"""

import sys
import yaml
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential

INPUT = Path("agents.yaml")
OUTPUT_DIR = Path("docs")
OUTPUT = OUTPUT_DIR / "AGENTS.md"


def section(title: str, level: int = 2) -> str:
    return f"{'#' * level} {title}\n"


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    reraise=True,
)
def enhance_content_via_llm(content: str) -> str:
    """
    Platzhalter für zukünftige LLM-Integration.
    Aktuell pass-through; hier können API-Calls mit Retry-Logik ergänzt werden.
    """
    return content


def generate_markdown(data: dict) -> str:
    lines = []

    # Projekt-Kopf
    p = data["project"]
    lines.append(f"# {p['name']}\n")
    lines.append(f"> {p['description']}\n")

    lines.append(section("Projekt-Übersicht"))
    overview = enhance_content_via_llm(p["overview"])
    lines.append(f"{overview}\n")

    lines.append(section("Technologie-Stack"))
    stack = p["stack"]
    lines.append(f"- **Generator:** {stack['generator']}")
    lines.append(f"- **Theme:** {stack['theme']}")
    lines.append(f"- **Python-Env:** {stack['python_env']}")
    lines.append(f"- **Plugins:** {', '.join(stack['plugins'])}")
    lines.append(f"- **Markdown-Extensions:** {', '.join(stack['markdown_extensions'])}")
    lines.append(f"- **Editor:** {stack['editor']}")
    lines.append(f"- **Automatisierung:** {', '.join(stack['automation'])}\n")

    lines.append(section("Verzeichnisstruktur"))
    for key, value in p["directories"].items():
        lines.append(f"- `{key}` — {value}")
    lines.append("")

    lines.append(section("Build- und Entwicklungs-Befehle"))
    cmd = p["commands"]
    lines.append(f"### Lokaler Server: `{cmd['local_server']['script']}`\n")
    lines.append(f"{cmd['local_server']['description']}\n")
    lines.append(f"### Deploy: `{cmd['deploy']['script']}`\n")
    for i, step in enumerate(cmd["deploy"]["steps"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    lines.append(section("Inhalts-Konventionen"))
    c = p["conventions"]
    lines.append("**YAML-Frontmatter (Pflicht):**\n")
    for key, desc in c["frontmatter"]["fields"].items():
        lines.append(f"- `{key}`: {desc}")
    lines.append("")
    lines.append(f"**Wiki-Links:** `{c['wiki_links']['syntax']}`\n")
    lines.append(f"**Medien-Referenzen:** `{c['media_references']}`\n")
    lines.append("**Admonitions:** " + ", ".join(f"`{a}`" for a in c["admonitions"]) + "\n")
    lines.append("**Strukturelle Elemente:**\n")
    for elem in c["structural_elements"]:
        lines.append(f"- {elem}")
    lines.append("")

    lines.append(section("Git & Ignore-Regeln"))
    for note in p["git_rules"]["notes"]:
        lines.append(f"- {note}")
    lines.append(f"- Ignoriert: {', '.join(p['git_rules']['ignored'])}\n")

    lines.append(section("Sicherheits- und Pflegehinweise"))
    for note in p["safety_notes"]:
        lines.append(f"- {note}")
    lines.append("")

    # Agents
    for agent in data["agents"]:
        lines.append(section(f"Agent: {agent['name']}", level=2))
        lines.append(f"**Rolle:** {agent['role']}\n")
        lines.append(f"**Trigger:** {', '.join(f'`{t}`' for t in agent['trigger'])}\n")
        lines.append(f"**Tools:** {', '.join(f'`{t}`' for t in agent['tools'])}\n")
        prompt = enhance_content_via_llm(agent["prompt"])
        lines.append(f"{prompt}\n")
        lines.append(section("Workflow", level=3))
        for phase in agent["workflow"]:
            lines.append(f"#### Phase {phase['phase']}: {phase['title']}\n")
            for i, step in enumerate(phase["steps"], 1):
                lines.append(f"{i}. {step}")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    try:
        if not INPUT.exists():
            print(f"[ERROR] Eingabedatei nicht gefunden: {INPUT}", file=sys.stderr)
            return 1

        with open(INPUT, "r", encoding="utf-8") as f:
            raw_yaml = f.read()
    except OSError as exc:
        print(f"[ERROR] Datei konnte nicht gelesen werden: {exc}", file=sys.stderr)
        return 1

    try:
        data = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as exc:
        print(f"[ERROR] YAML-Parsing fehlgeschlagen: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("[ERROR] YAML-Struktur ungültig: Root-Element muss ein Dictionary sein.", file=sys.stderr)
        return 1

    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
        markdown = generate_markdown(data)

        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(markdown)
    except OSError as exc:
        print(f"[ERROR] Markdown-Datei konnte nicht geschrieben werden: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] {OUTPUT} erfolgreich generiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
