def update_settings(updates, settings):
    for key, value in updates.items():
        if value is not None:
            setattr(settings, key, value)
