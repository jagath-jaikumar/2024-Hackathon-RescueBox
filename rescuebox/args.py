from dataclasses import dataclass


@dataclass
class RescueBoxArgs:
    audio_files: str | list[str]
