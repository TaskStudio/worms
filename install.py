import subprocess
import sys
import os


def install():
    venv_path = ".venv"

    if not os.path.exists(venv_path):
        subprocess.run([sys.executable, "-m", "venv", venv_path])

    activate_script = os.path.join(".venv", "Scripts", "activate")
    activate_cmd = f"{activate_script} && "

    install_cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

    full_cmd = activate_cmd + " ".join(install_cmd)

    subprocess.check_call(full_cmd, shell=True)
    with open("requirements.txt", "w") as requirements_file:
        subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            stdout=requirements_file,
            text=True,
            check=True,
        )


install()
