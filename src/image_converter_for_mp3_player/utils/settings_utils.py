from image_converter_for_mp3_player.config import Settings


def update_settings(updates: dict, settings: Settings):
    for key, value in updates.items():
        if value is not None:
            setattr(settings, key, value)
