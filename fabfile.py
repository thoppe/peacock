from fabric.api import *

def commit():
    local("git commit -a")
    local("git status")
    local("git push")

def test():
    local("python petstore_minimal.py")

