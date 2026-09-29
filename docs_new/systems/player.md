---
title: Игрок (obj_player)
tags:
  - player
  - movement
  - collision
  - depth
  - persistence
---

# Игрок (`obj_player`)

`obj_player` — управляемый персонаж: persistent-инстанс, который переживает переходы между комнатами, читает ввод движения, разрешает коллизии со стенами и склонами, держит маркер взаимодействия и центрирует камеру. Родитель — `par_actor` (цепочка `par_actor` → `par_depth`), спрайт и маска — `spr_Chara_walking_D`.

## События

| Событие | Файл | Содержание |
|---------|------|------------|
| Create | `objects/obj_player/Create_0.gml` | Дедупликация инстансов, инициализация полей, `resolve_solid`/`solid_free`, спавн-оверрайд `global.__next_spawn_*`, unstuck при спавне внутри стены, создание `obj_pointMarker` |
| Step | `objects/obj_player/Step_0.gml` | Конвейер кадра: `scr_player_debug_ghost` → `scr_player_ui_blocking` → `scr_player_room_lock` → `scr_player_movement` → `scr_player_animation` → `scr_player_facing` → `scr_player_marker_update` → `event_inherited()` (depth) |
| Begin Step | `objects/obj_player/Step_1.gml` | `__room_born = room`, сброс `__dedup_survivor` |
| End Step | `objects/obj_player/Step_2.gml` | Follow-камера `view_camera[0]` |
| CleanUp | `objects/obj_player/CleanUp_0.gml` | Уничтожение `marker_id`, инвалидация `global.obj_player` |

Draw-событие не зарегистрировано: `Draw_0.gml` — файл-сирота, спрайт рисует движок.

## Persistent и дедупликация

`obj_player` помечен `persistent: true`: при `room_goto` инстанс переносится в новую комнату, а редакторская копия игрока в этой комнате создаёт дубль. Create каждого инстанса выбирает выжившего:

- `__room_born`: комната, в которой выполнен Create инстанса. Перенесённый инстанс на стартовой волне Create держит `__room_born` прошлой комнаты. Это и есть признак выжившего.
- `__dedup_survivor`: метка «уже выбранного выжившего». Действует только на стартовой волне Create (случай двух редакторских дублей: поздний Create иначе убил бы «осевшего» игрока). Сбрасывается в Begin Step.
- Create дубля уничтожает всех, кроме выжившего, и завершается по `exit`: дубль не пишет `global.obj_player` и не создаёт маркер.

Позиция выжившего разрешается по приоритету:

1. `global.__next_spawn_x` / `global.__next_spawn_y` / `global.__next_spawn_facing`: явный спавн-оверрайд (пишут `scr_saveLoad` при загрузке сейва и `scr_defaultLoad` при новой игре; `obj_Init` лишь инициализирует их в `undefined`). Применяется к выжившему, глобалы обнуляются в `undefined`. Facing дополнительно ставит спрайт через `scr_sprite_for_facing`. DEV-спавн идёт по отдельному каналу `global.__dev_spawn_*` → `scr_global_handle_dev_spawn` и `__next_spawn_*` не трогает.
2. Если жив `obj_changingRoomsController`, позицию уже задал переход: контроллер пишет `obj_player.x = newX`, `obj_player.y = newY` сразу после `room_goto` (`scr_room_fade_update`), если переход не помечен `__player_pos_by_manager` (катсценный путь Room Start менеджера).
3. Иначе редакторские координаты дубля переносятся на выжившего.

После дедупа выживший «оседает»: `__room_born = room`, затем каждый Begin Step обновляет `__room_born` текущей комнатой. Поэтому второй Create от программного спавна отличается от перенесённого: «уроженец» комнаты без метки выжившего уничтожается дедупом нового инстанса. Сам DEV-спавн (`scr_global_handle_dev_spawn`, вызывает `obj_globalManager`) второй инстанс не создаёт: при живом игроке переставляет его, при отсутствии создаёт.

В конце Create инстанс пишет `global.obj_player = id`, глобальную ссылку на единственного игрока. CleanUp обнуляет её в `noone`, если ссылка указывает на уничтожаемый инстанс.

## Движение

`scr_player_movement` возвращает struct итогового ввода `{up, down, left, right}` с опциональным полем `slide_facing` (на пути с FSM его может не быть, читается через `variable_struct_exists`); результат читает и `scr_player_animation`.

Гарды ввода (в порядке проверки):

- `move_active`: прямой драйв координатами от катсцены (`ActionMove*`, хелперы `scr_cutscene_classes`). Пока флаг взведён, ввод игнорируется, `xspd`/`yspd` обнуляются. Страховка: при `move_active && !global.cutscene_active` флаг гасится, иначе игрок остался бы замороженным на всю сессию.
- `can_move` выставляет `scr_player_ui_blocking`: `false` при блокирующем UI (`scr_checkUIBlocking(false, false)`), `false` во время катсцены без partial control (`global.active_cutscene_manager.partial_control_type > 0` разрешает движение).
- `instance_exists(obj_changingRoomsController)`: на время фейда ввод не читается, скорость нулевая.

Скорости:

| Поле | Значение | Назначение |
|------|----------|------------|
| `walk_spd` | `1` | Шаг за кадр при ходьбе |
| `run_spd` | `1.6` | Шаг за кадр при зажатом действии `run` (дефолт `vk_shift`) |
| `current_spd` | `0` | Выбранная скорость кадра: `scr_input_down("run") ? run_spd : walk_spd` |
| `xspd`, `yspd` | `0` | Целочисленное смещение кадра после резолва дробной части |
| `x_frac`, `y_frac` | `0` | Аккумулятор дробной части шага |

Особенности расчёта:

- Противоположные клавиши оси разруливает FSM `scr_player_process_mutually_exclusive_inputs` (enum `PLAYER_AXIS_FSM`, состояния в полях `__v_fsm`/`__h_fsm`): при зажатых `up+down` или `left+right` приоритет у последней нажатой.
- Диагональная нормализация отсутствует намеренно (Delta-code стиль Undertale/Deltarune): по диагонали персонаж быстрее, но шаг кадра всегда строго целый, что убирает субпиксельный jitter и дрожание камеры.
- `run_spd` дробный: целая часть накапливается в `x_frac`/`y_frac`, на позицию применяется только `floor` от аккумулятора. Дробная часть самих `x`/`y` (после телепортов перехода или катсцены) забирается в аккумулятор: координаты возвращаются к целым без потери дистанции.
- `prev_x`/`prev_y` обновляются в начале функции до ранних выходов: `scr_player_animation` считает движение как «позиция сдвинулась за кадр».

Применение скорости:

- `ghost_mode == true`: `x += xspd; y += yspd` без коллизий.
- Иначе выполняется `scr_collision_resolve()`, затем `x += xspd; y += yspd`.

После резолва считается подсказка `slide_facing`: если ввод шёл в заблокированную ось, а тело едет по другой, в struct дописывается направление фактического движения; `scr_player_animation` ставит его приоритетнее ввода.

## Коллизии

Solid-группы — `obj_collider`, `par_decor`, `par_interactable`. Проверка «клетка свободна» — инстанс-функция `solid_free(_px, _py)`, объединяющая `place_meeting` по всем трём группам: поджатие к стене и step-up останавливаются перед любым solid-типом. `obj_slopeCollider` сюда не входит: треугольник склона легально пересекает bbox игрока и резолвится отдельно.

`scr_collision_resolve` вызывается из `scr_player_movement` до применения `xspd`/`yspd` и работает в контексте игрока:

1. `resolve_solid(obj_collider)` → `resolve_solid(par_decor)` → `resolve_solid(par_interactable)` (инстанс-метод из Create). Каждый проход предиктивно корректирует `xspd`/`yspd`: поджатие к стене попиксельно (лимит `max(1, ceil|xspd|, ceil|yspd|) + 1` шагов), step-up на низкий бортик до `ceil|xspd|` px при свободных клетках подъёма и назначения, snap-down (спуск на уступ до `ceil|xspd|` px), стык к полу/потолку по вертикали.
2. Склоны: `instance_place_list` по `obj_slopeCollider` в клетке `(x + xspd, y + yspd)` (broad-phase по прямоугольной маске `spr_collider`); каждый найденный клин резолвится `scr_player_slope_resolve`, следующий клин видит уже подправленные скорости.
3. Корректирующее выталкивание: резолв предиктивный и не выводит тело, уже сидящее внутри solid (пересекающиеся коллайдеры разных групп, сдвинувшийся коллайдер). Ищется ближайшая свободная клетка кольцами радиусом `1..16` по 8 направлениям (шаг 45°), координаты округляются.

Отдельный unstuck есть и в Create: при спавне внутри solid применяется спиральный поиск кольцами радиусом `1..50`, 8 лучей, кандидаты округляются и клампятся к границам комнаты до проверки.

## Склоны

`obj_slopeCollider` наследует `par_entity` напрямую: под `obj_collider` склон вёл бы себя как прямоугольная стена. Проверка двухфазная:

- **Broad phase**: прямоугольная маска `spr_collider` (`spriteMaskId` в `obj_slopeCollider.yy`): `instance_place_list` в `scr_collision_resolve` отбирает клинья, чей прямоугольник пересекает клетку назначения.
- **Narrow phase**: инстанс-метод `collision(_dx, _dy, _inst)`: `rectangle_in_triangle` прямоугольника `_inst` со смещением против треугольника `tri_x`/`tri_y`. Инстанс передаётся явно: на кадре перехода живых `obj_player` бывает два, и `obj_player.bbox_*` дал бы чужой прямоугольник.

Геометрию считает `slope_update_geometry` (Create и каждый Step, как страховка на случай изменения трансформа в рантайме):

- Базовый треугольник спрайта: залиты углы TL, BL, BR (прямой угол в BL), пустой — TR; читается tight-bbox спрайта, не инстанса (AABB повёрнутого прямоугольника шире треугольника).
- Локальные вершины масштабируются `image_xscale`/`image_yscale` и поворачиваются на `image_angle` (в GM против часовой стрелки) в room-координаты.
- `slope_in_x`/`slope_in_y`: единичная нормаль гипотенузы, смотрящая внутрь треугольника: от середины гипотенузы (TL→BR) к прямому углу (BL). По знаку компонент резолв отличает «пол» (нормаль вниз) от «потолка» (нормаль вверх).
- `dir`: legacy-поле совместимости: ближайший квадрант `floor(image_angle / 90) mod 4`, затем кумулятивно `+1` при `image_xscale < 0`, `+3` при `image_yscale < 0` и ещё `+2`, если отрицательны оба scale (итог по модулю 4).

`scr_player_slope_resolve(_slope)` выполняет два прохода скольжения с лимитом итераций `ceil(current_spd) + 1`:

- Горизонтальный: пока срабатывает `_slope.collision(xspd, 0, id)`, идёт сдвиг по Y на `−sign(slope_in_y)` (наружу из залитой части клина); каждый шаг требует свободной целевой клетки по всем трём solid-группам и по треугольникам соседних клиньев (`scr_player_cell_blocked_by_slope`, текущий склон исключается, промежуточная клетка на нём законна). Если скольжение не помогло, `xspd = 0` (стена).
- Вертикальный: симметрично, сдвиг по X на `−sign(slope_in_x)`, иначе `yspd = 0`.

Событие Collision у `obj_slopeCollider` пустое: обработка целиком в `scr_player_slope_resolve`.

## Анимация, facing и маркер

`facing_direction` — направление взгляда (`global.DIR`: `RIGHT=0`, `LEFT=1`, `UP=2`, `DOWN=3`). Источник истины — спрайт: `scr_player_facing` каждый Step синхронизирует поле через `scr_facing_for_sprite` (выходит, пока `global.active_cutscene_manager.is_running`); спрайт вне набора ходьбы (idle, эмоция от катсцены) даёт `-1`; прежний facing сохраняется. При спавне поле ставится из `global.__next_spawn_facing` или `global.DIR.UP`.

`scr_player_animation(ui_blocking, movement_inputs)`:

- Не работает во время катсцены (`global.cutscene_active` или `global.active_cutscene_manager.is_running`).
- Выбор спрайта по приоритету: `slide_facing` → `right` → `left` → `down` → `up` (на диагонали спрайт всегда горизонтальный, осознанный Undertale-стиль). Маппинг: `scr_sprite_for_facing` → `spr_Chara_walking_{R,L,D,U}`.
- `is_moving`: фактическое смещение (`x`/`y` ≠ `prev_x`/`prev_y`). При блокировке или стоянии: `image_speed = 0`, `image_index = 0`. При движении с нажатыми клавишами: `image_speed = current_spd / walk_spd`, частота кадров масштабируется под бег; старт с `image_index = 1`, чтобы не мелькал idle-кадр.

`marker_id` — невидимый `obj_pointMarker` (persistent), создаётся в Create на слое `scr_layer_ensure_instances()`. У маркера собственный дедуп (`instance_number(obj_pointMarker) > 1` → самоуничтожение) и пересоздание в `scr_player_marker_update` при внешней потере. Позиция по `facing_direction` от origin игрока (низ спрайта):

| Facing | Точка маркера |
|--------|---------------|
| `RIGHT` | `(x + 15, y − 6)` |
| `LEFT` | `(x − 15, y − 6)` |
| `UP` | `(x, y − 15)` |
| `DOWN` | `(x, y + 5)` |

Читатели маркера — `scr_interaction` (скрипт `interactionWithNPCsOrObjects`: `point_in_rectangle` по bbox интерактива, `position_meeting` по маске при `_use_mask_check`), `obj_save`, `obj_sound_test`; все берут точку через `global.obj_player.marker_id`, а не по object index: при дубле `obj_pointMarker` тот отдал бы чужой инстанс. `instance_find(obj_pointMarker, 0)` применяет только сам игрок: при перехвате живого маркера в Create и в `scr_player_marker_update`. Debug-отрисовку кружка по F3 делает `obj_globalManager` Draw GUI.

## Depth и камера

Глубину обрабатывает `par_depth` через `event_inherited()` в конце Step; ручного `depth = -y` у игрока нет. У игрока `depth_mode` по умолчанию `"auto"`: `depth = -y` пересчитывается dirty-flag'ом при реальном смещении. Иерархия приоритетов `par_depth`: `attached_target` → `is_static` → `depth_mode == "manual"` (внешний код, например `ActionSetDepth` в катсценах) → авто.

Камера обрабатывается в End Step: `view_camera[0]` центрируется на игроке с клампом к границам комнаты (`clamp(x − vw/2, 0, room_width − vw)`, аналогично по Y), координаты целые. При `global.cutscene_camera_override` блок пропускается: камерой владеет катсцена.

## Ghost-режим и блокировка перехода

`ghost_mode` — эффективное значение двух независимых каналов:

| Канал | Кто пишет | Снятие |
|-------|-----------|--------|
| `debug_ghost` | F8 под `global.debug` (`scr_player_debug_ghost`) | Повторный F8 |
| `transition_ghost` | `scr_global_on_room_change` при смене комнаты | Таймер `global.__transition_safety_frames` (16 кадров) в `scr_global_transition_safety` |

Эффективный флаг: `ghost_mode = debug_ghost || transition_ghost`; каждый писатель обновляет его от своего канала. Пока окно безопасности активно, `scr_global_transition_safety` каждый кадр проверяет игрока на пересечение с solid и выталкивает кольцевым поиском (радиус до 32 px, среди свободных клеток выбирается ближайшая к точке входа `__transition_entry_x`/`__transition_entry_y`).

`room_change_lock` блокирует повторный триггер `objRoomChanger`: взводится при касании чейнджера и при смене комнаты; `scr_player_room_lock` сбрасывает его, когда игрок покинул хитбокс `objRoomChanger`.

## Ключевые поля инстанса

| Поле | Назначение |
|------|------------|
| `global.obj_player` | Единственная глобальная ссылка на игрока (Create/CleanUp) |
| `__room_born`, `__dedup_survivor` | Дедупликация persistent-инстанса (Create / Begin Step) |
| `walk_spd`, `run_spd`, `current_spd`, `xspd`, `yspd`, `x_frac`, `y_frac` | Скорости и аккумулятор дробного шага |
| `can_move` | Блокировка движения UI/катсценой (`scr_player_ui_blocking`) |
| `move_active`, `target_x`, `target_y`, `auto_face` | Контракт с катсценами: прямой драйв координатами (`ActionMove*`) |
| `facing_direction` | Направление взгляда; синхрон со спрайтом |
| `current_emotion` | Эмоция по умолчанию (`"default"`) для fallback катсцен и диалога |
| `debug_ghost`, `transition_ghost`, `ghost_mode` | Каналы призрачного режима |
| `room_change_lock` | Блок повторного триггера `objRoomChanger` |
| `marker_id` | Ссылка на `obj_pointMarker` |
| `prev_x`, `prev_y` | Позиция начала кадра для `is_moving` |
| `__v_fsm`, `__h_fsm` | Состояния FSM взаимоисключающих клавиш |

## См. также

- [Ввод](input.md) — `scr_input_down`, действия `up`/`down`/`left`/`right`/`run`, ребинды
- [Взаимодействие](interaction.md) — читатели `obj_pointMarker`, `scr_interaction`
- [Переходы между комнатами](room-transitions.md) — `objRoomChanger`, `obj_changingRoomsController`, фейд
- [Система сохранений](save-system.md) — спавн-оверрайд `global.__next_spawn_*` при загрузке
- [Debug и тестирование](debug-and-testing.md) — F8 ghost-mode, debug-оверлей `obj_globalManager`
- [UI и меню](ui-and-menus.md) — `scr_checkUIBlocking`, блокировка ввода
- [Иерархия объектов](../architecture/object-hierarchy.md) — `par_depth`, `par_actor`, `par_entity`, `par_decor`, `par_interactable`
- [Глобальное состояние](../architecture/global-state.md) — `global.DIR`, `global.obj_player`, `global.__next_spawn_*`
- [Partial Control](../cutscenes/partial-control.md) — движение игрока во время катсцены

<!-- sources: objects/obj_player/Create_0.gml; objects/obj_player/Step_0.gml; objects/obj_player/Step_1.gml; objects/obj_player/Step_2.gml; objects/obj_player/CleanUp_0.gml; objects/obj_player/Draw_0.gml; objects/obj_player/obj_player.yy; scripts/scr_player_movement/scr_player_movement.gml; scripts/scr_player_process_mutually_exclusive_inputs/scr_player_process_mutually_exclusive_inputs.gml; scripts/scr_collision_resolve/scr_collision_resolve.gml; scripts/scr_player_slope_resolve/scr_player_slope_resolve.gml; objects/obj_slopeCollider/Create_0.gml; objects/obj_slopeCollider/Step_0.gml; objects/obj_slopeCollider/Collision_obj_player.gml; objects/obj_slopeCollider/obj_slopeCollider.yy; scripts/scr_player_animation/scr_player_animation.gml; scripts/scr_player_facing/scr_player_facing.gml; scripts/scr_player_marker_update/scr_player_marker_update.gml; scripts/scr_player_ui_blocking/scr_player_ui_blocking.gml; scripts/scr_player_debug_ghost/scr_player_debug_ghost.gml; scripts/scr_player_room_lock/scr_player_room_lock.gml; objects/par_depth/Create_0.gml; objects/par_depth/Step_0.gml; objects/par_actor/par_actor.yy; objects/par_entity/Create_0.gml; objects/obj_pointMarker/Create_0.gml; objects/obj_pointMarker/obj_pointMarker.yy; objects/objRoomChanger/Collision_obj_player.gml; scripts/scr_room_fade_update/scr_room_fade_update.gml; scripts/scr_global_on_room_change/scr_global_on_room_change.gml; scripts/scr_global_transition_safety/scr_global_transition_safety.gml; scripts/scr_global_handle_dev_spawn/scr_global_handle_dev_spawn.gml; scripts/scr_constants/scr_constants.gml; scripts/scr_saveLoad/scr_saveLoad.gml; scripts/scr_defaultLoad/scr_defaultLoad.gml; scripts/scr_global_debug_hotkeys/scr_global_debug_hotkeys.gml; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml; scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml; scripts/scr_layer_ensure_instances/scr_layer_ensure_instances.gml; scripts/scr_inputApi/scr_inputApi.gml; scripts/scr_settingsManager/scr_settingsManager.gml; objects/obj_Init/Create_0.gml; objects/obj_globalManager/Step_0.gml; objects/obj_globalManager/Draw_64.gml; objects/obj_save/Step_0.gml; objects/obj_sound_test/Step_0.gml -->
