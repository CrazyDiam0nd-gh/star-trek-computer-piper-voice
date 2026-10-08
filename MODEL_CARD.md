# Model card - Ship's Computer (Piper voice)

> DRAFT. Items marked TODO must be settled before the first release.

## Summary
- **Type:** Piper (VITS) text-to-speech voice, one speaker, English (en-US), 22.05 kHz. Two versions are published:
  **high** (larger model, default) and **medium** (the original, smaller model).
- **Format:** ONNX (`en_US-ships_computer-high.onnx` / `en_US-ships_computer-medium.onnx`, each with a `.onnx.json`),
  CPU inference.
- **Intended use:** personal / hobby home-automation announcements and fan projects.
- **Not intended for:** impersonating a real person, deceptive audio, commercial use.

## What the voice is
A synthetic voice in the *style* of the Star Trek ship's computer. It was trained on AI-generated speech, not on
recordings of any person, and is not a clone of or endorsed by any real person or by Paramount.

## How it was made
1. 3,828 short sentences (public-domain prose plus smart-home style replies).
2. GreyFoxx74 made a custom voice in Voicebox (from a 27-second prepared sample, using the `chatterbox_turbo` engine)
   and generated about 3,800 clips with it (see the credits in the README).
   Licences (from web search results on 2026-10-07; verify against each project's LICENSE file before release):
   Voicebox ([jamiepine/voicebox](https://github.com/jamiepine/voicebox)) is reported as MIT; Chatterbox Turbo
   (Resemble AI) is MIT, with PerTh watermarking of its output. Neither is reported to restrict training on or
   redistributing models trained from generated audio. TODO: confirm in the LICENSE files and Hugging Face model card.
3. Both versions were fine-tuned on the same clips with the Piper 1.x trainer, starting from different public Piper
   checkpoints (from the `rhasspy/piper-checkpoints` collection):
   - **high:** started from Piper's **Lessac high** checkpoint; about 93 training epochs were used for the released
     checkpoint (chosen by ear over later checkpoints).
   - **medium** (the original release): started from Piper's **Amy medium** checkpoint; final validation mel loss
     about 0.384.
4. Exported to ONNX with default speaking settings baked in.

## Recommended Piper app settings
Also baked into each voice's `.onnx.json`:
- high: `length_scale 1.1`, `noise_scale 0.8`, `noise_w 0.8`
- medium: `length_scale 1.15`, `noise_scale 0.5`, `noise_w 0.5`

## Terms of use (TODO: confirm final wording)
- Free to use and share, **not for profit**: do not sell it or use it in paid products/services; any website or
  generator offering it must be free to use.
- Do not use it to deceive anyone into thinking a real person said something.
- Piper is GPL-3.0. TODO: check the licences of the Lessac high and Amy medium base checkpoints the models were
  fine-tuned from and state them here.

## Known limitations
- Numbers, acronyms and unusual names may be mispronounced.
- English only, one speaker, no emotion control.
