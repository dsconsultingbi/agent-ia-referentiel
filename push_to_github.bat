@echo off
cd /d C:\agent_ia_referentiel

:: Initialisation du dépôt Git
git init

:: Ajout du dépôt distant GitHub
git remote add origin https://github.com/dsconsultingbi/agent-ia-referentiel.git

:: Ajout de tous les fichiers
git add .

:: Commit initial
git commit -m "Initial commit depuis le dossier local"

:: Passage à la branche main
git branch -M main

:: Push vers GitHub
git push -u origin main

pause
