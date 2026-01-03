import os
import sys
import arcade

_texture_cache = {}
_sound_cache = {}


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def load_texture_cached(path: str):
    full_path = resource_path(path)
    if full_path not in _texture_cache:
        try:
            texture = arcade.load_texture(full_path)
            if texture is None or not hasattr(texture, 'image'):
                print(f"Warning: Failed to load texture: {path}")
                texture = arcade.Texture.create_empty("fallback", (1, 1))
            _texture_cache[full_path] = texture
        except Exception as e:
            print(f"Error loading texture {path}: {e}")
            _texture_cache[full_path] = arcade.Texture.create_empty("fallback", (1, 1))
    return _texture_cache[full_path]


def load_sound_cached(path: str):
    full_path = resource_path(path)
    if full_path not in _sound_cache:
        _sound_cache[full_path] = arcade.Sound(full_path)
    return _sound_cache[full_path]