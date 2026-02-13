# Архитектура проекта

Обзор структуры и организации проекта UndefinedTale#888 в GameMaker Studio 2.

## Поток запуска

```
rm_init → obj_Init.Create_0 (полная инициализация) → room_goto(rm_roomMenu)
rm_roomMenu → obj_menu.Create_0 (меню) → Alarm_0 (музыка через 1 кадр)
```

### Порядок инициализации

1. **`obj_Init`** (создаётся в `rm_init`) — центральная точка инициализации:
    - `scr_constants()` — глобальные константы (`global.DIR`, `SETTINGS_STATE`)
    - Создаёт `obj_globalManager` (если нет)
    - `scr_loadSettings()` + `scr_applySettings()` — настройки, input_map, debug
    - Загрузка game_state, save slots
    - `ChatterboxLoadFromFile()` — диалоги
    - Ставит `global.__init_done = true`
    - `room_goto(rm_roomMenu)` (только из `rm_init`)

2. **`obj_globalManager`** (persistent) — runtime-менеджер:
    - Fallback-инициализация если `obj_Init` не отработал (DEV-LOAD, F5/F6)
    - Карта комнат (`global.rooms_by_name`)
    - Система уведомлений
    - Музыкальная система (`global.play_music`, `global.play_music_immediate`)
    - Дебаг-флаги
    - UI звуки

3. **`obj_menu`** — главное меню:
    - Опции меню, навигация
    - `Alarm_0` — запуск музыки с задержкой 1 кадр

### Защита от повторной инициализации

`obj_Init` создаётся через `GlobalRoomCreationCode` в каждой комнате, но `global.__init_done` guard предотвращает повторный запуск.

## Системные объекты

| Объект | Persistent | Назначение |
|--------|-----------|------------|
| `obj_Init` | Нет | Центральная инициализация (однократная) |
| `obj_globalManager` | Да | Runtime: музыка, уведомления, комнаты, дебаг |
| `obj_menu` | Нет | Главное меню |
| `obj_settingsManager` | Нет | UI настроек (overlay или отдельная комната) |
| `obj_saveManager` | Нет | Выбор сейв-слота, DEV-LOAD |
| `obj_inGameMenu` | Нет | Внутриигровое меню (INFO/ITEMS/SETTINGS) |
| `obj_player` | Нет | Игрок |
| `obj_actor` | Нет | NPC/актор в катсценах |
| `obj_Init_dialogue` | Нет | Тестовый объект диалогов (клавиши 1/2) |

## Основные скрипты

### Инициализация и настройки

- **`scr_constants`** — глобальные константы (`global.DIR`, `SETTINGS_STATE`)
- **`scr_settingsManager`** — загрузка/сохранение/применение/сброс настроек:
    - `scr_loadSettings()` — читает файл, мигрирует недостающие ключи
    - `scr_saveSettings(settings)` — записывает в файл
    - `scr_applySettings(settings)` — применяет (debug, окно, звук, input_map)
    - `scr_resetSettings()` — сброс к дефолтам
    - `scr_settings_deep_copy(settings)` — глубокая копия struct
    - `scr_settings_apply_and_save(settings)` — применить + сохранить
    - `scr_resetInputToDefault(settings)` — сброс только клавиш
    - `scr_buildInputMap(settings)` — struct действие → массив клавиш

### Input API (`scr_inputApi`)

- **`scr_input_down(action)`** — клавиша зажата (с cutscene-блокировкой)
- **`scr_input_pressed(action)`** — клавиша только что нажата
- **`scr_input_repeater(action, delay, interval)`** — авто-повтор
- **`scr_input_rebind(action, new_key)`** — переназначение клавиши
- **`scr_input_rebind_slot(action, slot, key, [settings])`** — переназначение конкретного слота
- **`__scr_input_is_ui_caller()`** — внутренняя: проверка UI-объекта для bypass катсцены

Во время катсцены (`global.cutscene_active`) ввод блокируется для всех объектов кроме UI (textbox, settings, menu, save, inGameMenu). Не-UI объекты получают ввод только через `__cutscene_virtual_down`.

### Игрок

- **`scr_player_movement`** — движение с коллизиями (4 направления, top-down)
- **`scr_player_animation`** — спрайты по направлению + анимация ходьбы
- **`scr_player_facing`** — синхронизация `facing_direction` из `sprite_index` (через `scr_sprite_to_facing`)
- **`scr_player_marker_update`** — позиция маркера взаимодействия
- **`scr_player_ui_blocking`** — блокировка ввода при открытых UI
- **`scr_player_debug_ghost`** — режим призрака (проход через стены)
- **`scr_player_room_lock`** — блокировка roomchanger после перехода

### Направление ↔ Спрайт (`scr_facing_sprite`)

- **`scr_facing_to_sprite(facing, [chara_sprites])`** — направление → спрайт ходьбы
- **`scr_sprite_to_facing(spr, [chara_sprites])`** — спрайт → направление

Оба принимают опциональный `chara_sprites` struct для кастомных NPC-спрайтов.

### Сохранение / Загрузка

- **`scr_saveLoad`** — сохранение/загрузка позиции и комнаты игрока
- **`scr_game_state_load()`** — загрузка общего состояния игры (last_played_save_slot и т.д.)
- **`scr_global_handle_dev_spawn()`** — создание игрока при DEV-LOAD

### Катсцены

- **`scr_cutscene_classes`** — классы действий катсцены (ActionMoveTo, ActionSetFacing, ActionDialogue и др.)
- **`cutscene_set_facing`** — установка направления актора в катсцене
- **`obj_actor`** — универсальный NPC для катсцен (движение, auto_face, idle-анимации)

## Комнаты

| Комната | Назначение |
|---------|------------|
| `rm_init` | Стартовая комната, только инициализация |
| `rm_roomMenu` | Главное меню |
| `rm_savesSelect` | Выбор сейв-слота |
| `rm_settings` | Настройки (отдельная комната) |
| `rm_devLoad` | DEV-LOAD (выбор комнаты для отладки) |
| `rm_*` | Игровые комнаты |

## Музыкальная система

Определена в `obj_globalManager.Create_0`:

- **`global.play_music(snd_asset)`** — плавная смена трека (фейд-ин/фейд-аут)
- **`global.play_music_immediate(snd_asset)`** — мгновенная смена (без фейда)
- **`global.is_menu_room(room)`** — проверка, является ли комната «меню» (для автоматической музыки)

Громкость управляется через `global.__music_volume` (из настроек).

## Система уведомлений

- **`global.show_notification(text)`** — показывает текст на экране на 1 секунду
- Отрисовка и таймер — в `obj_globalManager`

## Соглашения по именованию

- **Скрипты**: `scr_название` (внутренние: `__scr_название`)
- **Объекты**: `obj_название`
- **Спрайты**: `spr_название`
- **Звуки**: `snd_название`, `music_название`
- **Комнаты**: `rm_название`
- **Шрифты**: `ft_название`
- **Переменные**: `snake_case`, константы в struct (`global.DIR.UP`)
- **Приватные глобальные**: `global.__название` (двойное подчёркивание)
