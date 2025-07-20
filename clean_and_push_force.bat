@echo off
cd /d C:\agent_ia_referentiel

echo 🔥 Suppression de l'historique contenant des secrets...
git filter-repo --path .streamlit/secrets.toml --invert-paths

echo 🔄 Reconnexion au dépôt distant...
git remote remove origin
git remote add origin https://github.com/dsconsultingbi/agent-ia-referentiel.git

echo 🚀 Push forcé du repo nettoyé...
git push origin --force --all
git push origin --force --tags

echo ✅ Nettoyage terminé. Le push a été forcé sans les secrets.
pause
