# Model card - Star Trek Computer (Piper voice)

> DRAFT. Items marked TODO must be settled before the first release.

## Summary
- **Type:** Piper (VITS) text-to-speech voice, one speaker, English (en-US), TODO: 22.05 kHz medium (V2) or high (V3).
- **Format:** ONNX (`en_US-startrek_computer-medium.onnx` + `.onnx.json`), CPU inference.
- **Intended use:** personal / hobby home-automation announcements and fan projects.
- **Not intended for:** impersonating a real person, deceptive audio, commercial use.

## What the voice is
A synthetic voice in the *style* of the Star Trek ship's computer. It was trained on AI-generated speech, not on
recordings of any person, and is not a clone of or endorsed by any real person or by Paramount.

## How it was made
1. 3,828 short sentences (public-domain prose plus smart-home style replies).
2. GreyFoxx converted them to speech with an AI voice tool (TODO: name the tool and confirm its terms allow training
   and redistributing a model from its output).
3. A Piper model was fine-tuned on those clips with the Piper 1.x trainer (TODO: record base model and training time
   for the release that ships).
4. Exported to ONNX with default speaking settings baked in.

## Recommended Piper app settings
`length_scale 1.15`, `noise_scale 0.5`, `noise_w 0.5` (TODO: re-confirm for the shipped release).

## Terms of use (TODO: confirm final wording)
- Free to use and share, **not for profit**: do not sell it or use it in paid products/services; any website or
  generator offering it must be free to use.
- Do not use it to deceive anyone into thinking a real person said something.
- Piper is GPL-3.0. TODO: check the licence of the base voice the model was fine-tuned from and state it here.

## Known limitations
- Numbers, acronyms and unusual names may be mispronounced.
- English only, one speaker, no emotion control.
