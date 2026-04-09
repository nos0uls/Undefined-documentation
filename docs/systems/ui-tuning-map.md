# Карта тонкой настройки UI, debug и dialogue

Эта страница нужна как быстрый справочник по местам, где лежит **тонкая настройка** интерфейса, диалогов, портретов, debug overlay и маркеров взаимодействия в проекте `Undefinedtale888`.

Все пути ниже указаны **относительно корня проекта `Undefinedtale888/`**.

## Что считать "тонкой настройкой"

Под этим здесь понимаются места, где меняются:

- размеры и позиция textbox
- внутренние margins и wrap текста
- позиция и размер portrait
- позиция `>` marker внутри textbox
- расположение option choices
- смещение interaction marker
- debug overlay offsets, scale и draw-проекция
- выбор dialogue file / node для конкретного interactable

## 1. Textbox layout и текст

### `objects/textboxTest_scribble/Draw_64.gml`
Главный файл для визуальной настройки dialogue textbox.

Здесь находятся:

- `box_width`
  - общая ширина textbox
- `box_height`
  - общая высота textbox
- `box_x`, `box_y`
  - положение textbox на GUI
- `box_scale_x`, `box_scale_y`
  - масштаб `spr_dialogue_box`
- `has_portrait`
  - выбирает активный preset: `with_portrait` или `without_portrait`
- `active_text_offset_x`, `active_text_offset_y`
  - смещение стартовой точки текста относительно центра textbox
- `active_text_wrap_width`, `active_text_wrap_height`
  - явная область wrap для основного текста
- `active_marker_visible`
  - решает, рисуется ли `>` marker в текущем preset
- `active_marker_offset_x`, `active_marker_offset_y`
  - позиция `>` marker относительно центра textbox
- `active_marker_scale`
  - размер `>` marker
- `inner_left`, `inner_width`
  - рабочая область choices и безопасная ширина внутри textbox
- `inner_right`
  - правая граница безопасной внутренней области
- `inner_top`, `inner_bottom`
  - верхняя и нижняя границы безопасной внутренней области
- `text_padding_left`
  - левый safe padding textbox
- `text_padding_right`
  - правый safe padding textbox
- `text_padding_top`
  - верхний safe padding textbox
- `text_padding_bottom`
  - нижний safe padding textbox
- `text_wrap_width`, `text_wrap_height`
  - итоговые значения wrap, которые передаются в Scribble
- `text_x`, `text_y`
  - итоговая стартовая точка текста: `box center + offset`
- `var _marker = scribble(">")`
  - сам continue marker внутри textbox
- `_marker.draw(...)`
  - точная позиция continue marker: `box center + marker offset`
- `textScribble.draw(...)`
  - точная позиция текста: `box center + text offset`
- `choice_text_scale`
  - активный размер текста choices для текущего `option_count`
- `choice_group_offset_y`
  - вертикальный offset всей группы choices от центра textbox
- `choice_wrap_widths`
  - активные wrap-ширины choices после чтения preset
- `choice_slot_x`, `choice_slot_y`
  - активные позиции choice slots после чтения preset

### Layout zones: как теперь мыслить настройку

- `box_x`, `box_y`
  - это anchor всей layout-схемы, то есть центр textbox
- `text_offset_x_*`, `text_offset_y_*`
  - ставят старт текста относительно центра textbox
- `text_wrap_width_*`, `text_wrap_height_*`
  - задают размер текстовой зоны явно, без автозависимости от portrait
- `marker_offset_x_*`, `marker_offset_y_*`
  - ставят continue marker как отдельную точку внутри textbox
- `portrait_offset_x_*`, `portrait_offset_y_*`
  - ставят portrait относительно того же центра textbox
- `text_padding_*`
  - остаются safe bounds для внутренней области textbox и choice layout
- `choice_text_scale_*`, `choice_group_offset_y_*`
  - задают отдельный layout preset для choices по количеству опций
- `choice_wrap_width_ratio_*`, `choice_slot_x_*`, `choice_slot_y_*`
  - задают ширину wrap и координаты каждого choice slot для `1/2/3/4` вариантов

### Важно про marker внутри textbox
Сейчас именно здесь живёт `>` marker продолжения.

Если нужно менять marker, логично менять именно этот файл:

- либо скрывать `>` marker в нужном preset
- либо переносить marker в другую точку
- либо менять его scale отдельно от текста

В текущей реализации правило уже такое:

- текст не сдвигается автоматически от portrait, а берёт свой явный `text_offset_*`

## 2. Старт dialogue окна

### `scripts/readDialogue/readDialogue.gml`
Файл, который создаёт `textboxTest_scribble` при обычном взаимодействии.

Здесь лежат:

- `dialogue_x`
  - X-позиция instance textbox при создании
- `dialogue_y`
  - Y-позиция instance textbox при создании
- `instance_create_depth(..., textboxTest_scribble)`
  - точка создания dialogue controller

Это не основной GUI layout, но это важная входная точка, если нужно понять, откуда вообще стартует диалог.

## 3. Portrait draw и его runtime

### `objects/obj_face/Draw_64.gml`
Главная тонкая настройка portrait draw.

Здесь лежат:

- `_offset_x`, `_offset_y`
  - позиция portrait относительно центра textbox
- `_scale`
  - масштаб portrait для активного preset
- `_x`
  - итоговая X-позиция portrait: `box center + portrait offset`
- `_y`
  - итоговая Y-позиция portrait: `box center + portrait offset`
- `draw_sprite_ext(current_sprite, 0, _x, _y, _scale, _scale, 0, c_white, 1)`
  - фактическая отрисовка portrait с масштабом

Если portrait "летает" не внутри textbox, это первое место, которое надо проверять.

### `objects/textboxTest_scribble/Create_0.gml`
Единая точка хранения layout preset-переменных для dialogue UI.

Здесь лежат:

- `text_offset_x_with_portrait`, `text_offset_y_with_portrait`
  - старт текста для portrait preset
- `text_wrap_width_with_portrait`, `text_wrap_height_with_portrait`
  - размер текстовой зоны для portrait preset
- `marker_visible_with_portrait`, `marker_offset_x_with_portrait`, `marker_offset_y_with_portrait`
  - настройки continue marker для portrait preset
- `portrait_offset_x_with_portrait`, `portrait_offset_y_with_portrait`, `portrait_scale_with_portrait`
  - настройки portrait для portrait preset
- `text_offset_x_without_portrait`, `text_offset_y_without_portrait`
  - старт текста для preset без portrait
- `text_wrap_width_without_portrait`, `text_wrap_height_without_portrait`
  - размер текстовой зоны для preset без portrait
- `marker_visible_without_portrait`, `marker_offset_x_without_portrait`, `marker_offset_y_without_portrait`
  - настройки continue marker для preset без portrait
- `portrait_offset_x_without_portrait`, `portrait_offset_y_without_portrait`, `portrait_scale_without_portrait`
  - симметричный набор настроек для режима без portrait
- `choice_text_scale_1..4`, `choice_group_offset_y_1..4`
  - отдельные presets размера и вертикальной посадки choices для каждого `option_count`
- `choice_wrap_width_ratio_1`, `choice_wrap_width_ratio_2`, `choice_wrap_width_ratio_3`, `choice_wrap_width_ratio_4_0..3`
  - presets wrap-ширины choices
- `choice_slot_x_*`, `choice_slot_y_*`
  - presets позиции choice slots для `1/2/3/4` вариантов

Важно:

- `textboxTest_scribble` теперь владеет всем layout preset целиком
- `obj_face/Draw_64.gml` только читает `portrait_offset_*` и `portrait_scale_*`
- `textboxTest_scribble/Draw_64.gml` читает текстовые, marker и choice-настройки из тех же preset-блоков
- старой автосвязки `portrait margin -> text column` больше нет

### `objects/obj_face/Step_0.gml`
Runtime-логика выбора portrait sprite.

Здесь решается:

- есть ли вообще валидный portrait
- какой кадр рисовать: `mouth_closed` или `mouth_open`
- когда portrait скрывается полностью

Это не файл для позиционирования, но это основной файл для понимания, **почему portrait виден или не виден**.

### `objects/textboxTest_scribble/Create_0.gml`
Создание и базовая инициализация portrait/runtime части dialogue UI.

Здесь важно:

- создаётся `obj_face`, если его ещё нет
- настраивается `scribble_typist`
- задаётся `typist.function_per_char(...)`
- задаются preset-переменные текста, marker и portrait для двух режимов layout
- задаются отдельные choice preset-переменные для `1/2/3/4` вариантов выбора
- инициализируются `mouth_open_prev`, `mouth_closed_prev`, `sound_prev`
- инициализируются `talk_hold_timer`, `talk_hold_frames`, `talk_open_now`

Также здесь живёт фильтр символов для talk animation:

- `.` `!` `?` `:` `;` `…` `-` `—` не открывают рот
- запятая остаётся активной

### `objects/textboxTest_scribble/Step_0.gml`
Главный runtime-файл portrait state.

Здесь лежат:

- `apply_current_dialogue_state()`
  - обновление actor/emotion/sprite/sound по текущей строке
- `update_talk_animation_state()`
  - логика открытия/закрытия рта
- синхронизация `global.current_actor`, `global.current_emote`, `global.current_sprite`

Если portrait draw уже настроен, но кадры или actor/emotion работают странно, смотреть нужно сюда.

## 4. Actor/emotion -> portrait mapping

### `scripts/scr_parse_emote/scr_parse_emote.gml`
Нормализация actor/emotion и fallback-логика.

Здесь решается:

- narrator fallback
- default emotion
- использование previous emotion
- итоговый выбор ключа actor/emotion

### `scripts/map_emotions/map_emotions.gml`
Таблица сопоставления actor/emotion -> ресурсы portrait/sound.

Здесь лежит:

- какие sprite используются для `mouth_closed`
- какие sprite используются для `mouth_open`
- какой voice sound связан с actor/emotion

Если диалог правильно парсится, но показывается не тот portrait, проблема обычно здесь.

## 5. Interaction marker у игрока

### `scripts/scr_player_marker_update/scr_player_marker_update.gml`
Главный файл для offset interaction marker относительно игрока.

Здесь лежат:

- `pointX`
- `pointY`
- индивидуальные offsets для `RIGHT`, `LEFT`, `UP`, `DOWN`

Это главное место для ручной подстройки interaction distance и feel.

### `objects/obj_player/Create_0.gml`
Здесь создаётся постоянный instance marker:

- `marker_id = instance_create_depth(x, y, -infinity, obj_pointMarker);`

### `objects/obj_pointMarker/Create_0.gml`
Файл состояния самого marker object.

Важно:

- `visible = false`
- marker сам по себе не является обычным видимым UI-элементом
- он используется как логическая точка взаимодействия
- его debug-отрисовка отдельно выводится через F3

### `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml`
Проверка взаимодействия через marker.

Здесь лежит:

- проверка существования `obj_pointMarker`
- `place_meeting(...)` или `point_in_rectangle(...)`
- вызов `readDialogue(_scriptToReadFrom, _node)`

## 6. Debug overlay и debug toggles

### `objects/obj_globalManager/Draw_64.gml`
Главный файл для debug overlay.

Здесь находятся:

- `draw_debug_collider(...)`
  - проекция world collider в GUI overlay
- `_camx`, `_camy`, `_s`, `_ox`, `_oy`
  - ключевые параметры пересчёта позиции и масштаба
- F1 overlay
- F2 collider overlay
- F3 interaction marker debug draw

Если debug rectangle смещён, растянут или не совпадает с объектом, смотреть нужно сюда в первую очередь.

### `objects/obj_Init/Create_0.gml`
Базовая инициализация debug flags.

Здесь лежат:

- `global.debug_show_info`
- `global.debug_show_colliders`
- `global.debug_show_hitbox`
- `global.debug_show_music`

### `objects/obj_player/Create_0.gml`
Локальная синхронизация player-side debug flags с global-state.

Здесь лежат:

- `debug_show_info`
- `debug_show_colliders`
- `debug_show_hitbox`

### `scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml`
Файл hotkeys для переключения debug overlay.

Здесь лежат:

- `F1` -> `debug_show_info`
- `F2` -> `debug_show_colliders`
- `F3` -> marker debug

## 7. Dialogue entry points для конкретных объектов

Эти файлы важны, если нужно понять, **какой именно dialogue file и node реально запускаются**.

### `objects/obj_asher/Step_0.gml`
Пример interactable, который запускает:

- `testDialogue.yarn`
- node `Bench`

### `objects/obj_bench/Step_0.gml`
Ещё один пример конкретного dialogue entry point.

### `objects/obj_sheepFountain/Step_0.gml`
Ещё один пример dialogue entry point для другого interactable.

## 8. Самый короткий маршрут по частым задачам

### Если нужно подвигать portrait
Смотри:

- `objects/obj_face/Create_0.gml`
- `objects/obj_face/Draw_64.gml`
- `objects/textboxTest_scribble/Draw_64.gml`

### Если нужно изменить wrap текста вокруг portrait
Смотри:

- `objects/textboxTest_scribble/Draw_64.gml`

### Если нужно скрыть или сдвинуть `>` marker
Смотри:

- `objects/textboxTest_scribble/Draw_64.gml`

### Если нужно изменить interaction marker возле игрока
Смотри:

- `scripts/scr_player_marker_update/scr_player_marker_update.gml`

### Если нужно чинить F2/F3 debug overlay
Смотри:

- `objects/obj_globalManager/Draw_64.gml`
- `scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml`
- `objects/obj_Init/Create_0.gml`

## 9. Практическое правило для текущей portrait-задачи

Для текущего dialogue portrait layout важно помнить:

- portrait position настраивается в `objects/obj_face/Draw_64.gml`
- textbox main text wrap настраивается через preset-переменные в `objects/textboxTest_scribble/Create_0.gml`
- choice layout для `1/2/3/4` тоже настраивается через preset-переменные в `objects/textboxTest_scribble/Create_0.gml`
- `>` marker внутри textbox тоже живёт в `objects/textboxTest_scribble/Draw_64.gml`
- если portrait рисуется внутри textbox, `>` marker не должен рисоваться поверх portrait без отдельного согласованного layout
- `objects/textboxTest_scribble/Draw_64.gml` теперь в основном читает presets и рисует по ним
