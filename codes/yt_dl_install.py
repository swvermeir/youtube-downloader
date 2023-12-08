import subprocess

install = True

subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip"])
modules = ['youtube-dl', 'requests', 'winshell', 'pywin32', 'pyunpack', 'patool', "beautifulsoup4", "tqdm"]
for module in modules:
    if install:
        subprocess.run(["py", "-m", "pip", "install", module])
    else:
        subprocess.run(["py", "-m", "pip", "uninstall", "-y", module])
