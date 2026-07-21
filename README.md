---
title: English Practice
emoji: ðŸ—£ï¸
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# English Practice â€” Tuteur d'anglais (Ã©coute + expression orale)

Appli 100% open source : tu parles en anglais â†’ transcription (Whisper) â†’
correction + rÃ©ponse (Mistral, quantifiÃ© GGUF) â†’ tout tourne dans ce Space.

## DÃ©ploiement sur Hugging Face Spaces

1. CrÃ©e un nouveau Space sur https://huggingface.co/new-space
   - **SDK** : Docker
   - **Hardware** : CPU basic (gratuit) pour commencer
2. Pousse ces fichiers dans le repo du Space (via git push ou l'interface web) :
   - Dockerfile
   - requirements.txt
   - app/main.py
   - app/static/index.html
   - ce README.md (avec l'en-tÃªte YAML en haut, obligatoire pour HF Spaces)
3. Le Space build automatiquement l'image Docker et dÃ©marre le service sur le port 7860.
4. Premier dÃ©marrage : le modÃ¨le Mistral GGUF (~4-5 Go) se tÃ©lÃ©charge depuis le Hub,
   Ã§a peut prendre plusieurs minutes selon la charge du Hub.

## Limites du tier gratuit (CPU basic)

- Vitesse : Mistral 7B sur CPU sans GPU rÃ©pond en plusieurs secondes Ã  ~1 minute
  par rÃ©ponse. C'est utilisable mais pas instantanÃ©.
- Mise en veille : un Space gratuit s'endort aprÃ¨s une pÃ©riode d'inactivitÃ© et
  redÃ©marre Ã  froid (recharge du modÃ¨le) Ã  la prochaine visite.
- Stockage non persistant (sur le tier gratuit) : le modÃ¨le est re-tÃ©lÃ©chargÃ©
  Ã  chaque redÃ©marrage Ã  froid, sauf si tu actives un stockage persistant (payant).
- Si c'est trop lent, deux leviers : un modÃ¨le plus petit (Mistral-7B existe aussi
  en quantification plus agressive, ex. Q3_K_S), ou passer Ã  un tier Space payant
  avec plus de vCPU/RAM.

## Modifier le modÃ¨le utilisÃ©

Dans app/main.py, les variables LLM_REPO et LLM_FILE pointent vers un modÃ¨le
GGUF communautaire sur le Hub. Tu peux les changer (ou les surcharger via variables
d'environnement du Space) pour tester d'autres quantifications ou d'autres modÃ¨les
(ex. Llama 3 8B Instruct GGUF).

## Tester en local avant de dÃ©ployer

docker build -t english-practice .
docker run -p 7860:7860 english-practice

Puis ouvre http://localhost:7860 dans ton navigateur.

## Pistes d'amÃ©lioration

- SynthÃ¨se vocale (Piper/Coqui TTS) pour une rÃ©ponse audio du tuteur.
- Historique de conversation multi-tours.
- Niveau ajustable (dÃ©butant/intermÃ©diaire/avancÃ©) via le prompt.
- Cache du modÃ¨le sur un stockage persistant pour Ã©viter le re-tÃ©lÃ©chargement Ã  froid.