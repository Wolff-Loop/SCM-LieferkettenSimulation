from pathlib import Path

root = Path(".")
output = Path("repo_review.txt")

included_extensions = {
    ".py",
    ".md",
    ".json",
    ".txt",
    ".toml",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
}

excluded_parts = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "builds",
    "dist",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "node_modules",
}

files = []

for path in root.rglob("*"):
    if not path.is_file():
        continue

    if any(part in excluded_parts for part in path.parts):
        continue

    if path.name == "repo_review.txt":
        continue

    if path.suffix.lower() in included_extensions:
        files.append(path)

files.sort(key=lambda path: str(path).lower())

with output.open("w", encoding="utf-8") as review:
    review.write("# Repository Review Export\n\n")

    review.write("## Git information\n\n")
    review.write("Branch: feature/event-system\n\n")

    review.write("## File overview\n\n")
    for path in files:
        review.write(f"- {path.as_posix()}\n")

    review.write("\n---\n\n")

    for path in files:
        review.write(f"# FILE: {path.as_posix()}\n\n")
        review.write("```")
        review.write(path.suffix.lstrip(".") or "text")
        review.write("\n")

        try:
            content = path.read_text(encoding="utf-8")
            review.write(content)
        except UnicodeDecodeError:
            review.write("[Datei konnte nicht als UTF-8 gelesen werden]")

        if not content.endswith("\n"):
            review.write("\n")

        review.write("```\n\n---\n\n")

print(f"Erstellt: {output.resolve()}")
print(f"Dateigröße: {output.stat().st_size / 1024:.1f} KB")
print(f"Enthaltene Dateien: {len(files)}")
