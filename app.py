#!/usr/bin/env python3
"""
Personal Tracker CLI - Refactored modular version with aesthetic themes
Features:
 - All trackers (learning, project, reading, fitness, diet, etc.)
 - Add/List/Update/Delete/Search/Analyze/Export/Backup/Restore/Archive
 - Focus mode (Pomodoro), Undo, Settings
 - Three themes: Oceanic (default), Pastel, CyberDark
 - Slightly faster & smoother animations
 - Cleaner modular code for maintainability
"""

from __future__ import annotations
import json
import os
import sys
import time
import shutil
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple

# ---------------------------
# Constants & File Settings
# ---------------------------
VERSION = "1.1.0"
DATA_FILE = "data.json"
BACKUP_DIR = "backup"
ARCHIVE_FILE = "archive.json"
LOG_FILE = "log.txt"
MAX_BACKUPS = 10

# ---------------------------
# Trackers (unchanged)
# ---------------------------
TRACKERS = {
    'learning': {'name': 'Learning Tracker', 'fields': ['subject', 'topic', 'hours', 'status'], 'icon': '🎓'},
    'project': {'name': 'Project Tracker', 'fields': ['name', 'type', 'progress', 'deadline', 'status'], 'icon': '🧩'},
    'reading': {'name': 'Reading Tracker', 'fields': ['title', 'author', 'pages', 'status', 'rating'], 'icon': '📚'},
    'fitness': {'name': 'Fitness Tracker', 'fields': ['activity', 'duration', 'calories', 'date'], 'icon': '🏃'},
    'diet': {'name': 'Diet/Meal Tracker', 'fields': ['meal', 'type', 'calories', 'mood'], 'icon': '🍎'},
    'sleep': {'name': 'Sleep Tracker', 'fields': ['date', 'hours', 'quality', 'notes'], 'icon': '💤'},
    'mood': {'name': 'Mood Tracker', 'fields': ['date', 'mood', 'notes'], 'icon': '🧘'},
    'goal': {'name': 'Goal Tracker', 'fields': ['goal', 'deadline', 'progress', 'category'], 'icon': '🧭'},
    'time': {'name': 'Time Tracker', 'fields': ['task', 'duration', 'category', 'focus'], 'icon': '⏱'},
    'event': {'name': 'Event Tracker', 'fields': ['event', 'date', 'time', 'reminder', 'notes'], 'icon': '📅'},
    'expense': {'name': 'Expense Tracker', 'fields': ['description', 'amount', 'category', 'date'], 'icon': '💸'},
    'income': {'name': 'Income Tracker', 'fields': ['source', 'amount', 'date', 'notes'], 'icon': '💰'},
    'savings': {'name': 'Savings/Budget Tracker', 'fields': ['month', 'budget', 'spent', 'saved', 'goal_status'], 'icon': '🪙'},
    'shopping': {'name': 'Shopping List', 'fields': ['item', 'category', 'priority', 'purchased'], 'icon': '🛒'},
    'journal': {'name': 'Daily Journal', 'fields': ['date', 'title', 'reflection'], 'icon': '🗓'},
    'gratitude': {'name': 'Gratitude Tracker', 'fields': ['date', 'entry', 'mood'], 'icon': '🧠'},
    'bug': {'name': 'Bug Tracker', 'fields': ['bug', 'project', 'status', 'severity', 'fix_date'], 'icon': '💻'},
    'snippet': {'name': 'Code Snippet Tracker', 'fields': ['title', 'language', 'tags', 'snippet'], 'icon': '⚙️'},
    'interview': {'name': 'Interview Prep Tracker', 'fields': ['company', 'topic', 'attempts', 'result', 'notes'], 'icon': '🚀'},
    'habit': {'name': 'Habit Tracker', 'fields': ['habit', 'date', 'completed', 'notes'], 'icon': '✨'},
    'task': {'name': 'Task Tracker', 'fields': ['task', 'priority', 'status', 'deadline', 'notes'], 'icon': '✅'}
}

# ---------------------------
# Icons & Quotes (unchanged)
# ---------------------------
ICONS = {
    'learning': '🎓', 'project': '🧩', 'reading': '📚',
    'fitness': '🏃', 'diet': '🍎', 'sleep': '💤', 'mood': '🧘',
    'goal': '🧭', 'time': '⏱', 'event': '📅',
    'expense': '💸', 'income': '💰', 'savings': '🪙', 'shopping': '🛒',
    'journal': '🗓', 'gratitude': '🧠',
    'bug': '💻', 'snippet': '⚙️', 'interview': '🚀',
    'habit': '✨', 'task': '✅',
    'star': '⭐', 'fire': '🔥', 'rocket': '🚀', 'sparkles': '✨',
    'trophy': '🏆', 'medal': '🏅', 'target': '🎯', 'lightning': '⚡',
    'check': '✓', 'cross': '✗', 'arrow': '→', 'bullet': '•'
}

QUOTES = [
    "The secret of getting ahead is getting started. - Mark Twain",
    "Small progress is still progress. Keep going! 💪",
    "Success is the sum of small efforts repeated day in and day out. ⭐",
    "Your only limit is you. Break through it! 🚀",
    "Dream big, start small, act now. 🎯",
    "Discipline is choosing between what you want now and what you want most.",
    "Every expert was once a beginner. Keep learning! 📚",
    "The best time to start was yesterday. The next best time is now. ⏰",
    "You are capable of amazing things! 🌟",
    "Progress, not perfection. 💫"
]

# ---------------------------
# Theme Manager
# ---------------------------
class Theme:
    def __init__(self, name: str, palette: Dict[str, str], gradient: List[str], bg: Optional[str] = None):
        self.name = name
        self.palette = palette
        self.gradient = gradient
        self.bg = bg or ''

    def c(self, key: str) -> str:
        return self.palette.get(key, self.palette.get('END', '\033[0m'))

# Three aesthetic themes
THEMES: Dict[str, Theme] = {
    'oceanic': Theme(
        "Oceanic",
        palette={
            'HEADER': '\033[38;5;109m',  # muted teal-blue
            'BLUE': '\033[38;5;110m',
            'CYAN': '\033[38;5;117m',
            'GREEN': '\033[38;5;72m',    # sea green
            'YELLOW': '\033[38;5;187m',  # sand beige
            'RED': '\033[38;5;174m',     # coral tint
            'MAGENTA': '\033[38;5;182m',
            'WHITE': '\033[38;5;254m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        },
        gradient=['\033[38;5;109m', '\033[38;5;110m', '\033[38;5;117m', '\033[38;5;187m']
    ),

    'pastel': Theme(
        "Pastel",
        palette={
            'HEADER': '\033[38;5;224m',  # soft peach
            'BLUE': '\033[38;5;189m',    # light lavender
            'CYAN': '\033[38;5;152m',    # mint
            'GREEN': '\033[38;5;151m',   # pale sage
            'YELLOW': '\033[38;5;229m',  # buttercream
            'RED': '\033[38;5;217m',     # rose
            'MAGENTA': '\033[38;5;218m', # blush pink
            'WHITE': '\033[38;5;255m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        },
        gradient=['\033[38;5;224m', '\033[38;5;189m', '\033[38;5;218m']
    ),

    'cyberdark': Theme(
        "CyberDark",
        palette={
            'HEADER': '\033[38;5;81m',   # soft cyan glow
            'BLUE': '\033[38;5;33m',     # dim navy-blue
            'CYAN': '\033[38;5;87m',     # electric teal
            'GREEN': '\033[38;5;40m',    # neon green (subtle)
            'YELLOW': '\033[38;5;228m',  # pale amber
            'RED': '\033[38;5;203m',     # warm red highlight
            'MAGENTA': '\033[38;5;171m', # soft magenta
            'WHITE': '\033[38;5;251m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        },
        gradient=['\033[38;5;33m', '\033[38;5;87m', '\033[38;5;171m']
    )
}

# Default theme key
DEFAULT_THEME_KEY = 'oceanic'

# ---------------------------
# Utility Functions
# ---------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def now_str(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(fmt)

def safe_input(prompt: str = "") -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print()
        return ""

# ---------------------------
# Visual & Animation Helpers
# Slightly faster timings for smoother UX (per user's choice)
# ---------------------------
ANIM_DELAY = {
    'typing': 0.02,     # was 0.05 -> faster
    'sparkle': 0.02,    # was 0.03 -> faster
    'loading_frame': 0.08, # was 0.1
    'rocket': 0.08
}

LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
ROCKET_FRAMES = ["🚀        "," 🚀       ","  🚀      ","   🚀     ","    🚀    ",
                 "     🚀   ","      🚀  ","       🚀 ","        🚀"]

def loading_animation(theme: Theme, message="Loading", duration=1.0):
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = LOADING_FRAMES[i % len(LOADING_FRAMES)]
        sys.stdout.write(f'\r{theme.c("CYAN")}{frame} {message}...{theme.c("END")}')
        sys.stdout.flush()
        time.sleep(ANIM_DELAY['loading_frame'])
        i += 1
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def rocket_launch(theme: Theme):
    for frame in ROCKET_FRAMES:
        sys.stdout.write(f'\r{theme.c("YELLOW")}{frame}{theme.c("END")}')
        sys.stdout.flush()
        time.sleep(ANIM_DELAY['rocket'])
    print()

def typing_effect(theme: Theme, text: str, delay: float = None):
    d = delay or ANIM_DELAY['typing']
    for char in text:
        sys.stdout.write(f"{theme.c('GREEN')}{char}{theme.c('END')}")
        sys.stdout.flush()
        time.sleep(d)
    print()

def sparkle_text(theme: Theme, text: str, delay: float = None):
    d = delay or ANIM_DELAY['sparkle']
    colors = theme.gradient if theme.gradient else [theme.c('CYAN')]
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        sys.stdout.write(f"{color}{char}{theme.c('END')}")
        sys.stdout.flush()
        time.sleep(d)
    print()

def subtle_border(theme: Theme, width=70):
    colors = theme.gradient
    border = ""
    for i in range(width):
        color = colors[i % len(colors)]
        border += f"{color}═{theme.c('END')}"
    return border

# ---------------------------
# Persistence & Backup
# ---------------------------
def ensure_dirs():
    os.makedirs(BACKUP_DIR, exist_ok=True)

def load_json_file(path: str) -> Optional[dict]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def write_json_file(path: str, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------------------
# Main Tracker Class (modular)
# ---------------------------
class PersonalTracker:
    def __init__(self):
        ensure_dirs()
        self.data = self._load_data_or_default()
        self.settings = self.data.get('settings', {'theme': DEFAULT_THEME_KEY, 'user': 'User'})
        self.theme_key = self.settings.get('theme', DEFAULT_THEME_KEY)
        self.theme = THEMES.get(self.theme_key, THEMES[DEFAULT_THEME_KEY])
        self.undo_stack: List[Tuple[str, str, int, dict]] = []

    # -----------------------
    # Data Loading & Saving
    # -----------------------
    def _create_default_data(self) -> dict:
        d = {'settings': {'theme': DEFAULT_THEME_KEY, 'user': 'User'}}
        for t in TRACKERS.keys():
            d[t] = []
        return d

    def _load_data_or_default(self) -> dict:
        if not os.path.exists(DATA_FILE):
            return self._create_default_data()
        data = load_json_file(DATA_FILE)
        if data is None:
            print(f"{THEMES['oceanic'].c('YELLOW')}⚠️  Data file corrupted or unreadable. Attempting to recover...{THEMES['oceanic'].c('END')}")
            # attempt to recover latest backup
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')])
            if backups:
                latest = os.path.join(BACKUP_DIR, backups[-1])
                recovered = load_json_file(latest)
                if recovered:
                    self._save_data_to_file(recovered, create_backup=False)
                    print(f"{THEMES['oceanic'].c('GREEN')}Recovered data from backup: {backups[-1]}{THEMES['oceanic'].c('END')}")
                    return recovered
            return self._create_default_data()
        return data

    def _save_data_to_file(self, data: dict, create_backup: bool = True) -> bool:
        try:
            if create_backup and os.path.exists(DATA_FILE):
                self._create_backup()
            write_json_file(DATA_FILE, data)
            return True
        except Exception as e:
            self._error(f"Error saving data: {e}")
            return False

    def save_data(self, create_backup: bool = True) -> bool:
        self.data['settings'] = self.settings
        ok = self._save_data_to_file(self.data, create_backup=create_backup)
        return ok

    def _create_backup(self):
        try:
            if os.path.exists(DATA_FILE):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.json")
                shutil.copy2(DATA_FILE, backup_file)
                self._cleanup_old_backups()
        except Exception:
            pass

    def _cleanup_old_backups(self):
        try:
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')])
            while len(backups) > MAX_BACKUPS:
                old = backups.pop(0)
                os.remove(os.path.join(BACKUP_DIR, old))
        except Exception:
            pass

    # -----------------------
    # Logging & messaging
    # -----------------------
    def _log(self, action: str):
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"[{now_str()}] {action}\n")
        except Exception:
            pass

    def _success(self, message: str):
        print()
        print(f"{self.theme.c('GREEN')}{self.theme.c('BOLD')}{'═' * 70}{self.theme.c('END')}")
        print(f"{self.theme.c('GREEN')}{'  ' * 15}✓ SUCCESS ✓{self.theme.c('END')}")
        print(f"{self.theme.c('GREEN')}{self.theme.c('BOLD')}{'═' * 70}{self.theme.c('END')}")
        typing_effect(self.theme, f"  {message}", ANIM_DELAY['typing'])
        print(f"{self.theme.c('GREEN')}{self.theme.c('BOLD')}{'═' * 70}{self.theme.c('END')}\n")
        time.sleep(0.2)

    def _error(self, message: str):
        print()
        print(f"{self.theme.c('RED')}{self.theme.c('BOLD')}{'═' * 70}{self.theme.c('END')}")
        print(f"{self.theme.c('RED')}{'  ' * 15}✗ ERROR ✗{self.theme.c('END')}")
        print(f"{self.theme.c('RED')}{self.theme.c('BOLD')}{'═' * 70}{self.theme.c('END')}")
        print(f"{self.theme.c('RED')}  {message}{self.theme.c('END')}")
        print(f"{self.theme.c('RED')}{self.theme.c('BOLD')}{'═' * 70}{self.theme.c('END')}\n")
        time.sleep(0.2)

    # -----------------------
    # UI: Header & Menus
    # -----------------------
    def display_header(self):
        clear_screen()
        print(subtle_border(self.theme, 70))
        title = "🎯 PERSONAL TRACKER CLI 🎯"
        print()
        print(f"{self.theme.c('BOLD')}", end='')
        for i, ch in enumerate(title):
            color = self.theme.gradient[i % len(self.theme.gradient)]
            sys.stdout.write(f"{color}{ch}{self.theme.c('END')}")
            sys.stdout.flush()
            time.sleep(0.01)
        print(self.theme.c('END'))
        print()
        username = self.settings.get('user', 'User')
        print(f"{self.theme.c('MAGENTA') if 'MAGENTA' in self.theme.palette else self.theme.c('CYAN')}{ICONS['star']} Welcome back, {self.theme.c('BOLD')}{username}! {ICONS['star']}{self.theme.c('END')}")
        print()
        quote = QUOTES[hash(datetime.now().strftime("%Y-%m-%d")) % len(QUOTES)]
        print(f"{self.theme.c('YELLOW')}{ICONS['sparkles']} {quote}{self.theme.c('END')}\n")
        total_entries = sum(len(self.data.get(t, [])) for t in TRACKERS.keys())
        print(f"{self.theme.c('GREEN')}{ICONS['fire']} Total Entries: {total_entries}  ", end='')
        print(f"{ICONS['trophy']} Trackers Active: {sum(1 for t in TRACKERS if len(self.data.get(t, [])) > 0)}{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        print()

    def display_menu(self):
        menu_items = [
            ("1", "➕", "Add Entry", "GREEN"),
            ("2", "📋", "List Entries", "CYAN"),
            ("3", "✏️", "Update Entry", "YELLOW"),
            ("4", "🗑️", "Delete Entry", "RED"),
            ("5", "🔍", "Search / Filter", "MAGENTA"),
            ("6", "📊", "Analyze / Insights", "BLUE"),
            ("7", "📤", "Export / Backup", "CYAN"),
            ("8", "⏱", "Focus Mode", "YELLOW"),
            ("9", "🎨", "Settings", "MAGENTA"),
            ("0", "🚪", "Exit", "RED"),
        ]
        for num, icon, text, color in menu_items:
            color_code = self.theme.c(color) if color in self.theme.palette else self.theme.c('WHITE')
            print(f"{self.theme.c('BOLD')}{num}.{self.theme.c('END')}  {icon}  {color_code}{text}{self.theme.c('END')}")
        print(f"\n{self.theme.c('CYAN')}{ICONS['lightning']} Quick commands: {self.theme.c('YELLOW')}'add habit', 'list expenses', 'analyze mood'{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))

    # -----------------------
    # Input Validation
    # -----------------------
    def validate_input(self, prompt: str, field_type: str = 'text', required: bool = True):
        while True:
            raw = safe_input(f"{self.theme.c('CYAN')}{prompt}{self.theme.c('END')}").strip()
            if not raw and not required:
                return raw
            if not raw and required:
                print(f"{self.theme.c('YELLOW')}⚠️  This field is required!{self.theme.c('END')}")
                continue
            if field_type == 'number':
                try:
                    return float(raw)
                except ValueError:
                    print(f"{self.theme.c('YELLOW')}⚠️  Please enter a valid number!{self.theme.c('END')}")
            elif field_type == 'int':
                try:
                    return int(raw)
                except ValueError:
                    print(f"{self.theme.c('YELLOW')}⚠️  Please enter a valid integer!{self.theme.c('END')}")
            elif field_type == 'date':
                try:
                    datetime.strptime(raw, "%Y-%m-%d")
                    return raw
                except ValueError:
                    print(f"{self.theme.c('YELLOW')}⚠️  Please enter date in YYYY-MM-DD format!{self.theme.c('END')}")
            elif field_type == 'rating':
                try:
                    r = int(raw)
                    if 1 <= r <= 5:
                        return r
                    else:
                        print(f"{self.theme.c('YELLOW')}⚠️  Rating must be between 1-5!{self.theme.c('END')}")
                except ValueError:
                    print(f"{self.theme.c('YELLOW')}⚠️  Please enter a valid number!{self.theme.c('END')}")
            else:
                return raw

    # -----------------------
    # CRUD: Add / List / Update / Delete
    # -----------------------
    def _generate_id(self, tracker_type: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        count = len(self.data.get(tracker_type, []))
        return f"{tracker_type[:3].upper()}{timestamp}{count:03d}"

    def _create_progress_bar(self, progress: float, width=20) -> str:
        filled = int((progress / 100.0) * width) if progress is not None else 0
        empty = max(0, width - filled)
        if progress >= 75:
            color = self.theme.c('GREEN')
        elif progress >= 50:
            color = self.theme.c('YELLOW')
        elif progress >= 25:
            color = self.theme.c('MAGENTA')
        else:
            color = self.theme.c('RED')
        bar = f"{color}█{self.theme.c('END')}" * filled + f"{self.theme.c('WHITE')}░{self.theme.c('END')}" * empty
        return f"[{bar}]"

    def _create_bar_chart(self, value: float, max_value: float, width=30) -> str:
        if not max_value:
            return ""
        filled = int((value / max_value) * width)
        colors = [self.theme.c('GREEN'), self.theme.c('CYAN'), self.theme.c('YELLOW'), self.theme.c('MAGENTA')]
        bar = ""
        for i in range(filled):
            color = colors[i % len(colors)]
            bar += f"{color}▓{self.theme.c('END')}"
        return bar

    def add_entry(self, tracker_type: Optional[str] = None):
        if not tracker_type:
            print(self.theme.c('CYAN') + f"\n{ICONS['sparkles']} Available Trackers:" + self.theme.c('END'))
            print(subtle_border(self.theme, 70))
            for i, (key, value) in enumerate(TRACKERS.items(), 1):
                icon = TRACKERS[key]['icon']
                count = len(self.data.get(key, []))
                color = self.theme.gradient[i % len(self.theme.gradient)]
                print(f"{color}{i:2d}. {icon} {value['name']} ({count} entries){self.theme.c('END')}")
            print(subtle_border(self.theme, 70))
            choice = safe_input(f"\n{self.theme.c('CYAN')}Select tracker (number or name): {self.theme.c('END')}").strip().lower()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(TRACKERS):
                    tracker_type = list(TRACKERS.keys())[idx]
            except ValueError:
                if choice in TRACKERS:
                    tracker_type = choice
                else:
                    self._error("Invalid tracker!")
                    safe_input("\nPress Enter to continue...")
                    return

        if tracker_type not in TRACKERS:
            self._error("Invalid tracker!")
            safe_input("\nPress Enter to continue...")
            return

        tracker = TRACKERS[tracker_type]
        loading_animation(self.theme, f"Preparing {tracker['name']}", duration=0.6)
        print(f"{self.theme.c('GREEN')}{ICONS['sparkles']} Adding to {tracker['name']}{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        entry = {'id': self._generate_id(tracker_type), 'created_at': datetime.now().isoformat()}
        for field in tracker['fields']:
            prompt = f"{ICONS['arrow']} Enter {field}: "
            if field in ['hours', 'duration', 'calories', 'amount', 'spent', 'saved', 'budget']:
                entry[field] = self.validate_input(prompt, 'number')
            elif field in ['progress', 'attempts']:
                entry[field] = self.validate_input(prompt, 'int')
            elif field in ['date', 'deadline', 'fix_date']:
                default_date = datetime.now().strftime("%Y-%m-%d")
                entry[field] = self.validate_input(f"{prompt}[{default_date}]: ", 'date', required=False) or default_date
            elif field in ['quality', 'focus', 'rating']:
                entry[field] = self.validate_input(prompt, 'rating')
            elif field in ['completed', 'purchased', 'reminder']:
                val = safe_input(f"{self.theme.c('CYAN')}{prompt}(yes/no): {self.theme.c('END')}").strip().lower()
                entry[field] = val in ['yes', 'y', 'true', '1']
            else:
                entry[field] = self.validate_input(prompt)

        if tracker_type not in self.data:
            self.data[tracker_type] = []
        self.data[tracker_type].append(entry)
        if self.save_data():
            self._success(f"Entry added successfully! ID: {entry['id']}")
            self._log(f"Added entry to {tracker_type}: {entry['id']}")
            rocket_launch(self.theme)
        safe_input("\nPress Enter to continue...")

    def list_entries(self, tracker_type: Optional[str] = None, entries: Optional[List[dict]] = None):
        if not tracker_type:
            print(self.theme.c('CYAN') + f"\n{ICONS['sparkles']} Available Trackers:" + self.theme.c('END'))
            print(subtle_border(self.theme, 70))
            for i, (key, value) in enumerate(TRACKERS.items(), 1):
                icon = TRACKERS[key]['icon']
                count = len(self.data.get(key, []))
                color = self.theme.gradient[i % len(self.theme.gradient)]
                print(f"{color}{i:2d}. {icon} {value['name']} ({count} entries){self.theme.c('END')}")
            print(subtle_border(self.theme, 70))
            choice = safe_input(f"\n{self.theme.c('CYAN')}Select tracker (number or name): {self.theme.c('END')}").strip().lower()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(TRACKERS):
                    tracker_type = list(TRACKERS.keys())[idx]
            except ValueError:
                if choice in TRACKERS:
                    tracker_type = choice
                else:
                    self._error("Invalid tracker!")
                    safe_input("\nPress Enter to continue...")
                    return

        if tracker_type not in TRACKERS:
            self._error("Invalid tracker!")
            safe_input("\nPress Enter to continue...")
            return

        if entries is None:
            entries = self.data.get(tracker_type, [])

        if not entries:
            print(self.theme.c('YELLOW') + f"\n📭 No entries in {TRACKERS[tracker_type]['name']}" + self.theme.c('END'))
            safe_input("\nPress Enter to continue...")
            return

        loading_animation(self.theme, "Loading entries", duration=0.6)
        icon = TRACKERS[tracker_type]['icon']
        print(f"\n{self.theme.c('BOLD')}{self.theme.c('CYAN')}{icon} {TRACKERS[tracker_type]['name']}{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))

        for idx, entry in enumerate(entries, 1):
            color = self.theme.gradient[idx % len(self.theme.gradient)]
            print(f"\n{color}{self.theme.c('BOLD')}Entry #{idx}{self.theme.c('END')} {self.theme.c('MAGENTA')}(ID: {entry.get('id', 'N/A')}){self.theme.c('END')}")
            for field in TRACKERS[tracker_type]['fields']:
                value = entry.get(field, 'N/A')
                if field == 'progress' and isinstance(value, (int, float)):
                    bar = self._create_progress_bar(value)
                    print(f"  {self.theme.c('YELLOW')}{field}:{self.theme.c('END')} {value}% {bar}")
                elif field in ['completed', 'purchased', 'reminder'] and isinstance(value, bool):
                    status = f"{self.theme.c('GREEN')}✓ Yes{self.theme.c('END')}" if value else f"{self.theme.c('RED')}✗ No{self.theme.c('END')}"
                    print(f"  {self.theme.c('YELLOW')}{field}:{self.theme.c('END')} {status}")
                else:
                    print(f"  {self.theme.c('YELLOW')}{field}:{self.theme.c('END')} {self.theme.c('WHITE')}{value}{self.theme.c('END')}")
            print(f"{color}{'─' * 70}{self.theme.c('END')}")

        print(f"\n{self.theme.c('GREEN')}{ICONS['check']} Total entries: {len(entries)}{self.theme.c('END')}")
        safe_input("\nPress Enter to continue...")

    def _select_tracker(self) -> Optional[str]:
        print(self.theme.c('CYAN') + f"\n{ICONS['sparkles']} Available Trackers:" + self.theme.c('END'))
        print(subtle_border(self.theme, 70))
        for i, (key, value) in enumerate(TRACKERS.items(), 1):
            icon = TRACKERS[key]['icon']
            count = len(self.data.get(key, []))
            color = self.theme.gradient[i % len(self.theme.gradient)]
            print(f"{color}{i:2d}. {icon} {value['name']} ({count} entries){self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        choice = safe_input(f"\n{self.theme.c('CYAN')}Select tracker (number or name): {self.theme.c('END')}").strip().lower()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(TRACKERS):
                return list(TRACKERS.keys())[idx]
        except ValueError:
            if choice in TRACKERS:
                return choice
        self._error("Invalid tracker!")
        safe_input("\nPress Enter to continue...")
        return None

    def update_entry(self, tracker_type: Optional[str] = None):
        if not tracker_type:
            tracker_type = self._select_tracker()
            if not tracker_type:
                return
        entries = self.data.get(tracker_type, [])
        if not entries:
            print(self.theme.c('YELLOW') + f"\n📭 No entries in {TRACKERS[tracker_type]['name']}" + self.theme.c('END'))
            safe_input("\nPress Enter to continue...")
            return
        self.list_entries(tracker_type, entries)
        try:
            entry_id = safe_input(f"\n{self.theme.c('CYAN')}Enter entry ID to update: {self.theme.c('END')}").strip()
            entry_idx = None
            for idx, entry in enumerate(entries):
                if entry.get('id') == entry_id:
                    entry_idx = idx
                    break
            if entry_idx is None:
                self._error("Entry not found!")
                safe_input("\nPress Enter to continue...")
                return
            self.undo_stack.append(('update', tracker_type, entry_idx, entries[entry_idx].copy()))
            print(self.theme.c('GREEN') + f"\n{ICONS['sparkles']} Updating entry (press Enter to keep current value)" + self.theme.c('END'))
            print(subtle_border(self.theme, 70))
            for field in TRACKERS[tracker_type]['fields']:
                current_value = entries[entry_idx].get(field, '')
                prompt = f"{ICONS['arrow']} {field} [{self.theme.c('MAGENTA')}{current_value}{self.theme.c('END')}]: "
                new_value = safe_input(f"{self.theme.c('CYAN')}{prompt}{self.theme.c('END')}").strip()
                if new_value:
                    if field in ['hours', 'duration', 'calories', 'amount', 'spent', 'saved', 'budget']:
                        try:
                            entries[entry_idx][field] = float(new_value)
                        except ValueError:
                            print(self.theme.c('YELLOW') + "⚠️  Invalid number, keeping current value" + self.theme.c('END'))
                    elif field in ['progress', 'attempts']:
                        try:
                            entries[entry_idx][field] = int(new_value)
                        except ValueError:
                            print(self.theme.c('YELLOW') + "⚠️  Invalid integer, keeping current value" + self.theme.c('END'))
                    elif field in ['completed', 'purchased', 'reminder']:
                        entries[entry_idx][field] = new_value.lower() in ['yes', 'y', 'true', '1']
                    else:
                        entries[entry_idx][field] = new_value
            entries[entry_idx]['updated_at'] = datetime.now().isoformat()
            if self.save_data():
                self._success("Entry updated successfully!")
                self._log(f"Updated entry in {tracker_type}: {entry_id}")
        except Exception as e:
            self._error(f"Error updating entry: {e}")
        safe_input("\nPress Enter to continue...")

    def delete_entry(self, tracker_type: Optional[str] = None):
        if not tracker_type:
            tracker_type = self._select_tracker()
            if not tracker_type:
                return
        entries = self.data.get(tracker_type, [])
        if not entries:
            print(self.theme.c('YELLOW') + f"\n📭 No entries in {TRACKERS[tracker_type]['name']}" + self.theme.c('END'))
            safe_input("\nPress Enter to continue...")
            return
        self.list_entries(tracker_type, entries)
        try:
            entry_id = safe_input(f"\n{self.theme.c('CYAN')}Enter entry ID to delete: {self.theme.c('END')}").strip()
            entry_idx = None
            for idx, entry in enumerate(entries):
                if entry.get('id') == entry_id:
                    entry_idx = idx
                    break
            if entry_idx is None:
                self._error("Entry not found!")
                safe_input("\nPress Enter to continue...")
                return
            confirm = safe_input(f"{self.theme.c('RED')}Are you sure you want to delete this entry? (yes/no): {self.theme.c('END')}").strip().lower()
            if confirm in ['yes', 'y']:
                self.undo_stack.append(('delete', tracker_type, entry_idx, entries[entry_idx].copy()))
                deleted = entries.pop(entry_idx)
                if self.save_data():
                    self._success("Entry deleted successfully!")
                    self._log(f"Deleted entry from {tracker_type}: {entry_id}")
            else:
                print(self.theme.c('YELLOW') + "❌ Deletion cancelled" + self.theme.c('END'))
        except Exception as e:
            self._error(f"Error deleting entry: {e}")
        safe_input("\nPress Enter to continue...")

    # -----------------------
    # Search / Analyze / Export
    # -----------------------
    def parse_quick_command(self, cmd: str) -> Tuple[Optional[str], Optional[str]]:
        cmd = (cmd or "").lower().strip()
        patterns = [
            (r'^add (\w+)$', 'add'),
            (r'^list (\w+)$', 'list'),
            (r'^analyze (\w+)$', 'analyze'),
            (r'^delete (\w+)$', 'delete'),
            (r'^search (\w+)$', 'search'),
        ]
        for pattern, action in patterns:
            match = re.match(pattern, cmd)
            if match:
                tracker = match.group(1)
                if tracker in TRACKERS:
                    return action, tracker
        return None, None

    def search_entries(self, tracker_type: Optional[str] = None):
        if not tracker_type:
            tracker_type = self._select_tracker()
            if not tracker_type:
                return
        entries = self.data.get(tracker_type, [])
        if not entries:
            print(self.theme.c('YELLOW') + f"\n📭 No entries in {TRACKERS[tracker_type]['name']}" + self.theme.c('END'))
            safe_input("\nPress Enter to continue...")
            return
        print(self.theme.c('CYAN') + f"\n{ICONS['sparkles']} Search Options:" + self.theme.c('END'))
        print(subtle_border(self.theme, 70))
        print(f"{self.theme.c('GREEN')}1. Search by keyword{self.theme.c('END')}")
        print(f"{self.theme.c('YELLOW')}2. Filter by date range{self.theme.c('END')}")
        print(f"{self.theme.c('MAGENTA')}3. Filter by field value{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        choice = safe_input(f"\n{self.theme.c('CYAN')}Select option: {self.theme.c('END')}").strip()
        filtered_entries: List[dict] = []
        if choice == '1':
            keyword = safe_input(f"{self.theme.c('CYAN')}Enter keyword: {self.theme.c('END')}").strip().lower()
            loading_animation(self.theme, "Searching", duration=0.6)
            for entry in entries:
                for value in entry.values():
                    if keyword in str(value).lower():
                        filtered_entries.append(entry)
                        break
        elif choice == '2':
            start_date = safe_input(f"{self.theme.c('CYAN')}Start date (YYYY-MM-DD) or 'today': {self.theme.c('END')}").strip().lower()
            end_date = safe_input(f"{self.theme.c('CYAN')}End date (YYYY-MM-DD) or 'today': {self.theme.c('END')}").strip().lower()
            if start_date == 'today':
                start_date = datetime.now().strftime("%Y-%m-%d")
            if end_date == 'today':
                end_date = datetime.now().strftime("%Y-%m-%d")
            loading_animation(self.theme, "Filtering by date", duration=0.6)
            for entry in entries:
                entry_date = entry.get('date', entry.get('created_at', ''))[:10]
                if start_date <= entry_date <= end_date:
                    filtered_entries.append(entry)
        elif choice == '3':
            field = safe_input(f"{self.theme.c('CYAN')}Enter field name: {self.theme.c('END')}").strip()
            value = safe_input(f"{self.theme.c('CYAN')}Enter value to filter: {self.theme.c('END')}").strip().lower()
            loading_animation(self.theme, "Filtering", duration=0.6)
            for entry in entries:
                if str(entry.get(field, '')).lower() == value:
                    filtered_entries.append(entry)
        else:
            self._error("Invalid option!")
            safe_input("\nPress Enter to continue...")
            return
        if filtered_entries:
            self._success(f"Found {len(filtered_entries)} matching entries")
            self.list_entries(tracker_type, filtered_entries)
        else:
            print(self.theme.c('YELLOW') + "\n❌ No matching entries found" + self.theme.c('END'))
            safe_input("\nPress Enter to continue...")

    def analyze_data(self, tracker_type: Optional[str] = None):
        if not tracker_type:
            tracker_type = self._select_tracker()
            if not tracker_type:
                return
        entries = self.data.get(tracker_type, [])
        if not entries:
            print(self.theme.c('YELLOW') + f"\n📭 No entries to analyze in {TRACKERS[tracker_type]['name']}" + self.theme.c('END'))
            safe_input("\nPress Enter to continue...")
            return
        loading_animation(self.theme, "Analyzing data", duration=0.8)
        icon = TRACKERS[tracker_type]['icon']
        print(f"\n{self.theme.c('BOLD')}{self.theme.c('CYAN')}{icon} Analysis for {TRACKERS[tracker_type]['name']}{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        print(f"\n{self.theme.c('GREEN')}{ICONS['fire']} Total Entries: {self.theme.c('BOLD')}{len(entries)}{self.theme.c('END')}")
        # route to specialized analyzers
        if tracker_type == 'learning':
            self._analyze_learning(entries)
        elif tracker_type == 'expense':
            self._analyze_expenses(entries)
        elif tracker_type == 'mood':
            self._analyze_mood(entries)
        elif tracker_type == 'habit':
            self._analyze_habits(entries)
        elif tracker_type == 'fitness':
            self._analyze_fitness(entries)
        elif tracker_type == 'goal':
            self._analyze_goals(entries)
        elif tracker_type == 'task':
            self._analyze_tasks(entries)
        elif tracker_type == 'time':
            self._analyze_time(entries)
        else:
            print(self.theme.c('YELLOW') + f"\n{ICONS['sparkles']} Basic statistics shown above" + self.theme.c('END'))
        self._provide_suggestions(tracker_type, entries)
        safe_input("\nPress Enter to continue...")

    # --- Analysis implementations:
    def _analyze_learning(self, entries: List[dict]):
        total_hours = sum(float(e.get('hours', 0)) for e in entries)
        subjects = {}
        for entry in entries:
            subject = entry.get('subject', 'Unknown')
            subjects[subject] = subjects.get(subject, 0) + float(entry.get('hours', 0))
        print(f"\n{self.theme.c('YELLOW')}{ICONS['time']} Total Study Hours: {self.theme.c('BOLD')}{total_hours:.1f}{self.theme.c('END')}")
        print(f"{self.theme.c('CYAN')}{ICONS['learning']} Subjects Covered: {self.theme.c('BOLD')}{len(subjects)}{self.theme.c('END')}")
        if subjects:
            print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Hours by Subject:{self.theme.c('END')}")
            max_v = max(subjects.values())
            for subject, hours in sorted(subjects.items(), key=lambda x: x[1], reverse=True):
                bar = self._create_bar_chart(hours, max_v)
                print(f"  {self.theme.c('CYAN')}{subject}:{self.theme.c('END')} {self.theme.c('YELLOW')}{hours:.1f}h{self.theme.c('END')} {self.theme.c('GREEN')}{bar}{self.theme.c('END')}")

    def _analyze_expenses(self, entries: List[dict]):
        total = sum(float(e.get('amount', 0)) for e in entries)
        categories = defaultdict(float)
        for entry in entries:
            category = entry.get('category', 'Other')
            categories[category] += float(entry.get('amount', 0))
        print(f"\n{self.theme.c('RED')}{ICONS['expense']} Total Expenses: {self.theme.c('BOLD')}${total:.2f}{self.theme.c('END')}")
        print(f"{self.theme.c('CYAN')}{ICONS['target']} Categories: {self.theme.c('BOLD')}{len(categories)}{self.theme.c('END')}")
        if total > 0:
            print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Expenses by Category:{self.theme.c('END')}")
            for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total) * 100
                bar = self._create_bar_chart(amount, total)
                print(f"  {self.theme.c('CYAN')}{category}:{self.theme.c('END')} {self.theme.c('YELLOW')}${amount:.2f}{self.theme.c('END')} ({percentage:.1f}%) {self.theme.c('GREEN')}{bar}{self.theme.c('END')}")
        if entries:
            avg = total / len(entries)
            print(f"\n{self.theme.c('BLUE')}{ICONS['arrow']} Average Expense: {self.theme.c('BOLD')}${avg:.2f}{self.theme.c('END')}")

    def _analyze_mood(self, entries: List[dict]):
        moods = defaultdict(int)
        for entry in entries:
            mood = entry.get('mood', 'Unknown')
            moods[mood] += 1
        print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Mood Distribution:{self.theme.c('END')}")
        for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(entries)) * 100
            bar = self._create_bar_chart(count, len(entries))
            mood_color = 'GREEN' if 'happy' in mood.lower() else 'YELLOW' if 'neutral' in mood.lower() else 'RED'
            print(f"  {self.theme.c(mood_color) if mood_color in self.theme.palette else self.theme.c('GREEN')}{mood}:{self.theme.c('END')} {count} times ({percentage:.1f}%) {bar}")
        recent_entries = sorted(entries, key=lambda x: x.get('date', ''))[-7:]
        if recent_entries:
            happy_count = sum(1 for e in recent_entries if 'happy' in e.get('mood', '').lower())
            if happy_count >= len(recent_entries) * 0.6:
                # pulse_text replacement with sparkle for simplicity
                sparkle_text(self.theme, f"\n{ICONS['fire']} You've been mostly happy this week! Keep it up!", 0.02)
            elif happy_count < len(recent_entries) * 0.3:
                print(f"\n{self.theme.c('CYAN')}{ICONS['sparkles']} Tough week? Remember to take care of yourself.{self.theme.c('END')}")

    def _analyze_habits(self, entries: List[dict]):
        habits = defaultdict(lambda: {'completed': 0, 'total': 0})
        for entry in entries:
            habit = entry.get('habit', 'Unknown')
            habits[habit]['total'] += 1
            if entry.get('completed', False):
                habits[habit]['completed'] += 1
        print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Habit Statistics:{self.theme.c('END')}")
        for habit, stats in habits.items():
            rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            bar = self._create_progress_bar(rate)
            print(f"  {self.theme.c('CYAN')}{habit}:{self.theme.c('END')} {stats['completed']}/{stats['total']} ({rate:.1f}%) {bar}")
            streak = self._calculate_streak(entries, habit)
            if streak > 0:
                print(f"    {self.theme.c('YELLOW')}{ICONS['fire']} Current streak: {self.theme.c('BOLD')}{streak} days{self.theme.c('END')}")

    def _analyze_fitness(self, entries: List[dict]):
        total_duration = sum(float(e.get('duration', 0)) for e in entries)
        total_calories = sum(float(e.get('calories', 0)) for e in entries)
        print(f"\n{self.theme.c('GREEN')}{ICONS['fitness']} Total Workout Time: {self.theme.c('BOLD')}{total_duration:.0f} minutes{self.theme.c('END')}")
        print(f"{self.theme.c('RED')}{ICONS['fire']} Total Calories Burned: {self.theme.c('BOLD')}{total_calories:.0f}{self.theme.c('END')}")
        if entries:
            avg_duration = total_duration / len(entries)
            print(f"{self.theme.c('CYAN')}{ICONS['arrow']} Average Workout: {self.theme.c('BOLD')}{avg_duration:.1f} minutes{self.theme.c('END')}")

    def _analyze_goals(self, entries: List[dict]):
        total_progress = sum(float(e.get('progress', 0)) for e in entries)
        completed = sum(1 for e in entries if float(e.get('progress', 0)) >= 100)
        print(f"\n{self.theme.c('GREEN')}{ICONS['trophy']} Completed Goals: {self.theme.c('BOLD')}{completed}/{len(entries)}{self.theme.c('END')}")
        if entries:
            avg_progress = total_progress / len(entries)
            bar = self._create_progress_bar(avg_progress)
            print(f"{self.theme.c('CYAN')}{ICONS['target']} Average Progress: {self.theme.c('BOLD')}{avg_progress:.1f}%{self.theme.c('END')} {bar}")
        categories = defaultdict(int)
        for entry in entries:
            cat = entry.get('category', 'Other')
            categories[cat] += 1
        print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Goals by Category:{self.theme.c('END')}")
        for cat, count in categories.items():
            print(f"  {self.theme.c('CYAN')}{cat}:{self.theme.c('END')} {self.theme.c('YELLOW')}{count} goals{self.theme.c('END')}")

    def _analyze_tasks(self, entries: List[dict]):
        statuses = defaultdict(int)
        priorities = defaultdict(int)
        for entry in entries:
            status = entry.get('status', 'Unknown')
            priority = entry.get('priority', 'Medium')
            statuses[status] += 1
            priorities[priority] += 1
        print(f"\n{self.theme.c('GREEN')}{ICONS['check']} Task Status:{self.theme.c('END')}")
        for status, count in statuses.items():
            percentage = (count / len(entries)) * 100
            bar = self._create_bar_chart(count, len(entries))
            print(f"  {self.theme.c('CYAN')}{status}:{self.theme.c('END')} {count} ({percentage:.1f}%) {self.theme.c('GREEN')}{bar}{self.theme.c('END')}")
        print(f"\n{self.theme.c('YELLOW')}{ICONS['target']} Task Priority:{self.theme.c('END')}")
        for priority, count in priorities.items():
            print(f"  {self.theme.c('CYAN')}{priority}:{self.theme.c('END')} {self.theme.c('YELLOW')}{count} tasks{self.theme.c('END')}")

    def _analyze_time(self, entries: List[dict]):
        total_time = sum(float(e.get('duration', 0)) for e in entries)
        categories = defaultdict(float)
        focus_scores = []
        for entry in entries:
            cat = entry.get('category', 'Other')
            duration = float(entry.get('duration', 0))
            categories[cat] += duration
            focus = entry.get('focus')
            if focus:
                focus_scores.append(int(focus))
        print(f"\n{self.theme.c('CYAN')}{ICONS['time']} Total Time Tracked: {self.theme.c('BOLD')}{total_time:.1f} hours{self.theme.c('END')}")
        if focus_scores:
            avg_focus = sum(focus_scores) / len(focus_scores)
            bar = self._create_progress_bar(avg_focus * 20)
            print(f"{self.theme.c('YELLOW')}{ICONS['target']} Average Focus Level: {self.theme.c('BOLD')}{avg_focus:.1f}/5{self.theme.c('END')} {bar}")
        print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Time by Category:{self.theme.c('END')}")
        for cat, time_spent in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (time_spent / total_time * 100) if total_time > 0 else 0
            bar = self._create_bar_chart(time_spent, total_time)
            print(f"  {self.theme.c('CYAN')}{cat}:{self.theme.c('END')} {self.theme.c('YELLOW')}{time_spent:.1f}h{self.theme.c('END')} ({percentage:.1f}%) {self.theme.c('GREEN')}{bar}{self.theme.c('END')}")

    def _provide_suggestions(self, tracker_type: str, entries: List[dict]):
        print(f"\n{self.theme.c('YELLOW')}{self.theme.c('BOLD')}{ICONS['lightning']} Smart Suggestions:{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        recent_days = 7
        recent_date = (datetime.now() - timedelta(days=recent_days)).strftime("%Y-%m-%d")
        recent_entries = [e for e in entries if e.get('date', e.get('created_at', ''))[:10] >= recent_date]
        if not recent_entries and len(entries) > 0:
            print(f"  {self.theme.c('RED')}{ICONS['cross']} No activity in the last {recent_days} days. Time to get back on track!{self.theme.c('END')}")
        elif len(recent_entries) > len(entries) * 0.7:
            sparkle_text(self.theme, f"  {ICONS['fire']} Great consistency! You're on fire!", 0.02)
        if tracker_type == 'habit':
            incomplete = sum(1 for e in recent_entries if not e.get('completed', False))
            if incomplete > len(recent_entries) * 0.5:
                print(f"  {self.theme.c('YELLOW')}{ICONS['lightning']} Try focusing on one habit at a time to build momentum!{self.theme.c('END')}")
        elif tracker_type == 'expense':
            if len(recent_entries) >= 2:
                recent_total = sum(float(e.get('amount', 0)) for e in recent_entries[-7:])
                prev_entries = entries[:-7][-7:] if len(entries) > 7 else []
                prev_total = sum(float(e.get('amount', 0)) for e in prev_entries)
                if prev_total > 0 and recent_total > prev_total * 1.3:
                    increase = ((recent_total - prev_total) / prev_total) * 100
                    print(f"  {self.theme.c('RED')}{ICONS['expense']} Spending increased by {increase:.0f}% this week. Consider reviewing your budget!{self.theme.c('END')}")
        elif tracker_type == 'fitness':
            if len(recent_entries) < 3:
                print(f"  {self.theme.c('YELLOW')}{ICONS['fitness']} Try to exercise at least 3 times a week for better health!{self.theme.c('END')}")
        elif tracker_type == 'goal':
            low_progress = [e for e in entries if float(e.get('progress', 0)) < 25]
            if low_progress:
                print(f"  {self.theme.c('YELLOW')}{ICONS['target']} You have {len(low_progress)} goals with low progress. Break them into smaller tasks!{self.theme.c('END')}")
        elif tracker_type == 'task':
            pending = [e for e in entries if e.get('status', '').lower() in ['pending', 'todo', 'open']]
            if len(pending) > 10:
                print(f"  {self.theme.c('YELLOW')}{ICONS['task']} You have {len(pending)} pending tasks. Prioritize the top 3 for today!{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))

    def _calculate_streak(self, entries: List[dict], habit: str) -> int:
        habit_entries = sorted([e for e in entries if e.get('habit') == habit], key=lambda x: x.get('date', ''), reverse=True)
        if not habit_entries:
            return 0
        streak = 0
        current_date = datetime.now().date()
        for entry in habit_entries:
            entry_date_str = entry.get('date', '')
            if not entry_date_str:
                continue
            try:
                entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                if entry_date == current_date and entry.get('completed', False):
                    streak += 1
                    current_date -= timedelta(days=1)
                elif entry_date < current_date:
                    break
            except ValueError:
                continue
        return streak

    # -----------------------
    # Export / Backup / Restore / Archive
    # -----------------------
    def export_data(self):
        print(self.theme.c('CYAN') + f"\n{ICONS['sparkles']} Export Options:" + self.theme.c('END'))
        print(subtle_border(self.theme, 70))
        print(f"{self.theme.c('GREEN')}1. Export all data to JSON{self.theme.c('END')}")
        print(f"{self.theme.c('YELLOW')}2. Export summary report (TXT){self.theme.c('END')}")
        print(f"{self.theme.c('MAGENTA')}3. Export to CSV (select tracker){self.theme.c('END')}")
        print(f"{self.theme.c('CYAN')}4. Create monthly report{self.theme.c('END')}")
        print(subtle_border(self.theme, 70))
        choice = safe_input(f"\n{self.theme.c('CYAN')}Select option: {self.theme.c('END')}").strip()
        try:
            if choice == '1':
                loading_animation(self.theme, "Exporting to JSON", duration=0.6)
                filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                write_json_file(filename, self.data)
                self._success(f"Exported to {filename}")
            elif choice == '2':
                loading_animation(self.theme, "Generating summary report", duration=0.6)
                self._export_summary()
            elif choice == '3':
                self._export_csv()
            elif choice == '4':
                loading_animation(self.theme, "Creating monthly report", duration=0.6)
                self._export_monthly_report()
            else:
                self._error("Invalid option!")
        except Exception as e:
            self._error(f"Export failed: {e}")
        safe_input("\nPress Enter to continue...")

    def _export_summary(self):
        filename = "summary.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("PERSONAL TRACKER - SUMMARY REPORT\n")
            f.write(f"Generated: {now_str()}\n")
            f.write("=" * 70 + "\n\n")
            for tracker_type, tracker_info in TRACKERS.items():
                entries = self.data.get(tracker_type, [])
                f.write(f"\n{tracker_info['name']}: {len(entries)} entries\n")
                f.write("-" * 70 + "\n")
                if entries:
                    if tracker_type == 'expense':
                        total = sum(float(e.get('amount', 0)) for e in entries)
                        f.write(f"Total expenses: ${total:.2f}\n")
                    elif tracker_type == 'learning':
                        total_hours = sum(float(e.get('hours', 0)) for e in entries)
                        f.write(f"Total study hours: {total_hours:.1f}\n")
        self._success(f"Summary exported to {filename}")

    def _export_csv(self):
        tracker_type = self._select_tracker()
        if not tracker_type:
            return
        entries = self.data.get(tracker_type, [])
        if not entries:
            self._error("No data to export!")
            return
        loading_animation(self.theme, "Exporting to CSV", duration=0.6)
        filename = f"{tracker_type}_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            fields = TRACKERS[tracker_type]['fields']
            f.write(','.join(fields) + '\n')
            for entry in entries:
                values = [str(entry.get(field, '')).replace(',', ';') for field in fields]
                f.write(','.join(values) + '\n')
        self._success(f"Exported to {filename}")

    def _export_monthly_report(self):
        month = safe_input(f"{self.theme.c('CYAN')}Enter month (YYYY-MM) or press Enter for current month: {self.theme.c('END')}").strip()
        if not month:
            month = datetime.now().strftime("%Y-%m")
        filename = f"monthly_report_{month}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"MONTHLY REPORT - {month}\n")
            f.write("=" * 70 + "\n\n")
            for tracker_type, tracker_info in TRACKERS.items():
                entries = self.data.get(tracker_type, [])
                monthly_entries = [e for e in entries if month in e.get('date', e.get('created_at', ''))]
                if monthly_entries:
                    f.write(f"\n{tracker_info['name']}: {len(monthly_entries)} entries\n")
                    f.write("-" * 70 + "\n")
        self._success(f"Monthly report exported to {filename}")

    def _restore_backup(self):
        try:
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')])
            if not backups:
                self._error("No backups available!")
                safe_input("\nPress Enter to continue...")
                return
            print(self.theme.c('CYAN') + f"\n{ICONS['sparkles']} Available Backups:" + self.theme.c('END'))
            print(subtle_border(self.theme, 70))
            for i, backup in enumerate(backups[-10:], 1):
                print(f"{self.theme.c('CYAN')}{i}. {backup}{self.theme.c('END')}")
            print(subtle_border(self.theme, 70))
            choice = safe_input(f"\n{self.theme.c('CYAN')}Select backup to restore (number): {self.theme.c('END')}").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(backups[-10:]):
                    backup_file = os.path.join(BACKUP_DIR, backups[-10:][idx])
                    confirm = safe_input(f"{self.theme.c('RED')}This will overwrite current data. Continue? (yes/no): {self.theme.c('END')}").strip().lower()
                    if confirm in ['yes', 'y']:
                        loading_animation(self.theme, "Restoring from backup", duration=0.8)
                        with open(backup_file, 'r', encoding='utf-8') as f:
                            self.data = json.load(f)
                        self.save_data(create_backup=False)
                        self._success("Data restored from backup!")
                        self._log(f"Restored from backup: {backups[-10:][idx]}")
                    else:
                        print(self.theme.c('YELLOW') + "❌ Restore cancelled" + self.theme.c('END'))
                else:
                    self._error("Invalid selection!")
            except ValueError:
                self._error("Invalid input!")
        except Exception as e:
            self._error(f"Error restoring backup: {e}")
        safe_input("\nPress Enter to continue...")

    def _archive_old_entries(self):
        loading_animation(self.theme, "Scanning for old entries", duration=0.6)
        cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        archived_count = 0
        archive_data = {}
        for tracker_type in TRACKERS.keys():
            entries = self.data.get(tracker_type, [])
            old_entries = []
            new_entries = []
            for entry in entries:
                entry_date = entry.get('date', entry.get('created_at', ''))[:10]
                if entry_date < cutoff_date:
                    old_entries.append(entry)
                    archived_count += 1
                else:
                    new_entries.append(entry)
            if old_entries:
                archive_data[tracker_type] = old_entries
                self.data[tracker_type] = new_entries
        if archived_count > 0:
            try:
                existing_archive = {}
                if os.path.exists(ARCHIVE_FILE):
                    with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
                        existing_archive = json.load(f)
                for tracker_type, entries in archive_data.items():
                    if tracker_type not in existing_archive:
                        existing_archive[tracker_type] = []
                    existing_archive[tracker_type].extend(entries)
                with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(existing_archive, f, indent=2, ensure_ascii=False)
                self.save_data()
                self._success(f"Archived {archived_count} old entries!")
                self._log(f"Archived {archived_count} entries older than 30 days")
            except Exception as e:
                self._error(f"Error archiving: {e}")
        else:
            print(self.theme.c('YELLOW') + "ℹ️  No old entries to archive" + self.theme.c('END'))
        safe_input("\nPress Enter to continue...")

    # -----------------------
    # Undo
    # -----------------------
    def _undo_last_action(self):
        if not self.undo_stack:
            self._error("Nothing to undo!")
            safe_input("\nPress Enter to continue...")
            return
        action, tracker_type, idx, entry = self.undo_stack.pop()
        try:
            loading_animation(self.theme, "Undoing action", duration=0.6)
            if action == 'delete':
                self.data[tracker_type].insert(idx, entry)
                self._success("Delete action undone!")
            elif action == 'update':
                self.data[tracker_type][idx] = entry
                self._success("Update action undone!")
            self.save_data()
            self._log(f"Undone {action} action in {tracker_type}")
        except Exception as e:
            self._error(f"Error undoing action: {e}")
        safe_input("\nPress Enter to continue...")

    # -----------------------
    # Focus Mode (Pomodoro)
    # -----------------------
    def focus_mode(self):
        print(self.theme.c('CYAN') + f"\n{ICONS['time']} Focus Mode (Pomodoro Timer)" + self.theme.c('END'))
        print(subtle_border(self.theme, 70))
        try:
            duration = int(safe_input(f"{self.theme.c('CYAN')}Enter focus duration in minutes [25]: {self.theme.c('END')}").strip() or "25")
            task = safe_input(f"{self.theme.c('CYAN')}What are you working on? {self.theme.c('END')}").strip()
            loading_animation(self.theme, "Initializing Focus Mode", duration=0.6)
            print(f"\n{self.theme.c('GREEN')}{self.theme.c('BOLD')}{ICONS['rocket']} Starting {duration}-minute focus session...{self.theme.c('END')}")
            print(f"{self.theme.c('YELLOW')}Press Ctrl+C to stop early{self.theme.c('END')}\n")
            start_time = time.time()
            end_time = start_time + (duration * 60)
            try:
                while time.time() < end_time:
                    remaining = int(end_time - time.time())
                    mins, secs = divmod(remaining, 60)
                    frame = LOADING_FRAMES[int(time.time() * 2) % len(LOADING_FRAMES)]
                    progress = ((duration * 60 - remaining) / (duration * 60)) * 100
                    bar = self._create_progress_bar(progress)
                    sys.stdout.write(f"\r{self.theme.c('CYAN')}{frame} {self.theme.c('BOLD')}⏱  {mins:02d}:{secs:02d}{self.theme.c('END')} {bar}")
                    sys.stdout.flush()
                    time.sleep(0.5)
                print(f"\n\n{self.theme.c('GREEN')}{self.theme.c('BOLD')}")
                sparkle_text(self.theme, "🎉 Focus session complete! Great work! 🎉", 0.03)
                print(self.theme.c('END'))
                rocket_launch(self.theme)
                focus_rating = self.validate_input("Rate your focus (1-5): ", 'rating')
                entry = {
                    'id': self._generate_id('time'),
                    'task': task,
                    'duration': duration / 60,
                    'category': 'Focus Session',
                    'focus': focus_rating,
                    'created_at': datetime.now().isoformat()
                }
                if 'time' not in self.data:
                    self.data['time'] = []
                self.data['time'].append(entry)
                self.save_data()
                self._success("Session logged to Time Tracker!")
            except KeyboardInterrupt:
                elapsed = int(time.time() - start_time) / 60
                print(f"\n\n{self.theme.c('YELLOW')}{ICONS['cross']} Session stopped early. You focused for {elapsed:.1f} minutes.{self.theme.c('END')}")
        except ValueError:
            self._error("Invalid input!")
        except Exception as e:
            self._error(f"Error: {e}")
        safe_input("\nPress Enter to continue...")

    # -----------------------
    # Settings & Theme Manager
    # -----------------------
    def settings_menu(self):
        while True:
            self.display_header()
            print(self.theme.c('CYAN') + f"{ICONS['sparkles']} Settings" + self.theme.c('END'))
            print(subtle_border(self.theme, 70))
            print(f"\n{self.theme.c('GREEN')}1. Change username (Current: {self.theme.c('BOLD')}{self.settings['user']}{self.theme.c('END')}{self.theme.c('GREEN')}){self.theme.c('END')}")
            print(f"{self.theme.c('YELLOW')}2. Change theme (Current: {self.theme.c('BOLD')}{self.theme.name}{self.theme.c('END')}{self.theme.c('YELLOW')}){self.theme.c('END')}")
            print(f"{self.theme.c('CYAN')}3. View statistics{self.theme.c('END')}")
            print(f"{self.theme.c('MAGENTA')}4. Backup data{self.theme.c('END')}")
            print(f"{self.theme.c('BLUE')}5. Restore from backup{self.theme.c('END')}")
            print(f"{self.theme.c('YELLOW')}6. Archive old entries{self.theme.c('END')}")
            print(f"{self.theme.c('GREEN')}7. Undo last action{self.theme.c('END')}")
            print(f"{self.theme.c('RED')}0. Back to main menu{self.theme.c('END')}")
            print(subtle_border(self.theme, 70))
            choice = safe_input(f"\n{self.theme.c('CYAN')}Select option: {self.theme.c('END')}").strip()
            if choice == '1':
                new_name = safe_input(f"{self.theme.c('CYAN')}Enter new username: {self.theme.c('END')}").strip()
                if new_name:
                    loading_animation(self.theme, "Updating username", duration=0.5)
                    self.settings['user'] = new_name
                    self.save_data()
                    self._success("Username updated!")
                safe_input("\nPress Enter to continue...")
            elif choice == '2':
                self._choose_theme()
            elif choice == '3':
                self._show_global_stats()
            elif choice == '4':
                loading_animation(self.theme, "Creating backup", duration=0.6)
                self._create_backup()
                self._success("Backup created!")
                safe_input("\nPress Enter to continue...")
            elif choice == '5':
                self._restore_backup()
            elif choice == '6':
                self._archive_old_entries()
            elif choice == '7':
                self._undo_last_action()
            elif choice == '0':
                break
            else:
                self._error("Invalid option!")
                safe_input("\nPress Enter to continue...")

    def _choose_theme(self):
        print(f"\nAvailable themes:")
        for i, (k, t) in enumerate(THEMES.items(), 1):
            print(f"  {i}. {t.name} ({k})")
        choice = safe_input(f"\n{self.theme.c('CYAN')}Select theme (name or number): {self.theme.c('END')}").strip().lower()
        picked = None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(THEMES):
                picked = list(THEMES.keys())[idx]
        except ValueError:
            if choice in THEMES:
                picked = choice
        if not picked:
            self._error("Invalid theme!")
            safe_input("\nPress Enter to continue...")
            return
        loading_animation(self.theme, "Applying theme", duration=0.6)
        self.theme_key = picked
        self.theme = THEMES.get(self.theme_key, self.theme)
        self.settings['theme'] = self.theme_key
        self.save_data()
        self._success(f"Theme changed to {self.theme.name}")
        safe_input("\nPress Enter to continue...")

    def _show_global_stats(self):
        loading_animation(self.theme, "Calculating statistics", duration=0.6)
        print(self.theme.c('CYAN') + f"\n{ICONS['trophy']} Global Statistics" + self.theme.c('END'))
        print(subtle_border(self.theme, 70))
        total_entries = sum(len(self.data.get(t, [])) for t in TRACKERS.keys())
        print(f"\n{self.theme.c('GREEN')}{ICONS['fire']} Total entries across all trackers: {self.theme.c('BOLD')}{total_entries}{self.theme.c('END')}")
        print(f"\n{self.theme.c('MAGENTA')}{ICONS['sparkles']} Entries by Tracker:{self.theme.c('END')}")
        for tracker_type, tracker_info in TRACKERS.items():
            count = len(self.data.get(tracker_type, []))
            if count > 0:
                icon = TRACKERS[tracker_type]['icon']
                bar = self._create_bar_chart(count, total_entries, 20)
                print(f"  {icon} {self.theme.c('CYAN')}{tracker_info['name']}:{self.theme.c('END')} {self.theme.c('YELLOW')}{count}{self.theme.c('END')} {bar}")
        try:
            size = os.path.getsize(DATA_FILE)
            print(f"\n{self.theme.c('BLUE')}{ICONS['target']} Data file size: {self.theme.c('BOLD')}{size / 1024:.2f} KB{self.theme.c('END')}")
        except:
            pass
        try:
            backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')]
            print(f"{self.theme.c('CYAN')}{ICONS['arrow']} Backups available: {self.theme.c('BOLD')}{len(backups)}{self.theme.c('END')}")
        except:
            pass
        print(subtle_border(self.theme, 70))
        safe_input("\nPress Enter to continue...")

    # -----------------------
    # Run Loop
    # -----------------------
    def run(self):
        clear_screen()
        print("\n" * 3)
        sparkle_text(self.theme, "     🎯 PERSONAL TRACKER CLI 🎯", 0.06)
        print()
        typing_effect(self.theme, f"          Version {VERSION}", 0.03)
        print()
        rocket_launch(self.theme)
        loading_animation(self.theme, "Initializing", duration=1.6)
        while True:
            try:
                self.display_header()
                self.display_menu()
                choice = safe_input(f"\n{self.theme.c('CYAN')}{self.theme.c('BOLD')}Enter your choice: {self.theme.c('END')}").strip()
                action, tracker = self.parse_quick_command(choice)
                if action:
                    loading_animation(self.theme, f"Processing command", duration=0.6)
                    if action == 'add':
                        self.add_entry(tracker)
                    elif action == 'list':
                        self.list_entries(tracker)
                    elif action == 'analyze':
                        self.analyze_data(tracker)
                    elif action == 'delete':
                        self.delete_entry(tracker)
                    elif action == 'search':
                        self.search_entries(tracker)
                    continue
                if choice == '1':
                    self.add_entry()
                elif choice == '2':
                    self.list_entries()
                elif choice == '3':
                    self.update_entry()
                elif choice == '4':
                    self.delete_entry()
                elif choice == '5':
                    self.search_entries()
                elif choice == '6':
                    self.analyze_data()
                elif choice == '7':
                    self.export_data()
                elif choice == '8':
                    self.focus_mode()
                elif choice == '9':
                    self.settings_menu()
                elif choice == '0':
                    confirm = safe_input(f"\n{self.theme.c('RED')}🚪 Are you sure you want to exit? (yes/no): {self.theme.c('END')}").strip().lower()
                    if confirm in ['yes', 'y']:
                        loading_animation(self.theme, "Saving data", duration=0.6)
                        self.save_data()
                        print(f"\n{self.theme.c('CYAN')}{self.theme.c('BOLD')}")
                        sparkle_text(self.theme, "👋 Thanks for using Personal Tracker! Stay productive!", 0.04)
                        print(self.theme.c('END'))
                        rocket_launch(self.theme)
                        break
                else:
                    self._error("Invalid option! Please try again.")
                    safe_input("\nPress Enter to continue...")
            except Exception as e:
                # Catch-all to prevent crash; log and show friendly message
                self._error(f"Unexpected error: {e}")
                self._log(f"Unexpected error: {e}")
                safe_input("\nPress Enter to continue...")

# ---------------------------
# Entry point
# ---------------------------
def main():
    app = PersonalTracker()
    app.run()

if __name__ == "__main__":
    main()
