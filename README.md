# Ship's Computer - Piper voice (Star Trek-inspired)

An **unofficial, AI-generated** text-to-speech voice in the style of the Star Trek ship's computer, for
[Piper](https://github.com/OHF-Voice/piper1-gpl) and Home Assistant. It runs on a CPU, so a Raspberry Pi or a Home
Assistant box is enough. This repo holds the installer and instructions; the voice itself is a download on the
[Releases page](https://github.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice/releases).

> **Unofficial fan project. Not affiliated with or endorsed by Paramount or the Star Trek franchise.** The voice was
> trained on AI-generated speech. It is not a recording or a clone of any real person. See [MODEL_CARD.md](MODEL_CARD.md)
> for the terms of use.

Samples (download to play). The same five lines in each voice:

| Line | high | medium |
|---|---|---|
| "Working. Diverting auxiliary power to the forward sensors." | [play](samples/01-working.wav) | [play](samples/medium/01-working.wav) |
| "Scan complete. No life signs detected." | [play](samples/02-scan-complete.wav) | [play](samples/medium/02-scan-complete.wav) |
| "Warning. Hull breach on deck seven." | [play](samples/03-warning.wav) | [play](samples/medium/03-warning.wav) |
| "Welcome aboard. All systems are operating normally." | [play](samples/04-welcome.wav) | [play](samples/medium/04-welcome.wav) |
| "Insufficient data. Please restate the query." | [play](samples/05-insufficient-data.wav) | [play](samples/medium/05-insufficient-data.wav) |

## What is this, and what do I need?

This is a **voice for Piper**, the free text-to-speech engine that Home Assistant uses to talk. Each voice is just two
files (a voice model and its config). You do not need Docker, a GPU or an account: install the two files into whatever Piper
you already use.

**Which section should I follow?**

| You use... | Follow |
|---|---|
| Home Assistant OS / Supervised with the **Piper app** (most people) | [Home Assistant (Piper app)](#home-assistant-piper-app) |
| Piper on the command line, in scripts or other software | [Piper command line](#piper-command-line) |
| Home Assistant **Container/Core** (no apps), or Piper on a separate machine | [Docker (Wyoming)](#docker-wyoming-only-if-you-have-no-piper-app) |

Not sure? If your Home Assistant has a **Settings -> Apps** (or *Add-ons*) page where you can install things like
Piper, you want the first row.

**Requirements:** one of the setups above. The optional installer needs Python 3.9 or newer; you can also download
the files by hand.

## Choose a voice: high or medium

Two versions are available. Both are the same ship's-computer voice trained on the same ~3,800 clips; they differ in
the Piper model they were trained on top of.

| | **high** (default) | **medium** (the original) |
|---|---|---|
| Voice name | `en_US-ships_computer-high` | `en_US-ships_computer-medium` |
| Trained on | Piper's public **Lessac high** checkpoint | Piper's public **Amy medium** checkpoint |
| Size | ~114 MB | ~64 MB |
| Character | Sounds more human, smoother flow | The first voice we made; lighter and faster; some people prefer its sound |
| Baked-in settings | `length_scale 1.1`, `noise_scale 0.8`, `noise_w 0.8` | `length_scale 1.15`, `noise_scale 0.5`, `noise_w 0.5` |

Not sure? Listen to the samples above and pick the one you like. **Medium** was the first voice we made, and some
people prefer its sound; **high** sounds more human. Medium is also the lighter choice on very limited hardware.
You can install both: they have different names, so Home Assistant lists them side by side.

## Install

Each voice is two files that must stay together: `en_US-ships_computer-high.onnx` and `.onnx.json` (or the `-medium`
pair).

**Option A - installer (checks the download against `SHA256SUMS`):**

```bash
pipx install git+https://github.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice.git

# Home Assistant: copy straight into the share folder over SSH (needs the Terminal & SSH app, see below)
stc-piper-voice install --scp root@homeassistant.local:/share/piper

# Or into a local Piper voices folder
stc-piper-voice install --dest ~/piper-voices
```

Add `--model medium` to install the medium voice instead (`--model high` is the default); run the command twice, once
per model, to have both.

`--dry-run` shows what would happen without downloading anything. `--tag v0.1.0` installs a specific release.

**Option B - by hand:** download the two files of the voice you want, plus `SHA256SUMS`, from the latest release. Check them
(`sha256sum -c --ignore-missing SHA256SUMS`) and copy the two voice files into your Piper voices folder.

## Home Assistant (Piper app)

1. Get both files into the **`/share/piper`** folder on Home Assistant. **Do not use the Piper app's "Open Web UI"
   upload:** Home Assistant limits app web-page uploads to 16 MiB and this voice is larger, so you get
   *HTTP 413 - Maximum request body size 16777216 exceeded*. Use the official **Samba share** app
   (`smb://<ha-ip>/share`), the **Terminal & SSH** app (`scp` / `--scp` above), or any other access to `/share`.
2. **Restart the Piper app.**
3. **Settings -> Devices & services -> Wyoming Protocol -> Piper -> three dots -> Reload.** HA caches the voice list.
4. **Settings -> Voice assistants** -> your assistant -> **Text-to-speech: piper**, language **English (United States)**,
   voice **ships_computer** (the high and medium versions are listed by quality).
5. Or from an automation:
   ```yaml
   action: tts.speak
   target:
     entity_id: tts.piper
   data:
     media_player_entity_id: media_player.your_speaker
     message: "Working. Cleaning program complete."
     options:
       voice: en_US-ships_computer-high   # or en_US-ships_computer-medium
   ```

**Speaking style.** Each voice file bakes in its intended settings (high: `length_scale 1.1`, `noise_scale 0.8`,
`noise_w 0.8`; medium: 1.15 / 0.5 / 0.5), but the Piper app applies its own *length_scale / noise_scale / noise_w* options to every voice and
overrides them (defaults 1.0 / 0.667 / 0.333). If the voice sounds different from the samples, open
**Settings -> Apps -> Piper -> Configuration**, set those three values, then Save and Restart. They apply to every
voice in that Piper app, so if you run both versions you cannot have each at its own settings; pick the one you use most.

## Piper command line

```bash
pip install piper-tts
echo "Working." | piper --model en_US-ships_computer-high.onnx --output_file out.wav
```

## Docker (Wyoming) - only if you have no Piper app

**Skip this section if you use the Home Assistant Piper app or the command line.** Docker is not needed to use the
voice and the installer never uses it.

Why it exists: Home Assistant talks to Piper over a network protocol called Wyoming. The Piper app is simply a
ready-made Wyoming Piper server. If your Home Assistant has no apps (Home Assistant Container or Core) or you want
Piper on another machine, you run a Wyoming Piper server yourself, and Docker is the easy way to do that.

1. Put the two voice files in a folder (here `piper-data`) and start the server with that folder mounted:
   ```bash
   mkdir -p piper-data && cp en_US-ships_computer-high.onnx* piper-data/   # or the -medium files
   docker run -d --name piper-ships-computer -p 10200:10200 -v "$PWD/piper-data:/data" \
     rhasspy/wyoming-piper --voice en_US-ships_computer-high   # or -medium
   ```
2. In Home Assistant: **Settings -> Devices & services -> Add integration -> Wyoming Protocol**, enter the IP of the
   machine running Docker and port `10200`.
3. Choose the voice in your assistant as described in the Home Assistant section.

This uses the standard `rhasspy/wyoming-piper` image; check its documentation for current options. (Untested with
this voice.)

## Optional: make the whole house feel like a starship (LCARS)

The voice pairs well with an LCARS-style Home Assistant dashboard. I use the community LCARS theme for Home
Assistant ([th3jesta/ha-lcars](https://github.com/th3jesta/ha-lcars); a separate project, not part of this one;
LCARS is a design language from Star Trek). Neither is required.

## Optional: a ship's-computer assistant

See [`examples/openai-conversation-prompt.txt`](examples/openai-conversation-prompt.txt): instructions for Home
Assistant's OpenAI Conversation agent that make it answer briefly, in plain speakable text, like a starship computer.
Only entities you have exposed to Assist can be controlled.

## Troubleshooting

| Symptom | Fix |
|---|---|
| HTTP 413 when uploading in the Piper app | Home Assistant caps app web uploads at 16 MiB. Put the files in `/share/piper` (Samba / SSH) instead. |
| Voice not in the list | Restart the Piper app, then reload Wyoming -> Piper. Both file names must match exactly apart from the extension. |
| Only some voices listed | Piper lists voices per language. Set the assistant's TTS language to English (United States). |
| Different from the samples | The Piper app's own style options override the voice's. Set them to 1.1 / 0.8 / 0.8 for high, 1.15 / 0.5 / 0.5 for medium (see above). |
| `Checksum mismatch` from the installer | The download was corrupted or the release is wrong. Retry; if it persists, open an issue. |

## Reporting a problem

[Open an issue](https://github.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice/issues/new/choose) and include:
what you expected vs what happened, where you use the voice (HA app / Docker / CLI) with versions, and the installer
output or Piper logs. **Never paste tokens or passwords.**

## Development

```bash
git clone https://github.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice.git
cd star-trek-computer-piper-voice
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Status of this README

Verified: the installer's download, checksum and local-copy logic (unit tests, Linux). **Not yet verified:** the `--scp`
path against a real Home Assistant, Windows and macOS runs (CI will cover tests only), and the Docker command.
The first release has not been published yet.

## Credits & Acknowledgements

### Star Trek-Inspired Computer Voice - [GreyFoxx74](https://github.com/GreyFoxx74)

Special thanks to **[GreyFoxx74](https://github.com/GreyFoxx74)** for the time, effort and technical work involved in creating the Star Trek-inspired computer voice used in this project.

GreyFoxx74 developed the voice model and generated the audio dataset through a multi-stage process:

- **Voice sample creation:** Created multiple audio samples inspired by Star Trek starship computers using various audio tools and AI technologies.
- **Audio preparation:** Selected the clearest samples and combined them into a single 27-second WAV file using Audacity, working within Voicebox's maximum sample duration.
- **Voice model training:** Imported the prepared audio into Voicebox, supplied the corresponding transcription and generated a custom voice model.
- **Voice generation testing:** Tested different synthesis engines and determined that `chatterbox_turbo` produced better results than `Qwen 1.7B` for this particular voice.
- **Dataset generation:** Developed and ran a script that processed a source CSV containing approximately 3,800 unique sentences, automatically requesting audio generation through Voicebox and saving the resulting files locally.
- **Further processing:** The completed collection of approximately 3,800 voice samples was then passed to **CrazyDiam0nd** for additional GPU-based processing into the final TTS implementation.

This work provided the foundation for the project's custom Star Trek-inspired computer voice.

**A huge thank you to GreyFoxx74 for their contribution, experimentation and dedication to bringing this voice to life.**

### Other

- [Piper](https://github.com/OHF-Voice/piper1-gpl) (engine and trainer; GPL-3.0).
- No code was copied from other projects.

## Disclaimer

Unofficial. Not affiliated with, authorised or endorsed by Paramount or the Star Trek franchise. Star Trek and related
names belong to their owners.

## License

The MIT licence in [LICENSE](LICENSE) covers the scripts, tests and documentation in this repository only. The voice model (the GitHub Release files) has separate terms: [MODEL_CARD.md](MODEL_CARD.md).
