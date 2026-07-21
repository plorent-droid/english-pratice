---
title: English Practice
emoji: ???
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---
# English Practice ? Tuteur d'anglais (écoute + expression orale)

Appli 100% open source : tu parles en anglais ? transcription (Whisper) ?
correction + réponse (Mistral, quantifié GGUF) ? tout tourne dans ce Space.

## Déploiement sur Hugging Face Spaces

1. Crée un nouveau Space sur https://huggingface.co/new-space
   - **SDK** : Docker
   - **Hardware** : CPU basic (gratuit) pour commencer
2. Pousse ces fichiers dans le repo du Space (via `git push` ou l'interface web) :
   - `Dockerfile`
   - `requirements.txt`
   - `app/main.py`
   - `app/static/index.html`
   - ce `README.md` (avec l'en-tête YAML en haut, obligatoire pour HF Spaces)
3. Le Space build automatiquement l'image Docker et démarre le service sur le port 7860.
4. Premier démarrage : le modèle Mistral GGUF (~4-5 Go) se télécharge depuis le Hub,
   ça peut prendre plusieurs minutes selon la charge du Hub.

## ?? Limites du tier gratuit (CPU basic)

- **Vitesse** : Mistral 7B sur CPU sans GPU répond en plusieurs secondes à ~1 minute
  par réponse. C'est utilisable mais pas instantané.
- **Mise en veille** : un Space gratuit s'endort après une période d'inactivité et
  redémarre à froid (recharge du modèle) à la prochaine visite.
- **Stockage non persistant** (sur le tier gratuit) : le modèle est re-téléchargé
  à chaque redémarrage à froid, sauf si tu actives un stockage persistant (payant).
- Si c'est trop lent, deux leviers : un modèle plus petit (`Mistral-7B` existe aussi
  en quantification plus agressive, ex. `Q3_K_S`), ou passer à un tier Space payant
  avec plus de vCPU/RAM.

## Modifier le modèle utilisé

Dans `app/main.py`, les variables `LLM_REPO` et `LLM_FILE` pointent vers un modèle
GGUF communautaire sur le Hub. Tu peux les changer (ou les surcharger via variables
d'environnement du Space) pour tester d'autres quantifications ou d'autres modèles
(ex. Llama 3 8B Instruct GGUF).

## Tester en local avant de déployer

```powershell
docker build -t english-practice .
docker run -p 7860:7860 english-practice
```

Puis ouvre http://localhost:7860 dans ton navigateur.

## Pistes d'amélioration

- Synthèse vocale (Piper/Coqui TTS) pour une réponse audio du tuteur.
- Historique de conversation multi-tours.
- Niveau ajustable (débutant/intermédiaire/avancé) via le prompt.
- Cache du modèle sur un stockage persistant pour éviter le re-téléchargement à froid.
