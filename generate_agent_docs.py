#!/usr/bin/env python3
"""
Generiert eine menschenlesbare Markdown-Datei (docs/AGENTS.md)
aus der maschinenlesbaren agents.yaml.
"""

import yaml
from pathlib import Path

INPUT = Path("agents.yaml")
OUTPUT_DIR = Path("docs")
OUTPUT = OUTPUT_DIR / "AGENTS.md"


def section(title: str, level: int = 2) -> str:
    return f"{'#' * level} {title}\n"


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"{INPUT} nicht gefunden.")

    with open(INPUT, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    OUTPUT_DIR.mkdir(exist_ok=True)
    lines = []

    # Projekt-Kopf
    p = data["project"]
    lines.append(f"# {p['name']}\n")
    lines.append(f"> {p['description']}\n")

    lines.append(section("Projekt-Übersicht"))
    lines.append(f"{p['overview']}\n")

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
        lines.append(f"{agent['prompt']}\n")
        lines.append(section("Workflow", level=3))
        for phase in agent["workflow"]:
            lines.append(f"#### Phase {phase['phase']}: {phase['title']}\n")
            for i, step in enumerate(phase["steps"], 1):
                lines.append(f"{i}. {step}")
            lines.append("")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] {OUTPUT} erfolgreich generiert.")


if __name__ == "__main__":
    main()
