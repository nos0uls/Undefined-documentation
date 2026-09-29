---
title: Иерархия объектов
tags:
  - architecture
  - objects
  - depth
  - interaction
  - save-system
---

# Иерархия объектов

Дерево наследования всех 53 объектов проекта и контракты родителей `par_*`: глубина (`par_depth`), персистентное состояние сущностей (`par_interactable`), декорации (`par_decor`), актёры (`par_actor`) и маркер gameplay-объектов (`par_entity`).

## Дерево наследования { #tree }

Построено по `parentObjectId` из `objects/*/*.yy`. Два корня-родителя: `par_depth` (Z-сортировка) и `par_entity` (маркер без родителя).

```text
par_depth                        # корень: depth-контракт
├── par_actor                    # маркер движущихся актёров
│   ├── obj_actor                # generic actor (move_to_point, idle)
│   │   └── obj_dummy
│   └── obj_player               # persistent
├── par_decor                    # статичные декорации (is_static = true)
│   ├── bush
│   ├── obj_kachela
│   ├── obj_lantern
│   ├── obj_sign
│   ├── obj_tree1
│   ├── obj_tree2
│   ├── pinkBench
│   ├── sand
│   └── spr_pinkBench
├── par_interactable             # интерактивные объекты (entity_state)
│   ├── npc1
│   │   └── npc2
│   ├── obj_asher
│   ├── obj_bench
│   ├── obj_dialoguetest
│   ├── obj_save
│   └── obj_sheepFountain
└── obj_visualObject             # спрайт без коллизии (sprite_override)

par_entity                       # корень-маркер, без родителя и полей
├── obj_collider                 # прямоугольный коллайдер
└── obj_slopeCollider            # треугольный коллайдер склона
```

!!! note "obj_slopeCollider: прямой наследник par_entity"
    `obj_slopeCollider` наследует `par_entity` напрямую, минуя `obj_collider`: под `obj_collider` склон вёл себя как прямоугольная стена, и узкая треугольная проверка `collision()` не доходила до дела (`objects/obj_slopeCollider/Create_0.gml`).

Объекты без родителя (не входят в gameplay-иерархию):

- **Persistent-контроллеры**: `obj_Init`, `obj_globalManager`, `obj_cutsceneManager`, `obj_music_ctrl`, `obj_changingRoomsController`, `obj_pointMarker`, `o_SharedTweener`, `screenshot`;
- **Меню и UI**: `obj_menu`, `obj_inGameMenu`, `obj_settingsManager`, `obj_saveManager`, `obj_menuBGSpriteChanger`, `obj_p3r_background`, `obj_p3r_pause`, `obj_p3r_settings`, `obj_p3r_title`, `obj_p3r_transition`;
- **Прочее**: `objRoomChanger`, `obj_anim`, `obj_face`, `textboxTest_scribble`, `obj_devLoader`, `obj_cutsceneTest`, `obj_menuTest`, `obj_sound_test`.

## `par_depth`: контракт глубины { #par-depth }

Базовый родитель Z-сортировки для изометрического вида: чем ниже объект на экране, тем ближе к камере. В `Create_0` задаёт `depth = -y`: аргумент `depth` у `instance_create_depth` для наследников перезаписывается и мёртв.

Глубина управляется тремя полями, которые в `Step_0` образуют четыре режима по приоритету:

| Приоритет | Условие | Поведение |
|-----------|---------|-----------|
| 1 | `attached_target != noone` | Привязка: `depth` копируется из цели каждый кадр (шляпы, оружие на NPC). Цель уничтожена → привязка сбрасывается, один раз ставится `depth = -y`, дальше работает обычный режим |
| 2 | `is_static == true` | Заморозка: глубина вычислена один раз в `Create`, дальше не трогается. Ставят декорации (`par_decor`, `obj_visualObject`, `obj_bench`, `obj_save`) |
| 3 | `depth_mode == "manual"` | Ручной режим: `par_depth` не трогает `depth`, её задаёт внешний код. Ставят `ActionSetDepth` и `c_depth` через макрос `__CUTSCENE_DEPTH_MODE_MANUAL` |
| 4 | `depth_mode == "auto"` (по умолчанию) | Авто: `depth = -y`, пересчёт только при реальном сдвиге (dirty-flag по `__depth_prev_x`/`__depth_prev_y`) |

Ключевые правила контракта:

- У `depth_mode` ровно два осмысленных значения: `"auto"` и `"manual"`; любое другое молча эквивалентно `"auto"`. `is_static` и `attached_target` — отдельные поля, а не значения `depth_mode`.
- Запись `depth` снаружи в режиме `"auto"` временна: перезапишется `-y` при первом сдвиге. Долговременная ручная глубина обязана ставить `depth_mode = "manual"`.
- Снапшот/restore катсцен (`__cutscene_snapshot_instance`/`__cutscene_apply_instance_snapshot` в `scr_cutscene_classes`) сохраняют и режим, и значение: после отката `depth_mode` возвращается к исходному.

!!! warning "Наследники со своим Step обязаны вызвать event_inherited()"
    Без `event_inherited()` в `Step_0` depth-FSM родителя не отработает и глубина перестанет обновляться. `par_depth/Step_0` специально не использует `exit`, чтобы дочерний код после `event_inherited()` не прерывался.

## `par_entity`: маркер gameplay-объектов { #par-entity }

Корень без родителя. `Create_0` содержит только комментарий: полей, методов и логики у `par_entity` нет; роль чисто группировочная. Выборки идут по object index наследников: `scr_collision_resolve()` проверяет `obj_collider` (стены) и `obj_slopeCollider` (склоны, метод `collision(_dx, _dy, _inst)` по треугольнику `tri_x`/`tri_y`).

Наследники `par_entity` не получают depth-сортировку: коллайдеры невидимы и не сортируются с актёрами.

## `par_interactable`: интерактивные объекты { #par-interactable }

Родитель всего, с чем игрок взаимодействует: NPC, скамейки, сейвпоинты. Наследует `par_depth`, добавляет поля сущности и методы реестра состояния.

### Поля

| Поле | Тип | Значение по умолчанию | Назначение |
|------|-----|----------------------|------------|
| `is_interactable` | bool | `true` | Отключает взаимодействие; читает `scr_interaction` |
| `category` | string | `"generic"` | Группировка (npc/prop/save…); читателей пока нет |
| `display_name` | string | `"Объект"` | Человекочитаемое имя; ждёт UI-потребителя |
| `entity_id` | string | см. ниже | Ключ записи в `global.entity_state` |
| `interaction_count` | real | `0` | Счётчик взаимодействий; инкрементит `scr_interaction` |
| `seen_dialogues` | array | `[]` | Ключи `"файл:нода"` просмотренных диалогов |

### `entity_id`

Уникальный идентификатор сущности внутри комнаты. Порядок назначения:

1. Явное значение: в Instance Creation Code комнаты или через vars-struct `instance_create_*` (тогда поле существует до `Create`).
2. Детерминированный fallback: `object_get_name(object_index) + ":" + xstart + ":" + ystart` (стабилен между заходами в комнату и сессиями).

!!! warning "Два инстанса одного объекта в одной точке"
    Fallback даст им одинаковый `entity_id`, поэтому для таких случаев `entity_id` назначается явно в редакторе или коде.

### Методы `__entity_state_save` / `__entity_state_restore`

Объявлены как instance-функции в `par_interactable/Create_0.gml` (не в `scripts/`); над реестром работают функции `scr_entity_state_get`/`scr_entity_state_set` из `scripts/scr_entity_state/scr_entity_state.gml`.

- **`__entity_state_restore()`**: читает запись `room_name:entity_id` из `global.entity_state`; восстанавливает `interaction_count`, `seen_dialogues`, `x`, `y` (каждое поле восстанавливается только при верном типе). После восстановления позиции пересчитывает `depth = -y`, если объект не прикреплён и не в `"manual"`. Идемпотентна.
- **`__entity_state_save([_custom_fields])`**: пишет `{interaction_count, seen_dialogues, x, y}` в реестр; ключи структуры `_custom_fields` копируются поверх (точка расширения для наследников). Возвращает результат `scr_entity_state_set`.

### События Room Start / Room End

- **`Other_4` (Room Start)**: повторный вызов `__entity_state_restore()` (первый стоит в конце `Create_0` и покрывает `entity_id`, заданный до `Create`). Instance Creation Code комнаты выполняется после `Create` и до Room Start, поэтому здесь `entity_id` уже финальный. Если метод не объявлен (дочерний `Create` не вызвал `event_inherited()`), пишется WARN `[entity_state]` вместо падения.
- **`Other_5` (Room End)**: автосохранение `__entity_state_save()`. Пишется на выходе из комнаты, чтобы захватить и перемещения, сделанные катсценой.

Реестр `global.entity_state` создаётся в `obj_Init` (`rm_init`) и персистится в файлы сейвов через `scr_saveSave`/`scr_saveLoad` (сейв без записи грузится в пустой реестр, `scr_defaultLoad` сбрасывает его в `{}` при новой игре). Зарезервированная сущность `"_room"` хранит комнатные мировые флаги (функции `scr_world_flag_set`/`scr_world_flag_get` из того же скрипта).

### Контракт взаимодействия

У `par_interactable` нет метода `interact()`: наследники в `Step_0` вызывают `scr_interaction(dialogue_filename, dialogue_node, [_use_mask_check])` из `scripts/interactionWithNPCsOrObjects/` (ресурс называется `interactionWithNPCsOrObjects` по историческим причинам). Функция проверяет: `scr_input_pressed("confirm")` → маркер `obj_pointMarker` игрока → `is_interactable` → `scr_checkUIBlocking` → режим partial control активной катсцены → касание маркера. При успехе: пушит `id` в `global.__interacted_targets` (очередь для `ActionWaitForInteract`, максимум 32), открывает диалог `readDialogue`, инкрементит `interaction_count`, дописывает `"файл:нода"` в `seen_dialogues` и сразу вызывает `__entity_state_save()`.

`dialogue_filename`/`dialogue_node` задаются в object properties наследника и переопределяются на инстансе в комнате; пустые значения делают объект молчаливым (`npc1/Step_0.gml`).

## `par_decor`: статичные декорации { #par-decor }

Наследует `par_depth`; `Create_0` ставит `is_static = true`, поэтому глубина вычисляется один раз при спавне. Твёрдость задаётся выборкой по object index (`place_meeting/instance_place(..., par_decor)` в `scr_collision_resolve`), отдельного флага нет. Большинство наследников (`bush`, `obj_tree1`, `sand`…) не имеют своих событий, вся инициализация идёт от родителя.

## `par_actor`: актёры { #par-actor }

Наследует `par_depth`; оба события (`Create_0`, `Step_0`): только `event_inherited()`. Сам по себе `par_actor` — маркер «движущийся актёр»; вся движковая логика живёт в `obj_actor`:

- **Движение**: `move_active`, `target_x`/`target_y`, `move_speed`, `move_blocked`, `use_collision`; метод `move_to_point(_tx, _ty, _spd, _collision)`: движение к точке с опциональной остановкой о solid-набор (`obj_collider` + `par_decor` + `par_interactable`).
- **Idle**: `idle_timer`, `idle_delay_frames`, `idle_anim_speed`, `chara_idle_sprites`; методы `set_idle_config`, `set_idle_sprites`, `__apply_idle_sprite`.
- **Прочее**: `auto_face`, `auto_walk`, `facing_direction`, `__cutscene_anim_override`.

Наследники: `obj_actor` → `obj_dummy` и `obj_player` (persistent, `marker_id` для `obj_pointMarker`).

## Сводная таблица { #summary-table }

| Объект | Родитель | События | Добавляет / перекрывает | Наследники |
|--------|----------|---------|------------------------|------------|
| `par_depth` | — | Create, Step | depth-контракт: `depth_mode`, `is_static`, `attached_target`, `depth = -y` | `par_actor`, `par_decor`, `par_interactable`, `obj_visualObject` |
| `par_actor` | `par_depth` | Create, Step | Оба события: `event_inherited()`; маркер актёров | `obj_actor`, `obj_player` |
| `par_decor` | `par_depth` | Create | `is_static = true` | `bush`, `obj_kachela`, `obj_lantern`, `obj_sign`, `obj_tree1`, `obj_tree2`, `pinkBench`, `sand`, `spr_pinkBench` |
| `par_interactable` | `par_depth` | Create, Room Start, Room End | `is_interactable`, `entity_id`, `interaction_count`, `seen_dialogues`, `__entity_state_save`/`__entity_state_restore` | `npc1` (→ `npc2`), `obj_asher`, `obj_bench`, `obj_dialoguetest`, `obj_save`, `obj_sheepFountain` |
| `par_entity` | — | Create | Маркер без полей и логики | `obj_collider`, `obj_slopeCollider` |
| `obj_actor` | `par_actor` | Create, Step | `move_to_point`, idle-система, `facing_direction` | `obj_dummy` |
| `obj_player` | `par_actor` | Create, Step, Begin/End Step, CleanUp | Управление, коллизии, `marker_id`; persistent | — |
| `npc1` | `par_interactable` | Create, Step | `dialogue_filename`/`dialogue_node` → `scr_interaction` | `npc2` |
| `obj_collider` | `par_entity` | Create, Step | Прямоугольная стена для `scr_collision_resolve` | — |
| `obj_slopeCollider` | `par_entity` | Create, Step, Collision `obj_player` | `slope_update_geometry`, `collision()` по треугольнику | — |
| `obj_visualObject` | `par_depth` | Create | `is_static = true`, `sprite_override` | — |

## См. также

- [Обзор архитектуры](overview.md) — слои систем и поток данных
- [Комнаты](rooms.md) — `rm_init`, Instance Creation Code
- [Взаимодействие](../systems/interaction.md) — `scr_interaction`, `obj_pointMarker`
- [Система сохранений](../systems/save-system.md) — `global.entity_state` в сейвах
- [Классы экшенов катсцен](../cutscenes/action-classes.md) — `ActionSetDepth`, снапшоты `depth_mode`
- [Объекты и события](../reference/objects-and-events.md) — полный реестр объектов

<!-- sources: objects/par_depth/Create_0.gml; objects/par_depth/Step_0.gml; objects/par_entity/Create_0.gml; objects/par_interactable/Create_0.gml; objects/par_interactable/Other_4.gml; objects/par_interactable/Other_5.gml; objects/par_decor/Create_0.gml; objects/par_actor/Create_0.gml; objects/par_actor/Step_0.gml; objects/obj_actor/Create_0.gml; objects/obj_actor/Step_0.gml; objects/obj_slopeCollider/Create_0.gml; objects/obj_visualObject/Create_0.gml; objects/obj_bench/Create_0.gml; objects/obj_save/Create_0.gml; objects/obj_collider/Create_0.gml; objects/obj_player/Create_0.gml; objects/obj_Init/Create_0.gml:330-339; objects/npc1/Step_0.gml; objects/npc1/npc1.yy; scripts/scr_entity_state/scr_entity_state.gml; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml; scripts/scr_collision_resolve/scr_collision_resolve.gml; scripts/scr_player_slope_resolve/scr_player_slope_resolve.gml; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:18,727-759,941-987,2941-2958,4526-4597; scripts/c_depth/c_depth.gml; scripts/scr_saveSave/scr_saveSave.gml:100-107; scripts/scr_saveLoad/scr_saveLoad.gml:122-137; scripts/scr_defaultLoad/scr_defaultLoad.gml:29; scripts/readDialogue/readDialogue.gml; docs_new/_meta/objects.txt; docs_new/_meta/rooms.txt -->
