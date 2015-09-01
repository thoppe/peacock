from fabric.api import *

def commit():
    local("git commit -a")
    local("git status")
    local("git push")



