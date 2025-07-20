@echo off
cd /d C:\agent_ia_referentiel

echo 🔄 Ajout des fichiers au commit...
git add .

echo ✅ Commit des fichiers nettoyés...
git commit -m "🔒 Clean: suppression de la clé API + ajout .gitignore"

echo 🚀 Push vers GitHub...
git push -u origin main

pause
