from pathlib import Path
import os
import azure.cognitiveservices.speech as speechsdk

def tts_generate(script):
    output_dir = Path("outputs/audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not region:
        raise RuntimeError("Azure Speech key or region not set")

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=region
    )

    # Education-friendly voice
    speech_config.speech_synthesis_voice_name = "en-IN-NeerjaNeural"

    for scene in script:
        scene_id = scene["scene_id"]
        text = scene["script"]

        audio_path = output_dir / f"scene_{scene_id}.wav"

        audio_config = speechsdk.audio.AudioOutputConfig(
            filename=str(audio_path)
        )

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(
                f"TTS failed for scene {scene_id}: {result.reason}"
            )

        print(f"[✓] Generated audio for scene {scene_id}")
