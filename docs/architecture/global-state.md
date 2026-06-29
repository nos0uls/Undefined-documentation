---
tags:
  - runtime
  - persistent-objects
---

# Глобальное Состояние (Global State)

Система управления данными: **Init-time** (холодный старт), **Runtime** (текущая сессия) и **Persistent** (сохранения).

## Init-time State (`obj_Init`)

Глобальные структуры инициализируются в `obj_Init.Create`. Все переменные `global.*` доступны глобально.

### UI Blocking (`scr_checkUIBlocking`)

В отличие от полноценного UI Stack, блокировка ввода реализована через `scr_checkUIBlocking()`. Это функция, которая проверяет существование ключевых UI-объектов и возвращает `true`, если ввод должен быть заблокирован.

```gml
function scr_checkUIBlocking(exclude_self = false, include_cutscene = true) {
    var ui_objects = [
        textboxTest_scribble,
        obj_settingsManager,
        obj_menu,
        obj_saveManager,
        obj_inGameMenu,
        obj_p3r_title,
        obj_p3r_pause,
        obj_p3r_settings
    ];
    // ... + global.settings_closing + active_cutscene_id / cutscene_camera_override
    // ... + obj_sound_test (is_open check)
}
```

| Источник блокировки | Условие |
|---------------------|---------|
| `global.settings_closing` | Меню настроек закрывается |
| `global.active_cutscene_id != ""` | Идёт катсцена |
| `global.cutscene_camera_override == true` | Камера захвачена катсценой |
| `instance_exists(textboxTest_scribble)` | Открыт диалог |
| `instance_exists(obj_settingsManager)` | Открыты настройки |
| `instance_exists(obj_menu)` | Открыто главное меню |
| `instance_exists(obj_saveManager)` | Открыт экран сейвов |
| `instance_exists(obj_inGameMenu)` | Открыто in-game меню |
| `instance_exists(obj_p3r_title)` | Открыт P3R title |
| `instance_exists(obj_p3r_pause)` | Открыт P3R pause |
| `instance_exists(obj_p3r_settings)` | Открыты P3R settings |
| `instance_exists(obj_sound_test)` + `is_open` | Открыт GUI теста звука |

### Комнаты и сейвы

*   **`global.rooms_by_name`** — `ds_map`, заполняется в цикле `room_first .. room_last`. Загружает комнаты по строковому имени (`scr_roomFromName`).
*   **`global.__service_menu_rooms`** — массив строк: `["rm_roomMenu", "rm_savesSelect", "rm_settings", "rm_devLoad"]`.
*   **`global.is_menu_room(room)`** — функция. Проверяет, входит ли комната в список service-меню.
*   **`global.__save_slot_metadata_cache`** — структура (`{}`), кэширует x/y/facing/room для `save1..save3` на старте. Убирает дисковый I/O при первом открытии меню выбора.

### Инвентарь и статы

Инициализируются в конце `obj_Init.Create` через `scr_inventory_init`:

??? note "Переменные инвентаря и статов"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.inventory` | array | Массив из 8 слотов предметов. `undefined` означает пустой слот. |
    | `global.equipped_weapon` | struct | Ссылка на экипированный `WeaponItem` из `global.inventory`. |
    | `global.equipped_armor` | struct | Ссылка на экипированный `ArmorItem` из `global.inventory`. |
    | `global.stat_hp / maxhp / atk / def / lv / gold / xp` | real | Базовые статы персонажа. |
    | `global.stat_prevlv` | real | Предыдущий уровень (для анимации). |
    | `global.name` | string | Имя персонажа (default: `"CHARA"`). |

### Emote-система

??? note "Переменные emote-системы"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.global_emote_system` | struct | Объект-контейнер с полем `active_emotes` — массивом активных эмоций. |
    | `global.global_emote_system.active_emotes` | array | Список структур эмоций с полями `target`, `sprite`, `frames_left`, `offset_x`, `offset_y`. |

### Debug-флаги

??? note "Переменные debug-режима"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.debug` | bool | Глобальный флаг debug-режима. Включается через F12 x5 или настройки. |
    | `global.debug_show_info` | bool | Overlay FPS, координат, имени комнаты (F1). |
    | `global.debug_show_colliders` | bool | Отрисовка коллайдеров (F2). |
    | `global.debug_show_hitbox` | bool | Отрисовка хитбокса игрока и маркера (F3). |
    | `global.debug_show_music` | bool | Overlay музыкальной отладки (F9). |
    | `global.__debug_activation_count` | real | Счётчик нажатий F12 для активации debug. |
    | `global.__debug_activation_timer` | real | Таймер 2 секунд для серии нажатий F12. |

### Сюжет и прогресс

??? note "Переменные сюжета и состояния мира"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.flag` | struct | Произвольные флаги сюжета (устанавливаются через `ActionSetFlag`). |
    | `global.plot` | real | Числовый прогресс сюжета (устанавливается через `ActionSetPlot`). |
    | `global.entity_state` | struct | Реестр состояния NPC, дверей, сундуков по ключу `"room_name:entity_id"`. Сериализуется в save-файл. |
    | `global.room_flags` | struct | Пост-катсценные изменения мира: ключ — имя комнаты, значение — список объектов. |

### Диалог Face-система

??? note "Переменные face-системы"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.current_actor` | instance | Кто говорит в данный момент (default: `obj_player`). |
    | `global.current_emote` | string | Текущий эмоут для портрета (default: `"default"`). |
    | `global.is_talking` | real | Флаг активного диалога. |
    | `global.talk_index` | real | Индекс текущей реплики. |
    | `global.current_sprite` | sprite | Текущий спрайт портрета. |
    | `global.current_voice` | sound | Звук голоса (default: `snd_text_ch1`). |
    | `global.voice_speed` | real | Скорость голоса (default: `1`). |

### Камера

??? note "Переменные камеры"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.camera_x` | real | X-координата viewport (обновляется каждый кадр в `obj_globalManager.Step_2`). |
    | `global.camera_y` | real | Y-координата viewport. |
    | `global.camera_w` | real | Ширина viewport. |
    | `global.camera_h` | real | Высота viewport. |

### DEV-LOAD и спаун

??? note "Переменные спавна и переходов"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.__dev_spawn` | bool | Флаг: нужно ли телепортировать игрока при входе в комнату. |
    | `global.__dev_spawn_x/y` | real | Координаты DEV-LOAD. |
    | `global.__dev_spawn_facing` | real | Направление DEV-LOAD (default: `global.DIR.UP`). |
    | `global.obj_player` | instance | Ссылка на текущий объект игрока (`noone`, пока не создан). |
    | `global.__next_spawn_x/y` | undefined | Принудительные координаты спавна (из сейвов/переходов). |
    | `global.__next_spawn_facing` | undefined | Принудительное направление спавна. |
    | `global.__transition_safety_frames` | real | Таймер безопасности после перехода между комнатами (default: `0`). |

### Уведомления

```gml
global.show_notification = function(_text) {
    with (obj_globalManager) {
        notification_active = true;
        notification_text = _text;
        notification_timer = notification_duration;
    }
}
```

Определяется в `obj_Init.Create`, но рисуется в `obj_globalManager.Draw_64`.

## Runtime State (`obj_globalManager`)

`obj_globalManager` — runtime-менеджер. Он не инициализирует глобалы (это делает `obj_Init`), но держит локальное состояние и обрабатывает события каждый кадр.

### Ответственность
*   **Смена комнат**: `current_room` + `scr_global_on_room_change()`.
*   **Debug**: `scr_debug_activation_check()`, `scr_global_debug_hotkeys()`, F7 quick-save.
*   **Уведомления**: `notification_active`, `notification_text`, `notification_timer`, `notification_duration`.
*   **DEV-LOAD**: `scr_global_handle_dev_spawn()`.
*   **Катсцены runtime**: `cutscene_runtime_tweens`, `emotes`, `shakes`, `spins`, `jumps`, `fade`.
*   **Меню**: `scr_global_reset_settings_flag()`, `scr_callMenuInit()`.
*   **Полноэкранный режим**: `scr_global_toggle_fullscreen()` (клавиша Q).
*   **Безопасность перехода**: `scr_global_transition_safety()`.

### Состояние переходов между комнатами

| Переменная | Тип | Назначение |
|------------|-----|------------|
| `global.__transition_safety_frames` | real | Таймер безопасности после перехода (16 кадров). |
| `global.__service_menu_rooms` | array | Список служебных комнат, исключаемых из игровых переходов. |
| `global.is_menu_room(room)` | function | Проверяет, относится ли комната к служебным. |
| `global.__next_spawn_x/y/facing` | undefined | Принудительные координаты и направление спавна после загрузки или перехода. |

### Save slot metadata

| Переменная | Тип | Назначение |
|------------|-----|------------|
| `global.__save_slot_names` | array | `["save1", "save2", "save3"]`. |
| `global.__save_slot_metadata_cache` | struct | Кэш `x`, `y`, `facing`, `room`, `playtime`, `exists` для каждого слота. Читается один раз на старте. |
| `global.current_save_slot` | string | Текущий активный слот. |
| `global.last_played_save_slot` | string | Последний использованный слот (из `game_state.dat`). |

!!! warning "Музыка не здесь"
    `global.play_music()`, `global.play_music_fade()`, `global.play_music_immediate()` и все music-глобалы создаются в `scr_music_init()` (вызывается из `obj_Init`). Актуальные фейды обновляет `obj_music_ctrl.Step` каждый кадр. `obj_globalManager` НЕ управляет музыкой напрямую.

## Persistent State (`game_state.dat`)

Долгосрочные данные, которые должны пережить перезапуск игры, хранятся в структуре `global.game_state` и сериализуются в файл.

### Структура данных
По умолчанию состояние выглядит так (`scr_game_state_default`):
```json
{
    "last_played_save_slot": "save1",
    "total_playtime_seconds": 0
}
```

### API
Работа с состоянием ведется через скрипты `scr_game_state_*`:

| Функция | Описание |
|---------|----------|
| `scr_game_state_default()` | Возвращает структуру по умолчанию. |
| `scr_game_state_load()` | Читает `game_state.dat` (формат `key=value`, `\n`-разделённые строки). При отсутствии файла — возвращает default. |
| `scr_game_state_save(state)` | Записывает структуру в файл. |

!!! warning "Отличие от Save File"
    `game_state.dat` — это мета-данные **игры** (какой слот последний).
    Прогресс игрока (уровень, инвентарь, координаты) хранится в отдельных файлах слотов (`save1.txt`, `save2.txt`, `save3.txt`).

## Настройки Игрока (`player_settings.dat`)

Настройки управления, звука и графики вынесены в отдельную структуру `global.player_settings`.

| Функция | Описание |
|---------|----------|
| `scr_loadSettings()` | Читает `player_settings.dat`. |
| `scr_applySettings(settings)` | Применяет: разрешение, полноэкранный/безрамочный режим, громкость. Также активирует `global.debug` если `settings.debug_enabled == true`. |
| `scr_saveSettings(settings)` | Записывает настройки на диск. |
| `scr_settings_deep_copy(settings)` | Глубокая копия для локального редактирования в меню настроек. |

Так можно сбросить прогресс игры, не теряя настройки управления.

---

## См. также

- [Инициализация](initialization.md) — `obj_Init`, `global.__init_done`
- [Объекты системы](objects.md) — `obj_Init`, `obj_globalManager`, `obj_music_ctrl`
- [Система ввода](../systems/input.md) — `global.input_map`, `global.player_settings`
- [Система музыки](../systems/music.md) — `global.play_music()`
- [Диалоговые портреты](../systems/dialogue-portraits.md) — `global.current_actor`, `global.current_emote`
