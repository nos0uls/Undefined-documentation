#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_inventories.py — генератор машинных инвентарей W0-inv для Undefinedtale888.

Источник: проект GameMaker (read-only):
  P = /media/n0souls/New Volume/GitHub/Undefinedtale-888/Undefinedtale888
Выход: текстовые файлы рядом со скриптом (_meta/):
  scripts.txt, objects.txt, rooms.txt, globals.txt, json_actions.txt, datafiles.txt

Форматы .yy — «JSON с висячими запятыми» (GameMaker), чистятся перед json.loads.
Только факты из файлов, без интерпретаций.
"""
import json
import os
import re
import sys
from collections import Counter, OrderedDict

P = "/media/n0souls/New Volume/GitHub/Undefinedtale-888/Undefinedtale888"
OUT = os.path.dirname(os.path.abspath(__file__))


def load_yy(path):
    """Парсит .yy (JSON с trailing commas)."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return json.loads(text)


def rel(path):
    return os.path.relpath(path, P)


# ---------------------------------------------------------------- scripts.txt
def gen_scripts():
    # grep-эквивалент: '^function ' расширен до '^\s*function ' (методы внутри
    # функций) + строки JSDoc /// @function/@description/@desc с номерами строк.
    re_line = re.compile(r"(^\s*function\s|///\s*@(function|description|desc)\b)")
    files = []
    for root, _dirs, names in os.walk(os.path.join(P, "scripts")):
        for n in names:
            if n.endswith(".gml"):
                files.append(os.path.join(root, n))
    files.sort(key=rel)

    out = []
    n_files = 0
    n_funcs = 0
    for f in files:
        hits = []
        with open(f, encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                if re_line.search(line):
                    hits.append((i, line.rstrip()))
        if hits:
            n_files += 1
            out.append("=== %s ===" % rel(f))
            for i, line in hits:
                out.append("%6d: %s" % (i, line))
                if re.match(r"^\s*function\s", line):
                    n_funcs += 1
            out.append("")
    header = [
        "# scripts.txt — инвентарь scripts/**/*.gml",
        "# Для каждого файла: строки 'function ...', '/// @function', '/// @description', '/// @desc'",
        "# с номерами строк (grep -n).",
        "# Файлов с объявлениями: %d; объявлений 'function': %d" % (n_files, n_funcs),
        "",
    ]
    _write("scripts.txt", "\n".join(header + out))


# ---------------------------------------------------------------- objects.txt
EVENT_NAMES = {
    0: "Create", 1: "Destroy", 11: "Trigger", 12: "CleanUp", 13: "Gesture",
}
STEP_NAMES = {0: "Step", 1: "Begin Step", 2: "End Step"}
OTHER_NAMES = {
    0: "Outside Room", 1: "Boundary", 2: "Game Start", 3: "Game End",
    4: "Room Start", 5: "Room End",
    62: "Async Save/Load", 63: "Async Dialog", 64: "Async HTTP",
    65: "Async Networking", 66: "Async Steam", 67: "Async Social",
    68: "Async Push", 69: "Async Save", 70: "Audio Playback",
    71: "Audio Recording", 72: "Gesture", 73: "System", 74: "Broadcast Message",
}
DRAW_NAMES = {
    0: "Draw", 64: "Draw GUI", 72: "Draw Begin", 73: "Draw End",
    74: "Draw GUI Begin", 75: "Draw GUI End", 76: "Pre Draw", 77: "Post Draw",
}
TYPE_NAMES = {
    2: "Alarm", 4: "Collision", 5: "Keyboard", 6: "Mouse",
    7: "Other", 8: "Draw", 9: "Key Press", 10: "Key Release",
}


def event_name(et, en, col=None):
    if et in EVENT_NAMES:
        return EVENT_NAMES[et]
    if et == 2:
        return "Alarm %d" % en
    if et == 3:
        return STEP_NAMES.get(en, "Step?%d" % en)
    if et == 4:
        return "Collision %s" % (col or "?")
    if et == 7:
        if 10 <= en <= 25:
            return "Other User %d" % (en - 10)
        return "Other %s" % OTHER_NAMES.get(en, "?%d" % en)
    if et == 8:
        return DRAW_NAMES.get(en, "Draw ?%d" % en)
    return "%s %d" % (TYPE_NAMES.get(et, "Type%d" % et), en)


def gen_objects():
    files = []
    for root, _dirs, names in os.walk(os.path.join(P, "objects")):
        for n in names:
            if n.endswith(".yy"):
                files.append(os.path.join(root, n))
    files.sort(key=rel)

    out = []
    for f in files:
        d = load_yy(f)
        name = d.get("name", os.path.basename(f)[:-3])
        parent = (d.get("parentObjectId") or {}).get("name")
        sprite = (d.get("spriteId") or {}).get("name")
        persistent = d.get("persistent", False)
        out.append("=== %s ===" % name)
        out.append("file:       %s" % rel(f))
        out.append("parent:     %s" % (parent if parent else "-"))
        out.append("spriteId:   %s" % (sprite if sprite else "-"))
        out.append("persistent: %s" % persistent)
        evs = d.get("eventList", [])
        out.append("events:     %d" % len(evs))
        for ev in evs:
            et = ev.get("eventType")
            en = ev.get("eventNum")
            col = (ev.get("collisionObjectId") or {}).get("name")
            out.append("  - %s (eventType=%s, eventNum=%s)" % (event_name(et, en, col), et, en))
        out.append("")
    header = [
        "# objects.txt — инвентарь objects/**/*.yy",
        "# name, parentObjectId.name, spriteId.name, persistent, список событий",
        "# (eventType/eventNum -> имя события GameMaker).",
        "# Объектов: %d" % len(files),
        "",
    ]
    _write("objects.txt", "\n".join(header + out))


# ---------------------------------------------------------------- rooms.txt
def gen_rooms():
    files = []
    for root, _dirs, names in os.walk(os.path.join(P, "rooms")):
        for n in names:
            if n.endswith(".yy"):
                files.append(os.path.join(root, n))
    files.sort(key=rel)

    out = []
    for f in files:
        d = load_yy(f)
        name = d.get("name", os.path.basename(f)[:-3])
        rs = d.get("roomSettings", {})
        out.append("=== %s ===" % name)
        out.append("file:  %s" % rel(f))
        out.append("size:  %s x %s (roomSettings.Width x .Height)"
                   % (rs.get("Width"), rs.get("Height")))
        total_inst = Counter()
        layers = d.get("layers", [])
        out.append("layers: %d" % len(layers))

        def emit_layer(layer, indent):
            lname = layer.get("name") or layer.get("%Name") or "?"
            ltype = layer.get("resourceType", "?")
            ldepth = layer.get("depth")
            insts = layer.get("instances")
            extra = ""
            if isinstance(insts, list):
                extra = " — instances: %d" % len(insts)
                for inst in insts:
                    on = (inst.get("objectId") or {}).get("name")
                    total_inst[on if on else "null"] += 1
            out.append("  %s- %s [%s, depth=%s]%s" % ("  " * indent, lname, ltype, ldepth, extra))
            for sub in layer.get("layers", []) or []:
                emit_layer(sub, indent + 1)

        for l in layers:
            emit_layer(l, 0)
        out.append("instances total: %d" % sum(total_inst.values()))
        for obj, cnt in sorted(total_inst.items(), key=lambda kv: (-kv[1], kv[0])):
            out.append("  %s: %d" % (obj, cnt))
        out.append("")
    header = [
        "# rooms.txt — инвентарь rooms/**/*.yy",
        "# имя, размер (roomSettings), слои (name/resourceType/depth),",
        "# подсчёт инстансов по objectId.name.",
        "# Комнат: %d" % len(files),
        "",
    ]
    _write("rooms.txt", "\n".join(header + out))


# ---------------------------------------------------------------- globals.txt
def gen_globals():
    re_use = re.compile(r"global\.([A-Za-z_][A-Za-z0-9_]*)")
    files = []
    for base in ("scripts", "objects", "rooms"):
        for root, _dirs, names in os.walk(os.path.join(P, base)):
            for n in names:
                if n.endswith(".gml"):
                    files.append(os.path.join(root, n))
    files.sort(key=rel)

    counts = Counter()
    occurrences = {}  # name -> list[(file, line, is_write)]
    for f in files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                for m in re_use.finditer(line):
                    name = m.group(1)
                    counts[name] += 1
                    rest = line[m.end():]
                    is_write = bool(re.match(r"\s*[+\-*/%|&^]?=(?!=)", rest))
                    occurrences.setdefault(name, []).append((rel(f), i, is_write))

    out = []
    for name in sorted(counts):
        occ = occurrences[name]
        first_write = next(((f, i) for f, i, w in occ if w), None)
        writes = sum(1 for _f, _i, w in occ if w)
        fw = ("%s:%d" % first_write) if first_write else "-"
        out.append("%-50s first_write=%-60s mentions=%d writes=%d" % (name, fw, counts[name], writes))
    header = [
        "# globals.txt — все global.<name> в .gml (scripts/, objects/, rooms/)",
        "# first_write — файл:строка первого присваивания 'global.x =' (вcl. += и т.п.),",
        "# mentions — всего вхождений (чтения+записи), writes — присваиваний.",
        "# Уникальных имён: %d" % len(counts),
        "",
    ]
    _write("globals.txt", "\n".join(header + out))


# ---------------------------------------------------------------- json_actions.txt
def gen_json_actions():
    path = os.path.join(P, "scripts", "cutscene_action_factory", "cutscene_action_factory.gml")
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    re_key = re.compile(r'f\[\$\s*"([^"]+)"\]\s*=\s*(.*)')
    re_get = re.compile(r'__cutscene_json_get_(?:string|real|bool|value|color|real_opt|real_opt)\(\s*(_map|_pos_map|_phase|_actors_raw|_pt),\s*"([^"]+)"')
    re_exists = re.compile(r'variable_struct_exists\(\s*(_map|_pos_map|_phase|_actors_raw|_pt|_seq_entry|_sub_entry|_entry),\s*"([^"]+)"')
    re_vget = re.compile(r'variable_struct_get\(\s*(_map|_pos_map|_phase),\s*"([^"]+)"')
    re_dollar = re.compile(r'(_map|_pos_map|_phase|_actors_raw|_pt)\[\$\s*"([^"]+)"\]')
    # helpers с неявными полями (проверено по cutscene_load_json.gml):
    implicit = [
        (re.compile(r'__cutscene_json_get_target\(\s*_map'), "target|target_ref (via __cutscene_json_get_target)"),
        (re.compile(r'__cutscene_json_get_seconds\(\s*_map'), "seconds|duration|time (via __cutscene_json_get_seconds)"),
        (re.compile(r'__cutscene_json_get_frames\(\s*_map'), "frames|seconds|duration|time (via __cutscene_json_get_frames)"),
        (re.compile(r'__cutscene_json_points_to_array'), "points (via __cutscene_json_points_to_array: {x,y}|[x,y])"),
        (re.compile(r'__cutscene_json_parse_direction'), "direction (via __cutscene_json_parse_direction: right/left/up/down|r/l/u/d|num)"),
    ]

    # Границы хендлеров: строки 'f[$ "..."' + конец функции (строка '}' верхнего уровня).
    keys = []
    for i, line in enumerate(lines, 1):
        m = re_key.search(line)
        if m:
            keys.append((i, m.group(1), m.group(2).strip()))

    out = []
    out.append("source: scripts/cutscene_action_factory/cutscene_action_factory.gml (%d lines)" % len(lines))
    out.append("dispatch: поле 'type' -> __cutscene_json_normalize_action_type -> global.__cutscene_action_factory[$ type]")
    out.append("          (__cutscene_json_action_from_struct, scripts/cutscene_load_json/cutscene_load_json.gml:199-221)")
    out.append("legacy-алиасы типов (normalize, cutscene_load_json.gml:223-235):")
    out.append("  shakeobj->shake_object, visible->set_visible, instant_mode->set_instant,")
    out.append("  waittalk/wait_talk->wait_for_dialogue, depth->set_depth, facing->set_facing,")
    out.append("  autofacing->auto_facing, autowalk->auto_walk")
    out.append("")
    out.append("Всего ключей f[$ ...]: %d" % len(keys))
    out.append("")

    for idx, (lineno, name, rhs) in enumerate(keys):
        end = keys[idx + 1][0] - 1 if idx + 1 < len(keys) else len(lines)
        alias = re.match(r'f\[\$\s*"([^"]+)"\]', rhs)
        if alias:
            out.append("%-28s line %-5d -> alias of '%s'" % (name, lineno, alias.group(1)))
            continue
        fields = OrderedDict()
        for j in range(lineno, min(end, len(lines)) + 1):
            line = lines[j - 1]
            for rgx, getf in ((re_get, lambda m: (m.group(1), m.group(2))),
                              (re_exists, lambda m: (m.group(1), m.group(2))),
                              (re_vget, lambda m: (m.group(1), m.group(2))),
                              (re_dollar, lambda m: (m.group(1), m.group(2)))):
                for mm in rgx.finditer(line):
                    src, fld = getf(mm)
                    key = fld if src == "_map" else "%s[].%s" % ({ "_phase": "phases", "_pos_map": "actors", "_actors_raw": "actors", "_pt": "points" }.get(src, src), fld)
                    fields.setdefault(key, set()).add(j)
            for rgx, label in implicit:
                if rgx.search(line):
                    fields.setdefault(label, set()).add(j)
        out.append("%-28s line %-5d fields: %s"
                   % (name, lineno, ", ".join(fields.keys()) if fields else "(нет)"))

    _write("json_actions.txt",
           "# json_actions.txt — типы JSON-экшенов cutscene_action_factory.gml\n"
           "# Для каждого ключа f[$ \"type\"]: номер строки и читаемые поля.\n"
           "# Поля вида 'phases[].x'/'actors[].x' — чтения из вложенных struct.\n\n"
           + "\n".join(out))


# ---------------------------------------------------------------- datafiles.txt
def gen_datafiles():
    base = os.path.join(P, "datafiles")
    entries = []
    total = 0
    for root, dirs, names in os.walk(base):
        dirs.sort()
        for n in sorted(names):
            fp = os.path.join(root, n)
            sz = os.path.getsize(fp)
            total += sz
            entries.append((rel(fp), sz))
    out = ["%10d  %s" % (sz, p) for p, sz in entries]
    header = [
        "# datafiles.txt — дерево datafiles/ с размерами (байты)",
        "# Файлов: %d, всего байт: %d" % (len(entries), total),
        "",
    ]
    _write("datafiles.txt", "\n".join(header + out))


def _write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")
    print("wrote %s (%d bytes)" % (name, os.path.getsize(os.path.join(OUT, name))))


if __name__ == "__main__":
    gen_scripts()
    gen_objects()
    gen_rooms()
    gen_globals()
    gen_json_actions()
    gen_datafiles()
