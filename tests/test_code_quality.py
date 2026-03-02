import subprocess

def test_flake8():
    result = subprocess.run(["flake8", "app/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Problèmes flake8:\n{result.stdout}"

def test_black():
    result = subprocess.run(["black", "--check", "app/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Problèmes de format black:\n{result.stdout}"

def test_mypy():
    result = subprocess.run(["mypy", "app/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Problèmes mypy:\n{result.stdout}"
