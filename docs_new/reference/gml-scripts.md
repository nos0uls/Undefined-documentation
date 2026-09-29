---
title: Справочник GML-скриптов
tags:
  - reference
  - gml
---

# Справочник GML-скриптов

Все пользовательские функции из `scripts/` проекта Undefinedtale-888: сигнатуры, назначение и ссылки на разделы документации.

!!! info "Генерируемая страница"
    Таблицы собираются скриптом `_meta/gen_reference.py` из `_meta/scripts.txt` (+ `///`-комментарии исходников). После изменения кода страницу пересобирают, а не правят вручную.

!!! note "Что не входит в таблицы"
    - Библиотеки: Chatterbox (`Chatterbox*`, `__Chatterbox*`, `IsChatterbox`), Scribble (`scribble*`, `__scribble*`), TweenGMS (`TGMX_*`, `o_SharedTweener`).
    - Внутренний тестовый фреймворк: `scr_test_*`, `scr_stress_tests`.
    - Макрос-файлы без функций (`currentENUMS`, конфиги библиотек).

Всего функций: **414** в **127** файлах. Колонка «Док-страница» ведёт на тематический раздел; `—` — отдельной страницы нет.

## Системные скрипты (`scripts/scr_*`)

### `scripts/scr_SFXPlay/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_play_sfx` | `scr_play_sfx(_sound_or_key, _volume = 1, _pitch = 1, _fallback_sound = undefined)` | Проигрывает UI-звук с учётом громкости SFX из настроек (global.__sfx_volume). | [Музыка и звук](../systems/music.md) |
| `scr_SFXPlay` | `scr_SFXPlay(_action, _volume = 1, _pitch = 1)` | Legacy-алиас (имя вне snake_case сохранено ради ~70 точек вызова) — обёртка над scr_play_sfx с ui_snd_select как fallback-звуком. | [Музыка и звук](../systems/music.md) |

### `scripts/scr_anim/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_anim` | `scr_anim(_sprite, _framespeed)` | Создаёт obj_anim в точке вызывающего инстанса и активирует его: инстанс obj_anim пишет кадры спрайта в target (это сам вызывающий объект). | [Иерархия объектов](../architecture/object-hierarchy.md) |

### `scripts/scr_callMenuInit/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_callMenuInit` | `scr_callMenuInit()` | Обработка клавиши меню в игре. Открывает игровое меню при нажатии клавиши меню, если нет UI-блокеров. Исключает служебные комнаты (меню, настройки, выбор сейвов), где… | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_checkItemSkip/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_checkItemSkip` | `scr_checkItemSkip()` | Считает пустые слоты инвентаря (предметы, которые можно пропустить/пропустить). Используется для расчёта max_itemskip — количества пустых слотов. | [Инвентарь и статы](../systems/inventory-and-stats.md) |

### `scripts/scr_checkPlayerFacing/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_checkPlayerFacing` | `scr_checkPlayerFacing(_target_x, _target_y)` | Проверяет, смотрит ли игрок в сторону заданной точки. | [Игрок](../systems/player.md) |

### `scripts/scr_checkUIBlocking/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_checkUIBlocking` | `scr_checkUIBlocking(exclude_self = false, include_cutscene = true)` | Проверяет, заблокирован ли ввод из-за открытых UI элементов. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_ui_objects_list` | `scr_ui_objects_list()` | Единый список UI-объектов проекта. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_checkUIBlocking_raw` | `scr_checkUIBlocking_raw(exclude_self = false, include_cutscene = true)` | Полный пересчёт UI-блокировки без кэша. Вызывается из scr_checkUIBlocking. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_collision_resolve/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_collision_resolve` | `scr_collision_resolve()` | Разрешает коллизию игрока со всеми solid-группами: obj_collider + par_decor + par_interactable. | [Игрок](../systems/player.md) |

### `scripts/scr_constants/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_constants` | `scr_constants()` | Инициализирует глобальные константы направлений и состояний меню настроек. | [Инициализация](../architecture/initialization.md) |

### `scripts/scr_cutscene_animate/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `Script312` | `Script312()` | Пустой стаб (DELETE_CANDIDATE): имя не совпадает с ресурсом, живой аналог — `cutscene_animate` | — |

### `scripts/scr_cutscene_classes/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `CutsceneAction` | `CutsceneAction() constructor` | Базовый конструктор действия катсцены (Command pattern) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_get_resolver` | `__cutscene_get_resolver(_manager)` | Возвращает метод `resolve_target` менеджера, если он есть | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_resolve_target_ref` | `__cutscene_resolve_target_ref(_resolver, _target)` | Резолвит `target_ref` через resolver; без resolver — только живой instance id | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_resolve_target` | `__cutscene_resolve_target(_manager, _target)` | Резолвит цель действия в instance id | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_warn_unresolved` | `__cutscene_warn_unresolved(_action_name, _role, _target)` | Логирует нерезолвнутую цель действия. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_validate_mode` | `__cutscene_validate_mode(_value, _allowed, _fallback, _owner, _param)` | Валидирует строковый режим по списку допустимых значений. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_parallel_push` | `__cutscene_parallel_push(_manager, _parallel)` | Регистрирует ActionParallel как активную группу (стек вложенных parallel). | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_parallel_pop` | `__cutscene_parallel_pop(_manager)` | Снимает верхнюю parallel-группу со стека. | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_parallel_splice` | `__cutscene_parallel_splice(_parallel, _branch_index, _actions)` | Вставляет действия в продолжение конкретной ветки parallel-группы. | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_parallel_request_abort` | `__cutscene_parallel_request_abort(_manager)` | Помечает ближайшую (внутреннюю) parallel-группу на прерывание. | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_resolve_targets` | `__cutscene_resolve_targets(_manager, _target)` | Резолвит цель в массив instance id (несколько актёров по ключу) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_resolve_copy_source` | `__cutscene_resolve_copy_source(_manager, _copy_target)` | Нормализует copy_target до реального instance id, чтобы ActionActorCreate не вызывал instance_exists() на строке. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_is_instant` | `__cutscene_is_instant(_manager)` | Возвращает флаг instant-режима менеджера | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_get_global_manager` | `__cutscene_get_global_manager()` | Возвращает `global.active_cutscene_manager` | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_runtime_owner_id` | `__cutscene_runtime_owner_id()` | Возвращает id активной катсцены — это нужно, чтобы каждый runtime-эффект знал, какая катсцена его создала. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_normalize_direction` | `__cutscene_normalize_direction(_dir)` | Нормализует направление: строка/число → `global.DIR.*` | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_direction_angle` | `__cutscene_direction_angle(_dir)` | Направление `DIR` → угол в градусах | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_angle_to_direction` | `__cutscene_angle_to_direction(_angle)` | Угол в градусах → направление `DIR` | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_actor_apply_facing` | `__cutscene_actor_apply_facing(_inst, _dir)` | Применяет направление к актёру: спрайт ходьбы + `facing_direction` | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_move_step` | `__cutscene_move_step(_actor, _tx, _ty, _spd, _use_collision, _apply_move_state = true)` | Выполняет один шаг движения актёра к цели. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_move_cleanup` | `__cutscene_move_cleanup(_actor)` | Очищает состояние движения актёра после завершения. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_sync_move_target` | `__cutscene_sync_move_target(_inst)` | Подтягивает target_x/target_y актёра к его текущей позиции. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_attachments_remove_by_target` | `__cutscene_attachments_remove_by_target(_target_inst)` | Удаляет запись attachment из global.__cutscene_attachments по target_inst. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_find_active_textbox` | `__cutscene_find_active_textbox()` | Выбирает наиболее «живое» диалоговое окно среди textboxTest_scribble. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_dialogue_is_active` | `__cutscene_dialogue_is_active(_dialogue_controller = noone)` | Проверяет, открыто ли диалоговое окно (опционально — конкретный контроллер) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_find_dialogue_ctrl` | `__cutscene_find_dialogue_ctrl(_manager)` | Возвращает живой контроллер диалогового окна: сначала `dialogue_controller` менеджера, затем fallback на «живое» окно textboxTest_scribble | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_normalize_yarn_path` | `__cutscene_normalize_yarn_path(_file)` | Нормализует путь к yarn-файлу для Chatterbox: "\\" → "/", срезает префиксы "datafiles/" и "Dialogues/" (контент может указывать файл с ними или без). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_ease_value` | `__cutscene_ease_value(_t, _easing)` | Вычисляет easing-коэффициент прогресса по имени кривой | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_runtime_get_value` | `__cutscene_runtime_get_value(_kind, _target, _property)` | Читает свойство цели runtime-эффекта (`instance`/`camera`) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_runtime_set_value` | `__cutscene_runtime_set_value(_kind, _target, _property, _value)` | Пишет свойство цели runtime-эффекта (`instance`/`camera`) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_snapshot_instance` | `__cutscene_snapshot_instance(_inst)` | Создаёт snapshot состояния инстанса (позиция, спрайт, трансформация). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_create_snapshot` | `__cutscene_create_snapshot(_manager, _config)` | Создаёт полный snapshot состояния катсцены (актёры, камера, музыка, глобальные переменные). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_cleanup_transients` | `__cutscene_cleanup_transients(_manager, _snapshot = undefined)` | Удаляет временные объекты, созданные после checkpoint (актеры, не существовавшие в snapshot). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_apply_instance_snapshot` | `__cutscene_apply_instance_snapshot(_inst, _data, _with_move = true)` | Применяет к инстансу визуальные поля из snapshot-записи (x/y/sprite/image_*/depth/visible). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_restore_actor_states` | `__cutscene_restore_actor_states(_actor_map, _actors_snap)` | Восстанавливает состояния актёров actor_map из snapshot-секции actors. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_restore_camera_state` | `__cutscene_restore_camera_state(_cam_data)` | Возвращает view-позицию камеры и global.camera_x/y по snapshot-секции camera. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_restore_music_state` | `__cutscene_restore_music_state(_music_data)` | Восстанавливает трек и громкость из snapshot-секции music и перезапускает сохранённый трек, если это валидный звуковой ассет. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_restore_global_states` | `__cutscene_restore_global_states(_globals)` | Восстанавливает глобальные переменные из snapshot-секции globals с проверкой типов: при смене типа значение пропускается с warning. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_restore_instance_states` | `__cutscene_restore_instance_states(_instances)` | Восстанавливает зарегистрированные в snapshot инстансы по имени объекта. move_-поля им не применяются — секция хранит только визуальное состояние. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_tween_to` | `cutscene_runtime_tween_to(_target, _property, _to_value, _frames, _easing = __CUTSCENE_EASE_LINEAR, _from_value = undefined, _kind = __CUTSCENE_KIND_INSTANCE)` | Регистрирует runtime-твин свойства инстанса/камеры | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_fade_to` | `cutscene_runtime_fade_to(_alpha, _frames, _color = c_black)` | Управляет runtime fade-оверлеем (альфа, цвет) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_resolve_emote_sprite` | `cutscene_runtime_resolve_emote_sprite(_sprite = undefined)` | Резолвит спрайт эмоции в asset-индекс: строка ищется по имени ресурса, real — проверяется sprite_exists; при undefined/неразрешённом входе подставляется fallback из… | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_show_emote` | `cutscene_runtime_show_emote(_target, _sprite = undefined, _duration = __CUTSCENE_EMOTE_DURATION, _offset_x = 0, _offset_y = __CUTSCENE_EMOTE_OFFSET_Y, _scale = 1)` | Показывает эмоцию через глобальную emote system, не завязанную на cutscene manager. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_play_sfx` | `cutscene_runtime_play_sfx(_sound_or_key, _volume = 1, _pitch = 1)` | Проигрывает SFX из катсцены через `scr_play_sfx` | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_set_visible` | `cutscene_runtime_set_visible(_target, _visible)` | Меняет `visible` цели из runtime-эффектов | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_flip_x` | `cutscene_runtime_flip_x(_target, _flipped)` | Отражает спрайт цели по горизонтали (`image_xscale`) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_halt` | `cutscene_runtime_halt(_target)` | Останавливает движение цели из runtime-эффектов | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_make_shake_entry` | `__cutscene_make_shake_entry(_kind, _target, _frames, _magnitude, _magnitude_x, _magnitude_y, _decay, _frequency)` | Собирает запись shake-эффекта — общий конструктор для object- и camera-вариантов (различаются только kind/target и проверкой цели). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_shake_object` | `cutscene_runtime_shake_object(_target, _frames = 20, _magnitude = 4, _magnitude_x = undefined, _magnitude_y = undefined, _decay = false, _frequency = 1)` | Регистрирует runtime-тряску объекта | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_shake_camera` | `cutscene_runtime_shake_camera(_frames = 20, _magnitude = 4, _magnitude_x = undefined, _magnitude_y = undefined, _decay = false, _frequency = 1)` | Регистрирует runtime-тряску камеры | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_spin_object` | `cutscene_runtime_spin_object(_target, _speed, _frames = __CUTSCENE_DEFAULT_EFFECT_FRAMES)` | Регистрирует runtime-вращение объекта | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_jump_to` | `cutscene_runtime_jump_to(_target, _x, _y, _frames, _height = __CUTSCENE_JUMP_HEIGHT, _easing = __CUTSCENE_EASE_LINEAR)` | Регистрирует runtime-прыжок цели в точку | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_ensure_state` | `cutscene_runtime_ensure_state()` | Ленивая инициализация `global.__cutscene_runtime` | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_runtime_remove_at` | `__cutscene_runtime_remove_at(_array, _index, _item)` | Удаляет элемент runtime-массива с откатом применённого эффекта | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_cleanup_owner` | `cutscene_runtime_cleanup_owner(_owner)` | Принудительно деактивирует все runtime-эффекты, созданные катсценой _owner (tween/shake/spin/jump и singleton-fade). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_runtime_rollback_owner_shakes` | `__cutscene_runtime_rollback_owner_shakes(_owner)` | Синхронно снимает применённое смещение с целей шейков владельца и обнуляет applied_x/y. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_step` | `cutscene_runtime_step()` | Покадровое обновление всех runtime-эффектов (вызывается из Step менеджера) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `cutscene_runtime_draw_gui` | `cutscene_runtime_draw_gui(_camx, _camy, _scale, _offset_x, _offset_y)` | Рисует fade-оверлей катсцены в Draw GUI (вызывается из obj_globalManager/Draw_64). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `ActionWait` | `ActionWait(frames) constructor` | Пауза очереди на N кадров | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMarkNode` | `ActionMarkNode(_name) constructor` | Записывает имя достигнутой ноды (`last_reached_node` менеджера) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionGoToNode` | `ActionGoToNode(_target_name) constructor` | Переход очереди к ноде, помеченной `ActionMarkNode` | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSequence` | `ActionSequence(actions_array) constructor` | Последовательное выполнение массива действий | [Action-классы](../cutscenes/action-classes.md) |
| `ActionFollowPath` | `ActionFollowPath(target_ref, points_array, speed, _use_collision = false, auto_facing = true) constructor` | Движение актёра по массиву точек `{x, y}` | [Action-классы](../cutscenes/action-classes.md) |
| `ActionActorCreate` | `ActionActorCreate(name, x, y, sprite_or_obj) constructor` | Создаёт актёра катсцены и регистрирует его в `actor_map` | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMoveBase` | `ActionMoveBase(_target, _speed, _use_collision = false) constructor` | Базовый класс для движения актёра. Содержит общую логику для ActionMove и ActionMoveRelative. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMove` | `ActionMove(target_ref, _target_x, _target_y, speed, use_collision = false) constructor` | Движение актёра к абсолютной точке с заданной скоростью | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMoveRelativeDirection` | `ActionMoveRelativeDirection(target_ref, direction_ref, speed, frames, _use_collision = false) constructor` | Движение по направлению заданное число кадров | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMoveDirect` | `ActionMoveDirect(target_ref, _target_x, _target_y, frames_or_speed, use_speed = false, _use_collision = false) constructor` | Движение к точке за N кадров или с заданной скоростью | [Action-классы](../cutscenes/action-classes.md) |
| `ActionAnimate` | `ActionAnimate(target_ref, _sprite, image_index_set = undefined, image_speed_set = undefined) constructor` | Смена спрайта/кадра/скорости анимации цели | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetAnimationFrame` | `ActionSetAnimationFrame(target_ref, _image_index, _image_speed, _pause) constructor` | Устанавливает конкретный кадр анимации и скорость для актёра, не меняя его спрайт. Полезно для "заморозки" позы (pose hold) и синхронизации кадров. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionDialogue` | `ActionDialogue(_dialogue_file, _node_title = undefined, _block_queue = true, _auto_advance = false) constructor` | Запуск yarn-диалога внутри катсцены | [Action-классы](../cutscenes/action-classes.md) |
| `ActionRunFunction` | `ActionRunFunction(_func_ref, arg_array = []) constructor` | Вызывает произвольную функцию в момент старта действия. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetFacing` | `ActionSetFacing(target_ref, direction) constructor` | Мгновенно разворачивает актёра: спрайт движения + facing_direction. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionWaitForDialogue` | `ActionWaitForDialogue(dialogue_controller_ref = undefined) constructor` | Ожидание завершения реплики диалогового окна | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetDialogueSpeed` | `ActionSetDialogueSpeed(speed) constructor` | Устанавливает скорость печати текста в диалоговом окне. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionWaitTyping` | `ActionWaitTyping() constructor` | Ждет завершения печати текста в диалоговом окне. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionDialogueControl` | `ActionDialogueControl(prevent_skip, stay_open, auto_advance) constructor` | Устанавливает флаги управления поведением диалогового окна. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetPortraitNext` | `ActionSetPortraitNext(target, emotion) constructor` | Устанавливает эмоцию портрета для следующей реплики. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetPortraitNow` | `ActionSetPortraitNow(target, emotion) constructor` | Немедленно устанавливает эмоцию портрета в obj_face. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionClearDialogue` | `ActionClearDialogue() constructor` | Уничтожает активное диалоговое окно. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetProperty` | `ActionSetProperty(target_ref, _property_name, value, _target_kind = __CUTSCENE_KIND_INSTANCE) constructor` | Присвоение свойства инстанса или камеры | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetDepth` | `ActionSetDepth(target_ref, depth_value) constructor` | Установка `depth` цели и перевод в manual-режим | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMoveRelative` | `ActionMoveRelative(_target, _dx, _dy, _speed_pf, _use_collision = false) constructor` | Cutscene action: двигает актёра от текущей позиции на offset (_dx, _dy). Target-координаты вычисляются в start(), чтобы учесть актуальную позицию. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetXY` | `ActionSetXY(target_ref, _x, _y) constructor` | Мгновенный телепорт цели в точку | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetPositionRelative` | `ActionSetPositionRelative(_target, _dx, _dy) constructor` | Cutscene action: мгновенно сдвигает актёра на (_dx, _dy) от текущей позиции. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetInstantMode` | `ActionSetInstantMode(enabled = true) constructor` | Включает instant-режим: действия выполняются за один кадр | [Action-классы](../cutscenes/action-classes.md) |
| `ActionHalt` | `ActionHalt(target_ref) constructor` | Остановка текущего движения цели | [Action-классы](../cutscenes/action-classes.md) |
| `ActionFlip` | `ActionFlip(target_ref, flipped) constructor` | Переворачивает спрайт актора по горизонтали через image_xscale. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSpin` | `ActionSpin(target_ref, speed, frames = __CUTSCENE_DEFAULT_EFFECT_FRAMES) constructor` | Вращение цели (`image_angle`) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionShakeBase` | `ActionShakeBase(_frames, _magnitude = 4, _magnitude_x = undefined, _magnitude_y = undefined, _decay = false, _frequency = 1) constructor` | Базовый класс для shake эффектов. Содержит общую логику для ActionShakeObject и ActionCameraShake. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionShakeObject` | `ActionShakeObject(target_ref, frames = 20, _magnitude = 4, _magnitude_x = undefined, _magnitude_y = undefined, _decay = false, _frequency = 1) constructor` | Тряска объекта (runtime-эффект) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionPlaySFX` | `ActionPlaySFX(_sound_or_key, _volume = 1, _pitch = 1) constructor` | Проигрывание звука | [Action-классы](../cutscenes/action-classes.md) |
| `ActionEmote` | `ActionEmote(target_ref, _sprite = undefined, _duration = __CUTSCENE_EMOTE_DURATION, _offset_x = 0, _offset_y = __CUTSCENE_EMOTE_OFFSET_Y, _scale = 1, _wait_for_finish = false) constructor` | Эмоция (попап) над актёром | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetEmotion` | `ActionSetEmotion(target_ref, emotion = "default", apply_to_sprite = true, apply_to_portrait = true) constructor` | Команда катсцены для установки emotional state актёру. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionFadeTo` | `ActionFadeTo(target_alpha, frames, color = c_black) constructor` | Плавный переход fade-оверлея к заданной альфе | [Action-классы](../cutscenes/action-classes.md) |
| `ActionFadeIn` | `ActionFadeIn(frames, color = c_black) constructor` | Проявление экрана (`ActionFadeTo` к 0) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionFadeOut` | `ActionFadeOut(frames, color = c_black) constructor` | Затемнение экрана (`ActionFadeTo` к 1) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionTween` | `ActionTween(target_ref, _property_name, to_value, frames, easing = __CUTSCENE_EASE_LINEAR, from_value = undefined, _target_kind = __CUTSCENE_KIND_INSTANCE) constructor` | Твин свойства цели к значению за N кадров | [Action-классы](../cutscenes/action-classes.md) |
| `ActionLerp` | `ActionLerp(target_ref, _property_name, to_value, factor = 0.1, threshold = 0.5, _target_kind = __CUTSCENE_KIND_INSTANCE) constructor` | Пошаговое линейное приближение (lerp) свойства объекта или камеры к целевому значению. Использует реальный коэффициент factor (0..1) на каждый шаг. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionJump` | `ActionJump(target_ref, _x, _y, frames, height = __CUTSCENE_JUMP_HEIGHT, easing = __CUTSCENE_EASE_LINEAR) constructor` | Прыжок цели в точку по параболе | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraShake` | `ActionCameraShake(frames = __CUTSCENE_DEFAULT_EFFECT_FRAMES, _magnitude = 4, _magnitude_x = undefined, _magnitude_y = undefined, _decay = false, _frequency = 1) constructor` | Тряска камеры (runtime-эффект) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionGroup` | `ActionGroup(_targets, _context, _generator_fn) constructor` | Создаёт параллельное действие по генератору для каждой цели. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionParallel` | `ActionParallel(actions_array) constructor` | Параллельное выполнение веток действий | [Action-классы](../cutscenes/action-classes.md) |
| `ActionScheduleAction` | `ActionScheduleAction(delay_seconds, inner_action, blocking, tag) constructor` | Запуск вложенного действия с задержкой (schedule) | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_update_attachments` | `__cutscene_update_attachments()` | Обновляет привязанных к родителям актёров (attachments) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `ActionAttachToTarget` | `ActionAttachToTarget(target_ref, parent_ref, _offset_x, _offset_y, follow_facing, follow_scale, follow_depth, duration_seconds, detach_on_cutscene_end) constructor` | Привязка актёра к родителю со смещением | [Action-классы](../cutscenes/action-classes.md) |
| `ActionDetach` | `ActionDetach(target_ref, destroy_after_detach) constructor` | Отвязывает актёра от родителя и опционально уничтожает его. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionBranch` | `ActionBranch(condition_func, true_actions, false_actions) constructor` | Ветвление очереди по функции-условию | [Action-классы](../cutscenes/action-classes.md) |
| `ActionBranchFlag` | `ActionBranchFlag(flag_key, operator, expected_val, true_actions, false_actions) constructor` | Ветвление катсцены на основе значения в global.flag[flag_key]. | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_resolve_state_value` | `__cutscene_resolve_state_value(var_path)` | Разрешает значение переменной состояния мира по имени или dot-пути. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_compare_values` | `__cutscene_compare_values(actual, expected)` | Сравнивает значения состояния с толерантностью к строкам/числам/bool из JSON. | [Архитектура катсцен](../cutscenes/architecture.md) |
| `ActionGuardGlobal` | `ActionGuardGlobal(var_name, equals_value, inner_actions, _if_false, _stop_when, _end_var, _end_equals, _end_node, _end_timeout_frames) constructor` | Блокировка/ожидание по значению глобальной переменной | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraCenter` | `ActionCameraCenter(_center_x, _center_y) constructor` | Мгновенное центрирование камеры на точке | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraPanBase` | `ActionCameraPanBase(_frames) constructor` | Базовый класс для панорамирования камеры. Содержит общую логику для ActionCameraPan и ActionCameraPanSpeed. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraPan` | `ActionCameraPan(view_x, view_y, frames) constructor` | Панорамирование камеры к точке за N кадров | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraPanSpeed` | `ActionCameraPanSpeed(_speed_x, _speed_y, frames) constructor` | Панорамирование камеры к точке с заданной скоростью | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraPanToObj` | `ActionCameraPanToObj(_target, frames) constructor` | Панорамирование камеры к объекту за N кадров | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraTrackBase` | `ActionCameraTrackBase(_target, _offset_x = 0, _offset_y = 0) constructor` | Базовый класс для отслеживания цели камерой. Содержит общую логику для ActionCameraTrack и ActionCameraTrackUntilStop. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraTrack` | `ActionCameraTrack(target_ref, frames, offset_x = 0, offset_y = 0) constructor` | Следование камеры за целью N кадров | [Action-классы](../cutscenes/action-classes.md) |
| `ActionCameraTrackUntilStop` | `ActionCameraTrackUntilStop(target_ref, offset_x = 0, offset_y = 0) constructor` | Следование камеры за целью до её остановки | [Action-классы](../cutscenes/action-classes.md) |
| `ActionWaitForInteract` | `ActionWaitForInteract(target_ref, timeout_frames = 0, timeout_action = __CUTSCENE_ON_EVENT_CONTINUE, interact_action = __CUTSCENE_ON_EVENT_CONTINUE) constructor` | Ожидание взаимодействия игрока с целью (с таймаутом) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetFlag` | `ActionSetFlag(key, value) constructor` | Запись `global.flag[key] = value` | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSetPlot` | `ActionSetPlot(value) constructor` | Запись `global.plot = value` | [Action-классы](../cutscenes/action-classes.md) |
| `ActionSpawnEntity` | `ActionSpawnEntity(object_name, x, y, key, depth_val, persistent_flag) constructor` | Спавн объекта в комнате (spawn_entity) | [Action-классы](../cutscenes/action-classes.md) |
| `ActionDestroy` | `ActionDestroy(target_ref) constructor` | Уничтожает объект с защитой от уничтожения игрока. Объединённый класс для ActionActorDestroy и ActionDestroyEntity. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionRoomChange` | `ActionRoomChange(target_room_ref, px, py, actor_pos_struct) constructor` | Смена комнаты из катсцены с переходом | [Action-классы](../cutscenes/action-classes.md) |
| `ActionPartialControl` | `ActionPartialControl(_control_type, whitelist_array, allowed_actions_array = undefined) constructor` | Частичный контроль ввода игрока во время катсцены | [Частичный контроль](../cutscenes/partial-control.md) |
| `__cutscene_cleanup_old_checkpoints` | `__cutscene_cleanup_old_checkpoints()` | Удаляет старые checkpoint-ы при превышении лимита (LRU). | [Архитектура катсцен](../cutscenes/architecture.md) |
| `ActionCheckpointState` | `ActionCheckpointState(_checkpoint_id, _config) constructor` | Создаёт snapshot состояния катсцены и сохраняет его в global registry. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionRestoreState` | `ActionRestoreState(_checkpoint_id, _options) constructor` | Восстанавливает состояние из checkpoint. | [Action-классы](../cutscenes/action-classes.md) |
| `__cutscene_room_entry_spawn` | `__cutscene_room_entry_spawn(_entry)` | Мёртвая функция спавна по entry-записи — тело зачищено (DELETE_CANDIDATE) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `scr_room_entry_check` | `scr_room_entry_check()` | Точка вызова из obj_globalManager/Step_0 при смене комнаты. | [Переходы комнат](../systems/room-transitions.md) |

### `scripts/scr_cutscene_make/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_cutscene_make` | `scr_cutscene_make()` | Заглушка (DELETE_CANDIDATE): сборка катсцен идёт через `c_begin`/`c_play` или `cutscene_load_json`; возвращает `noone` | [Обзор архитектуры](../architecture/overview.md) |

### `scripts/scr_cutscene_music/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `__cutscene_music_call` | `__cutscene_music_call(_func_name, _args)` | Проверяет существование и вызывает глобальную music-функцию, если она доступна. Число аргументов не ограничено — массив разворачивается целиком. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicPlay` | `ActionMusicPlay(_snd_asset, _fade_sec, _volume = 1.0, _persist_room_change = true) constructor` | Cutscene action: переключает музыку на указанный трек с кроссфейдом и целевой громкостью. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicStop` | `ActionMusicStop(_fade_sec, _use_layered = false) constructor` | Cutscene action: останавливает музыку с опциональным фейдом. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicVolume` | `ActionMusicVolume(_vol, _fade_sec) constructor` | Cutscene action: плавно меняет громкость текущего трека. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicPitch` | `ActionMusicPitch(_pitch) constructor` | Cutscene action: устанавливает pitch текущего трека. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicPause` | `ActionMusicPause() constructor` | Cutscene action: ставит текущую музыку на паузу (включая intro, layer2 и prev-каналы). | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicResume` | `ActionMusicResume() constructor` | Cutscene action: снимает музыку с паузы. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicIntroLoop` | `ActionMusicIntroLoop(_intro_asset, _loop_asset, _fade_sec) constructor` | Cutscene action: играет intro один раз, затем переключается на loop. | [Action-классы](../cutscenes/action-classes.md) |
| `cutscene_music_pitch` | `cutscene_music_pitch(_pitch)` | Возвращает `ActionMusicPitch` для добавления в катсцену | [Action-классы](../cutscenes/action-classes.md) |
| `cutscene_music_pause` | `cutscene_music_pause()` | Возвращает ActionMusicPause для добавления в катсцену. | [Action-классы](../cutscenes/action-classes.md) |
| `cutscene_music_resume` | `cutscene_music_resume()` | Возвращает ActionMusicResume для добавления в катсцену. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicDuck` | `ActionMusicDuck(_multiplier, _fade_sec) constructor` | Cutscene action: приглушает музыку относительно текущей громкости. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicUnduck` | `ActionMusicUnduck(_fade_sec) constructor` | Cutscene action: снимает приглушение музыки. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicPlayLayered` | `ActionMusicPlayLayered(_calm_asset, _battle_asset, _fade_sec) constructor` | Cutscene action: запускает два трека синхронно (calm + battle). | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicSetIntensity` | `ActionMusicSetIntensity(_intensity, _fade_sec = 1.0) constructor` | Cutscene action: меняет соотношение calm/battle слоёв. | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicIntroLayered` | `ActionMusicIntroLayered(_intro_asset, _calm_asset, _battle_asset, _fade_sec, _start_intensity) constructor` | Cutscene action: играет intro, затем автоматически переключается на layered loop (calm + battle). | [Action-классы](../cutscenes/action-classes.md) |
| `ActionMusicPhaseSequence` | `ActionMusicPhaseSequence(_phases, _fade_sec) constructor` | Cutscene action: запускает фазовую последовательность музыки через MusicPhaseManager. Каждая фаза — структура {intro, calm, battle, intensity, fade}. | [Action-классы](../cutscenes/action-classes.md) |

### `scripts/scr_debug_activation_check/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_debug_activation_check` | `scr_debug_activation_check()` | Секретное включение debug по F12 (5 нажатий за 2 секунды). | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_debug_draw_helpers/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `draw_text_outlined` | `draw_text_outlined(xx, yy, text, scale, outline_col, text_col)` | Отрисовка текста с обводкой (4 направления) для debug overlay. | [Отладка и тесты](../systems/debug-and-testing.md) |
| `draw_debug_collider` | `draw_debug_collider(obj_type, color, _camx, _camy, _s, _ox, _oy)` | Отрисовка bbox/спрайта всех инстансов типа объекта для debug-оверлея | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_defaultLoad/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_defaultLoad` | `scr_defaultLoad()` | Сценарий «новой игры» при выборе пустого слота: сбрасывает сессионное состояние и переводит игрока в стартовую комнату. | [Сохранения](../systems/save-system.md) |

### `scripts/scr_emote_system/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `emote_show` | `emote_show(_target, _sprite = undefined, _duration = 60, _offset_x = 0, _offset_y = -24, _scale = 1)` | Показывает всплывающую эмоцию (попап) над головой персонажа. | [Диалоги](../systems/dialogue.md) |
| `emote_hide_all_for` | `emote_hide_all_for(_target)` | Скрывает все эмоции цели — тело зачищено (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |
| `emote_hide_all` | `emote_hide_all()` | Скрывает все эмоции — тело зачищено (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |
| `__emote_system_ready` | `__emote_system_ready()` | Проверяет, что глобальная система эмоций уже создана в obj_Init. | [Диалоги](../systems/dialogue.md) |
| `__emote_sprite_speed_per_frame` | `__emote_sprite_speed_per_frame(_spr)` | Переводит авторскую скорость анимации спрайта в кадры за один кадр игры. | [Диалоги](../systems/dialogue.md) |
| `emote_resolve_sprite` | `emote_resolve_sprite(_sprite)` | Превращает входные данные (строку или индекс) в валидный индекс спрайта. | [Диалоги](../systems/dialogue.md) |
| `emote_step` | `emote_step()` | Обновляет состояние всех эмоций (время жизни и анимацию). Должна вызываться в Step событии глобального менеджера. | [Диалоги](../systems/dialogue.md) |
| `emote_draw_gui` | `emote_draw_gui(_camx, _camy, _scale, _offset_x, _offset_y)` | Отрисовывает все активные эмоции на слое GUI. | [Диалоги](../systems/dialogue.md) |

### `scripts/scr_entity_state/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_entity_state_get` | `scr_entity_state_get(room_name, entity_id)` | Возвращает сохранённое состояние сущности из реестра global.entity_state. | [Сохранения](../systems/save-system.md) |
| `scr_entity_state_set` | `scr_entity_state_set(room_name, entity_id, state_struct)` | Сохраняет состояние сущности в реестр global.entity_state. | [Сохранения](../systems/save-system.md) |
| `scr_entity_state_clear` | `scr_entity_state_clear(room_name, entity_id)` | Удаляет сохранённое состояние конкретной сущности из global.entity_state. | [Сохранения](../systems/save-system.md) |
| `scr_world_flag_set` | `scr_world_flag_set(room_name, flag, value)` | Записывает персистентный флаг комнаты в мировое состояние. | [Сохранения](../systems/save-system.md) |
| `scr_world_flag_get` | `scr_world_flag_get(room_name, flag, _default = false)` | Читает персистентный флаг комнаты из мирового состояния. | [Сохранения](../systems/save-system.md) |

### `scripts/scr_format_playtime/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_format_playtime` | `scr_format_playtime(seconds)` | Преобразует количество секунд в строку формата H:MM:SS. | [Сохранения](../systems/save-system.md) |

### `scripts/scr_game_state/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_game_state_get_path` | `scr_game_state_get_path()` | Возвращает стандартизированный абсолютный путь к файлу game_state.dat. | [Сохранения](../systems/save-system.md) |
| `scr_game_state_default` | `scr_game_state_default()` | Возвращает структуру game_state по умолчанию. | [Сохранения](../systems/save-system.md) |
| `scr_game_state_load` | `scr_game_state_load()` | Загружает game_state из файла (game_state.dat). При отсутствии файла возвращает дефолт. Пытается конвертировать строковые значения в числа, если это возможно. | [Сохранения](../systems/save-system.md) |
| `scr_game_state_save` | `scr_game_state_save(state)` | Сохраняет структуру game_state в файл (game_state.dat) атомарно через .tmp. | [Сохранения](../systems/save-system.md) |

### `scripts/scr_get_next_game_room/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_room_is_dev_navigation_excluded` | `scr_room_is_dev_navigation_excluded(_room_name)` | Единый фильтр комнат, которые не должны быть целями dev-навигации (F5/F6 и список DEV-LOAD в obj_devLoader). | [Отладка и тесты](../systems/debug-and-testing.md) |
| `scr_get_next_game_room` | `scr_get_next_game_room(direction)` | Возвращает следующую/предыдущую игровую комнату, пропуская служебные | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_global_debug_hotkeys/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `__debug_jump_room` | `__debug_jump_room(_direction)` | Debug-прыжок по игровым комнатам с безопасным спавном (F5 назад, F6 вперёд). | [Отладка и тесты](../systems/debug-and-testing.md) |
| `scr_global_debug_hotkeys` | `scr_global_debug_hotkeys()` | Обрабатывает функциональные клавиши дебага (F1-F7, F9). | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_global_handle_dev_spawn/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_handle_dev_spawn` | `scr_global_handle_dev_spawn()` | Создаёт игрока в комнате после DEV-LOAD | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_global_handle_notifications/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_handle_notifications` | `scr_global_handle_notifications()` | Обновляет таймер уведомлений и отключает их после истечения (в секундах, FPS-независимо) Контракт self: читает и пишет инстанс-поля notification_active/… | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_global_music_fade_previous/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_music_fade_previous` | `scr_global_music_fade_previous()` | Обрабатывает плавное затухание предыдущего трека музыки (time-based). | [Музыка и звук](../systems/music.md) |

### `scripts/scr_global_music_update_current/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_music_update_current` | `scr_global_music_update_current()` | Обновляет громкость текущего трека (time-based fade), duck multiplier, и обрабатывает intro → loop переход. | [Музыка и звук](../systems/music.md) |

### `scripts/scr_global_on_room_change/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_on_room_change` | `scr_global_on_room_change(prev_room, new_room)` | Обработка смены комнаты: уведомления, музыка, антизастревание | [Переходы комнат](../systems/room-transitions.md) |

### `scripts/scr_global_quick_save/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_quick_save` | `scr_global_quick_save()` | Быстрый сейв в текущий слот (клавиша F7, вызывается только в debug-режиме). | [Сохранения](../systems/save-system.md) |

### `scripts/scr_global_reset_settings_flag/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_reset_settings_flag` | `scr_global_reset_settings_flag()` | Заглушка без эффекта. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_global_toggle_fullscreen/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_toggle_fullscreen` | `scr_global_toggle_fullscreen()` | Обрабатывает глобальную клавишу Q для мгновенного переключения полноэкранного режима. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_global_transition_safety/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_global_transition_safety` | `scr_global_transition_safety()` | Обрабатывает выталкивание игрока и выключение transition_ghost (принудительной части ghost_mode) после перехода | [Переходы комнат](../systems/room-transitions.md) |

### `scripts/scr_inputApi/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_input__keys_for_action` | `scr_input__keys_for_action(action)` | Возвращает массив клавиш, назначенных на указанное действие (например, "jump" -> [vk_space, ord("Z")]). | [Ввод](../systems/input.md) |
| `scr_input_actions_list` | `scr_input_actions_list()` | Единый список переназначаемых действий ввода. | [Ввод](../systems/input.md) |
| `scr_input_normalize_key` | `scr_input_normalize_key(code)` | Приводит сохранённый код клавиши к допустимому vk-значению | [Ввод](../systems/input.md) |
| `scr_input__is_cutscene_blocked_here` | `scr_input__is_cutscene_blocked_here(_action = "")` | Проверяет, должен ли ввод быть заблокирован из-за активной катсцены. | [Ввод](../systems/input.md) |
| `scr_input__partial_control_allows` | `scr_input__partial_control_allows(_mgr, _action)` | Проверяет, разрешено ли действие ввода в WHITELIST-режиме partial_control. | [Частичный контроль](../cutscenes/partial-control.md) |
| `scr_input_gamepad_update` | `scr_input_gamepad_update()` | Обновляет состояние осей стиков геймпада раз за кадр (вызывается из obj_globalManager/Step_0). | [Ввод](../systems/input.md) |
| `scr_input__gamepad_down` | `scr_input__gamepad_down(action)` | Проверяет ввод с геймпада (удержание кнопки или отклонение стика). | [Ввод](../systems/input.md) |
| `scr_input__gamepad_pressed` | `scr_input__gamepad_pressed(action)` | Проверяет одиночное нажатие кнопки геймпада или отклонение стика. | [Ввод](../systems/input.md) |
| `scr_input_down` | `scr_input_down(action)` | Проверяет, УДЕРЖИВАЕТСЯ ли клавиша или кнопка геймпада для указанного действия. | [Ввод](../systems/input.md) |
| `scr_input_pressed` | `scr_input_pressed(action)` | Проверяет, была ли НАЖАТА клавиша или кнопка геймпада (один раз) в этом кадре. | [Ввод](../systems/input.md) |
| `scr_input_repeater` | `scr_input_repeater(action, delay = undefined, interval = undefined)` | Обрабатывает повторение ввода (как при зажатии клавиши печати) с учётом клавиатуры и геймпада. | [Ввод](../systems/input.md) |
| `scr_input_rebind` | `scr_input_rebind(action, new_key)` | Переназначает основной слот действия (обёртка над scr_input_rebind_slot). | [Ввод](../systems/input.md) |
| `scr_input_rebind_slot` | `scr_input_rebind_slot(action, slotIndex, new_key, target_settings = undefined)` | Переназначает конкретный слот (1 или 2) для действия. | [Ввод](../systems/input.md) |
| `scr_input_keys_hint` | `scr_input_keys_hint(settings, action)` | Собирает человекочитаемую подсказку клавиш действия из настроек — например "Z/Enter". | [Ввод](../systems/input.md) |

### `scripts/scr_inventory_init/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_inventory_init` | `scr_inventory_init()` | Инициализация ООП-инвентаря. Вызывается один раз из obj_Init.Create_0. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `scr_stats_recalc` | `scr_stats_recalc()` | Пересчитывает эффективные stat_atk/stat_def как база + бонусы экипированных предметов (equipped_weapon.damage, equipped_armor.defense). | [Инвентарь и статы](../systems/inventory-and-stats.md) |

### `scripts/scr_item_apply_use/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_item_apply_use` | `scr_item_apply_use(_item)` | Применяет эффект предмета к состоянию игры (мутации глобалов/предмета). | [Инвентарь и статы](../systems/inventory-and-stats.md) |

### `scripts/scr_key_to_string/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_key_to_string` | `scr_key_to_string(key)` | Возвращает человекочитаемое имя клавиши | [Ввод](../systems/input.md) |

### `scripts/scr_layer_ensure_instances/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_layer_ensure_instances` | `scr_layer_ensure_instances()` | Гарантирует существование слоя "Instances" в текущей комнате; создаёт его на depth 0, если слоя нет. | [Комнаты](../architecture/rooms.md) |

### `scripts/scr_menu_shader_guard/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_menu_shader_push` | `scr_menu_shader_push()` | Включает ручную отрисовку application_surface (для шейдера меню) с учётом вложенности. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_menu_shader_pop` | `scr_menu_shader_pop()` | Отключает ручную отрисовку application_surface, когда вложенность меню обнулилась. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_menu_volume_guard/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_menu_volume_push` | `scr_menu_volume_push(target = 0.8)` | Ставит мастер-громкость на время меню (0.8 от текущей) с учётом вложенности. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_menu_volume_pop` | `scr_menu_volume_pop()` | Восстанавливает мастер-громкость, когда стек меню опустел. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_music_init/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_music_init` | `scr_music_init()` | Инициализация музыкальной системы: глобальные переменные и функции управления музыкой. Вызывается один раз из obj_Init.Create_0. | [Музыка и звук](../systems/music.md) |
| `__music_handoff_to_prev` | `__music_handoff_to_prev(_fade_sec)` | Переносит текущий трек (и battle-слой в layered-режиме) в prev-канал для плавного затухания — общий блок смены трека во всех play-функциях. | [Музыка и звук](../systems/music.md) |
| `__music_fade_lerp` | `__music_fade_lerp(_timer, _duration, _from, _to)` | Значение time-based фейда по оставшемуся времени таймера | [Музыка и звук](../systems/music.md) |

### `scripts/scr_npc_pick_dialogue/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_npc_pick_dialogue` | `scr_npc_pick_dialogue()` | Пустой стаб (DELETE_CANDIDATE): выбор реплики NPC делает контент через `readDialogue` | [Взаимодействие](../systems/interaction.md) |

### `scripts/scr_p3r_draw_cursor/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_p3r_draw_cursor` | `scr_p3r_draw_cursor(_x, _y, _size = 16, _color = undefined, _alpha = 1)` | Undertale-style red pixel heart cursor | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_p3r_draw_panel/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_p3r_draw_panel` | `scr_p3r_draw_panel(_x, _y, _w, _h, _alpha = 0.9, _slant = 0)` | Undertale-style rectangular box with white border and dark fill | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_draw_button` | `scr_p3r_draw_button(_x, _y, _w, _h, _selected, _alpha, _slant = 0)` | Undertale-style button row: selected = dark red highlight, unselected = plain | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_p3r_menu_init/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_p3r_menu_state_create` | `scr_p3r_menu_state_create(_options, _initial_index = 0)` | Creates a menu state struct for P3R menus | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_menu_get_selected` | `scr_p3r_menu_get_selected(_state)` | Returns the currently selected option [label, function] | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_menu_execute_selected` | `scr_p3r_menu_execute_selected(_state)` | Executes the function of the selected option | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_menu_close` | `scr_p3r_menu_close(_state)` | Marks menu for closing transition | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_p3r_menu_nav/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_p3r_menu_nav` | `scr_p3r_menu_nav(_index, _count, _wrap, _actions, _allow_horizontal = false)` | Navigation wrapper: vertical + optional horizontal | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_p3r_palette/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_p3r_palette` | `scr_p3r_palette()` | Global color palette for Undertale-style menus. Call once at init. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_p3r_particles/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_p3r_particles_create` | `scr_p3r_particles_create()` | Creates a particle system for Undertale-style menu effects. Returns struct with system + types. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_particles_destroy` | `scr_p3r_particles_destroy(_particles)` | Destroys a particle system and all its types | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_particles_burst` | `scr_p3r_particles_burst(_particles, _type, _x, _y, _count)` | Emits a burst of particles at position | [UI и меню](../systems/ui-and-menus.md) |
| `scr_p3r_particles_stream` | `scr_p3r_particles_stream(_particles, _type, _x, _y, _count)` | Emits a continuous stream of particles | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_parse_emote/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_parse_emote` | `scr_parse_emote(_speaker_data_raw, _display_raw = "", _actor_prev = "", _emotion_prev = "", _display_prev = "", _forced_emotion = "")` | Парсит raw speaker / speaker-data строки Chatterbox в нормализованный portrait state. | [Диалоги](../systems/dialogue.md) |
| `__parse_emote_resolve_display` | `__parse_emote_resolve_display(_display_in, _actor_key, _actor_prev_key, _display_prev_str)` | Общий resolve подписи спикера для обычной и forced-веток scr_parse_emote. | [Диалоги](../systems/dialogue.md) |

### `scripts/scr_player_animation/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_animation` | `scr_player_animation(ui_blocking, movement_inputs)` | Обрабатывает анимацию игрока: обновление спрайтов направления и скорости анимации. | [Игрок](../systems/player.md) |

### `scripts/scr_player_debug_ghost/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_debug_ghost` | `scr_player_debug_ghost()` | Обрабатывает debug-клавишу F8 для переключения режима призрака. | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_player_facing/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_sprite_for_facing` | `scr_sprite_for_facing(_facing)` | Возвращает спрайт ходьбы по направлению facing. | [Игрок](../systems/player.md) |
| `scr_facing_for_sprite` | `scr_facing_for_sprite(_sprite)` | Возвращает направление игрока по текущему спрайту. | [Игрок](../systems/player.md) |
| `scr_player_facing` | `scr_player_facing()` | Обновляет facing_direction на основе текущего спрайта. | [Игрок](../systems/player.md) |

### `scripts/scr_player_marker_update/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_marker_update` | `scr_player_marker_update()` | Обновляет позицию маркера взаимодействия по направлению взгляда игрока. | [Взаимодействие](../systems/interaction.md) |

### `scripts/scr_player_movement/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_movement` | `scr_player_movement()` | Обрабатывает движение игрока: чтение ввода, вычисление скорости, применение движения с коллизиями. | [Игрок](../systems/player.md) |

### `scripts/scr_player_process_mutually_exclusive_inputs/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_process_mutually_exclusive_inputs` | `scr_player_process_mutually_exclusive_inputs(_up, _down, _left, _right)` | Обрабатывает взаимоисключающие клавиши движения (up/down, left/right). При одновременном нажатии противоположных клавиш — приоритет последней нажатой. | [Игрок](../systems/player.md) |

### `scripts/scr_player_room_lock/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_room_lock` | `scr_player_room_lock()` | Сбрасывает блок комнатного перехода, когда игрок вышел из хитбокса roomChanger. | [Переходы комнат](../systems/room-transitions.md) |

### `scripts/scr_player_slope_resolve/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_slope_resolve` | `scr_player_slope_resolve(_slope)` | Скольжение игрока вдоль диагонали склона и запрет входа в треугольник. Вызывается из scr_collision_resolve в контексте obj_player до применения xspd/yspd. | [Игрок](../systems/player.md) |
| `scr_player_cell_blocked_by_slope` | `scr_player_cell_blocked_by_slope(_tx, _ty, _exclude)` | Проверяет, заходит ли bbox вызывающего инстанса в целевой точке (_tx,_ty) в треугольник любого клина, кроме _exclude. | [Игрок](../systems/player.md) |

### `scripts/scr_player_ui_blocking/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_player_ui_blocking` | `scr_player_ui_blocking()` | Проверяет блокировку UI и выставляет can_move, учитывая катсцену. | [Игрок](../systems/player.md) |

### `scripts/scr_resetGameToDefault/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_resetGameToDefault` | `scr_resetGameToDefault()` | Полностью очищает игровые данные и завершает игру (game_end). | [Сохранения](../systems/save-system.md) |

### `scripts/scr_roomFromName/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_roomFromName` | `scr_roomFromName(_name)` | Возвращает id комнаты по строковому имени, либо -1 если не найдено. | [Комнаты](../architecture/rooms.md) |

### `scripts/scr_room_fade_update/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_room_fade_update` | `scr_room_fade_update()` | Обновляет логику фейда при переходе между комнатами. | [Переходы комнат](../systems/room-transitions.md) |

### `scripts/scr_saveLoad/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_saveLoad` | `scr_saveLoad(_change_room = true)` | Загружает сейв из global.current_save_slot. | [Сохранения](../systems/save-system.md) |
| `scr_save_slot_names` | `scr_save_slot_names()` | Единый список слотов сохранений. | [Сохранения](../systems/save-system.md) |
| `scr_save_metadata_defaults` | `scr_save_metadata_defaults(_slot, _path)` | Базовая структура метаданных слота для отсутствующего/битого сейва. | [Сохранения](../systems/save-system.md) |
| `scr_save_read_metadata` | `scr_save_read_metadata(_slot_path)` | Читает «шапку» сейв-файла (x, y, facing, room, playtime). | [Сохранения](../systems/save-system.md) |

### `scripts/scr_saveSave/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_saveSave` | `scr_saveSave()` | Пишет текущее состояние сессии в слот global.current_save_slot. | [Сохранения](../systems/save-system.md) |

### `scripts/scr_settingsManager/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_settings_parse_real` | `scr_settings_parse_real(value_str, fallback)` | Преобразует строку из файла настроек в число. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_settings_safe_volume` | `scr_settings_safe_volume(v)` | Возвращает громкость в диапазоне 0..1; нечисловое значение или NaN заменяет на 1. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_loadSettings` | `scr_loadSettings()` | Загружает настройки из файла. Если файла нет, возвращает настройки по умолчанию. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_saveSettings` | `scr_saveSettings(settings)` | Сохраняет переданные настройки в файл. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_applySettings` | `scr_applySettings(settings)` | Применяет настройки к игре (изменяет громкость, разрешение, включает дебаг). | [UI и меню](../systems/ui-and-menus.md) |
| `scr_resetSettings` | `scr_resetSettings()` | Сбрасывает все настройки к значениям по умолчанию (копия + apply/save). | [UI и меню](../systems/ui-and-menus.md) |
| `scr_settings_deep_copy` | `scr_settings_deep_copy(settings)` | Создаёт точную копию структуры настроек . | [UI и меню](../systems/ui-and-menus.md) |
| `scr_settings_apply_and_save` | `scr_settings_apply_and_save(local_settings, mode = "both")` | Применяет и/или сохраняет настройки | [UI и меню](../systems/ui-and-menus.md) |
| `scr_resetInputToDefault` | `scr_resetInputToDefault(settings)` | Сбрасывает только клавиши управления к дефолту | [UI и меню](../systems/ui-and-menus.md) |
| `scr_settings_misc_items` | `scr_settings_misc_items()` | Единый источник раскладки пунктов категории «Разное» меню настроек: возвращает упорядоченный массив строковых id пунктов. | [UI и меню](../systems/ui-and-menus.md) |
| `scr_buildInputMap` | `scr_buildInputMap(settings)` | Создает структуру "действие -> массив клавиш" для системы ввода. | [Ввод](../systems/input.md) |

### `scripts/scr_settings_step_category/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_settings_step_category` | `scr_settings_step_category(actions)` | Обработка выбранной категории настроек (навигация и подтверждения). | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_settings_step_confirm_reset/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_settings_step_confirm_reset` | `scr_settings_step_confirm_reset(actions)` | Экран подтверждения сбросов (управление и полный сброс игры). | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_settings_step_rebind/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_settings_step_rebind` | `scr_settings_step_rebind(actions)` | Обработка режима переназначения клавиш. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_settings_step_root/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_settings_step_root` | `scr_settings_step_root(actions)` | Обрабатывает корневой список категорий меню настроек. | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_toggle_debug_flag/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_toggle_debug_flag` | `scr_toggle_debug_flag(flag_name)` | Переключает debug-флаг. Источник истины — global.* (читается obj_globalManager/Draw_64); instance-копий на игроке больше нет, так что переключение работает и без… | [Отладка и тесты](../systems/debug-and-testing.md) |

### `scripts/scr_ui_list_controller/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_ui_list_controller` | `scr_ui_list_controller(index, count, rows_per_col, columns, actions)` | Универсальная навигация по списку с несколькими колонками | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_ui_nav_vertical/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_ui_nav_vertical` | `scr_ui_nav_vertical(index, count, wrap, actions)` | Простая вертикальная навигация по списку | [UI и меню](../systems/ui-and-menus.md) |

### `scripts/scr_ui_read_actions/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_ui_read_actions` | `scr_ui_read_actions(exclude_self = false)` | Единое чтение ввода для меню (up/down/left/right/confirm/back/delete) | [UI и меню](../systems/ui-and-menus.md) |

## DSL-команды катсцен (`scripts/c_*`, `c_cmd.gml`)

### `scripts/c_autofacing/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_autofacing` | `c_autofacing(_target, _enabled)` | Устанавливает `auto_face` цели через `ActionSetProperty` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_autowalk/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_autowalk` | `c_autowalk(_target, _enabled)` | Устанавливает `auto_walk` цели через `ActionSetProperty` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_begin/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_begin` | `c_begin(_id = "")` | Открывает сессию сборки катсцены: создаёт build-менеджер `obj_cutsceneManager` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_cmd/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `__get_active_mgr` | `__get_active_mgr()` | Возвращает активный менеджер катсцены или недособранный build-менеджер | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_builder_add` | `__cutscene_builder_add(_action)` | Добавляет action в очередь активного/build-менеджера через `cutscene_add` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_selected_actor` | `__cutscene_selected_actor()` | Возвращает актёра, выбранного командой (для команд без явной цели) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_cmd_target_missing` | `__cutscene_cmd_target_missing(_target)` | Проверяет, что цель не задана (`noone`/`undefined`/пустая строка) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_cmd_require_target` | `__cutscene_cmd_require_target(_cmd_name, _target)` | Гейт `c_*`-команды: без цели пишет warning в лог и возвращает `false` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_bridge_real` | `__cutscene_bridge_real(_value, _default = 0)` | Приводит аргумент из Chatterbox к числу; нечисловой/пустой вход → `_default` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_bridge_real_opt` | `__cutscene_bridge_real_opt(_value)` | Числовой мост для опциональных аргументов команд: отсутствующий или нечисловой вход → undefined (дефолт возьмёт конструктор Action). | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `__cutscene_bridge_color` | `__cutscene_bridge_color(_value, _default = c_black)` | Приводит аргумент Chatterbox к константе цвета (имя или число) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_play_json` | `cutscene_play_json(_path)` | Загружает JSON-катсцену (`cutscene_load_json`) и сразу запускает её | [JSON-экшены](../cutscenes/json-actions.md) |
| `c_play_json` | `c_play_json(_path)` | Алиас `cutscene_play_json` | [JSON-экшены](../cutscenes/json-actions.md) |
| `cutscene_stop_active` | `cutscene_stop_active()` | Останавливает активную катсцену (`finish_cutscene`); возвращает `true`/`false` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_is_active` | `cutscene_is_active()` | Возвращает `global.cutscene_active` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_dialogue_is_active` | `cutscene_dialogue_is_active()` | Проверяет, идёт ли диалог, открытый катсценой | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_register_chatterbox_functions` | `cutscene_register_chatterbox_functions()` | Регистрирует `c_*`-команды как функции Chatterbox для вызова из yarn | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_dialogue` | `c_dialogue(_file, _node = undefined)` | Добавляет `ActionDialogue` — запуск yarn-диалога | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_animate` | `c_animate(_target, _sprite, _image_index = undefined, _image_speed = undefined)` | Добавляет `ActionAnimate` — смена спрайта/кадра/скорости анимации цели | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_tween` | `c_tween(_target, _property, _to_value, _frames, _easing = undefined, _from_value = undefined, _kind = "instance")` | Добавляет `ActionTween` — твин свойства цели (или камеры при `kind="camera"`) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_tween_camera` | `c_tween_camera(_property, _to_value, _frames, _easing = undefined, _from_value = undefined)` | Добавляет `ActionTween` для свойства камеры | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_fadein` | `c_fadein(_frames, _color = undefined)` | Добавляет `ActionFadeIn` — проявление экрана за N кадров | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_fadeout` | `c_fadeout(_frames, _color = undefined)` | Добавляет `ActionFadeOut` — затемнение экрана за N кадров | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_sfx` | `c_sfx(_sound_or_key, _volume = undefined, _pitch = undefined)` | Добавляет `ActionPlaySFX` — проигрывание звука | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_emote` | `c_emote(_target, _sprite = undefined, _frames = undefined, _offset_x = undefined, _offset_y = undefined, _scale = undefined)` | Добавляет `ActionEmote` — эмоция над целью | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_jump` | `c_jump(_target, _x, _y, _frames, _height = undefined, _easing = undefined)` | Добавляет `ActionJump` — прыжок цели в точку | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_halt` | `c_halt(_target = undefined)` | Добавляет `ActionHalt` — остановка движения цели (без аргумента — выбранного актёра) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_flip` | `c_flip(_target, _flipped = undefined)` | Добавляет `ActionFlip` — горизонтальное отражение спрайта цели | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_spin` | `c_spin(_target, _speed, _frames = undefined)` | Добавляет `ActionSpin` — вращение цели | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_shakeobj` | `c_shakeobj(_target = undefined, _frames = undefined, _magnitude = undefined)` | Добавляет `ActionShakeObject` — тряска цели (без аргумента — выбранного актёра) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_visible` | `c_visible(_target, _visible = undefined)` | Устанавливает `visible` цели через `ActionSetProperty` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_instant` | `c_instant(_enabled = undefined)` | Добавляет `ActionSetInstantMode` — мгновенное выполнение действий | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_walk` | `c_walk(_target, _dir, _speed, _frames, _use_collision = undefined)` | Добавляет `ActionMoveRelativeDirection` — движение по направлению N кадров | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_walkdirect` | `c_walkdirect(_target, _x, _y, _frames, _use_collision = undefined)` | Добавляет `ActionMoveDirect` — движение к точке за N кадров | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_walkdirect_speed` | `c_walkdirect_speed(_target, _x, _y, _speed, _use_collision = undefined)` | Добавляет `ActionMoveDirect` — движение к точке с заданной скоростью | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_waittalk` | `c_waittalk()` | Добавляет `ActionWaitForDialogue` — ждать завершения реплики | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_sprite` | `c_sprite(_target, _sprite, _image_index = undefined, _image_speed = undefined)` | Алиас `c_animate` (`ActionAnimate`) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_soundplay` | `c_soundplay(_sound_or_key, _volume = undefined, _pitch = undefined)` | Алиас `c_sfx` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_var_instance` | `c_var_instance(_target, _property, _value)` | Добавляет `ActionSetProperty` — присвоить свойство цели | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_var_lerp_instance` | `c_var_lerp_instance(_target, _property, _from, _to, _frames, _easing = undefined)` | Добавляет `ActionTween` — твин свойства с явным начальным значением | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_lerp` | `c_lerp(_target, _property, _from, _to, _frames, _easing = undefined)` | Прокси к `c_var_lerp_instance` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `c_var_lerp_to_instance` | `c_var_lerp_to_instance(_target, _property, _to, _frames, _easing = undefined)` | Добавляет `ActionTween` — твин свойства от текущего значения | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_cmd_x/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_cmd_x` | `c_cmd_x(arg0, arg1, arg2, arg3, arg4, arg5, arg6)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_delaycmd/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_delaycmd` | `c_delaycmd(_target, _delay_frames, _inner_cmd, _arg0)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_delaywalk/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_delaywalk` | `c_delaywalk(_target, _delay_frames, _dir, _speed, _frames)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_depth/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_depth` | `c_depth(_target, _depth)` | DSL-команда «depth»: задаёт цели глубину и переводит её в manual-режим par_depth. | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_end/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_end` | `c_end(_mgr = noone)` | Завершает сессию катсцены. Порядок целей: явный менеджер → build-менеджер (отмена недособранной сцены) → активная катсцена (остановка играющей, как cutscene_stop_active). | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_facing/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_facing` | `c_facing(_target, _dir)` | Добавляет разворот цели (`cutscene_set_facing` → `ActionSetFacing`) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_instance/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_instance` | `c_instance(_key, _x, _y)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_pan/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_pan` | `c_pan(_x, _y, _frames)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_pan_wait/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_pan_wait` | `c_pan_wait(arg0, arg1, arg2)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_panobj/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_panobj` | `c_panobj(_target, _frames)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_panspeed/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_panspeed` | `c_panspeed(_x, _y, _frames)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_play/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_play` | `c_play(_mgr = noone)` | Запускает собранную катсцену (`start_cutscene`); без менеджера — warning + `noone` | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_setxy/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_setxy` | `c_setxy(_target, _x, _y)` | Добавляет `ActionSetXY` — мгновенный телепорт цели | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_shake/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_shake` | `c_shake(_frames = undefined, _magnitude = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_speaker/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_speaker` | `c_speaker(_speaker_name)` | Устанавливает имя спикера (nameplate) активного диалогового окна | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/c_wait/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `c_wait` | `c_wait(_frames)` | Добавляет `ActionWait` — пауза очереди на N кадров | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

## Обёртки и загрузчики катсцен (`scripts/cutscene_*`)

### `scripts/cutscene_action_factory/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_init_action_factory` | `cutscene_init_action_factory()` | Заполняет `global.__cutscene_action_factory` — dispatch типа JSON-экшена → конструктор `Action*` | [JSON-экшены](../cutscenes/json-actions.md) |

### `scripts/cutscene_actor_create/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_actor_create` | `cutscene_actor_create(_target_key, _x, _y, _sprite_or_obj = undefined, _copy_from = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_actor_destroy/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_actor_destroy` | `cutscene_actor_destroy(_target_ref)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_add/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_add` | `cutscene_add(_mgr, _action)` | Добавляет action-структуру в очередь менеджера катсцен. | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_tween` | `cutscene_tween(_target, _property, _to_value, _frames, _easing = undefined, _from_value = undefined, _kind = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_fade_in` | `cutscene_fade_in(_frames, _color = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_fade_out` | `cutscene_fade_out(_frames, _color = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_play_sfx` | `cutscene_play_sfx(_sound_or_key, _volume = undefined, _pitch = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_emote` | `cutscene_emote(_target, _sprite = undefined, _frames = undefined, _offset_x = undefined, _offset_y = undefined, _scale = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_jump` | `cutscene_jump(_target, _x, _y, _frames, _height = undefined, _easing = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_halt` | `cutscene_halt(_target)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_flip` | `cutscene_flip(_target, _flipped = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_spin` | `cutscene_spin(_target, _speed, _frames = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_shake_object` | `cutscene_shake_object(_target, _frames = undefined, _magnitude = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_set_visible` | `cutscene_set_visible(_target, _visible = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_set_instant` | `cutscene_set_instant(_enabled = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_wait_for_dialogue` | `cutscene_wait_for_dialogue(_dialogue_controller = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |
| `cutscene_set_property` | `cutscene_set_property(_target, _property, _value, _kind = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_animate/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_animate` | `cutscene_animate(_target_ref, _sprite, _image_index_set = undefined, _image_speed_set = undefined)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_auto_facing_toggle/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_auto_facing_toggle` | `cutscene_auto_facing_toggle(_target_ref, _enabled)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_auto_walk_toggle/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_auto_walk_toggle` | `cutscene_auto_walk_toggle(_target_ref, _enabled)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_branch/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_branch` | `cutscene_branch(_condition_func, _true_actions, _false_actions = [])` | Return an ActionBranch struct | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_camera_center/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_camera_center` | `cutscene_camera_center(_center_x, _center_y)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [Архитектура катсцен](../cutscenes/architecture.md) |

### `scripts/cutscene_camera_pan/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_camera_pan` | `cutscene_camera_pan(_view_x, _view_y, _frames)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [Архитектура катсцен](../cutscenes/architecture.md) |

### `scripts/cutscene_camera_shake/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_camera_shake` | `cutscene_camera_shake(_frames, _magnitude = 4)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [Архитектура катсцен](../cutscenes/architecture.md) |

### `scripts/cutscene_camera_track/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_camera_track` | `cutscene_camera_track(_target_ref, _frames, _offset_x = 0, _offset_y = 0)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [Архитектура катсцен](../cutscenes/architecture.md) |

### `scripts/cutscene_dialogue/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_dialogue` | `cutscene_dialogue(_filename, _node)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_follow_path/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_follow_path` | `cutscene_follow_path(_target_ref, _points, _speed = 2, _collision = false)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_load_engine_settings/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_load_engine_settings` | `cutscene_load_engine_settings(_force_reload = false)` | Загружает глобальные настройки движка катсцен | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_default_engine_settings` | `__cutscene_default_engine_settings()` | Возвращает настройки по умолчанию (безопасные значения) | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_parse_engine_settings` | `__cutscene_parse_engine_settings(_map)` | Парсит настройки из struct и заполняет пропуски | [Архитектура катсцен](../cutscenes/architecture.md) |
| `__cutscene_json_get_string_array` | `__cutscene_json_get_string_array(_map, _key, _default = [])` | Берёт массив строк из struct | [JSON-экшены](../cutscenes/json-actions.md) |

### `scripts/cutscene_load_json/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_load_json` | `cutscene_load_json(_path)` | Читает JSON-файл катсцены и собирает менеджер с очередью действий | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_action_from_struct` | `__cutscene_json_action_from_struct(_mgr, _map, _fps)` | Создаёт Action из JSON-объекта | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_normalize_action_type` | `__cutscene_json_normalize_action_type(_type)` | Нормализует legacy-алиасы типов экшенов (`shakeobj` → `shake_object` и т.д.) | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_parse_direction` | `__cutscene_json_parse_direction(_val)` | Конвертирует значение направления (строка или число) в числовой DIR | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_string` | `__cutscene_json_get_string(_map, _key, _default = "")` | Берёт строку из struct с дефолтом | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_real` | `__cutscene_json_get_real(_map, _key, _default = 0)` | Берёт число из struct с дефолтом | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_real_opt` | `__cutscene_json_get_real_opt(_map, _key)` | Берёт число из struct; отсутствие ключа или нечисловое значение → undefined | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_bool` | `__cutscene_json_get_bool(_map, _key, _default = false)` | Берёт булево из struct (true/false или 1/0) | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_value` | `__cutscene_json_get_value(_map, _key, _default = undefined)` | Берёт значение из struct (любого типа: scalar/struct/array) | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_frames` | `__cutscene_json_get_frames(_map, _fps, _default = 0)` | Читает длительность: `frames` приоритетнее `seconds`/`duration`/`time` | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_color` | `__cutscene_json_get_color(_map, _key, _default = c_black)` | Читает цвет из JSON-поля (строка-имя или число) | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_target` | `__cutscene_json_get_target(_map)` | Берёт target из struct (target или target_ref) | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_get_seconds` | `__cutscene_json_get_seconds(_map, _default = 0)` | Берёт длительность в секундах из struct | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_points_to_array` | `__cutscene_json_points_to_array(_data)` | Преобразует массив точек из JSON в массив {x,y}-struct | [JSON-экшены](../cutscenes/json-actions.md) |
| `__cutscene_json_seconds_to_frames` | `__cutscene_json_seconds_to_frames(_seconds, _fps)` | Конвертирует секунды в кадры | [JSON-экшены](../cutscenes/json-actions.md) |

### `scripts/cutscene_move/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_move` | `cutscene_move(_target_ref, _x, _y, _speed = 1, _collision = false)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_parallel/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_parallel` | `cutscene_parallel(_actions_array)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_run_function/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_run_function` | `cutscene_run_function(_func, _args = [])` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_set_depth/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_set_depth` | `cutscene_set_depth(_target_ref, _depth)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_set_facing/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_set_facing` | `cutscene_set_facing(_target_ref, _direction)` | Возвращает действие, которое мгновенно разворачивает актёра (спрайт движения + facing_direction) при старте катсценного шага. | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_set_xy/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_set_xy` | `cutscene_set_xy(_target_ref, _x, _y)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

### `scripts/cutscene_wait/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `cutscene_wait` | `cutscene_wait(_seconds)` | Недостижимая команда/обёртка — тело зачищено (DELETE_CANDIDATE) | [GML DSL катсцен](../cutscenes/gml-dsl.md) |

## Прочие скрипты

### `scripts/actor_display_name/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `actor_display_name` | `actor_display_name(_actor_key)` | Возвращает человекочитаемое имя для actor code (для nameplate в textbox). | [Диалоги](../systems/dialogue.md) |

### `scripts/constructorsForInventory/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `Item` | `Item(_name, _description = "An Item") constructor` | Базовый конструктор предмета инвентаря | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `WeaponItem` | `WeaponItem(_name, _damage = 20, _description = "A Weapon") constructor` | Оружие: предмет со статом damage, use() надевает его в global.equipped_weapon. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `ArmorItem` | `ArmorItem(_name, _defense = 9, _description = "Armor") constructor` | Броня: предмет со статом defense, use() надевает её в global.equipped_armor. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `FoodItem` | `FoodItem(_name, _amount = 1, _heal = 10, _description = "Some food") constructor` | Еда: расходуемый предмет, use() лечит global.stat_hp и уменьшает amount. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `item_deserialize` | `item_deserialize(_data)` | Фабрика десериализации: восстанавливает предмет по полю __type из сейва. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `inventory_serialize` | `inventory_serialize(_inv_array)` | Сериализация всего инвентаря в массив плоских struct для сейва. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `inventory_deserialize` | `inventory_deserialize(_json_array)` | Десериализация всего инвентаря: инвариант — ровно 8 слотов. | [Инвентарь и статы](../systems/inventory-and-stats.md) |

### `scripts/draw_text_scribble/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `draw_text_scribble` | `draw_text_scribble(_x, _y, _string, _reveal = undefined)` | Эмуляция `draw_text()` через Scribble; вызовы только у placeholder-объектов `obj_p3r_*` (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |

### `scripts/draw_text_scribble_ext/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `draw_text_scribble_ext` | `draw_text_scribble_ext(_x, _y, _string, _width, _reveal = undefined)` | Эмуляция `draw_text_ext()` через Scribble | [Диалоги](../systems/dialogue.md) |

### `scripts/interactionWithMainCast/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `interactionWithMainCast` | `interactionWithMainCast(_scriptToReadFrom, _node)` | Мёртвая legacy-обёртка над `scr_interaction` (DELETE_CANDIDATE, тело зачищено) | [Взаимодействие](../systems/interaction.md) |

### `scripts/interactionWithNPCsOrObjects/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `scr_interaction` | `scr_interaction(_scriptToReadFrom, _node, _use_mask_check = false)` | Единая проверка взаимодействия с объектом через маркер перед игроком. | [Взаимодействие](../systems/interaction.md) |
| `interactionWithNPCsOrObjects` | `interactionWithNPCsOrObjects(_scriptToReadFrom, _node)` | Мёртвая legacy-обёртка над `scr_interaction` (DELETE_CANDIDATE, тело зачищено) | [Взаимодействие](../systems/interaction.md) |

### `scripts/map_emotions/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `map_emotions` | `map_emotions(_actor, _emotion)` | Возвращает ресурсы портрета и звука для actor/emotion. | [Диалоги](../systems/dialogue.md) |

### `scripts/playableCharacterInfo/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `playableCharacterInfo` | `playableCharacterInfo(_name = "Chara", _lv = 20, _hp = 99, _money = 20) constructor` | Конструктор данных игрового персонажа (не используется — DELETE_CANDIDATE). | [Инвентарь и статы](../systems/inventory-and-stats.md) |

### `scripts/readDialogue/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `readDialogue` | `readDialogue(_filename, _nodename)` | Открывает диалоговое окно: создаёт textboxTest_scribble и передаёт ему yarn-файл и стартовую ноду. | [Диалоги](../systems/dialogue.md) |

### `scripts/script_items/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `item_database_register` | `item_database_register(_name, _factory)` | Регистрирует фабрику для предмета по имени. Позволяет расширять базу предметов без модификации item_database. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `item_database` | `item_database(_name)` | Фабрика предметов: по имени возвращает НОВЫЙ экземпляр Item-наследника. Используется при создании предметов из катсцен, дропов, чит-кодов. | [Инвентарь и статы](../systems/inventory-and-stats.md) |
| `inventory_add` | `inventory_add(_item_or_name)` | Добавляет предмет в первый свободный слот global.inventory. | [Инвентарь и статы](../systems/inventory-and-stats.md) |

### `scripts/string_height_scribble/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `string_height_scribble` | `string_height_scribble(_string)` | Эмуляция `string_height()` через Scribble; вызовов в проекте нет (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |

### `scripts/string_height_scribble_ext/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `string_height_scribble_ext` | `string_height_scribble_ext(_string, _width)` | Эмуляция `string_height()` с переносом по ширине через Scribble (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |

### `scripts/string_length_scribble/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `string_length_scribble` | `string_length_scribble(_string)` | Эмуляция `string_length()` через Scribble (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |

### `scripts/string_width_scribble/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `string_width_scribble` | `string_width_scribble(_string)` | Эмуляция `string_width()` через Scribble (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |

### `scripts/string_width_scribble_ext/`

| Функция | Сигнатура | Назначение | Док-страница |
| --- | --- | --- | --- |
| `string_width_scribble_ext` | `string_width_scribble_ext(_string, _width)` | Эмуляция `string_width()` с переносом по ширине через Scribble (DELETE_CANDIDATE) | [Диалоги](../systems/dialogue.md) |

## См. также

- [Объекты и события](objects-and-events.md) — справочник объектов
- [Глоссарий](glossary.md) — термины проекта
- [GML DSL катсцен](../cutscenes/gml-dsl.md) — команды `c_*` в контексте движка

<!-- sources: _meta/scripts.txt; scripts/**/*.gml (/// @desc/@description/@summary); docs_new/_meta/nav_plan.md -->
