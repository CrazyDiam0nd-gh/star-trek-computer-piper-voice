# Star Trek Computer - Piper voice

An **unofficial, AI-generated** text-to-speech voice in the style of the Star Trek ship's computer, for
[Piper](https://github.com/OHF-Voice/piper1-gpl) and Home Assistant. It runs on a CPU, so a Raspberry Pi or a Home
Assistant box is enough. This repo holds the installer and instructions; the voice itself is a download on the
[Releases page](https://github.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice/releases).

> **Unofficial fan project. Not affiliated with or endorsed by Paramount or the Star Trek franchise.** The voice was
> trained on AI-generated speech. It is not a recording or a clone of any real person. See [MODEL_CARD.md](MODEL_CARD.md)
> for the terms of use.

Samples: [01-working](samples/01-working.wav), [02-cleaning-complete](samples/02-cleaning-complete.wav),
[03-warning](samples/03-warning.wav), [04-welcome](samples/04-welcome.wav) (download to play).

## Requirements

- Piper (the Home Assistant **Piper app**, a Wyoming Piper Docker container, or `piper-tts` on the command line).
- To use the installer: Python 3.9 or newer. (Or skip the installer and download the files by hand, see below.)

## Install

The voice is two files that must stay together: `en_US-startrek_computer-medium.onnx` and `.onnx.json`.

**Option A - installer (checks the download against `SHA256SUMS`):**

```bash
pipx install git+https://github.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice.git

# Home Assistant: copy straight into the share folder over SSH (needs the Terminal & SSH app, see below)
stc-piper-voice install --scp root@homeassistant.local:/share/piper

# Or into a local Piper voices folder
stc-piper-voice install --dest ~/piper-voices
```

`--dry-run` shows what would happen without downloading anything. `--tag v0.1.0` installs a specific release.

**Option B - by hand:** download the two files and `SHA256SUMS` from the latest release, check them
(`sha256sum -c SHA256SUMS`), and copy the two voice files into your Piper voices folder.

## Home Assistant (Piper app)

1. Get both files into the **`/share/piper`** folder on Home Assistant. **Do not use the Piper app's "Open Web UI"
   upload:** Home Assistant limits app web-page uploads to 16 MiB and this voice is larger, so you get
   *HTTP 413 - Maximum request body size 16777216 exceeded*. Use the official **Samba share** app
   (`smb://<ha-ip>/share`), the **Terminal & SSH** app (`scp` / `--scp` above), or any other access to `/share`.
2. **Restart the Piper app.**
3. **Settings -> Devices & services -> Wyoming Protocol -> Piper -> three dots -> Reload.** HA caches the voice list.
4. **Settings -> Voice assistants** -> your assistant -> **Text-to-speech: piper**, language **English (United States)**,
   voice **startrek_computer**.
5. Or from an automation:
   ```yaml
   action: tts.speak
   target:
     entity_id: tts.piper
   data:
     media_player_entity_id: media_player.your_speaker
     message: "Working. Cleaning program complete."
     options:
       voice: en_US-startrek_computer-medium
   ```

**Speaking style.** The voice file bakes in its intended settings, but the Piper app applies its own
*length_scale / noise_scale / noise_w* options to every voice and overrides them. If the voice sounds faster or
more wobbly than the samples, open **Settings -> Apps -> Piper -> Configuration** and set the three values listed
in [MODEL_CARD.md](MODEL_CARD.md), then Save and Restart. These apply to every voice in that Piper app.

## Piper command line

```bash
pip install piper-tts
echo "Working." | piper --model en_US-startrek_computer-medium.onnx --output_file out.wav
```

## Docker (Wyoming)

Put the two files in a folder and mount it as the data directory of a Wyoming Piper server, then add the **Wyoming
Protocol** integration in Home Assistant with that host and port `10200`:

```bash
docker run -d --name piper-startrek -p 10200:10200 -v "$PWD/piper-data:/data" \
  rhasspy/wyoming-piper --voice en_US-startrek_computer-medium
```

This uses the standard `rhasspy/wyoming-piper` image; check its documentation for current options.

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
| Faster or wobblier than the samples | The Piper app's own style options override the voice's. Set them as in MODEL_CARD.md. |
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

Scripts, tests and documentation: [MIT](LICENSE). The voice model has separate terms: [MODEL_CARD.md](MODEL_CARD.md).
