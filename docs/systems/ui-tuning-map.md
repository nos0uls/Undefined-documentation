---
tags:
  - ui
  - dialogue
  - ui-blocking
---

# Карта тонкой настройки UI, Debug и Dialogue

Быстрый справочник по файлам тонкой настройки интерфейса, диалогов, портретов, debug overlay и маркеров взаимодействия.

!!! tip "Пути в этом документе"
    Все пути указаны относительно корня проекта `Undefinedtale888/`.

## Обзор областей

| Область | Что настраивается | Основной файл |
|---------|-------------------|---------------|
| Textbox | Размер, позиция, wrap текста | `objects/textboxTest_scribble/Draw_64.gml` |
| Portrait | Позиция, масштаб, sprite | `objects/obj_face/Draw_64.gml` |
| Continue marker | Позиция `>` внутри textbox | `objects/textboxTest_scribble/Draw_64.gml` |
| Choices | Расположение option choices | `objects/textboxTest_scribble/Create_0.gml` |
| Interaction marker | Смещение от игрока | `scripts/scr_player_marker_update.gml` |
| Debug overlay | Offsets, scale, проекция | `objects/obj_globalManager/Draw_64.gml` |
| Dialogue entry | Yarn file / node | `scripts/readDialogue.gml` |

## Textbox layout

### `objects/textboxTest_scribble/Draw_64.gml`

Главный файл для визуальной настройки dialogue textbox.

??? note "Полный список переменных"
    | Переменная | Описание |
    |------------|----------|
    | `box_width`, `box_height` | Общие размеры textbox |
    | `box_x`, `box_y` | Положение на GUI |
    | `box_scale_x`, `box_scale_y` | Масштаб `spr_dialogue_box` |
    | `has_portrait` | Выбирает preset: `with_portrait` или `without_portrait` |
    | `active_text_offset_x/y` | Смещение старта текста от центра textbox |
    | `active_text_wrap_width/height` | Область wrap для основного текста |
    | `active_marker_visible` | Рисуется ли `>` marker в текущем preset |
    | `active_marker_offset_x/y` | Позиция `>` marker относительно центра textbox |
    | `active_marker_scale` | Размер `>` marker |
    | `inner_left`, `inner_width`, `inner_right` | Безопасная рабочая область внутри textbox |
    | `inner_top`, `inner_bottom` | Верхняя/нижняя граница безопасной области |
    | `text_padding_*` | Safe padding (left/right/top/bottom) |
    | `text_wrap_width`, `text_wrap_height` | Итоговые значения wrap для Scribble |
    | `text_x`, `text_y` | Итоговая стартовая точка: `box center + offset` |
    | `choice_text_scale` | Размер текста choices для текущего `option_count` |
    | `choice_group_offset_y` | Вертикальный offset группы choices от центра textbox |
    | `choice_wrap_widths` | Wrap-ширины choices после чтения preset |
    | `choice_slot_x`, `choice_slot_y` | Позиции choice slots после чтения preset |

#### Layout zones

Вся схема строится вокруг одного anchor:

- `box_x`, `box_y` — центр textbox, anchor всей схемы
- `text_offset_x_*`, `text_offset_y_*` — старт текста относительно центра
- `text_wrap_width_*`, `text_wrap_height_*` — размер текстовой зоны явно
- `marker_offset_x_*`, `marker_offset_y_*` — позиция continue marker как отдельная точка
- `portrait_offset_x_*`, `portrait_offset_y_*` — позиция portrait относительно того же центра
- `text_padding_*` — safe bounds для внутренней области и choices
- `choice_text_scale_*`, `choice_group_offset_y_*` — presets для choices по количеству опций
- `choice_wrap_width_ratio_*`, `choice_slot_x_*`, `choice_slot_y_*` — wrap и координаты slots для `1/2/3/4` вариантов

!!! info "Про marker внутри textbox"
    Текст не сдвигается автоматически от portrait — он берёт свой явный `text_offset_*`. Автосвязки `portrait margin → text column` не существует.

## Layout presets

### `objects/textboxTest_scribble/Create_0.gml`

Единая точка хранения preset-переменных.

??? note "Полный список preset-переменных"
    | Preset | Переменные | Назначение |
    |--------|-----------|------------|
    | with_portrait | `text_offset_x/y_with_portrait` | Старт текста |
    | | `text_wrap_width/height_with_portrait` | Размер текстовой зоны |
    | | `marker_visible/offset_x/y_with_portrait` | Настройки `>` marker |
    | | `portrait_offset_x/y/scale_with_portrait` | Настройки portrait |
    | without_portrait | `text_offset_x/y_without_portrait` | Старт текста (без portrait) |
    | | `text_wrap_width/height_without_portrait` | Размер текстовой зоны |
    | | `marker_visible/offset_x/y_without_portrait` | Настройки `>` marker |
    | | `portrait_offset_x/y/scale_without_portrait` | Симметричный набор |
    | choices 1..4 | `choice_text_scale_1..4` | Размер текста choices |
    | | `choice_group_offset_y_1..4` | Вертикальная посадка |
    | | `choice_wrap_width_ratio_*` | Wrap-ширины |
    | | `choice_slot_x/y_*` | Координаты slots |

!!! warning "Владение данными"
    `textboxTest_scribble` владеет **всеми** preset-переменными. `obj_face/Draw_64.gml` только читает `portrait_offset_*` и `portrait_scale_*`.

## Portrait draw

### `objects/obj_face/Draw_64.gml`

??? note "Переменные portrait draw"
    | Переменная | Описание |
    |------------|----------|
    | `_offset_x`, `_offset_y` | Позиция portrait относительно центра textbox |
    | `_scale` | Масштаб portrait для активного preset |
    | `_x`, `_y` | Итоговая позиция: `box center + portrait offset` |
    | `draw_sprite_ext(...)` | Фактическая отрисовка с масштабом |

!!! tip "Portrait 'летает'?"
    Если portrait позиционируется не внутри textbox — проверяй этот файл первым делом.

### `objects/obj_face/Step_0.gml`

Runtime-логика выбора portrait sprite.

- Валиден ли portrait (`mouth_closed`)
- Какой кадр: `mouth_closed` или `mouth_open`
- Когда portrait скрывается полностью

### `objects/textboxTest_scribble/Create_0.gml`

Создание и инициализация portrait/runtime.

??? note "Компоненты инициализации"
    | Компонент | Описание |
    |-----------|----------|
    | `obj_face` | Создаётся, если renderer ещё не существует |
    | `scribble_typist` | Настройка typist для текста |
    | `typist.function_per_char(...)` | Callback на каждый символ |
    | `mouth_open_prev`, `mouth_closed_prev`, `sound_prev` | Инициализация состояния |
    | `talk_hold_timer`, `talk_hold_frames`, `talk_open_now` | Таймеры анимации рта |

**Фильтр символов для talk animation:** `.` `!` `?` `:` `;` `…` `-` `—` не открывают рот. Запятая остаётся активной.

### `objects/textboxTest_scribble/Step_0.gml`

Главный runtime-файл portrait state.

| Функция | Назначение |
|---------|------------|
| `apply_current_dialogue_state()` | Обновление actor/emotion/sprite/sound |
| `update_talk_animation_state()` | Логика открытия/закрытия рта |
| `global.current_actor/emote/sprite` | Синхронизация глобального состояния |

## Dialogue entry

### `scripts/readDialogue/readDialogue.gml`

Создаёт `textboxTest_scribble` при обычном взаимодействии.

??? note "Параметры создания"
    | Переменная | Описание |
    |------------|----------|
    | `dialogue_x`, `dialogue_y` | Позиция instance textbox при создании |
    | `instance_create_depth(..., textboxTest_scribble)` | Точка создания dialogue controller |

!!! info "Не GUI layout"
    Это входная точка для понимания, **откуда** стартует диалог, а не основной GUI layout.

## Actor/emotion mapping

### `scripts/scr_parse_emote/scr_parse_emote.gml`

Нормализация actor/emotion и fallback-логика: narrator fallback, default emotion, previous emotion, итоговый выбор ключа.

### `scripts/map_emotions/map_emotions.gml`

Таблица actor/emotion → ресурсы portrait/sound.

| Ресурс | Описание |
|--------|----------|
| `mouth_closed` | Sprite для закрытого рта |
| `mouth_open` | Sprite для открытого рта |
| `sound` | Voice sound для actor/emotion |

!!! tip "Не тот portrait?"
    Если диалог парсится правильно, но показывается не тот portrait — проблема обычно здесь.

## Interaction marker

### `scripts/scr_player_marker_update/scr_player_marker_update.gml`

Главный файл для offset interaction marker относительно игрока.

| Переменная | Описание |
|------------|----------|
| `pointX`, `pointY` | Позиция marker |
| offsets для `RIGHT/LEFT/UP/DOWN` | Индивидуальные смещения по направлениям |

### `objects/obj_player/Create_0.gml`

Создаётся постоянный instance marker: `marker_id = instance_create_depth(x, y, -infinity, obj_pointMarker);`

### `objects/obj_pointMarker/Create_0.gml`

| Свойство | Описание |
|----------|----------|
| `visible = false` | Marker невидимый |
| Логическая точка | Используется для detection взаимодействия |
| Debug-отрисовка | Отдельно через F3 |

### `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml`

Проверка взаимодействия через marker.

- Проверка существования `obj_pointMarker`
- `place_meeting(...)` или `point_in_rectangle(...)`
- Вызов `readDialogue(_scriptToReadFrom, _node)`

## Debug overlay

### `objects/obj_globalManager/Draw_64.gml`

??? note "Компоненты debug overlay"
    | Компонент | Описание |
    |-----------|----------|
    | `draw_debug_collider(...)` | Проекция world collider в GUI overlay |
    | `_camx`, `_camy`, `_s`, `_ox`, `_oy` | Параметры пересчёта позиции и масштаба |
    | F1 overlay | Информация о позиции и направлении |
    | F2 collider overlay | Коллайдеры |
    | F3 interaction marker | Debug draw marker |

!!! tip "Debug смещён?"
    Если debug rectangle не совпадает с объектом — смотри сюда первым делом.

### `objects/obj_Init/Create_0.gml`

Базовая инициализация debug flags:

- `global.debug_show_info`
- `global.debug_show_colliders`
- `global.debug_show_hitbox`
- `global.debug_show_music`

### `objects/obj_player/Create_0.gml`

Локальная синхронизация player-side debug flags:

- `debug_show_info`
- `debug_show_colliders`
- `debug_show_hitbox`

### `scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml`

| Горячая клавиша | Флаг |
|-----------------|------|
| F1 | `debug_show_info` |
| F2 | `debug_show_colliders` |
| F3 | marker debug |

## Dialogue entry points

| Объект | Yarn file | Node |
|--------|-----------|------|
| `objects/obj_asher/Step_0.gml` | `testDialogue.yarn` | `Bench` |
| `objects/obj_bench/Step_0.gml` | — | — |
| `objects/obj_sheepFountain/Step_0.gml` | — | — |

## Быстрый маршрут по задачам

| Задача | Куда смотреть |
|--------|---------------|
| Подвинуть portrait | `obj_face/Draw_64.gml`, `textboxTest_scribble/Draw_64.gml` |
| Изменить wrap текста | `textboxTest_scribble/Draw_64.gml` |
| Скрыть/сдвинуть `>` marker | `textboxTest_scribble/Draw_64.gml` |
| Изменить interaction marker | `scr_player_marker_update.gml` |
| Починить F2/F3 debug overlay | `obj_globalManager/Draw_64.gml`, `scr_global_debug_hotkeys.gml`, `obj_Init/Create_0.gml` |

## См. также

- [Диалоговые портреты](dialogue-portraits.md)
- [Система взаимодействия](interaction.md)
- [Система ввода](input.md)
