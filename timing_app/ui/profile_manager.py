"""
profile_manager.py

Manages overlay profiles stored in profiles.ini.
Encapsulates load/save/delete logic and returns Profile objects.
"""

import os
import configparser
from dataclasses import dataclass
import profile
from typing import List, Optional, Tuple
import sys


@dataclass
class Profile:
    name: str
    columns: List[str]
    n_columns: int = 2
    display_mode: str = "time"   # "time" or "speed"
    sort_by_best: bool = False
    use_abbrev: bool = False
    window_x: int = 100
    window_y: int = 100
    radar_x: int = 200
    radar_y: int = 200
    radar_visible: bool = False
    radar_width: int = 300
    radar_height: int = 300
    radar_range_forward: int = 2
    radar_range_rear: int = 1
    radar_range_side: int = 5
    radar_symbol: str = "rectangle"
    radar_show_speeds: bool = False
    radar_player_color: str = "0,255,0,255"
    radar_ai_ahead_color: str = "0,128,255,255"
    radar_ai_behind_color: str = "255,64,64,255"
    radar_ai_alongside_color: str = "255,255,0,255"
    custom_fields: List[Tuple[str, int]] = None   # ✅ NEW

    def __post_init__(self):
        if self.custom_fields is None:
            self.custom_fields = []


LAST_SESSION_KEY = "__last_session__"


class ProfileManager:
    def __init__(self, ini_path: Optional[str] = None):
        base_dir = os.path.dirname(sys.argv[0])
        self._cfgfile = ini_path or os.path.join(base_dir, "profiles.ini")
        self._parser = configparser.ConfigParser()
        self._parser.read(self._cfgfile)

    # -------------------------
    # Query
    # -------------------------
    def list_profiles(self) -> List[str]:
        return [s for s in self._parser.sections() if s != LAST_SESSION_KEY]

    def has_profile(self, name: str) -> bool:
        return name in self._parser

    # -------------------------
    # Load/save/delete
    # -------------------------
    def load(self, name: str) -> Optional[Profile]:
        if name not in self._parser:
            return None
        sec = self._parser[name]

        # Parse custom fields: stored as "Label:Index;Label2:Index2"
        raw_custom = sec.get("custom_fields", "")
        custom_fields: List[Tuple[str, int]] = []
        for entry in raw_custom.split(";"):
            if not entry.strip():
                continue
            try:
                label, idx = entry.split(":")
                custom_fields.append((label.strip(), int(idx)))
            except ValueError:
                continue

        return Profile(
            name=name,
            columns=[c.strip() for c in sec.get("columns", "").split(",") if c.strip()],
            n_columns=sec.getint("n_columns", fallback=2),
            display_mode=sec.get("display_mode", fallback="time"),
            sort_by_best=sec.getboolean("sort_by_best", fallback=False),
            use_abbrev=sec.getboolean("use_abbrev", fallback=False),
            window_x=sec.getint("window_x", fallback=100),
            window_y=sec.getint("window_y", fallback=100),
            radar_x=sec.getint("radar_x", fallback=200),
            radar_y=sec.getint("radar_y", fallback=200),
            radar_visible=sec.getboolean("radar_visible", fallback=False),

            # ✅ NEW radar config fields
            radar_width=sec.getint("radar_width", fallback=300),
            radar_height=sec.getint("radar_height", fallback=300),
            radar_range_forward=int(float(sec.get("radar_range_forward", fallback="2"))),
            radar_range_rear=int(float(sec.get("radar_range_rear", fallback="1"))),
            radar_range_side=int(float(sec.get("radar_range_side", fallback="5"))),


            radar_symbol=sec.get("radar_symbol", fallback="rectangle"),
            radar_show_speeds=sec.getboolean("radar_show_speeds", fallback=False),
            radar_player_color=sec.get("radar_player_color", fallback="0,255,0,255"),
            radar_ai_ahead_color=sec.get("radar_ai_ahead_color", fallback="0,128,255,255"),
            radar_ai_behind_color=sec.get("radar_ai_behind_color", fallback="255,64,64,255"),
            radar_ai_alongside_color=sec.get("radar_ai_alongside_color", fallback="255,255,0,255"),
            custom_fields=custom_fields,
        )


    def save(self, profile: Profile):
        if profile.name not in self._parser:
            self._parser.add_section(profile.name)

        self._parser[profile.name]["columns"] = ",".join(profile.columns)
        self._parser[profile.name]["n_columns"] = str(profile.n_columns)
        self._parser[profile.name]["display_mode"] = profile.display_mode
        self._parser[profile.name]["sort_by_best"] = "true" if profile.sort_by_best else "false"
        self._parser[profile.name]["use_abbrev"] = "true" if profile.use_abbrev else "false"
        self._parser[profile.name]["window_x"] = str(profile.window_x)
        self._parser[profile.name]["window_y"] = str(profile.window_y)
        self._parser[profile.name]["radar_x"] = str(profile.radar_x)
        self._parser[profile.name]["radar_y"] = str(profile.radar_y)
        self._parser[profile.name]["radar_visible"] = "true" if profile.radar_visible else "false"
        self._parser[profile.name]["radar_width"] = str(profile.radar_width)
        self._parser[profile.name]["radar_height"] = str(profile.radar_height)
        self._parser[profile.name]["radar_range_forward"] = str(profile.radar_range_forward)
        self._parser[profile.name]["radar_range_rear"] = str(profile.radar_range_rear)
        self._parser[profile.name]["radar_range_side"] = str(profile.radar_range_side)
        self._parser[profile.name]["radar_symbol"] = profile.radar_symbol
        self._parser[profile.name]["radar_show_speeds"] = "true" if profile.radar_show_speeds else "false"
        self._parser[profile.name]["radar_player_color"] = profile.radar_player_color
        self._parser[profile.name]["radar_ai_ahead_color"] = profile.radar_ai_ahead_color
        self._parser[profile.name]["radar_ai_behind_color"] = profile.radar_ai_behind_color
        self._parser[profile.name]["radar_ai_alongside_color"] = profile.radar_ai_alongside_color
        # ✅ Save custom fields
        if profile.custom_fields:
            self._parser[profile.name]["custom_fields"] = ";".join(
                f"{label}:{idx}" for label, idx in profile.custom_fields
            )
        else:
            self._parser[profile.name]["custom_fields"] = ""

        with open(self._cfgfile, "w") as f:
            self._parser.write(f)

    def delete(self, name: str) -> bool:
        if name not in self._parser:
            return False
        self._parser.remove_section(name)
        with open(self._cfgfile, "w") as f:
            self._parser.write(f)
        return True

    # -------------------------
    # Last session helpers
    # -------------------------
    def load_last_session(self) -> Optional[Profile]:
        return self.load(LAST_SESSION_KEY)

    def save_last_session(self, profile: Profile):
        profile = Profile(
            name=LAST_SESSION_KEY,
            columns=profile.columns,
            n_columns=profile.n_columns,
            display_mode=profile.display_mode,
            sort_by_best=profile.sort_by_best,
            use_abbrev=profile.use_abbrev,
            window_x=profile.window_x,
            window_y=profile.window_y,
            radar_x=profile.radar_x,
            radar_y=profile.radar_y,
            radar_visible=profile.radar_visible,
            radar_width=profile.radar_width,
            radar_height=profile.radar_height,
            radar_range_forward=profile.radar_range_forward,
            radar_range_rear=profile.radar_range_rear,
            radar_range_side=profile.radar_range_side,
            radar_symbol=profile.radar_symbol,
            radar_show_speeds=profile.radar_show_speeds,
            radar_player_color=profile.radar_player_color,
            radar_ai_ahead_color=profile.radar_ai_ahead_color,
            radar_ai_behind_color=profile.radar_ai_behind_color,
            radar_ai_alongside_color=profile.radar_ai_alongside_color,
            custom_fields=profile.custom_fields,
        )
        if self._parser.has_section(LAST_SESSION_KEY):
            self._parser.remove_section(LAST_SESSION_KEY)
        self.save(profile)

