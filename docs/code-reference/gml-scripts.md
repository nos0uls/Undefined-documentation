---
tags:
  - code-reference
  - scripts
---

# GML Скрипты

Справочник функций и скриптов проекта **Undefinedtale-888**.

## Инициализация

### scr_constants

Инициализирует глобальные константы. Вызывается один раз из `obj_Init`.

```gml title="scripts/scr_constants/scr_constants.gml"
scr_constants();
// Результат:
// global.DIR = { RIGHT: 0, LEFT: 1, UP: 2, DOWN: 3 }
// global.SETTINGS_STATE = { ROOT: 0, CATEGORY: 1, REBIND: 2, CONFIRM_RESET: 3 }
```

## Настройки (scr_settingsManager)

### scr_loadSettings

Загружает настройки из файла `player_settings.dat`. Если файл отсутствует или содержит не все ключи — автоматически мигрирует и пересохраняет.

```gml title="scripts/scr_settingsManager/scr_settingsManager.gml"
/// @returns {struct} настройки игрока
var settings = scr_loadSettings();
```

### scr_saveSettings

Записывает настройки в файл. Использует ключи из `global.default_settings` как шаблон.

```gml title="scripts/scr_settingsManager/scr_settingsManager.gml"
/// @param {struct} settings
/// @returns {bool} успех
scr_saveSettings(global.player_settings);
```

### scr_applySettings

Применяет настройки к игре: debug-флаг, режим окна (borderless/windowed), громкость, input_map.

```gml title="scripts/scr_settingsManager/scr_settingsManager.gml"
/// @param {struct} settings
/// @returns {bool} успех
scr_applySettings(global.player_settings);
// (1)!
```

1. Внутри ставит: `global.debug`, `global.input_map`, `global.__music_volume`, `global.__sfx_volume`

### scr_settings_apply_and_save

Комбинация: обновляет `global.player_settings`, применяет и сохраняет.

```gml
/// @param {struct} local_settings
/// @param {string} [mode] — "apply", "save" или "both" (по умолчанию)
scr_settings_apply_and_save(local_settings); // (1)!
```

1. Сначала обновляет `global.player_settings` из `local_settings`, затем вызывает `scr_applySettings()` и `scr_saveSettings()`

### scr_buildInputMap

Собирает struct `действие → [клавиша1, клавиша2]` из настроек.

```gml
/// @param {struct} settings
/// @returns {struct} input_map
global.input_map = scr_buildInputMap(global.player_settings); // (1)!
```

1. Результат: `{ up: [vk_up, -1], down: [vk_down, -1], confirm: [ord("Z"), vk_enter], ... }` — каждому действию сопоставлен массив из двух клавиш.

## Input API (scr_inputApi)

### scr_input_down

Возвращает `true`, если клавиша действия зажата. Во время катсцены блокирует ввод для не-UI объектов.

```gml
/// @param {string} action — "up", "down", "left", "right", "confirm", "back", "menu", "delete"
if (scr_input_down("right")) { /* клавиша вправо зажата */ }
```

### scr_input_pressed

Возвращает `true` только в кадр нажатия.

```gml
if (scr_input_pressed("confirm")) { /* подтверждение */ }
```

## Коллизия

### scr_collision_resolve

Разрешает коллизию движения с тремя группами solid-объектов: `obj_collider`, `par_decor`, `par_interactable`. Заменяет устаревший `collision(obj_collider)`.

```gml
// Внутри scr_player_movement
scr_collision_resolve();
x += xspd;
y += yspd;
```

Используется при:
- обычном движении игрока
- скольжении вдоль стены (facing update)
- спавн-проверке (выталкивание при застревании)
- `scr_global_transition_safety` (защита при смене комнаты)

### scr_input_repeater

Авто-повтор: первое нажатие сразу, затем повтор через `delay` мс, далее каждые `interval` мс.

```gml
/// @param {string} action
/// @param {real} [delay] — задержка перед повтором (мс, по умолчанию 200)
/// @param {real} [interval] — интервал повтора (мс, по умолчанию 120)
if (scr_input_repeater("down")) { select_index++; }
```

### scr_input_rebind_slot

Переназначает конкретный слот (1 или 2) для действия. Защищает дефолтные клавиши от конфликтной перезаписи (swap-логика).

```gml
/// @param {string} action
/// @param {real} slotIndex — 1 или 2 (слот для записи)
/// @param {real} new_key
/// @param {struct} [target_settings] — по умолчанию global.player_settings
scr_input_rebind_slot("confirm", 1, ord("Z")); // (1)!
```

1. Защищает дефолтные клавиши от перезаписи — вернёт `false`, если попытка забрать дефолтную клавишу из её места. Если клавиша найдена в другом слоте, она освобождается (ставится дефолт для того слота). Записывает в выбранный слот (`slotIndex`).

## Направление ↔ Спрайт (scr_player_facing)

### scr_sprite_for_facing

Возвращает спрайт ходьбы для заданного направления.

```gml
/// @param {real} facing — global.DIR.RIGHT/LEFT/UP/DOWN
/// @returns {Asset.GMSprite}
sprite_index = scr_sprite_for_facing(facing_direction); // (1)!
```

1. Использует стандартную таблицу спрайтов игрока (`spr_Chara_walking_R/L/D/U`).

### scr_facing_for_sprite

Обратная функция: спрайт → направление.

```gml
/// @param {Asset.GMSprite} spr
/// @returns {real} global.DIR.*
facing_direction = scr_facing_for_sprite(sprite_index); // (1)!
```

1. Возвращает направление по текущему спрайту игрока — вызывается каждый кадр в `obj_player.Step` для синхронизации.

## Скрипты игрока

### scr_player_movement

Обработка движения игрока (4 направления, top-down) с коллизиями через `obj_collider`.

### scr_player_animation

Обновление спрайтов направления и анимации ходьбы. Не работает во время катсцены.

```gml
/// @param {bool} ui_blocking — если true, спрайт не меняется и анимация останавливается
/// @param {struct} movement_inputs — структура {up, down, left, right} из `scr_player_movement`
scr_player_animation(ui_blocking, movement_inputs);
```

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

### scr_player_process_mutually_exclusive_inputs

Обрабатывает взаимоисключающие клавиши движения (up/down, left/right). При одновременном нажатии противоположных клавиш использует приоритет последней нажатой.

```gml
/// @param {bool} up — нажата клавиша вверх
/// @param {bool} down — нажата клавиша вниз
/// @param {bool} left — нажата клавиша влево
/// @param {bool} right — нажата клавиша вправо
/// @return {struct} структура с полями up, down, left, right (bool)
var anim_inputs = scr_player_process_mutually_exclusive_inputs(up_key, down_key, left_key, right_key);
```

### scr_player_marker_update

Обновляет позицию маркера взаимодействия (`obj_pointMarker`) в зависимости от направления взгляда игрока.

```gml
/// @function scr_player_marker_update()
scr_player_marker_update();
```

## Input Rebind

### scr_input_rebind

Переназначает клавишу: удаляет её из всех действий, затем записывает в основной слот (slot 1) указанного действия. Для `"menu"` автоматически назначает `vk_escape` на slot 2.

```gml
/// @param {string} action
/// @param {real} new_key
scr_input_rebind("confirm", ord("X"));
```

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

## Система сохранений

| Скрипт | Описание |
|--------|----------|
| `scr_saveLoad` | Загружает текущий save-слот: позицию, комнату, инвентарь, флаги, plot, entity state. |
| `scr_saveSave` | Сохраняет текущее состояние в слот `global.current_save_slot`. |
| `scr_defaultLoad` | Устанавливает стартовую позицию и переходит в начальную комнату. |
| `scr_resetGameToDefault` | Удаляет все сейвы, настройки и `game_state.dat`, сбрасывает глобалы и закрывает игру. |
| `scr_global_quick_save` | Быстрое сохранение в текущий слот (F7). |

## Переходы между комнатами

| Скрипт | Описание |
|--------|----------|
| `scr_room_fade_update` | Обновляет fade-переход в `obj_changingRoomsController`. |
| `scr_global_transition_safety` | Выталкивает игрока из коллайдеров после перехода и снимает ghost mode. |
| `scr_global_on_room_change` | Сбрасывает уведомления, переключает музыку, включает защитный ghost mode. |
| `scr_get_next_game_room` | Возвращает следующую/предыдущую игровую комнату, пропуская служебные. |

## Emote-система

| Скрипт | Описание |
|--------|----------|
| `scr_emote_show` | Обёртка для показа эмоции над объектом. |
| `scr_emote_hide` | Обёртка для скрытия эмоций (для цели или всех). |
| `scr_parse_emote` | Парсит speaker-строку Yarn в структуру actor/emotion/display_name. |

## Инвентарь

| Скрипт | Описание |
|--------|----------|
| `scr_inventory_init` | Создаёт 8-слотовый `global.inventory` и стартовую экипировку. |
| `constructorsForInventory` | Конструкторы `Item`, `WeaponItem`, `ArmorItem`, `FoodItem` и сериализация. |
| `script_items` | Фабрика `item_database` и регистрация кастомных предметов. |

## NPC и диалоги

| Скрипт | Описание |
|--------|----------|
| `scr_interaction` | Единая точка входа взаимодействия с объектами и NPC. |
| `interactionWithNPCsOrObjects` | Legacy-обёртка над `scr_interaction` (bbox). |
| `interactionWithMainCast` | Legacy-обёртка над `scr_interaction` (mask). |
| `scr_npc_pick_dialogue` | Заглушка. В текущей версии не используется. |
| `readDialogue` | Создаёт текстбокс и запускает Yarn-диалог. |

## Entity State

| Скрипт | Описание |
|--------|----------|
| `scr_entity_state` | Работа с `global.entity_state` — сохранение и восстановление состояния сущностей. |

---

## См. также

- [Система ввода](../systems/input.md) — `scr_input_pressed()`, `scr_input_down()`, `scr_input_repeater()`, `scr_buildInputMap()`
- [Система сохранений](../systems/save-system.md) — `scr_saveLoad`, `scr_saveSave`
- [Система эмоций](../systems/emote.md) — `scr_emote_show`, `scr_parse_emote`
- [Инвентарь](../systems/inventory.md) — `scr_inventory_init`, `constructorsForInventory`
- [NPC и диалоги](../systems/npc-dialogue.md) — `scr_interaction`, `readDialogue`
- [Переходы между комнатами](../systems/room-transitions.md) — `scr_room_fade_update`, `scr_global_on_room_change`
- [Debug-инструменты](../systems/debug-tools.md) — `scr_global_debug_hotkeys`, `scr_player_debug_ghost`
- [Глобальное состояние](../architecture/global-state.md) — `global.game_state`, `global.player_settings`, `global.show_notification`, `global.is_menu_room()`
- [Система музыки](../systems/music.md) — `global.play_music()`, `global.play_music_immediate()`, `scr_music_init()`
- [События объектов](events.md) — `Create`, `Step`, `Draw_64`, `GlobalRoomCreationCode`
- [Глобальные функции](functions.md) — точка входа в справочник по функциям
