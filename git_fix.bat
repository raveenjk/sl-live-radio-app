@echo off
git rm -r --cached node_modules >nul 2>&1
git rm -r --cached dist >nul 2>&1
git add .
git commit -m "Fix gitignore and add favourite feature"
git push
