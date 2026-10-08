# Changelog

## Unreleased
- Repository skeleton: installer (`stc-piper-voice install`), tests, CI, issue templates, docs.
- Voice packaged as `en_US-ships_computer-high` (V3, epoch 93, settings 1.1/0.8/0.8), 5 samples.
- Original medium voice added as `en_US-ships_computer-medium` (fine-tuned from Piper's Amy medium; the high voice is from Lessac high). Installer: `--model high|medium`. Samples in `samples/medium/`.
- Credits for GreyFoxx74 (voice creation and dataset generation via Voicebox) added to README and model card.
