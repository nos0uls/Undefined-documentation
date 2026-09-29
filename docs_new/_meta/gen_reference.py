#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_reference.py — генератор справочных страниц docs_new/reference/.

Вход (рядом со скриптом, _meta/):
  scripts.txt  — инвентарь scripts/**/*.gml (function/@desc/@function строки)
  objects.txt  — инвентарь objects/**/*.yy (parent/sprite/persistent/events)

Дополнительно читает исходные .gml из проекта GameMaker (read-only) —
только для извлечения полного текста /// @desc/@description/@summary:
  P = /media/n0souls/New Volume/GitHub/Undefinedtale-888/Undefinedtale888

Выход:
  docs_new/reference/gml-scripts.md
  docs_new/reference/objects-and-events.md

Описания и ссылки на док-страницы, которые нельзя вывести из кода,
заданы вручную в таблицах DESC_OVERRIDES / PAGE_FOR / OBJ_GROUP / OBJ_PAGE.
"""
import os
import re
import sys

P = "/media/n0souls/New Volume/GitHub/Undefinedtale-888/Undefinedtale888"
META = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(META, ".."))
OUT_SCRIPTS = os.path.join(DOCS, "reference", "gml-scripts.md")
OUT_OBJECTS = os.path.join(DOCS, "reference", "objects-and-events.md")

# ---------------------------------------------------------------- исключения
# Библиотеки и внутренний тестовый фреймворк — не пользовательский код проекта.
LIB_PREFIXES = (
    "Chatterbox", "__Chatterbox", "IsChatterbox",   # Chatterbox
    "scribble", "__scribble",                        # Scribble
    "TGMX_",                                         # TweenGMS
    "scr_test_", "scr_stress_tests",                 # тестовый фреймворк
)

RE_FILE = re.compile(r"^=== (.+\.gml) ===$")
RE_LINE = re.compile(r"^\s*(\d+):\s+(.*)$")
RE_FUNC = re.compile(
    r"^function\s+(\w+)\s*\(([^)]*)\)\s*(?::\s*\w+\s*\([^)]*\))?\s*(constructor)?")


def is_library(dir_name):
    return dir_name.startswith(LIB_PREFIXES)


# ---------------------------------------------------------------- чтение .gml
_gml_cache = {}


def gml_lines(rel_path):
    """Строки исходника из проекта; None, если файла нет."""
    if rel_path not in _gml_cache:
        path = os.path.join(P, rel_path)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                _gml_cache[rel_path] = fh.read().splitlines()
        except OSError:
            _gml_cache[rel_path] = None
    return _gml_cache[rel_path]


def extract_desc(rel_path, lineno):
    """Текст /// @desc/@description/@summary над объявлением функции.

    Идёт вверх по comment-строкам (///-докблок и // -комментарии — последние
    иногда вклиниваются между докблоком и объявлением, см. scr_checkPlayerFacing).
    Останавливается на первой строке кода или пустой строке.
    """
    lines = gml_lines(rel_path)
    if lines is None:
        return ""
    i = lineno - 1
    block = []
    j = i - 1
    while j >= 0:
        s = lines[j].strip()
        if s.startswith("///"):
            block.insert(0, s)
        elif s.startswith("//") or s == "":
            pass
        else:
            break
        j -= 1
    parts = []
    capture = False
    for bl in block:
        m = re.match(r"///\s*@(desc|description|summary)\b\s*(.*)", bl)
        if m:
            if parts:
                break  # второй desc-блок (напр. @summary + @description) не клеим
            capture = True
            parts.append(m.group(2))
            continue
        if re.match(r"///\s*@", bl):
            capture = False
            continue
        if capture:
            parts.append(re.sub(r"^///\s*", "", bl))
    return " ".join(p for p in parts if p).strip()


def file_is_delete_candidate(rel_path):
    """Файл помечен DELETE_CANDIDATE в шапке."""
    lines = gml_lines(rel_path)
    if not lines:
        return False
    return any("DELETE_CANDIDATE" in ln for ln in lines[:8])


def shorten(text, limit=170):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    # Отрезаем по первой точке, если она не слишком рано.
    dot = text.find(". ")
    if 30 <= dot <= limit:
        return text[: dot + 1]
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "…"


# ------------------------------------------------------- описания (overrides)
# Для функций без ///-документации или с неочевидной сутью. Одна строка.
DESC_OVERRIDES = {
    # --- c_cmd.gml: инфраструктура DSL ---
    "__get_active_mgr": "Возвращает активный менеджер катсцены или недособранный build-менеджер",
    "__cutscene_builder_add": "Добавляет action в очередь активного/build-менеджера через `cutscene_add`",
    "__cutscene_selected_actor": "Возвращает актёра, выбранного командой (для команд без явной цели)",
    "__cutscene_cmd_target_missing": "Проверяет, что цель не задана (`noone`/`undefined`/пустая строка)",
    "__cutscene_cmd_require_target": "Гейт `c_*`-команды: без цели пишет warning в лог и возвращает `false`",
    "__cutscene_bridge_real": "Приводит аргумент из Chatterbox к числу; нечисловой/пустой вход → `_default`",
    "__cutscene_bridge_color": "Приводит аргумент Chatterbox к константе цвета (имя или число)",
    "cutscene_play_json": "Загружает JSON-катсцену (`cutscene_load_json`) и сразу запускает её",
    "c_play_json": "Алиас `cutscene_play_json`",
    "cutscene_stop_active": "Останавливает активную катсцену (`finish_cutscene`); возвращает `true`/`false`",
    "cutscene_is_active": "Возвращает `global.cutscene_active`",
    "cutscene_dialogue_is_active": "Проверяет, идёт ли диалог, открытый катсценой",
    "cutscene_register_chatterbox_functions": "Регистрирует `c_*`-команды как функции Chatterbox для вызова из yarn",
    # --- c_cmd.gml: команды ---
    "c_begin": "Открывает сессию сборки катсцены: создаёт build-менеджер `obj_cutsceneManager`",
    "c_play": "Запускает собранную катсцену (`start_cutscene`); без менеджера — warning + `noone`",
    "c_wait": "Добавляет `ActionWait` — пауза очереди на N кадров",
    "c_dialogue": "Добавляет `ActionDialogue` — запуск yarn-диалога",
    "c_animate": "Добавляет `ActionAnimate` — смена спрайта/кадра/скорости анимации цели",
    "c_tween": "Добавляет `ActionTween` — твин свойства цели (или камеры при `kind=\"camera\"`)",
    "c_tween_camera": "Добавляет `ActionTween` для свойства камеры",
    "c_fadein": "Добавляет `ActionFadeIn` — проявление экрана за N кадров",
    "c_fadeout": "Добавляет `ActionFadeOut` — затемнение экрана за N кадров",
    "c_sfx": "Добавляет `ActionPlaySFX` — проигрывание звука",
    "c_soundplay": "Алиас `c_sfx`",
    "c_emote": "Добавляет `ActionEmote` — эмоция над целью",
    "c_jump": "Добавляет `ActionJump` — прыжок цели в точку",
    "c_halt": "Добавляет `ActionHalt` — остановка движения цели (без аргумента — выбранного актёра)",
    "c_flip": "Добавляет `ActionFlip` — горизонтальное отражение спрайта цели",
    "c_spin": "Добавляет `ActionSpin` — вращение цели",
    "c_shakeobj": "Добавляет `ActionShakeObject` — тряска цели (без аргумента — выбранного актёра)",
    "c_visible": "Устанавливает `visible` цели через `ActionSetProperty`",
    "c_instant": "Добавляет `ActionSetInstantMode` — мгновенное выполнение действий",
    "c_walk": "Добавляет `ActionMoveRelativeDirection` — движение по направлению N кадров",
    "c_walkdirect": "Добавляет `ActionMoveDirect` — движение к точке за N кадров",
    "c_walkdirect_speed": "Добавляет `ActionMoveDirect` — движение к точке с заданной скоростью",
    "c_waittalk": "Добавляет `ActionWaitForDialogue` — ждать завершения реплики",
    "c_sprite": "Алиас `c_animate` (`ActionAnimate`)",
    "c_facing": "Добавляет разворот цели (`cutscene_set_facing` → `ActionSetFacing`)",
    "c_setxy": "Добавляет `ActionSetXY` — мгновенный телепорт цели",
    "c_autofacing": "Устанавливает `auto_face` цели через `ActionSetProperty`",
    "c_autowalk": "Устанавливает `auto_walk` цели через `ActionSetProperty`",
    "c_speaker": "Устанавливает имя спикера (nameplate) активного диалогового окна",
    "c_var_instance": "Добавляет `ActionSetProperty` — присвоить свойство цели",
    "c_var_lerp_instance": "Добавляет `ActionTween` — твин свойства с явным начальным значением",
    "c_lerp": "Прокси к `c_var_lerp_instance`",
    "c_var_lerp_to_instance": "Добавляет `ActionTween` — твин свойства от текущего значения",
    # --- scr_cutscene_classes.gml: инфраструктура ---
    "CutsceneAction": "Базовый конструктор действия катсцены (Command pattern)",
    "__cutscene_get_resolver": "Возвращает метод `resolve_target` менеджера, если он есть",
    "__cutscene_resolve_target_ref": "Резолвит `target_ref` через resolver; без resolver — только живой instance id",
    "__cutscene_resolve_target": "Резолвит цель действия в instance id",
    "__cutscene_resolve_targets": "Резолвит цель в массив instance id (несколько актёров по ключу)",
    "__cutscene_is_instant": "Возвращает флаг instant-режима менеджера",
    "__cutscene_get_global_manager": "Возвращает `global.active_cutscene_manager`",
    "__cutscene_normalize_direction": "Нормализует направление: строка/число → `global.DIR.*`",
    "__cutscene_direction_angle": "Направление `DIR` → угол в градусах",
    "__cutscene_angle_to_direction": "Угол в градусах → направление `DIR`",
    "__cutscene_actor_apply_facing": "Применяет направление к актёру: спрайт ходьбы + `facing_direction`",
    "__cutscene_dialogue_is_active": "Проверяет, открыто ли диалоговое окно (опционально — конкретный контроллер)",
    # /// @desc обрывается на «(см.» из-за среза shorten() по «. » внутри скобок.
    "__cutscene_find_dialogue_ctrl": "Возвращает живой контроллер диалогового окна: сначала `dialogue_controller` менеджера, затем fallback на «живое» окно textboxTest_scribble",
    "__cutscene_ease_value": "Вычисляет easing-коэффициент прогресса по имени кривой",
    "__cutscene_runtime_get_value": "Читает свойство цели runtime-эффекта (`instance`/`camera`)",
    "__cutscene_runtime_set_value": "Пишет свойство цели runtime-эффекта (`instance`/`camera`)",
    "cutscene_runtime_tween_to": "Регистрирует runtime-твин свойства инстанса/камеры",
    "cutscene_runtime_fade_to": "Управляет runtime fade-оверлеем (альфа, цвет)",
    "cutscene_runtime_play_sfx": "Проигрывает SFX из катсцены через `scr_play_sfx`",
    "cutscene_runtime_set_visible": "Меняет `visible` цели из runtime-эффектов",
    "cutscene_runtime_flip_x": "Отражает спрайт цели по горизонтали (`image_xscale`)",
    "cutscene_runtime_halt": "Останавливает движение цели из runtime-эффектов",
    "cutscene_runtime_shake_object": "Регистрирует runtime-тряску объекта",
    "cutscene_runtime_shake_camera": "Регистрирует runtime-тряску камеры",
    "cutscene_runtime_spin_object": "Регистрирует runtime-вращение объекта",
    "cutscene_runtime_jump_to": "Регистрирует runtime-прыжок цели в точку",
    "cutscene_runtime_ensure_state": "Ленивая инициализация `global.__cutscene_runtime`",
    "__cutscene_runtime_remove_at": "Удаляет элемент runtime-массива с откатом применённого эффекта",
    "cutscene_runtime_step": "Покадровое обновление всех runtime-эффектов (вызывается из Step менеджера)",
    "__cutscene_update_attachments": "Обновляет привязанных к родителям актёров (attachments)",
    "__cutscene_room_entry_spawn": "Спавнит сущности по entry-записи после смены комнаты",
    # --- scr_cutscene_classes.gml: action-классы ---
    "ActionWait": "Пауза очереди на N кадров",
    "ActionMarkNode": "Записывает имя достигнутой ноды (`last_reached_node` менеджера)",
    "ActionGoToNode": "Переход очереди к ноде, помеченной `ActionMarkNode`",
    "ActionSequence": "Последовательное выполнение массива действий",
    "ActionFollowPath": "Движение актёра по массиву точек `{x, y}`",
    "ActionActorCreate": "Создаёт актёра катсцены и регистрирует его в `actor_map`",
    "ActionMove": "Движение актёра к абсолютной точке с заданной скоростью",
    "ActionMoveRelativeDirection": "Движение по направлению заданное число кадров",
    "ActionMoveDirect": "Движение к точке за N кадров или с заданной скоростью",
    "ActionAnimate": "Смена спрайта/кадра/скорости анимации цели",
    "ActionDialogue": "Запуск yarn-диалога внутри катсцены",
    "ActionWaitForDialogue": "Ожидание завершения реплики диалогового окна",
    "ActionSetProperty": "Присвоение свойства инстанса или камеры",
    "ActionSetDepth": "Установка `depth` цели и перевод в manual-режим",
    "ActionSetXY": "Мгновенный телепорт цели в точку",
    "ActionSetInstantMode": "Включает instant-режим: действия выполняются за один кадр",
    "ActionHalt": "Остановка текущего движения цели",
    "ActionSpin": "Вращение цели (`image_angle`)",
    "ActionShakeObject": "Тряска объекта (runtime-эффект)",
    "ActionPlaySFX": "Проигрывание звука",
    "ActionEmote": "Эмоция (попап) над актёром",
    "ActionFadeTo": "Плавный переход fade-оверлея к заданной альфе",
    "ActionFadeIn": "Проявление экрана (`ActionFadeTo` к 0)",
    "ActionFadeOut": "Затемнение экрана (`ActionFadeTo` к 1)",
    "ActionTween": "Твин свойства цели к значению за N кадров",
    "ActionJump": "Прыжок цели в точку по параболе",
    "ActionCameraShake": "Тряска камеры (runtime-эффект)",
    "ActionParallel": "Параллельное выполнение веток действий",
    "ActionScheduleAction": "Запуск вложенного действия с задержкой (schedule)",
    "ActionAttachToTarget": "Привязка актёра к родителю со смещением",
    "ActionBranch": "Ветвление очереди по функции-условию",
    "ActionGuardGlobal": "Блокировка/ожидание по значению глобальной переменной",
    "ActionCameraCenter": "Мгновенное центрирование камеры на точке",
    "ActionCameraPan": "Панорамирование камеры к точке за N кадров",
    "ActionCameraPanSpeed": "Панорамирование камеры к точке с заданной скоростью",
    "ActionCameraPanToObj": "Панорамирование камеры к объекту за N кадров",
    "ActionCameraTrack": "Следование камеры за целью N кадров",
    "ActionCameraTrackUntilStop": "Следование камеры за целью до её остановки",
    "ActionWaitForInteract": "Ожидание взаимодействия игрока с целью (с таймаутом)",
    "ActionSetFlag": "Запись `global.flag[key] = value`",
    "ActionSetPlot": "Запись `global.plot = value`",
    "ActionSpawnEntity": "Спавн объекта в комнате (spawn_entity)",
    "ActionRoomChange": "Смена комнаты из катсцены с переходом",
    "ActionPartialControl": "Частичный контроль ввода игрока во время катсцены",
    # --- прочие скрипты без доков ---
    "cutscene_init_action_factory": "Заполняет `global.__cutscene_action_factory` — dispatch типа JSON-экшена → конструктор `Action*`",
    "cutscene_load_json": "Читает JSON-файл катсцены и собирает менеджер с очередью действий",
    "__cutscene_json_normalize_action_type": "Нормализует legacy-алиасы типов экшенов (`shakeobj` → `shake_object` и т.д.)",
    "__cutscene_json_get_frames": "Читает длительность: `frames` приоритетнее `seconds`/`duration`/`time`",
    "__cutscene_json_get_color": "Читает цвет из JSON-поля (строка-имя или число)",
    "cutscene_music_pitch": "Возвращает `ActionMusicPitch` для добавления в катсцену",
    "draw_text_scribble": "Эмуляция `draw_text()` через Scribble; вызовы только у placeholder-объектов `obj_p3r_*` (DELETE_CANDIDATE)",
    "draw_text_scribble_ext": "Эмуляция `draw_text_ext()` через Scribble",
    "string_height_scribble": "Эмуляция `string_height()` через Scribble; вызовов в проекте нет (DELETE_CANDIDATE)",
    "string_height_scribble_ext": "Эмуляция `string_height()` с переносом по ширине через Scribble (DELETE_CANDIDATE)",
    "string_length_scribble": "Эмуляция `string_length()` через Scribble (DELETE_CANDIDATE)",
    "string_width_scribble": "Эмуляция `string_width()` через Scribble (DELETE_CANDIDATE)",
    "string_width_scribble_ext": "Эмуляция `string_width()` с переносом по ширине через Scribble (DELETE_CANDIDATE)",
    "Item": "Базовый конструктор предмета инвентаря",
    "interactionWithMainCast": "Мёртвая legacy-обёртка над `scr_interaction` (DELETE_CANDIDATE, тело зачищено)",
    "interactionWithNPCsOrObjects": "Мёртвая legacy-обёртка над `scr_interaction` (DELETE_CANDIDATE, тело зачищено)",
    "scr_npc_pick_dialogue": "Пустой стаб (DELETE_CANDIDATE): выбор реплики NPC делает контент через `readDialogue`",
    "Script312": "Пустой стаб (DELETE_CANDIDATE): имя не совпадает с ресурсом, живой аналог — `cutscene_animate`",
    "scr_cutscene_make": "Заглушка (DELETE_CANDIDATE): сборка катсцен идёт через `c_begin`/`c_play` или `cutscene_load_json`; возвращает `noone`",
    "draw_debug_collider": "Отрисовка bbox/спрайта всех инстансов типа объекта для debug-оверлея",
    "emote_hide_all_for": "Скрывает все эмоции цели — тело зачищено (DELETE_CANDIDATE)",
    "emote_hide_all": "Скрывает все эмоции — тело зачищено (DELETE_CANDIDATE)",
    "__cutscene_room_entry_spawn": "Мёртвая функция спавна по entry-записи — тело зачищено (DELETE_CANDIDATE)",
    "scr_input_normalize_key": "Приводит сохранённый код клавиши к допустимому vk-значению",
    "__music_fade_lerp": "Значение time-based фейда по оставшемуся времени таймера",
}

STUB_DESC = "Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE)"

# ------------------------------------------------- ссылки на страницы доков
# Ключ — имя функции или регулярка-префикс в PAGE_RULES; значение — путь
# относительно reference/ и текст ссылки.
PAGE_LABELS = {
    "../systems/input.md": "Ввод",
    "../systems/player.md": "Игрок",
    "../systems/dialogue.md": "Диалоги",
    "../systems/interaction.md": "Взаимодействие",
    "../systems/inventory-and-stats.md": "Инвентарь и статы",
    "../systems/save-system.md": "Сохранения",
    "../systems/music.md": "Музыка и звук",
    "../systems/ui-and-menus.md": "UI и меню",
    "../systems/debug-and-testing.md": "Отладка и тесты",
    "../systems/room-transitions.md": "Переходы комнат",
    "../cutscenes/gml-dsl.md": "GML DSL катсцен",
    "../cutscenes/action-classes.md": "Action-классы",
    "../cutscenes/json-actions.md": "JSON-экшены",
    "../cutscenes/architecture.md": "Архитектура катсцен",
    "../cutscenes/partial-control.md": "Частичный контроль",
    "../cutscenes/actors-and-camera.md": "Актёры и камера",
    "../architecture/overview.md": "Обзор архитектуры",
    "../architecture/initialization.md": "Инициализация",
    "../architecture/rooms.md": "Комнаты",
    "../architecture/object-hierarchy.md": "Иерархия объектов",
    "../architecture/global-state.md": "Глобальное состояние",
}

# Точные назначения по имени функции.
PAGE_FOR = {
    # input
    "scr_input__keys_for_action": "../systems/input.md",
    "scr_input_actions_list": "../systems/input.md",
    "scr_input_normalize_key": "../systems/input.md",
    "scr_input__is_cutscene_blocked_here": "../systems/input.md",
    "scr_input__partial_control_allows": "../cutscenes/partial-control.md",
    "scr_input_gamepad_update": "../systems/input.md",
    "scr_input__gamepad_down": "../systems/input.md",
    "scr_input__gamepad_pressed": "../systems/input.md",
    "scr_input_down": "../systems/input.md",
    "scr_input_pressed": "../systems/input.md",
    "scr_input_repeater": "../systems/input.md",
    "scr_input_rebind": "../systems/input.md",
    "scr_input_rebind_slot": "../systems/input.md",
    "scr_input_keys_hint": "../systems/input.md",
    "scr_key_to_string": "../systems/input.md",
    "scr_buildInputMap": "../systems/input.md",
    # player / collision
    "scr_player_animation": "../systems/player.md",
    "scr_player_facing": "../systems/player.md",
    "scr_sprite_for_facing": "../systems/player.md",
    "scr_facing_for_sprite": "../systems/player.md",
    "scr_player_movement": "../systems/player.md",
    "scr_player_process_mutually_exclusive_inputs": "../systems/player.md",
    "scr_player_room_lock": "../systems/room-transitions.md",
    "scr_player_slope_resolve": "../systems/player.md",
    "scr_player_cell_blocked_by_slope": "../systems/player.md",
    "scr_player_ui_blocking": "../systems/player.md",
    "scr_player_debug_ghost": "../systems/debug-and-testing.md",
    "scr_collision_resolve": "../systems/player.md",
    "scr_checkPlayerFacing": "../systems/player.md",
    # dialogue / interaction / emote
    "readDialogue": "../systems/dialogue.md",
    "scr_parse_emote": "../systems/dialogue.md",
    "__parse_emote_resolve_display": "../systems/dialogue.md",
    "map_emotions": "../systems/dialogue.md",
    "actor_display_name": "../systems/dialogue.md",
    "draw_text_scribble": "../systems/dialogue.md",
    "draw_text_scribble_ext": "../systems/dialogue.md",
    "string_height_scribble": "../systems/dialogue.md",
    "string_height_scribble_ext": "../systems/dialogue.md",
    "string_length_scribble": "../systems/dialogue.md",
    "string_width_scribble": "../systems/dialogue.md",
    "string_width_scribble_ext": "../systems/dialogue.md",
    "emote_show": "../systems/dialogue.md",
    "emote_hide_all_for": "../systems/dialogue.md",
    "emote_hide_all": "../systems/dialogue.md",
    "emote_resolve_sprite": "../systems/dialogue.md",
    "emote_step": "../systems/dialogue.md",
    "emote_draw_gui": "../systems/dialogue.md",
    "__emote_system_ready": "../systems/dialogue.md",
    "__emote_sprite_speed_per_frame": "../systems/dialogue.md",
    "scr_interaction": "../systems/interaction.md",
    "interactionWithNPCsOrObjects": "../systems/interaction.md",
    "interactionWithMainCast": "../systems/interaction.md",
    "scr_npc_pick_dialogue": "../systems/interaction.md",
    "scr_player_marker_update": "../systems/interaction.md",
    # inventory / stats
    "Item": "../systems/inventory-and-stats.md",
    "WeaponItem": "../systems/inventory-and-stats.md",
    "ArmorItem": "../systems/inventory-and-stats.md",
    "FoodItem": "../systems/inventory-and-stats.md",
    "item_deserialize": "../systems/inventory-and-stats.md",
    "inventory_serialize": "../systems/inventory-and-stats.md",
    "inventory_deserialize": "../systems/inventory-and-stats.md",
    "item_database_register": "../systems/inventory-and-stats.md",
    "item_database": "../systems/inventory-and-stats.md",
    "inventory_add": "../systems/inventory-and-stats.md",
    "scr_inventory_init": "../systems/inventory-and-stats.md",
    "scr_stats_recalc": "../systems/inventory-and-stats.md",
    "scr_item_apply_use": "../systems/inventory-and-stats.md",
    "scr_checkItemSkip": "../systems/inventory-and-stats.md",
    "playableCharacterInfo": "../systems/inventory-and-stats.md",
    # save system / persistence
    "scr_saveLoad": "../systems/save-system.md",
    "scr_saveSave": "../systems/save-system.md",
    "scr_save_slot_names": "../systems/save-system.md",
    "scr_save_metadata_defaults": "../systems/save-system.md",
    "scr_save_read_metadata": "../systems/save-system.md",
    "scr_defaultLoad": "../systems/save-system.md",
    "scr_game_state_get_path": "../systems/save-system.md",
    "scr_game_state_default": "../systems/save-system.md",
    "scr_game_state_load": "../systems/save-system.md",
    "scr_game_state_save": "../systems/save-system.md",
    "scr_entity_state_get": "../systems/save-system.md",
    "scr_entity_state_set": "../systems/save-system.md",
    "scr_entity_state_clear": "../systems/save-system.md",
    "scr_world_flag_set": "../systems/save-system.md",
    "scr_world_flag_get": "../systems/save-system.md",
    "scr_global_quick_save": "../systems/save-system.md",
    "scr_resetGameToDefault": "../systems/save-system.md",
    "scr_format_playtime": "../systems/save-system.md",
    # settings / UI / menu
    "scr_loadSettings": "../systems/ui-and-menus.md",
    "scr_saveSettings": "../systems/ui-and-menus.md",
    "scr_applySettings": "../systems/ui-and-menus.md",
    "scr_resetSettings": "../systems/ui-and-menus.md",
    "scr_settings_parse_real": "../systems/ui-and-menus.md",
    "scr_settings_safe_volume": "../systems/ui-and-menus.md",
    "scr_settings_deep_copy": "../systems/ui-and-menus.md",
    "scr_settings_apply_and_save": "../systems/ui-and-menus.md",
    "scr_resetInputToDefault": "../systems/ui-and-menus.md",
    "scr_settings_misc_items": "../systems/ui-and-menus.md",
    "scr_settings_step_root": "../systems/ui-and-menus.md",
    "scr_settings_step_category": "../systems/ui-and-menus.md",
    "scr_settings_step_rebind": "../systems/ui-and-menus.md",
    "scr_settings_step_confirm_reset": "../systems/ui-and-menus.md",
    "scr_callMenuInit": "../systems/ui-and-menus.md",
    "scr_checkUIBlocking": "../systems/ui-and-menus.md",
    "scr_ui_objects_list": "../systems/ui-and-menus.md",
    "scr_checkUIBlocking_raw": "../systems/ui-and-menus.md",
    "scr_ui_list_controller": "../systems/ui-and-menus.md",
    "scr_ui_nav_vertical": "../systems/ui-and-menus.md",
    "scr_ui_read_actions": "../systems/ui-and-menus.md",
    "scr_menu_shader_push": "../systems/ui-and-menus.md",
    "scr_menu_shader_pop": "../systems/ui-and-menus.md",
    "scr_menu_volume_push": "../systems/ui-and-menus.md",
    "scr_menu_volume_pop": "../systems/ui-and-menus.md",
    "scr_global_reset_settings_flag": "../systems/ui-and-menus.md",
    "scr_global_toggle_fullscreen": "../systems/ui-and-menus.md",
    "scr_global_handle_notifications": "../systems/ui-and-menus.md",
    "scr_p3r_draw_cursor": "../systems/ui-and-menus.md",
    "scr_p3r_draw_panel": "../systems/ui-and-menus.md",
    "scr_p3r_draw_button": "../systems/ui-and-menus.md",
    "scr_p3r_menu_state_create": "../systems/ui-and-menus.md",
    "scr_p3r_menu_get_selected": "../systems/ui-and-menus.md",
    "scr_p3r_menu_execute_selected": "../systems/ui-and-menus.md",
    "scr_p3r_menu_close": "../systems/ui-and-menus.md",
    "scr_p3r_menu_nav": "../systems/ui-and-menus.md",
    "scr_p3r_palette": "../systems/ui-and-menus.md",
    "scr_p3r_particles_create": "../systems/ui-and-menus.md",
    "scr_p3r_particles_destroy": "../systems/ui-and-menus.md",
    "scr_p3r_particles_burst": "../systems/ui-and-menus.md",
    "scr_p3r_particles_stream": "../systems/ui-and-menus.md",
    # music / audio
    "scr_music_init": "../systems/music.md",
    "__music_handoff_to_prev": "../systems/music.md",
    "__music_fade_lerp": "../systems/music.md",
    "scr_global_music_fade_previous": "../systems/music.md",
    "scr_global_music_update_current": "../systems/music.md",
    "scr_play_sfx": "../systems/music.md",
    "scr_SFXPlay": "../systems/music.md",
    # debug
    "scr_debug_activation_check": "../systems/debug-and-testing.md",
    "draw_text_outlined": "../systems/debug-and-testing.md",
    "draw_debug_collider": "../systems/debug-and-testing.md",
    "scr_global_debug_hotkeys": "../systems/debug-and-testing.md",
    "__debug_jump_room": "../systems/debug-and-testing.md",
    "scr_toggle_debug_flag": "../systems/debug-and-testing.md",
    "scr_get_next_game_room": "../systems/debug-and-testing.md",
    "scr_room_is_dev_navigation_excluded": "../systems/debug-and-testing.md",
    "scr_global_handle_dev_spawn": "../systems/debug-and-testing.md",
    # rooms / transitions / init
    "scr_room_fade_update": "../systems/room-transitions.md",
    "scr_global_transition_safety": "../systems/room-transitions.md",
    "scr_global_on_room_change": "../systems/room-transitions.md",
    "scr_roomFromName": "../architecture/rooms.md",
    "scr_layer_ensure_instances": "../architecture/rooms.md",
    "scr_constants": "../architecture/initialization.md",
    "scr_anim": "../architecture/object-hierarchy.md",
    # cutscenes: JSON-движок и runtime
    "cutscene_play_json": "../cutscenes/json-actions.md",
    "c_play_json": "../cutscenes/json-actions.md",
    "cutscene_load_json": "../cutscenes/json-actions.md",
    "cutscene_init_action_factory": "../cutscenes/json-actions.md",
    "cutscene_load_engine_settings": "../cutscenes/json-actions.md",
    "ActionPartialControl": "../cutscenes/partial-control.md",
    "__cutscene_parallel_push": "../cutscenes/action-classes.md",
    "__cutscene_parallel_pop": "../cutscenes/action-classes.md",
    "__cutscene_parallel_splice": "../cutscenes/action-classes.md",
    "__cutscene_parallel_request_abort": "../cutscenes/action-classes.md",
    "scr_room_entry_check": "../systems/room-transitions.md",
}

# Префиксные правила (проверяются по порядку после PAGE_FOR).
PAGE_RULES = [
    (re.compile(r"^c_[a-z]"), "../cutscenes/gml-dsl.md"),
    (re.compile(r"^__cutscene_cmd_|^__cutscene_bridge_|^__get_active_mgr|^__cutscene_builder_add|^__cutscene_selected_actor"), "../cutscenes/gml-dsl.md"),
    (re.compile(r"^cutscene_(stop_active|is_active|dialogue_is_active|register_chatterbox_functions)$"), "../cutscenes/gml-dsl.md"),
    (re.compile(r"^cutscene_(add|branch|set_facing|tween|fade_in|fade_out|play_sfx|emote|jump|halt|flip|spin|shake_object|set_visible|set_instant|wait_for_dialogue|set_property|actor_create|actor_destroy|animate|auto_facing_toggle|auto_walk_toggle|camera_|dialogue|follow_path|move|parallel|run_function|set_depth|set_xy|wait)$"), "../cutscenes/gml-dsl.md"),
    (re.compile(r"^Action"), "../cutscenes/action-classes.md"),
    (re.compile(r"^cutscene_music_"), "../cutscenes/action-classes.md"),
    (re.compile(r"^ActionMusic|^__cutscene_music_"), "../cutscenes/action-classes.md"),
    (re.compile(r"^__cutscene_json_"), "../cutscenes/json-actions.md"),
    (re.compile(r"^cutscene_|^__cutscene|^CutsceneAction"), "../cutscenes/architecture.md"),
    (re.compile(r"^scr_input"), "../systems/input.md"),
    (re.compile(r"^scr_player"), "../systems/player.md"),
    (re.compile(r"^scr_save|^scr_defaultLoad|^scr_game_state|^scr_entity_state|^scr_world_flag"), "../systems/save-system.md"),
    (re.compile(r"^scr_settings|^scr_ui_|^scr_menu_|^scr_p3r_"), "../systems/ui-and-menus.md"),
    (re.compile(r"^scr_music|^__music|ActionMusic|^scr_SFXPlay|^scr_play_sfx"), "../systems/music.md"),
    (re.compile(r"^scr_debug|^__debug|^draw_debug|^draw_text_outlined|^scr_toggle_debug"), "../systems/debug-and-testing.md"),
    (re.compile(r"^scr_room_fade|^scr_global_transition|^scr_global_on_room"), "../systems/room-transitions.md"),
    (re.compile(r"^scr_global_"), "../architecture/global-state.md"),
    (re.compile(r"^emote_|^__emote"), "../systems/dialogue.md"),
    (re.compile(r"^scr_"), "../architecture/overview.md"),
]


def page_cell(func_name):
    href = PAGE_FOR.get(func_name)
    if href is None:
        for rx, h in PAGE_RULES:
            if rx.search(func_name):
                href = h
                break
    if href is None:
        return "—"
    return "[%s](%s)" % (PAGE_LABELS.get(href, href), href)


# ------------------------------------------------------------- парсинг scripts.txt
def parse_scripts():
    """-> [(rel_path, [ {name, args, ctor, stub, line} ])] по файлам."""
    path = os.path.join(META, "scripts.txt")
    files = []
    cur = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            m = RE_FILE.match(line)
            if m:
                cur = {"path": m.group(1), "funcs": []}
                files.append(cur)
                continue
            if cur is None:
                continue
            lm = RE_LINE.match(line)
            if not lm:
                continue
            lineno, text = int(lm.group(1)), lm.group(2).strip()
            fm = RE_FUNC.match(text)
            if fm:
                cur["funcs"].append({
                    "name": fm.group(1),
                    "args": fm.group(2).strip(),
                    "ctor": bool(fm.group(3)),
                    "stub": text.rstrip().endswith("{}"),
                    "line": lineno,
                })
    return files


def func_desc(rel_path, fn):
    if fn["name"] in DESC_OVERRIDES:
        return DESC_OVERRIDES[fn["name"]]
    if fn["stub"]:
        return STUB_DESC
    text = extract_desc(rel_path, fn["line"])
    if text:
        return shorten(text)
    if file_is_delete_candidate(rel_path):
        return "См. комментарий DELETE_CANDIDATE в шапке файла"
    return "—"


# ---------------------------------------------------------------- markdown
def md_row(*cells):
    return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"


# ------------------------------------------------------------- стиль (тире)
# « — » как суррогат связки — ИИ-маркер; чистим в генерируемом тексте.
# Парные вставки « — x — » → скобки; одиночные «X — пояснение» → «X: пояснение».
# Не трогаем: пустые ячейки `| — |`, строки sources-комментария, код-блоки.
_DASH_PAIR = re.compile(r"(?<=[\w`\)\]\"*А-Яа-яёЁ]) — ([^—|.;:\n]{1,80}?) — (?=[^\s|])")
_DASH_SOLO = re.compile(r"(?<=[\w`\)\]\"*А-Яа-яёЁ]) — (?=[^\s|])")


def fix_dashes(page_text):
    out_lines = []
    in_fence = False
    for line in page_text.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if in_fence or "<!-- sources:" in line:
            out_lines.append(line)
            continue
        line = _DASH_PAIR.sub(r" (\1) ", line)
        line = _DASH_SOLO.sub(": ", line)
        out_lines.append(line)
    return "\n".join(out_lines)


def script_group(dir_name):
    if dir_name.startswith("c_"):
        return "dsl"
    if dir_name.startswith("cutscene_"):
        return "cutscene_api"
    if dir_name.startswith("scr_"):
        return "scr"
    return "misc"


GROUP_TITLES = [
    ("scr", "Системные скрипты (`scripts/scr_*`)"),
    ("dsl", "DSL-команды катсцен (`scripts/c_*`, `c_cmd.gml`)"),
    ("cutscene_api", "Обёртки и загрузчики катсцен (`scripts/cutscene_*`)"),
    ("misc", "Прочие скрипты"),
]


def gen_scripts_page(files):
    groups = {k: [] for k, _t in GROUP_TITLES}
    total_funcs = 0
    for f in files:
        dir_name = os.path.basename(os.path.dirname(f["path"]))
        if is_library(dir_name):
            continue
        if not f["funcs"]:
            continue
        groups[script_group(dir_name)].append(f)
        total_funcs += len(f["funcs"])

    out = [
        "---",
        "title: Справочник GML-скриптов",
        "tags:",
        "  - reference",
        "  - gml",
        "---",
        "",
        "# Справочник GML-скриптов",
        "",
        "Все пользовательские функции из `scripts/` проекта Undefinedtale-888: сигнатуры, "
        "назначение и ссылки на разделы документации.",
        "",
        '!!! info "Генерируемая страница"',
        "    Таблицы собираются скриптом `_meta/gen_reference.py` из `_meta/scripts.txt` "
        "(+ `///`-комментарии исходников). После изменения кода страницу пересобирают, "
        "а не правят вручную.",
        "",
        '!!! note "Что не входит в таблицы"',
        "    - Библиотеки: Chatterbox (`Chatterbox*`, `__Chatterbox*`, `IsChatterbox`), "
        "Scribble (`scribble*`, `__scribble*`), TweenGMS (`TGMX_*`, `o_SharedTweener`).",
        "    - Внутренний тестовый фреймворк: `scr_test_*`, `scr_stress_tests`.",
        "    - Макрос-файлы без функций (`currentENUMS`, конфиги библиотек).",
        "",
        "Всего функций: **%d** в **%d** файлах. Колонка «Док-страница» ведёт на "
        "тематический раздел; `—` — отдельной страницы нет." % (
            total_funcs, sum(len(v) for v in groups.values())),
        "",
    ]

    for key, title in GROUP_TITLES:
        gfiles = sorted(groups[key], key=lambda f: f["path"])
        if not gfiles:
            continue
        out.append("## " + title)
        out.append("")
        for f in gfiles:
            dir_name = os.path.basename(os.path.dirname(f["path"]))
            out.append("### `scripts/%s/`" % dir_name)
            out.append("")
            out.append(md_row("Функция", "Сигнатура", "Назначение", "Док-страница"))
            out.append(md_row("---", "---", "---", "---"))
            for fn in f["funcs"]:
                sig = "%s(%s)" % (fn["name"], fn["args"])
                if fn["ctor"]:
                    sig += " constructor"
                out.append(md_row(
                    "`%s`" % fn["name"],
                    "`%s`" % sig,
                    func_desc(f["path"], fn),
                    page_cell(fn["name"]),
                ))
            out.append("")

    out += [
        "## См. также",
        "",
        "- [Объекты и события](objects-and-events.md) — справочник объектов",
        "- [Глоссарий](glossary.md) — термины проекта",
        "- [GML DSL катсцен](../cutscenes/gml-dsl.md) — команды `c_*` в контексте движка",
        "",
        "<!-- sources: _meta/scripts.txt; scripts/**/*.gml (/// @desc/@description/@summary); "
        "docs_new/_meta/nav_plan.md -->",
        "",
    ]
    return "\n".join(out)


# ------------------------------------------------------------- парсинг objects.txt
RE_OBJ = re.compile(r"^=== (\w+) ===$")


def parse_objects():
    path = os.path.join(META, "objects.txt")
    objs = []
    cur = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            m = RE_OBJ.match(line)
            if m:
                cur = {"name": m.group(1), "parent": "-", "sprite": "-",
                       "persistent": False, "events": []}
                objs.append(cur)
                continue
            if cur is None:
                continue
            s = line.strip()
            if s.startswith("parent:"):
                cur["parent"] = s.split(":", 1)[1].strip()
            elif s.startswith("spriteId:"):
                cur["sprite"] = s.split(":", 1)[1].strip()
            elif s.startswith("persistent:"):
                cur["persistent"] = s.split(":", 1)[1].strip() == "True"
            elif s.startswith("- "):
                cur["events"].append(s[2:].split(" (", 1)[0])
    return objs


OBJ_GROUPS_ORDER = [
    ("par", "Родители `par_*`"),
    ("sys", "Системные менеджеры"),
    ("world", "Игрок и мир"),
    ("ui", "UI и меню"),
    ("cutscene", "Катсцены"),
    ("debug", "Debug и прочее"),
]

OBJ_GROUP = {
    "par_actor": "par", "par_decor": "par", "par_depth": "par",
    "par_entity": "par", "par_interactable": "par",
    "obj_Init": "sys", "obj_globalManager": "sys", "obj_music_ctrl": "sys",
    "obj_changingRoomsController": "sys", "obj_saveManager": "sys",
    "obj_settingsManager": "sys", "o_SharedTweener": "sys",
    "obj_player": "world", "obj_collider": "world", "obj_slopeCollider": "world",
    "objRoomChanger": "world", "obj_pointMarker": "world",
    "obj_visualObject": "world", "obj_anim": "world", "obj_face": "ui",
    "npc1": "world", "npc2": "world", "obj_asher": "world", "obj_bench": "world",
    "obj_dialoguetest": "world", "obj_save": "world", "obj_sheepFountain": "world",
    "obj_sign": "world", "bush": "world", "obj_kachela": "world",
    "obj_lantern": "world", "obj_tree1": "world", "obj_tree2": "world",
    "pinkBench": "world", "sand": "world", "spr_pinkBench": "world",
    "obj_menu": "ui", "obj_inGameMenu": "ui", "obj_menuBGSpriteChanger": "ui",
    "obj_p3r_background": "ui", "obj_p3r_pause": "ui", "obj_p3r_settings": "ui",
    "obj_p3r_title": "ui", "obj_p3r_transition": "ui",
    "textboxTest_scribble": "ui",
    "obj_cutsceneManager": "cutscene", "obj_actor": "cutscene", "obj_dummy": "cutscene",
    "obj_devLoader": "debug", "obj_sound_test": "debug",
    "obj_cutsceneTest": "debug", "obj_menuTest": "debug", "screenshot": "debug",
}

OBJ_PAGE = {
    "par_actor": "../architecture/object-hierarchy.md",
    "par_decor": "../architecture/object-hierarchy.md",
    "par_depth": "../architecture/object-hierarchy.md",
    "par_entity": "../architecture/object-hierarchy.md",
    "par_interactable": "../architecture/object-hierarchy.md",
    "obj_Init": "../architecture/initialization.md",
    "obj_globalManager": "../architecture/global-state.md",
    "obj_music_ctrl": "../systems/music.md",
    "obj_changingRoomsController": "../systems/room-transitions.md",
    "obj_saveManager": "../systems/save-system.md",
    "obj_settingsManager": "../systems/ui-and-menus.md",
    "o_SharedTweener": "—",
    "obj_player": "../systems/player.md",
    "obj_collider": "../systems/player.md",
    "obj_slopeCollider": "../systems/player.md",
    "objRoomChanger": "../systems/room-transitions.md",
    "obj_pointMarker": "../systems/interaction.md",
    "obj_visualObject": "../architecture/object-hierarchy.md",
    "obj_anim": "../architecture/object-hierarchy.md",
    "npc1": "../systems/interaction.md",
    "npc2": "../systems/interaction.md",
    "obj_asher": "../systems/interaction.md",
    "obj_bench": "../systems/interaction.md",
    "obj_dialoguetest": "../systems/interaction.md",
    "obj_save": "../systems/save-system.md",
    "obj_sheepFountain": "../systems/interaction.md",
    "obj_sign": "../architecture/object-hierarchy.md",
    "bush": "../architecture/object-hierarchy.md",
    "obj_kachela": "../architecture/object-hierarchy.md",
    "obj_lantern": "../architecture/object-hierarchy.md",
    "obj_tree1": "../architecture/object-hierarchy.md",
    "obj_tree2": "../architecture/object-hierarchy.md",
    "pinkBench": "../architecture/object-hierarchy.md",
    "sand": "../architecture/object-hierarchy.md",
    "spr_pinkBench": "../architecture/object-hierarchy.md",
    "obj_menu": "../systems/ui-and-menus.md",
    "obj_inGameMenu": "../systems/ui-and-menus.md",
    "obj_menuBGSpriteChanger": "../systems/ui-and-menus.md",
    "obj_p3r_background": "../systems/ui-and-menus.md",
    "obj_p3r_pause": "../systems/ui-and-menus.md",
    "obj_p3r_settings": "../systems/ui-and-menus.md",
    "obj_p3r_title": "../systems/ui-and-menus.md",
    "obj_p3r_transition": "../systems/ui-and-menus.md",
    "obj_face": "../systems/dialogue.md",
    "textboxTest_scribble": "../systems/dialogue.md",
    "obj_cutsceneManager": "../cutscenes/architecture.md",
    "obj_actor": "../cutscenes/actors-and-camera.md",
    "obj_dummy": "../cutscenes/actors-and-camera.md",
    "obj_devLoader": "../systems/debug-and-testing.md",
    "obj_sound_test": "../systems/debug-and-testing.md",
    "obj_cutsceneTest": "../systems/debug-and-testing.md",
    "obj_menuTest": "../systems/debug-and-testing.md",
    "screenshot": "../systems/debug-and-testing.md",
}


def obj_page_cell(name):
    href = OBJ_PAGE.get(name)
    if not href or href == "—":
        return "—"
    return "[%s](%s)" % (PAGE_LABELS.get(href, href), href)


def gen_objects_page(objs):
    groups = {k: [] for k, _t in OBJ_GROUPS_ORDER}
    for o in objs:
        groups[OBJ_GROUP.get(o["name"], "debug")].append(o)

    out = [
        "---",
        "title: Объекты и события",
        "tags:",
        "  - reference",
        "  - objects",
        "  - events",
        "---",
        "",
        "# Объекты и события",
        "",
        "Все объекты проекта Undefinedtale-888 из `objects/`: родитель, persistent-флаг, "
        "спрайт и реализованные события GameMaker.",
        "",
        '!!! info "Генерируемая страница"',
        "    Таблицы собираются скриптом `_meta/gen_reference.py` из `_meta/objects.txt`. "
        "После изменения кода страницу пересобирают, а не правят вручную.",
        "",
        '!!! note "Наследование событий"',
        "    В колонке «События» перечислены только события с кодом в самом объекте; "
        "события родителя наследуются по стандартным правилам GameMaker "
        "(`event_inherited()`).",
        "",
    ]

    for key, title in OBJ_GROUPS_ORDER:
        gobjs = sorted(groups[key], key=lambda o: o["name"].lower())
        if not gobjs:
            continue
        out.append("## " + title)
        out.append("")
        out.append(md_row("Объект", "Родитель", "Persistent", "Спрайт", "События", "Док-страница"))
        out.append(md_row("---", "---", "---", "---", "---", "---"))
        for o in gobjs:
            parent = "`%s`" % o["parent"] if o["parent"] != "-" else "—"
            sprite = "`%s`" % o["sprite"] if o["sprite"] != "-" else "—"
            events = ", ".join(o["events"]) if o["events"] else "—"
            out.append(md_row(
                "`%s`" % o["name"],
                parent,
                "да" if o["persistent"] else "нет",
                sprite,
                events,
                obj_page_cell(o["name"]),
            ))
        out.append("")
        if key == "sys":
            out.append("`o_SharedTweener` — служебный объект библиотеки TweenGMS, "
                       "не игровой код.")
            out.append("")

    out += [
        "## См. также",
        "",
        "- [Справочник GML-скриптов](gml-scripts.md) — функции проекта",
        "- [Иерархия объектов](../architecture/object-hierarchy.md) — роль `par_*` родителей",
        "- [Инициализация](../architecture/initialization.md) — `obj_Init` и стартовая последовательность",
        "",
        "<!-- sources: _meta/objects.txt; objects/*/*.yy; docs_new/_meta/nav_plan.md -->",
        "",
    ]
    return "\n".join(out)


def main():
    files = parse_scripts()
    objs = parse_objects()
    if not files or not objs:
        sys.exit("gen_reference: пустой scripts.txt или objects.txt")

    with open(OUT_SCRIPTS, "w", encoding="utf-8") as fh:
        fh.write(fix_dashes(gen_scripts_page(files)))
    with open(OUT_OBJECTS, "w", encoding="utf-8") as fh:
        fh.write(fix_dashes(gen_objects_page(objs)))

    n_funcs = sum(
        len(f["funcs"]) for f in files
        if not is_library(os.path.basename(os.path.dirname(f["path"])))
    )
    print("gml-scripts.md: %d функций; objects-and-events.md: %d объектов"
          % (n_funcs, len(objs)))


if __name__ == "__main__":
    main()
