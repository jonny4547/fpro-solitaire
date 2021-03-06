import os
import sys

import pygame
from svg import Parser, Rasterizer

import card

card_svgs = None
icon_svgs = None
back_svg = None
empty_svg = None

card_surfaces: dict[str, pygame.Surface] = None
icon_surfaces: dict[str, pygame.Surface] = None
back_surface: pygame.Surface = None
empty_surface: pygame.Surface = None


def get_icon():
    return render_svg(load_svg("icon.svg"), 1, False)


def load_svgs():
    global card_svgs, icon_svgs, back_svg, empty_svg
    card_svgs = {(suit, symbol): load_svg(f"{suit.value}_{symbol.value}.svg") for suit in card.Suit for symbol in card.Symbol}
    icon_svgs = {file.removesuffix(".svg"): load_svg(os.path.join("icons", file)) for file in os.listdir(normalize_path("icons")) if file.endswith(".svg")}
    back_svg = load_svg("back.svg")
    empty_svg = load_svg("empty.svg")


def render_svgs(scale):
    global card_surfaces, icon_surfaces, back_surface, empty_surface
    card_surfaces = {k: render_svg(v, scale) for k, v in card_svgs.items()}
    icon_surfaces = {k: render_svg(v, scale) for k, v in icon_svgs.items()}
    back_surface = render_svg(back_svg, scale)
    empty_surface = render_svg(empty_svg, scale)


def normalize_path(file):
    dir = getattr(sys, "_MEIPASS", "")
    return os.path.join(dir, "assets", file)


def load_svg(file):
    return Parser.parse_file(normalize_path(file))


rasterizer = Rasterizer()


def render_svg(svg, scale, convert=True):
    global rasterizer
    surface_size = round(svg.width * scale), round(svg.height * scale)
    buffer = rasterizer.rasterize(svg, *surface_size, scale)
    surface = pygame.image.frombuffer(buffer, surface_size, "RGBA")
    return surface.convert_alpha() if convert else surface
