# GML Скрипты

Справочник основных скриптов и функций проекта UndefinedTale#888.

## Инициализация

### scr_constants

Инициализирует глобальные константы. Вызывается один раз из `obj_Init`.

```gml
scr_constants();
// Результат:
// global.DIR = { RIGHT: 0, LEFT: 1, UP: 2, DOWN: 3 }
// global.SETTINGS_STATE = { ROOT: 0, CATEGORY: 1, REBIND: 2, CONFIRM_RESET: 3 }
```

## Настройки (scr_settingsManager)

### scr_loadSettings

Загружает настройки из файла `player_settings.dat`. Если файл отсутствует или содержит не все ключи — автоматически мигрирует и пересохраняет.

```gml
/// @returns {struct} настройки игрока
var settings = scr_loadSettings();
```

### scr_saveSettings

Записывает настройки в файл. Использует ключи из `global.default_settings` как шаблон.

```gml
/// @param {struct} settings
/// @returns {bool} успех
scr_saveSettings(global.player_settings);
```

### scr_applySettings

Применяет настройки к игре: debug-флаг, режим окна (borderless/windowed), громкость, input_map.

```gml
/// @param {struct} settings
/// @returns {bool} успех
scr_applySettings(global.player_settings);
// Внутри ставит: global.debug, global.input_map, global.__music_volume, global.__sfx_volume
```

### scr_settings_apply_and_save

Комбинация: обновляет `global.player_settings`, применяет и сохраняет.

```gml
/// @param {struct} local_settings
/// @param {string} [mode] — "apply", "save" или "both" (по умолчанию)
scr_settings_apply_and_save(local_settings);
```

### scr_buildInputMap

Собирает struct `действие → [клавиша1, клавиша2]` из настроек.

```gml
/// @param {struct} settings
/// @returns {struct} input_map
global.input_map = scr_buildInputMap(global.player_settings);
// Результат: { up: [vk_up, -1], down: [vk_down, -1], confirm: [ord("Z"), vk_enter], ... }
```

## Input API (scr_inputApi)

### scr_input_down

Возвращает `true`, если клавиша действия зажата. Во время катсцены блокирует ввод для не-UI объектов.

```gml
/// @param {string} action — "up", "down", "left", "right", "confirm", "back", "menu"
if (scr_input_down("right")) { /* клавиша вправо зажата */ }
```

### scr_input_pressed

Возвращает `true` только в кадр нажатия.

```gml
if (scr_input_pressed("confirm")) { /* подтверждение */ }
```

### scr_input_repeater

Авто-повтор: первое нажатие сразу, затем повтор через `delay` мс, далее каждые `interval` мс.

```gml
/// @param {string} action
/// @param {real} [delay] — задержка перед повтором (мс, по умолчанию 200)
/// @param {real} [interval] — интервал повтора (мс, по умолчанию 60)
if (scr_input_repeater("down")) { select_index++; }
```

### scr_input_rebind_slot

Переназначает конкретный слот клавиши. Защищает дефолтные клавиши от перезаписи.

```gml
/// @param {string} action
/// @param {real} slotIndex — 1 (основная) или 2 (альтернативная)
/// @param {real} new_key
/// @param {struct} [target_settings] — по умолчанию global.player_settings
scr_input_rebind_slot("confirm", 1, ord("Z"));
```

## Направление ↔ Спрайт (scr_facing_sprite)

### scr_facing_to_sprite

Возвращает спрайт ходьбы для заданного направления.

```gml
/// @param {real} facing — global.DIR.RIGHT/LEFT/UP/DOWN
/// @param {struct} [chara_sprites] — { right, left, up, down } для кастомных NPC
/// @returns {Asset.GMSprite}
sprite_index = scr_facing_to_sprite(facing_direction);

// С кастомными спрайтами NPC:
sprite_index = scr_facing_to_sprite(dir, actor.chara_sprites);
```

### scr_sprite_to_facing

Обратная функция: спрайт → направление.

```gml
/// @param {Asset.GMSprite} spr
/// @param {struct} [chara_sprites]
/// @returns {real} global.DIR.* или -1
var f = scr_sprite_to_facing(sprite_index);
if (f != -1) facing_direction = f;
```

## Скрипты игрока

### scr_player_movement

Обработка движения игрока (4 направления, top-down) с коллизиями через `obj_collider`.

### scr_player_animation

Обновление спрайтов направления и анимации ходьбы. Не работает во время катсцены.

### scr_player_facing

Синхронизирует `facing_direction` из текущего `sprite_index`. Не работает во время катсцены.

```gml
// Вызывается в obj_player.Step_0
scr_player_facing();
```

### scr_player_ui_blocking

Проверяет, должен ли UI блокировать ввод игрока (открытое меню, диалог и т.д.).

### scr_player_debug_ghost

Режим призрака: проход через стены, включается/выключается в дебаг-режиме.

## Сохранение и загрузка

### scr_game_state_load

Загружает общее состояние игры из `game_state.dat` (последний слот и т.д.).

```gml
global.game_state = scr_game_state_load();
```

### scr_global_handle_dev_spawn

Создаёт игрока в комнате после DEV-LOAD с заданной позицией и направлением.

```gml
// Вызывается из obj_globalManager при global.__dev_spawn == true
scr_global_handle_dev_spawn();
```

## Музыкальная система

Инициализируется на старте через `scr_music_init()` и поддерживается отдельным runtime-контроллером. Подробности см. в `docs/systems/music.md`.

### global.play_music

Плавная смена трека с фейдом (старый трек затухает, новый нарастает).

```gml
global.play_music(music_menu);
```

### global.play_music_immediate

Мгновенная смена трека (без фейда).

```gml
global.play_music_immediate(music_battle);
```

## Утилиты

### global.show_notification

Показывает текстовое уведомление на экране (1 секунда).

```gml
global.show_notification("Settings saved!");
```

### global.is_menu_room

Проверяет, является ли комната «служебной» (меню, настройки, сейвы, devload).

```gml
if (global.is_menu_room(room)) { /* играть music_menu */ }
```

---

## См. также

- [Система ввода](../systems/input.md) — `scr_input_pressed()`, `scr_input_down()`, `scr_input_repeater()`, `scr_buildInputMap()`
- [Глобальное состояние](../architecture/global-state.md) — `global.game_state`, `global.player_settings`, `global.show_notification`, `global.is_menu_room()`
- [Система музыки](../systems/music.md) — `global.play_music()`, `global.play_music_immediate()`, `scr_music_init()`
- [События объектов](events.md) — `Create`, `Step`, `Draw_64`, `GlobalRoomCreationCode`
- [Глобальные функции](functions.md) — точка входа в справочник по функциям
