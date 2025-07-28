import os

def save_to_env(key: str, value: str, env_path: str = None):
    if env_path is None:
        # Get parent directory of current file and set .env path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        grandparent_dir = os.path.dirname(parent_dir)
        env_path = os.path.join(grandparent_dir, ".env")

    content = ""
    key_found = False

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            content = f.read()

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                key_found = True
                break

        if not key_found:
            if not content.endswith("\n"):
                content += "\n"
            content += f"\n{key}={value}\n"
        else:
            content = "\n".join(lines) + "\n"
    else:
        content = f"\n{key}={value}\n"

    with open(env_path, "w") as f:
        f.write(content)
