# ============================================================
# PAZZAN.CHRONOX - LUXURY MOBILE EDITION (TALLER BUTTONS & GLOW)
# Android / Pydroid 3 / Kivy
# ============================================================

import os
import json
import math
import time
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line


# ---------------- COHESIVE LUXURY PALETTE ----------------

GOLD = (0.89, 0.72, 0.39, 1)
GOLD_SOFT = (0.76, 0.61, 0.34, 1)
TEAL = (0.34, 0.73, 0.76, 1)
SLATE_ACCENT = (0.48, 0.56, 0.72, 1)
ROSE_MUTED = (0.78, 0.42, 0.48, 1)
SAGE_ACCENT = (0.38, 0.68, 0.56, 1)

DARK_BG = (0.028, 0.040, 0.072, 1)
DARK_CARD = (0.070, 0.092, 0.155, 0.86)
DARK_GLASS_BAR = (0.095, 0.125, 0.205, 0.84)
DARK_BORDER = (0.78, 0.63, 0.35, 0.48)
DARK_INPUT = (0.115, 0.145, 0.225, 1)
DARK_TEXT = (0.96, 0.95, 0.92, 1)
DARK_MUTED = (0.60, 0.67, 0.80, 1)
DARK_BTN_MUTED = (0.14, 0.18, 0.27, 1)

LIGHT_BG = (0.93, 0.94, 0.97, 1)
LIGHT_CARD = (0.99, 0.995, 1.0, 0.88)
LIGHT_GLASS_BAR = (1.0, 1.0, 1.0, 0.86)
LIGHT_BORDER = (0.68, 0.54, 0.28, 0.42)
LIGHT_INPUT = (0.87, 0.90, 0.95, 1)
LIGHT_TEXT = (0.09, 0.12, 0.19, 1)
LIGHT_MUTED = (0.38, 0.44, 0.56, 1)
LIGHT_BTN_MUTED = (0.82, 0.86, 0.92, 1)


# ---------------- ANIMATED BACKGROUND ----------------

class AmbientBackground(Widget):

    def __init__(self, dark=True, **kwargs):
        super().__init__(**kwargs)
        self.dark = dark
        self.phase = 0.0

        self.orbs = [
            {"rx": 0.20, "ry": 0.78, "rad": 0.38, "sx": 0.06, "sy": 0.05, "px": 0.0, "py": 1.2, "kind": "gold"},
            {"rx": 0.82, "ry": 0.56, "rad": 0.35, "sx": 0.05, "sy": 0.06, "px": 2.1, "py": 0.4, "kind": "teal"},
            {"rx": 0.48, "ry": 0.25, "rad": 0.42, "sx": 0.045, "sy": 0.055, "px": 4.0, "py": 2.7, "kind": "gold"},
        ]

        self.sparks = [
            (0.16, 0.86, 0.8, 1.4, dp(3.5), "gold"),
            (0.86, 0.74, 1.1, 1.8, dp(3.0), "teal"),
            (0.30, 0.48, 0.7, 1.2, dp(4.0), "gold"),
            (0.76, 0.32, 1.3, 1.5, dp(3.2), "teal"),
            (0.55, 0.66, 0.9, 1.7, dp(2.8), "gold"),
        ]

        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_interval(self.step, 1 / 30.0)

    def set_theme(self, dark):
        self.dark = dark
        self.redraw()

    def step(self, dt):
        self.phase += dt
        self.redraw()

    def redraw(self, *_):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return

        base_dim = min(self.width, self.height)

        with self.canvas:
            # Animated glowing orbs (more noticeable yet smooth)
            for orb in self.orbs:
                dx = math.sin(self.phase * orb["sx"] * 6.0 + orb["px"]) * self.width * 0.08
                dy = math.cos(self.phase * orb["sy"] * 6.0 + orb["py"]) * self.height * 0.06
                pulse = 1.0 + 0.08 * math.sin(self.phase * 1.4 + orb["px"])

                cx = self.x + self.width * orb["rx"] + dx
                cy = self.y + self.height * orb["ry"] + dy
                r = base_dim * orb["rad"] * pulse

                if orb["kind"] == "gold":
                    rgb = (0.91, 0.74, 0.40) if self.dark else (0.84, 0.65, 0.28)
                    a_outer = 0.075 if self.dark else 0.14
                    a_mid = 0.125 if self.dark else 0.20
                    a_core = 0.16 if self.dark else 0.24
                else:
                    rgb = (0.34, 0.76, 0.80) if self.dark else (0.22, 0.62, 0.68)
                    a_outer = 0.065 if self.dark else 0.12
                    a_mid = 0.115 if self.dark else 0.18
                    a_core = 0.145 if self.dark else 0.22

                Color(rgb[0], rgb[1], rgb[2], a_outer)
                Ellipse(pos=(cx - r * 1.35, cy - r * 1.35), size=(r * 2.7, r * 2.7))

                Color(rgb[0], rgb[1], rgb[2], a_mid)
                Ellipse(pos=(cx - r * 0.90, cy - r * 0.90), size=(r * 1.8, r * 1.8))

                Color(rgb[0], rgb[1], rgb[2], a_core)
                Ellipse(pos=(cx - r * 0.48, cy - r * 0.48), size=(r * 0.96, r * 0.96))

            # Floating ambient dust / light motes
            for idx, (bx, by, freq, amp, dot_sz, kind) in enumerate(self.sparks):
                drift_x = math.sin(self.phase * freq + idx) * dp(18)
                drift_y = ((self.phase * 12 * freq + idx * 45) % max(40, self.height * 0.35)) - dp(20)
                px = self.x + self.width * bx + drift_x
                py = self.y + self.height * (by - 0.12) + drift_y + math.cos(self.phase * amp) * dp(8)

                twinkle = 0.35 + 0.65 * abs(math.sin(self.phase * 2.0 + idx * 1.3))
                if kind == "gold":
                    rgb = (0.94, 0.78, 0.44) if self.dark else (0.80, 0.60, 0.22)
                else:
                    rgb = (0.40, 0.82, 0.86) if self.dark else (0.20, 0.58, 0.64)

                base_alpha = (0.48 if self.dark else 0.55) * twinkle
                Color(rgb[0], rgb[1], rgb[2], base_alpha * 0.35)
                Ellipse(pos=(px - dot_sz, py - dot_sz), size=(dot_sz * 3, dot_sz * 3))

                Color(rgb[0], rgb[1], rgb[2], base_alpha)
                Ellipse(pos=(px, py), size=(dot_sz, dot_sz))


# ---------------- BASIC LABEL ----------------

def make_label(text="", size=14, color=(1, 1, 1, 1),
               bold=False, align="center", height=None):
    w = Label(
        text=text,
        font_size=dp(size),
        color=color,
        bold=bold,
        halign=align,
        valign="middle",
        size_hint_y=None,
        height=dp(height if height is not None else max(28, size * 2.15)),
    )
    w.bind(size=lambda obj, val: setattr(obj, "text_size", val))
    return w


# ---------------- 3D + GLASS BRAND BAR ----------------

class Glass3DBar(BoxLayout):

    def __init__(self, dark=True, **kwargs):
        super().__init__(**kwargs)
        self.dark = dark
        self.orientation = "horizontal"
        self.padding = (dp(14), dp(4))
        self.spacing = dp(8)

        with self.canvas.before:
            self.shadow_color = Color(0, 0, 0, 0.42 if dark else 0.14)
            self.shadow = RoundedRectangle(
                pos=(self.x, self.y - dp(3)),
                size=self.size,
                radius=[dp(18)]
            )

            self.glass_color = Color(*(DARK_GLASS_BAR if dark else LIGHT_GLASS_BAR))
            self.glass = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

            self.sheen_color = Color(1, 1, 1, 0.10 if dark else 0.50)
            self.sheen = RoundedRectangle(
                pos=(self.x + dp(2), self.y + self.height * 0.52),
                size=(max(0, self.width - dp(4)), max(0, self.height * 0.44)),
                radius=[dp(16)]
            )

            self.border_color = Color(*(DARK_BORDER if dark else LIGHT_BORDER))
            self.border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(18)),
                width=1.25
            )

        self.bind(pos=self.draw, size=self.draw)

    def set_theme(self, dark):
        self.dark = dark
        self.shadow_color.rgba = (0, 0, 0, 0.42 if dark else 0.14)
        self.glass_color.rgba = DARK_GLASS_BAR if dark else LIGHT_GLASS_BAR
        self.sheen_color.rgba = (1, 1, 1, 0.10 if dark else 0.50)
        self.border_color.rgba = DARK_BORDER if dark else LIGHT_BORDER
        self.draw()

    def draw(self, *_):
        self.shadow.pos = (self.x, self.y - dp(3))
        self.shadow.size = self.size
        self.glass.pos = self.pos
        self.glass.size = self.size
        self.sheen.pos = (self.x + dp(2), self.y + self.height * 0.52)
        self.sheen.size = (max(0, self.width - dp(4)), max(0, self.height * 0.44))
        self.border.rounded_rectangle = (
            self.x, self.y, self.width, self.height, dp(18)
        )


# ---------------- GLASS CARD ----------------

class GlassCard(BoxLayout):

    def __init__(self, dark=True, **kwargs):
        super().__init__(**kwargs)
        self.dark = dark
        self.orientation = "vertical"
        self.padding = dp(14)
        self.spacing = dp(8)

        with self.canvas.before:
            self.shadow_color = Color(0, 0, 0, 0.28 if dark else 0.08)
            self.shadow = RoundedRectangle(
                pos=(self.x, self.y - dp(2.5)),
                size=self.size,
                radius=[dp(20)]
            )

            self.bg_color = Color(*(DARK_CARD if dark else LIGHT_CARD))
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(20)]
            )

            self.border_color = Color(*(DARK_BORDER if dark else LIGHT_BORDER))
            self.border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(20)),
                width=1.15
            )

        self.bind(pos=self.draw, size=self.draw)

    def set_theme(self, dark):
        self.dark = dark
        self.shadow_color.rgba = (0, 0, 0, 0.28 if dark else 0.08)
        self.bg_color.rgba = DARK_CARD if dark else LIGHT_CARD
        self.border_color.rgba = DARK_BORDER if dark else LIGHT_BORDER
        self.draw()

    def draw(self, *_):
        self.shadow.pos = (self.x, self.y - dp(2.5))
        self.shadow.size = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rounded_rectangle = (
            self.x, self.y, self.width, self.height, dp(20)
        )


# ---------------- COHESIVE TALL BUTTON ----------------

class CXButton(Button):

    def __init__(self, tone="gold", active=False, dark=True, **kwargs):
        self.tone = tone
        self.active = active
        self.dark = dark
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.font_size = dp(11.5)
        self.bold = True

        self.size_hint_y = None
        if not self.height:
            self.height = dp(54)

        self.bind(pos=self.draw, size=self.draw)
        self.bind(on_press=self.press_anim)
        self.bind(on_release=self.release_anim)

    def set_theme(self, dark):
        self.dark = dark
        self.draw()

    def draw(self, *_):
        muted_fill = DARK_BTN_MUTED if self.dark else LIGHT_BTN_MUTED
        colors = {
            "gold": GOLD,
            "teal": TEAL,
            "slate": SLATE_ACCENT,
            "rose": ROSE_MUTED,
            "sage": SAGE_ACCENT,
            "muted": muted_fill,
        }

        fill = colors.get(self.tone, GOLD)

        if self.tone == "muted":
            self.color = DARK_TEXT if self.dark else LIGHT_TEXT
        elif self.tone in ("rose", "slate"):
            self.color = (0.98, 0.98, 0.99, 1)
        else:
            self.color = (0.04, 0.06, 0.10, 1)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.28 if self.dark else 0.10)
            RoundedRectangle(
                pos=(self.x, self.y - dp(2.5)),
                size=self.size,
                radius=[dp(14)]
            )

            Color(*fill)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

            if self.active:
                Color(*(1, 1, 1, 0.85) if self.dark else (0.12, 0.16, 0.24, 0.65))
                Line(
                    rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)),
                    width=1.4
                )

    def press_anim(self, *_):
        Animation(opacity=0.72, duration=0.07).start(self)

    def release_anim(self, *_):
        Animation(opacity=1, duration=0.14).start(self)


# ---------------- THEME SWITCH ----------------

class ThemeSwitch(Button):

    def __init__(self, is_dark=True, **kwargs):
        super().__init__(**kwargs)
        self.is_dark = is_dark
        self.text = "DARK" if is_dark else "LIGHT"
        self.font_size = dp(9.5)
        self.bold = True
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.size_hint = (None, None)
        self.size = (dp(82), dp(38))

        self.bind(pos=self.draw, size=self.draw)

    def set_dark(self, dark):
        self.is_dark = dark
        self.text = "DARK" if dark else "LIGHT"
        self.draw()

    def draw(self, *_):
        self.color = (0.96, 0.95, 0.92, 1) if self.is_dark else (0.09, 0.12, 0.19, 1)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*(0.17, 0.22, 0.33, 1) if self.is_dark else (0.78, 0.82, 0.89, 1))
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(19)]
            )

            knob_x = self.x + dp(2) if self.is_dark else self.right - dp(36)
            Color(*(GOLD if self.is_dark else (0.91, 0.65, 0.22, 1)))
            Ellipse(
                pos=(knob_x, self.y + dp(2)),
                size=(dp(34), dp(34))
            )


# ---------------- ANALOG CLOCK ----------------

class AnalogClock(Widget):

    def __init__(self, dark=True, **kwargs):
        super().__init__(**kwargs)
        self.dark = dark
        self.bind(pos=self.draw_clock, size=self.draw_clock)
        Clock.schedule_interval(self.update_clock, 1)

    def set_theme(self, dark):
        self.dark = dark
        self.draw_clock()

    def update_clock(self, _dt):
        self.draw_clock()

    def draw_clock(self, *_):
        self.canvas.clear()

        cx = self.center_x
        cy = self.center_y
        radius = min(self.width, self.height) * 0.44
        if radius <= 0:
            return

        now = datetime.now()

        with self.canvas:
            Color(0.89, 0.72, 0.39, 0.15 if self.dark else 0.19)
            Ellipse(
                pos=(cx - radius * 1.05, cy - radius * 1.05),
                size=(radius * 2.1, radius * 2.1)
            )

            Color(*(0.075, 0.10, 0.165, 0.96) if self.dark else (0.97, 0.98, 1.0, 0.98))
            Ellipse(
                pos=(cx - radius, cy - radius),
                size=(radius * 2, radius * 2)
            )

            Color(*GOLD)
            Line(circle=(cx, cy, radius), width=1.6)

            for i in range(60):
                angle = math.radians(i * 6 - 90)
                outer = radius * 0.93
                inner = radius * (0.81 if i % 5 == 0 else 0.87)

                x1 = cx + math.cos(angle) * inner
                y1 = cy + math.sin(angle) * inner
                x2 = cx + math.cos(angle) * outer
                y2 = cy + math.sin(angle) * outer

                Color(*GOLD if i % 5 == 0 else TEAL)
                Line(
                    points=[x1, y1, x2, y2],
                    width=1.6 if i % 5 == 0 else 0.7
                )

            def hand(value, maximum, length, width, color):
                angle = math.radians(value / maximum * 360 - 90)
                x = cx + math.cos(angle) * radius * length
                y = cy + math.sin(angle) * radius * length
                Color(*color)
                Line(points=[cx, cy, x, y], width=width)

            hour = (now.hour % 12) + now.minute / 60
            minute = now.minute + now.second / 60
            second = now.second

            hour_color = (0.96, 0.95, 0.92, 1) if self.dark else (0.10, 0.13, 0.20, 1)
            hand(hour, 12, 0.48, 3.6, hour_color)
            hand(minute, 60, 0.69, 2.3, GOLD)
            hand(second, 60, 0.80, 1.15, TEAL)

            Color(*GOLD)
            Ellipse(pos=(cx - dp(5), cy - dp(5)), size=(dp(10), dp(10)))
            Color(*(0.075, 0.10, 0.165, 1) if self.dark else (0.97, 0.98, 1.0, 1))
            Ellipse(pos=(cx - dp(2), cy - dp(2)), size=(dp(4), dp(4)))


# ---------------- MAIN APP ----------------

class ChronoXApp(App):

    def build(self):
        self.title = "PAZZAN.CHRONOX"
        self.data_file = os.path.join(self.user_data_dir, "pazzan_chronox.json")

        self.dark = True
        self.cards = []
        self.buttons = []
        self.inputs = []
        self.themed_labels = []
        self.form_open = False
        self.editing_idx = None

        self.load_data()

        self.sw_running = False
        self.sw_elapsed = 0.0
        self.sw_started = 0.0
        self.lap_count = 0

        self.timer_running = False
        self.timer_remaining = 300.0
        self.timer_deadline = 0.0

        self.manager_active = None
        self.manager_started = 0.0

        Window.clearcolor = DARK_BG

        container = RelativeLayout()

        self.bg_anim = AmbientBackground(
            dark=self.dark,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        container.add_widget(self.bg_anim)

        self.root = BoxLayout(
            orientation="vertical",
            padding=(dp(10), dp(8)),
            spacing=dp(6),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        # 3D + Glass Top Brand Bar
        self.header = Glass3DBar(
            dark=self.dark,
            size_hint_y=None,
            height=dp(52)
        )

        self.brand = make_label(
            "PAZZAN.CHRONOX",
            size=17.5,
            color=GOLD,
            bold=True,
            align="left",
            height=42
        )
        self.header.add_widget(self.brand)

        self.theme_btn = ThemeSwitch(is_dark=self.dark)
        self.theme_btn.bind(on_release=self.toggle_theme)
        self.header.add_widget(self.theme_btn)

        self.root.add_widget(self.header)

        self.subtitle = make_label(
            "MAKE EVERY SECOND COUNT",
            size=10,
            color=DARK_MUTED,
            bold=True,
            align="left",
            height=20
        )
        self.themed_labels.append((self.subtitle, "muted"))
        self.root.add_widget(self.subtitle)

        self.sm = ScreenManager(transition=FadeTransition(duration=0.12))
        self.root.add_widget(self.sm)

        builders = {
            "Clock": self.make_clock,
            "Stopwatch": self.make_stopwatch,
            "Timer": self.make_timer,
            "Target": self.make_target,
            "Manage": self.make_manage,
        }

        for name in ["Clock", "Stopwatch", "Timer", "Target", "Manage"]:
            screen = Screen(name=name)
            screen.add_widget(builders[name]())
            self.sm.add_widget(screen)

        self.nav = GridLayout(
            cols=5,
            spacing=dp(5),
            size_hint_y=None,
            height=dp(56)
        )

        self.nav_buttons = {}
        for name in ["Clock", "Stopwatch", "Timer", "Target", "Manage"]:
            btn = self.reg_button(
                text=name.upper(),
                tone="muted",
                font_size=dp(9.2),
                height=54
            )
            btn.bind(on_release=lambda _b, n=name: self.go(n))
            self.nav.add_widget(btn)
            self.nav_buttons[name] = btn

        self.root.add_widget(self.nav)
        container.add_widget(self.root)

        self.go("Clock")
        self.apply_theme_colors()
        self.rebuild_target_list()

        Clock.schedule_interval(self.tick, 0.1)
        return container

    # ---------------- LAYOUT & THEME HELPERS ----------------

    def reg_button(self, **kwargs):
        btn = CXButton(dark=self.dark, **kwargs)
        self.buttons.append(btn)
        return btn

    def make_scroll_page(self):
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(3),
            scroll_type=["bars", "content"]
        )
        page = BoxLayout(
            orientation="vertical",
            spacing=dp(11),
            padding=(dp(2), dp(4), dp(2), dp(20)),
            size_hint_y=None
        )
        page.bind(minimum_height=page.setter("height"))
        scroll.add_widget(page)
        return scroll, page

    def add_card(self, page, height):
        card = GlassCard(
            dark=self.dark,
            size_hint_y=None,
            height=dp(height)
        )
        self.cards.append(card)
        page.add_widget(card)
        return card

    def make_heading(self, title, subtitle):
        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(54),
            spacing=dp(2)
        )
        main = make_label(
            title,
            size=21,
            color=DARK_TEXT if self.dark else LIGHT_TEXT,
            bold=True,
            height=32
        )
        sub = make_label(
            subtitle,
            size=10,
            color=DARK_MUTED if self.dark else LIGHT_MUTED,
            bold=True,
            height=20
        )
        self.themed_labels.append((main, "text"))
        self.themed_labels.append((sub, "muted"))
        box.add_widget(main)
        box.add_widget(sub)
        return box, main, sub

    def make_input(self, value="", int_only=True, hint="", halign="center"):
        ti = TextInput(
            text=value,
            hint_text=hint,
            multiline=False,
            input_filter="int" if int_only else None,
            font_size=dp(14.5),
            halign=halign,
            background_normal="",
            background_active="",
            background_color=DARK_INPUT if self.dark else LIGHT_INPUT,
            foreground_color=(1, 1, 1, 1) if self.dark else LIGHT_TEXT,
            hint_text_color=DARK_MUTED if self.dark else LIGHT_MUTED,
            cursor_color=GOLD,
            padding=[dp(8), dp(10), dp(8), dp(10)],
        )
        self.inputs.append(ti)
        return ti

    def apply_theme_colors(self):
        Window.clearcolor = DARK_BG if self.dark else LIGHT_BG
        self.bg_anim.set_theme(self.dark)
        self.header.set_theme(self.dark)
        self.theme_btn.set_dark(self.dark)

        if hasattr(self, "analog"):
            self.analog.set_theme(self.dark)

        for card in self.cards:
            card.set_theme(self.dark)

        for btn in self.buttons:
            btn.set_theme(self.dark)

        for lbl, role in self.themed_labels:
            if role == "text":
                lbl.color = DARK_TEXT if self.dark else LIGHT_TEXT
            elif role == "muted":
                lbl.color = DARK_MUTED if self.dark else LIGHT_MUTED

        for ti in self.inputs:
            ti.background_color = DARK_INPUT if self.dark else LIGHT_INPUT
            ti.foreground_color = (1, 1, 1, 1) if self.dark else LIGHT_TEXT
            ti.hint_text_color = DARK_MUTED if self.dark else LIGHT_MUTED

    def toggle_theme(self, *_):
        self.dark = not self.dark
        self.apply_theme_colors()
        self.rebuild_target_list()

    def go(self, name, *_):
        self.sm.current = name
        sub_map = {
            "Clock": "MAKE EVERY SECOND COUNT",
            "Stopwatch": "PRECISION TIME TRACKING",
            "Timer": "SET A TIME • STAY FOCUSED",
            "Target": "SET YOUR OWN DESTINATION",
            "Manage": "TRACK YOUR DAILY SESSIONS",
        }
        self.subtitle.text = sub_map.get(name, "MAKE EVERY SECOND COUNT")

        for page_name, btn in self.nav_buttons.items():
            is_active = (page_name == name)
            btn.tone = "gold" if is_active else "muted"
            btn.active = is_active
            btn.draw()

    # ---------------- CLOCK PAGE ----------------

    def make_clock(self):
        scroll, page = self.make_scroll_page()

        h, _, _ = self.make_heading(
            "Welcome back",
            "YOUR PERSONAL TIME EXPERIENCE"
        )
        page.add_widget(h)

        c = self.add_card(page, 330)
        c.add_widget(make_label("✦  LOCAL TIME  ✦", size=11, color=GOLD, bold=True, height=24))

        self.digital_time = make_label(
            "00:00:00 AM",
            size=31,
            color=DARK_TEXT if self.dark else LIGHT_TEXT,
            bold=True,
            height=48
        )
        self.themed_labels.append((self.digital_time, "text"))
        c.add_widget(self.digital_time)

        self.date_label = make_label("", size=12.5, color=TEAL, bold=True, height=24)
        c.add_widget(self.date_label)

        self.analog = AnalogClock(dark=self.dark, size_hint=(1, 1))
        c.add_widget(self.analog)

        note = self.add_card(page, 58)
        note.add_widget(make_label("TIME IS YOUR GREATEST LUXURY", size=12, color=GOLD, bold=True, height=28))

        return scroll

    # ---------------- STOPWATCH PAGE ----------------

    def make_stopwatch(self):
        scroll, page = self.make_scroll_page()

        h, _, _ = self.make_heading(
            "Stopwatch",
            "PRECISION TIME TRACKING"
        )
        page.add_widget(h)

        c = self.add_card(page, 174)

        self.sw_label = make_label("00:00:00.00", size=30, color=GOLD, bold=True, height=54)
        c.add_widget(self.sw_label)

        row = GridLayout(cols=4, spacing=dp(6), size_hint_y=None, height=dp(54))

        start_btn = self.reg_button(text="START", tone="teal", font_size=dp(9.5), height=54)
        start_btn.bind(on_release=self.sw_start)

        pause_btn = self.reg_button(text="PAUSE", tone="slate", font_size=dp(9.5), height=54)
        pause_btn.bind(on_release=self.sw_pause)

        reset_btn = self.reg_button(text="RESET", tone="rose", font_size=dp(9.5), height=54)
        reset_btn.bind(on_release=self.sw_reset)

        lap_btn = self.reg_button(text="LAP", tone="gold", font_size=dp(9.5), height=54)
        lap_btn.bind(on_release=self.sw_lap)

        for b in (start_btn, pause_btn, reset_btn, lap_btn):
            row.add_widget(b)

        c.add_widget(row)

        lap_card = self.add_card(page, 185)
        lap_card.add_widget(make_label("LAP HISTORY", size=11.5, color=GOLD, bold=True, height=24))

        self.lap_text = make_label(
            "Your laps will appear here.",
            size=12,
            color=DARK_MUTED if self.dark else LIGHT_MUTED,
            height=125
        )
        self.themed_labels.append((self.lap_text, "muted"))
        lap_card.add_widget(self.lap_text)

        return scroll

    # ---------------- TIMER PAGE ----------------

    def make_timer(self):
        scroll, page = self.make_scroll_page()

        h, _, _ = self.make_heading(
            "Countdown Timer",
            "SET A TIME • STAY FOCUSED"
        )
        page.add_widget(h)

        c = self.add_card(page, 268)

        self.timer_label = make_label("00:05:00", size=34, color=TEAL, bold=True, height=58)
        c.add_widget(self.timer_label)

        hints = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(20))
        min_hint = make_label("Min", size=10.5, color=DARK_MUTED if self.dark else LIGHT_MUTED, height=20)
        sec_hint = make_label("Sec", size=10.5, color=DARK_MUTED if self.dark else LIGHT_MUTED, height=20)
        self.themed_labels.extend([(min_hint, "muted"), (sec_hint, "muted")])
        hints.add_widget(min_hint)
        hints.add_widget(sec_hint)
        c.add_widget(hints)

        inputs = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(46))
        self.minutes_input = self.make_input("5")
        self.seconds_input = self.make_input("0")
        inputs.add_widget(self.minutes_input)
        inputs.add_widget(self.seconds_input)
        c.add_widget(inputs)

        row = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(54))
        start_btn = self.reg_button(text="START", tone="teal", font_size=dp(10), height=54)
        start_btn.bind(on_release=self.timer_start)

        pause_btn = self.reg_button(text="PAUSE", tone="slate", font_size=dp(10), height=54)
        pause_btn.bind(on_release=self.timer_pause)

        reset_btn = self.reg_button(text="RESET", tone="rose", font_size=dp(10), height=54)
        reset_btn.bind(on_release=self.timer_reset)

        for b in (start_btn, pause_btn, reset_btn):
            row.add_widget(b)

        c.add_widget(row)

        self.timer_status = make_label("Ready when you are.", size=12, color=GOLD, bold=True, height=28)
        page.add_widget(self.timer_status)

        return scroll

    # ---------------- TARGET PAGE ----------------

    def make_target(self):
        scroll, page = self.make_scroll_page()

        h, _, _ = self.make_heading(
            "MY TARGET",
            "SET YOUR OWN DESTINATION"
        )
        page.add_widget(h)

        # Prominent Countdown Box (Name + Big Countdown stay visible)
        countdown = self.add_card(page, 180)
        countdown.add_widget(make_label("ACTIVE COUNTDOWN", size=10.5, color=GOLD_SOFT, bold=True, height=20))

        self.active_target_title = make_label(
            "MY GOAL",
            size=23,
            color=GOLD,
            bold=True,
            height=38
        )
        countdown.add_widget(self.active_target_title)

        self.target_countdown = make_label(
            "-- DAYS",
            size=30,
            color=TEAL,
            bold=True,
            height=46
        )
        countdown.add_widget(self.target_countdown)

        self.target_detail = make_label(
            "00 : 00 : 00",
            size=19,
            color=DARK_TEXT if self.dark else LIGHT_TEXT,
            bold=True,
            height=30
        )
        self.themed_labels.append((self.target_detail, "text"))
        countdown.add_widget(self.target_detail)

        # Action bar: "+ ADD TARGET" and "EDIT" (tall touch targets)
        action_bar = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(8))
        self.add_target_toggle_btn = self.reg_button(
            text="+ ADD TARGET",
            tone="sage",
            height=54
        )
        self.add_target_toggle_btn.bind(on_release=self.toggle_add_form)

        self.edit_active_btn = self.reg_button(
            text="EDIT",
            tone="gold",
            size_hint_x=None,
            width=dp(96),
            height=54
        )
        self.edit_active_btn.bind(on_release=self.edit_selected_target)

        action_bar.add_widget(self.add_target_toggle_btn)
        action_bar.add_widget(self.edit_active_btn)
        page.add_widget(action_bar)

        # Collapsible Add / Edit Form Card
        self.add_target_card = GlassCard(
            dark=self.dark,
            size_hint_y=None,
            height=dp(0),
            opacity=0
        )
        self.cards.append(self.add_target_card)
        page.add_widget(self.add_target_card)

        self.form_heading_lbl = make_label(
            "Target Name",
            size=11,
            color=GOLD,
            bold=True,
            align="left",
            height=22
        )
        self.add_target_card.add_widget(self.form_heading_lbl)

        self.target_name_input = self.make_input(
            value="",
            int_only=False,
            hint="Enter custom target name...",
            halign="left"
        )
        self.target_name_input.size_hint_y = None
        self.target_name_input.height = dp(44)
        self.add_target_card.add_widget(self.target_name_input)

        self.add_target_card.add_widget(
            make_label("TARGET DATE & TIME", size=11, color=GOLD, bold=True, height=22)
        )

        grid = GridLayout(cols=3, spacing=dp(7), size_hint_y=None, height=dp(128))
        self.target_inputs = {}

        now = datetime.now()
        defaults = [
            ("Year", str(now.year + 1)),
            ("Month", str(now.month)),
            ("Day", str(now.day)),
            ("Hour", "0"),
            ("Minute", "0"),
            ("Second", "0"),
        ]

        for label_text, value in defaults:
            field_box = BoxLayout(orientation="vertical", spacing=dp(2))
            flbl = make_label(
                label_text,
                size=9.5,
                color=DARK_MUTED if self.dark else LIGHT_MUTED,
                height=18
            )
            self.themed_labels.append((flbl, "muted"))
            field = self.make_input(value, int_only=True, halign="center")
            field.size_hint_y = None
            field.height = dp(42)
            field_box.add_widget(flbl)
            field_box.add_widget(field)

            self.target_inputs[label_text.lower()] = field
            grid.add_widget(field_box)

        self.add_target_card.add_widget(grid)

        self.save_target_btn = self.reg_button(text="SAVE TARGET", tone="gold", height=54)
        self.save_target_btn.bind(on_release=self.save_target)
        self.add_target_card.add_widget(self.save_target_btn)

        self.target_status = make_label(
            "Tap '+ ADD TARGET' to create or 'EDIT' to update.",
            size=11.5,
            color=TEAL,
            bold=True,
            height=26
        )
        page.add_widget(self.target_status)

        # Saved Targets List Card
        self.saved_targets_card = self.add_card(page, 155)
        self.saved_targets_card.add_widget(
            make_label("SAVED TARGETS", size=11, color=GOLD, bold=True, align="left", height=22)
        )

        self.target_list_box = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )
        self.target_list_box.bind(minimum_height=self.target_list_box.setter("height"))
        self.saved_targets_card.add_widget(self.target_list_box)

        return scroll

    def _set_form_state(self, open_state, editing_idx=None):
        self.form_open = open_state
        self.editing_idx = editing_idx if open_state else None

        if self.form_open:
            self.add_target_card.height = dp(336)
            self.add_target_card.opacity = 1
            self.add_target_toggle_btn.text = "CANCEL"
            self.add_target_toggle_btn.tone = "rose"
            self.save_target_btn.text = "UPDATE TARGET" if self.editing_idx is not None else "SAVE TARGET"
        else:
            self.add_target_card.height = dp(0)
            self.add_target_card.opacity = 0
            self.add_target_toggle_btn.text = "+ ADD TARGET"
            self.add_target_toggle_btn.tone = "sage"
            self.save_target_btn.text = "SAVE TARGET"

        self.add_target_toggle_btn.draw()
        self.save_target_btn.draw()

    def toggle_add_form(self, *_):
        if self.form_open:
            self._set_form_state(False)
        else:
            self.target_name_input.text = ""
            self._set_form_state(True, editing_idx=None)

    def edit_selected_target(self, *_):
        active = self.get_active_target()
        if not active:
            self.target_name_input.text = ""
            self._set_form_state(True, editing_idx=None)
            return

        self.target_name_input.text = active.get("title", "")
        d = active.get("dt", {})
        for key in ("year", "month", "day", "hour", "minute", "second"):
            if key in d and key in self.target_inputs:
                self.target_inputs[key].text = str(d[key])

        self._set_form_state(True, editing_idx=self.active_target_idx)
        self.target_status.text = f"Editing: {active.get('title', 'MY GOAL')}"

    def get_active_target(self):
        if not self.targets:
            return None
        if 0 <= self.active_target_idx < len(self.targets):
            return self.targets[self.active_target_idx]
        self.active_target_idx = 0
        return self.targets[0]

    def save_target(self, *_):
        try:
            title = (self.target_name_input.text or "").strip() or "MY GOAL"
            values = {key: int(field.text) for key, field in self.target_inputs.items()}
            target_dt = datetime(
                values["year"],
                values["month"],
                values["day"],
                values["hour"],
                values["minute"],
                values["second"]
            )
            if target_dt <= datetime.now():
                self.target_status.text = "Please enter a valid name & future date."
                return

            item = {"title": title, "dt": values}

            if self.editing_idx is not None and 0 <= self.editing_idx < len(self.targets):
                self.targets[self.editing_idx] = item
                self.active_target_idx = self.editing_idx
                self.target_status.text = "Target updated!"
            else:
                self.targets.append(item)
                self.active_target_idx = len(self.targets) - 1
                self.target_status.text = "Target saved!"

            self.save_data()
            self.target_name_input.text = ""
            self.active_target_title.text = title
            self._set_form_state(False)
            self.rebuild_target_list()

        except (ValueError, TypeError, OverflowError):
            self.target_status.text = "Please enter a valid name & future date."

    def select_target(self, idx):
        if 0 <= idx < len(self.targets):
            self.active_target_idx = idx
            self.save_data()
            self.rebuild_target_list()

    def delete_target(self, idx):
        if 0 <= idx < len(self.targets):
            self.targets.pop(idx)
            if self.active_target_idx >= len(self.targets):
                self.active_target_idx = max(0, len(self.targets) - 1)
            if self.editing_idx == idx:
                self._set_form_state(False)
            self.save_data()
            self.rebuild_target_list()

    def rebuild_target_list(self):
        if not hasattr(self, "target_list_box"):
            return

        self.target_list_box.clear_widgets()

        if not self.targets:
            empty_lbl = make_label(
                "Tap '+ ADD TARGET' to create a countdown.",
                size=11.5,
                color=DARK_MUTED if self.dark else LIGHT_MUTED,
                height=30
            )
            self.target_list_box.add_widget(empty_lbl)
            self.saved_targets_card.height = dp(92)
            self.active_target_title.text = "MY GOAL"
            self.target_countdown.text = "-- DAYS"
            self.target_detail.text = "00 : 00 : 00"
            return

        for idx, item in enumerate(self.targets):
            row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(6))
            is_sel = (idx == self.active_target_idx)

            d = item["dt"]
            sub_date = f"{item['title']} ({d['year']}-{d['month']:02d}-{d['day']:02d})"
            sel_btn = self.reg_button(
                text=sub_date,
                tone="gold" if is_sel else "muted",
                active=is_sel,
                font_size=dp(10),
                height=50
            )
            sel_btn.bind(on_release=lambda _b, i=idx: self.select_target(i))

            edit_btn = self.reg_button(
                text="EDIT",
                tone="teal",
                size_hint_x=None,
                width=dp(64),
                font_size=dp(9.5),
                height=50
            )
            edit_btn.bind(on_release=lambda _b, i=idx: self._open_edit_at(i))

            del_btn = self.reg_button(
                text="DEL",
                tone="rose",
                size_hint_x=None,
                width=dp(58),
                font_size=dp(9.5),
                height=50
            )
            del_btn.bind(on_release=lambda _b, i=idx: self.delete_target(i))

            row.add_widget(sel_btn)
            row.add_widget(edit_btn)
            row.add_widget(del_btn)
            self.target_list_box.add_widget(row)

        self.saved_targets_card.height = dp(70 + len(self.targets) * 58)

    def _open_edit_at(self, idx):
        self.active_target_idx = idx
        self.save_data()
        self.edit_selected_target()
        self.rebuild_target_list()

    # ---------------- MANAGE PAGE ----------------

    def make_manage(self):
        scroll, page = self.make_scroll_page()

        h, _, _ = self.make_heading(
            "Time Manager",
            "TRACK YOUR DAILY SESSIONS"
        )
        page.add_widget(h)

        self.manage_labels = {}

        for category, tone in [("Study", "teal"), ("Break", "gold"), ("Personal", "slate")]:
            c = self.add_card(page, 120)

            row = BoxLayout(size_hint_y=None, height=dp(28))
            clbl = make_label(category, size=13, color=GOLD, bold=True, align="left", height=28)
            val = make_label(
                "00:00:00",
                size=14.5,
                color=DARK_TEXT if self.dark else LIGHT_TEXT,
                bold=True,
                align="right",
                height=28
            )
            self.themed_labels.append((val, "text"))
            row.add_widget(clbl)
            row.add_widget(val)
            c.add_widget(row)

            self.manage_labels[category] = val

            b = self.reg_button(text=f"START {category.upper()}", tone=tone, height=54)
            b.bind(on_release=lambda _b, cat=category: self.manager_start(cat))
            c.add_widget(b)

        stop_btn = self.reg_button(text="STOP SESSION", tone="rose", height=56)
        stop_btn.bind(on_release=self.manager_stop)
        page.add_widget(stop_btn)

        reset_btn = self.reg_button(text="RESET ALL TIMES", tone="muted", height=56)
        reset_btn.bind(on_release=self.manager_reset)
        page.add_widget(reset_btn)

        self.manager_status = make_label("No active session", size=11.5, color=TEAL, bold=True, height=28)
        page.add_widget(self.manager_status)

        return scroll

    # ---------------- DATA STORAGE ----------------

    def load_data(self):
        self.manager_totals = {"Study": 0.0, "Break": 0.0, "Personal": 0.0}
        self.targets = []
        self.active_target_idx = 0

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for key in self.manager_totals:
                self.manager_totals[key] = float(data.get("manager", {}).get(key, 0.0))

            raw_targets = data.get("targets")
            if isinstance(raw_targets, list):
                self.targets = raw_targets
            elif isinstance(data.get("target"), dict):
                self.targets = [{
                    "title": "MY GOAL",
                    "dt": data["target"]
                }]

            self.active_target_idx = int(data.get("active_target_idx", 0))
        except Exception:
            pass

    def save_data(self):
        try:
            data = {
                "manager": self.manager_totals,
                "targets": self.targets,
                "active_target_idx": self.active_target_idx
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    # ---------------- STOPWATCH LOGIC ----------------

    def sw_value(self):
        if self.sw_running:
            return self.sw_elapsed + (time.perf_counter() - self.sw_started)
        return self.sw_elapsed

    def sw_start(self, *_):
        if not self.sw_running:
            self.sw_started = time.perf_counter()
            self.sw_running = True

    def sw_pause(self, *_):
        if self.sw_running:
            self.sw_elapsed = self.sw_value()
            self.sw_running = False

    def sw_reset(self, *_):
        self.sw_running = False
        self.sw_elapsed = 0.0
        self.lap_count = 0
        self.sw_label.text = "00:00:00.00"
        self.lap_text.text = "Your laps will appear here."

    def sw_lap(self, *_):
        current = self.sw_value()
        if current > 0:
            self.lap_count += 1
            entry = f"Lap {self.lap_count:02d}   •   {self.format_duration(current)}"
            if self.lap_count == 1:
                self.lap_text.text = entry
            else:
                self.lap_text.text += "\n" + entry

    @staticmethod
    def format_duration(seconds):
        seconds = max(0.0, seconds)
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:05.2f}"

    # ---------------- TIMER LOGIC ----------------

    def _read_timer_inputs(self):
        mins = int(self.minutes_input.text or "0")
        secs = int(self.seconds_input.text or "0")
        if mins < 0 or secs < 0 or secs > 59:
            raise ValueError
        return mins * 60 + secs

    def timer_start(self, *_):
        if self.timer_running:
            return

        if self.timer_remaining <= 0:
            try:
                self.timer_remaining = self._read_timer_inputs()
            except ValueError:
                self.timer_status.text = "Please enter valid values."
                return

        if self.timer_remaining <= 0:
            self.timer_status.text = "Please enter valid values."
            return

        self.timer_deadline = time.perf_counter() + self.timer_remaining
        self.timer_running = True
        self.timer_status.text = "Timer is running."

    def timer_pause(self, *_):
        if self.timer_running:
            self.timer_remaining = max(0.0, self.timer_deadline - time.perf_counter())
            self.timer_running = False
            self.timer_status.text = "Timer paused."

    def timer_reset(self, *_):
        self.timer_running = False
        try:
            self.timer_remaining = self._read_timer_inputs()
        except ValueError:
            self.timer_remaining = 0.0

        self.timer_label.text = self.format_hms(self.timer_remaining)
        self.timer_status.text = "Ready when you are."

    @staticmethod
    def format_hms(seconds):
        seconds = max(0, int(seconds))
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    # ---------------- MANAGE LOGIC ----------------

    def manager_start(self, category, *_):
        if self.manager_active:
            self.manager_stop()

        self.manager_active = category
        self.manager_started = time.perf_counter()
        self.manager_status.text = f"Tracking: {category}"

    def manager_stop(self, *_):
        if self.manager_active:
            elapsed = time.perf_counter() - self.manager_started
            self.manager_totals[self.manager_active] += elapsed
            self.manager_active = None
            self.save_data()
            self.manager_status.text = "Session saved!"

    def manager_reset(self, *_):
        self.manager_totals = {"Study": 0.0, "Break": 0.0, "Personal": 0.0}
        self.manager_active = None
        self.manager_started = 0.0
        self.save_data()
        self.manager_status.text = "All times reset."

    # ---------------- MAIN UPDATE ----------------

    def tick(self, _dt):
        now = datetime.now()
        current_screen = self.sm.current

        if current_screen == "Clock":
            self.digital_time.text = now.strftime("%I:%M:%S %p")
            self.date_label.text = now.strftime("%A, %d %B %Y")

        if current_screen == "Stopwatch":
            self.sw_label.text = self.format_duration(self.sw_value())

        if self.timer_running:
            self.timer_remaining = max(0.0, self.timer_deadline - time.perf_counter())
            self.timer_label.text = self.format_hms(self.timer_remaining)
            if self.timer_remaining <= 0:
                self.timer_running = False
                self.timer_status.text = "Countdown complete!"

        if current_screen == "Target":
            active = self.get_active_target()
            if active:
                self.active_target_title.text = active.get("title", "MY GOAL")
                d = active.get("dt", {})
                try:
                    target_dt = datetime(
                        d["year"],
                        d["month"],
                        d["day"],
                        d["hour"],
                        d["minute"],
                        d["second"]
                    )
                    remaining = (target_dt - now).total_seconds()
                    if remaining > 0:
                        days = int(remaining // 86400)
                        rem = int(remaining % 86400)
                        hours, rem = divmod(rem, 3600)
                        minutes, seconds = divmod(rem, 60)

                        self.target_countdown.text = f"{days} DAYS"
                        self.target_detail.text = f"{hours:02d} : {minutes:02d} : {seconds:02d}"
                    else:
                        self.target_countdown.text = "Your target time has arrived!"
                        self.target_detail.text = "00 : 00 : 00"
                except Exception:
                    pass

        if current_screen == "Manage":
            for category, display in self.manage_labels.items():
                total = self.manager_totals[category]
                if category == self.manager_active:
                    total += time.perf_counter() - self.manager_started
                display.text = self.format_hms(total)


if __name__ == "__main__":
    ChronoXApp().run()
