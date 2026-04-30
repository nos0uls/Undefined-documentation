# Глобальное Состояние (Global State)

Управление состоянием игры разделено на уровни: **Init-time** (однократная загрузка), **Runtime** (текущая сессия) и **Persistent** (сохраняемые данные).

## Init-time State (`obj_Init`)

Большинство глобальных структур инициализируются один раз в `obj_Init.Create`. Они живут в `global.*` и доступны из любого места кода.

### UI Blocking (`scr_checkUIBlocking`)

В отличие от полноценного UI Stack, блокировка ввода реализована через `scr_checkUIBlocking()`. Это функция, которая проверяет существование ключевых UI-объектов и возвращает `true`, если ввод должен быть заблокирован.

```gml
function scr_checkUIBlocking(exclude_self = false, include_cutscene = true) {
    var ui_objects = [
        textboxTest_scribble,
        obj_settingsManager,
        obj_menu,
        obj_saveManager,
        obj_inGameMenu
    ];
    // ... + global.settings_closing + active_cutscene_id / cutscene_camera_override
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

### Комнаты и сейвы

*   **`global.rooms_by_name`** — `ds_map`, заполняется в цикле `room_first .. room_last`. Позволяет загружать комнаты по строковому имени (`scr_roomFromName`).
*   **`global.__service_menu_rooms`** — массив строк: `["rm_roomMenu", "rm_savesSelect", "rm_settings", "rm_devLoad"]`.
*   **`global.is_menu_room(room)`** — функция. Проверяет, входит ли комната в список service-меню.
*   **`global.__save_slot_metadata_cache`** — структура (`{}`), кэширует x/y/facing/room для `save1..save3` на старте. Убирает дисковый I/O при первом открытии меню выбора.

### Инвентарь и статы

Инициализируются в конце `obj_Init.Create`:

??? note "Переменные инвентаря и статов"
    | Переменная | Тип | Назначение |
    |------------|-----|------------|
    | `global.item[0..7]` | real | Содержимое слотов инвентаря (значения определяются `script_items()`). |
    | `global.item_count` | real | Количество предметов (обновляется `script_items()`). |
    | `global.SetArmor` | real | ID экипированной брони. |
    | `global.SetWeapon` | real | ID экипированного оружия. |
    | `global.max_itemskip` | real | Макс. пропуск предметов. |
    | `global.stat_hp / maxhp / atk / def / lv / gold / xp` | real | Базовые статы персонажа. |
    | `global.stat_prevlv` | real | Предыдущий уровень (для анимации). |
    | `global.name` | string | Имя персонажа (default: `"CHARA"`). |

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

!!! warning "Музыка не здесь"
    `global.play_music()`, `global.play_music_fade()`, `global.play_music_immediate()` и все music-глобалы создаются в `scr_music_init()` (вызывается из `obj_Init`). Актуальные фейды обновляет `obj_music_ctrl.Step` каждый кадр. `obj_globalManager` НЕ управляет музыкой напрямую.

## Persistent State (`game_state.dat`)

Долгосрочные данные, которые должны пережить перезапуск игры, хранятся в структуре `global.game_state` и сериализуются в файл.

### Структура данных
По умолчанию состояние выглядит так (`scr_game_state_default`):
```json
{
    "last_played_save_slot": "save1"
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

Это позволяет сбросить прогресс игры, не теряя настройки управления.

---

## См. также

- [Инициализация](initialization.md) — `obj_Init`, `global.__init_done`
- [Объекты системы](objects.md) — `obj_Init`, `obj_globalManager`, `obj_music_ctrl`
- [Система ввода](../systems/input.md) — `global.input_map`, `global.player_settings`
- [Система музыки](../systems/music.md) — `global.play_music()`
- [Диалоговые портреты](../systems/dialogue-portraits.md) — `global.current_actor`, `global.current_emote`
