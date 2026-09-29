# Review: architecture/object-hierarchy.md

Фактчек по коду ревизии 7ee444a. Источники: `objects/*/*.yy` (parentObjectId), `_meta/objects.txt`, код объектов и скриптов.

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 13 | «всех 53 объектов проекта» | OK — objects.txt:4 «Объектов: 53»; 53 каталога в `objects/` |
| 13 | `par_depth`/`par_interactable`/`par_decor`/`par_actor`/`par_entity` — роли | OK — по коду объектов (см. ниже) |
| 17 | Два корня-родителя: `par_depth` и `par_entity` | OK — objects.txt:483,492 parent `-` |
| 20–24 | `par_depth` → `par_actor` → `obj_actor` → `obj_dummy`; `par_actor` → `obj_player` | OK — yy: par_actor→par_depth (objects.txt:466), obj_actor→par_actor (:63), obj_dummy→obj_actor (:163), obj_player→par_actor (:354) |
| 25–34 | `par_decor` → 9 наследников (bush, obj_kachela, obj_lantern, obj_sign, obj_tree1, obj_tree2, pinkBench, sand, spr_pinkBench) | OK — все parent `par_decor` (objects.txt:8,203,210,416,444,451,510,517,535) |
| 35–42 | `par_interactable` → npc1→npc2, obj_asher, obj_bench, obj_dialoguetest, obj_save, obj_sheepFountain | OK — objects.txt:15,24,82,91,154,375,407 |
| 43 | `obj_visualObject` → `par_depth` | OK — objects.txt:458 |
| 45–47 | `par_entity` → `obj_collider`, `obj_slopeCollider` | OK — objects.txt:110,424 |
| 51 | `obj_slopeCollider` наследует `par_entity` напрямую, минуя `obj_collider`; причина — прямоугольная стена глушила треугольную проверку | OK — obj_slopeCollider.yy parent par_entity; obj_slopeCollider/Create_0.gml:3-4 |
| 55–57 | Списки объектов без родителя (26 шт.) | OK — полный и точный перечень parent `-` из objects.txt (28 минус 2 корня) |
| 61 | `Create_0` задаёт `depth = -y`; аргумент depth у `instance_create_depth` мёртв | OK — par_depth/Create_0.gml:29, комментарий :25-28 |
| 63–70 | Четыре режима по приоритету (attached_target → is_static → manual → auto) | OK — par_depth/Step_0.gml:12-44 |
| 67 | Цель уничтожена → привязка сбрасывается, `depth = -y` один раз | OK — par_depth/Step_0.gml:15-19 |
| 68 | `is_static` ставят par_decor, obj_visualObject, obj_bench, obj_save | OK — par_decor/Create_0.gml:7; obj_visualObject/Create_0.gml:2; obj_bench/Create_0.gml:4; obj_save/Create_0.gml:2 |
| 69 | `"manual"` ставят `ActionSetDepth` и `c_depth` через `__CUTSCENE_DEPTH_MODE_MANUAL` | OK — scr_cutscene_classes.gml:18 (макрос), :2953 (ActionSetDepth); c_depth.gml:9 (обёртка). Доп.: третий писатель — `__cutscene_runtime_set_value` при записи `"depth"` (scr_cutscene_classes.gml:727-728) |
| 70 | auto: `depth = -y` только при сдвиге (dirty-flag `__depth_prev_x/y`) | OK — par_depth/Step_0.gml:39-43; кэш в Create_0.gml:33-34 |
| 74 | У `depth_mode` два осмысленных значения; прочие молча = "auto"; is_static/attached_target — отдельные поля | OK — par_depth/Create_0.gml:14-22; Step_0.gml:20-31 |
| 75 | Внешняя запись `depth` в auto временна | OK — par_depth/Step_0.gml:33-35 |
| 76 | Снапшот/restore `__cutscene_snapshot_instance`/`__cutscene_restore_instance` сохраняют режим и значение | WRONG — функции `__cutscene_restore_instance` не существует. Snapshot пишет `depth_mode` (scr_cutscene_classes.gml:759); восстанавливает `__cutscene_apply_instance_snapshot` (:962-963), вызываемая из `__cutscene_restore_actor_states` (:997) и `__cutscene_restore_instance_states` (:1114) |
| 78–79 | `Step_0` без `exit`, чтобы дочерний код после `event_inherited()` не прерывался | OK — par_depth/Step_0.gml:4-5 |
| 83–85 | `par_entity` — маркер без полей; выборки по object index (`obj_collider`, `obj_slopeCollider` с `collision(_dx,_dy,_inst)` по `tri_x`/`tri_y`) | OK — par_entity/Create_0.gml:1-4; scr_collision_resolve.gml:11-25; obj_slopeCollider/Create_0.gml:73-86 (collision зовёт scr_player_slope_resolve.gml:26-76) |
| 89 | `par_interactable` наследует `par_depth` | OK — par_interactable.yy; Create_0.gml:4 `event_inherited()` |
| 95–100 | Таблица полей: is_interactable=true, category="generic", display_name="Объект", entity_id, interaction_count=0, seen_dialogues=[] | OK — par_interactable/Create_0.gml:6,12,13,26-30; is_interactable читается в interactionWithNPCsOrObjects.gml:35; «читателей нет» — Create_0.gml:8-11 |
| 104–110 | Порядок entity_id: явное значение → fallback `object_get_name(object_index) + ":" + xstart + ":" + ystart`; коллизия id у двух инстансов в одной точке | OK — Create_0.gml:18-28 (в коде `string(xstart)`/`string(ystart)`) |
| 114 | Методы — instance-функции в `par_interactable/Create_0.gml`; реестр — `scr_entity_state_get`/`set` в `scripts/scr_entity_state/` | OK — Create_0.gml:41-72; scr_entity_state.gml:6,27 |
| 116 | `__entity_state_restore()`: ключ `room_name:entity_id`, тип-проверки, `depth = -y` если не прикреплён и не manual; идемпотентна | OK — Create_0.gml:42-55; ключ `room_name + ":" + entity_id` — scr_entity_state.gml:14 |
| 117 | `__entity_state_save([_custom_fields])`: `{interaction_count, seen_dialogues, x, y}`, custom поверх, возвращает `scr_entity_state_set` | OK — Create_0.gml:58-72 |
| 121 | `Other_4` (Room Start): повторный restore; WARN `[entity_state]` вместо падения | OK — Other_4.gml:1-11 |
| 122 | `Other_5` (Room End): автосейв `__entity_state_save()` | OK — Other_5.gml:1-8 |
| 124 | Реестр создаётся в `obj_Init` (`rm_init`), персистится через `scr_saveSave`/`scr_saveLoad` | OK — obj_Init/Create_0.gml:339; rooms.txt:94-101 (obj_Init в rm_init); scr_saveSave.gml:100-107; scr_saveLoad.gml:122-137 |
| 124 | «`scr_defaultLoad` ставит `{}` при отсутствии записи» | WRONG — scr_defaultLoad — сценарий новой игры, сбрасывает `global.entity_state = {}` безусловно (scr_defaultLoad.gml:29). Fallback «нет записи → `{}`» — в scr_saveLoad.gml:122-137 (`_entity` по умолчанию, старые сейвы) |
| 124 | `"_room"` — зарезервированная сущность; `scr_world_flag_set`/`get` | OK — scr_entity_state.gml:74-80,89-96 |
| 128 | Цепочка проверок `scr_interaction`: confirm → маркер → is_interactable → UI-блокировка → partial control → касание | OK — interactionWithNPCsOrObjects.gml:25-82 |
| 128 | Пуш `id` в `global.__interacted_targets` (для `ActionWaitForInteract`, максимум 32), `readDialogue`, `interaction_count++`, `seen_dialogues`, `__entity_state_save()` | OK — interactionWithNPCsOrObjects.gml:83-109 (_MAX=32 :89-91); ActionWaitForInteract читает очередь scr_cutscene_classes.gml:4574-4597; readDialogue.gml:8 |
| 130 | `dialogue_filename`/`dialogue_node` — object properties; пустые значения → молчаливый объект | OK — npc1.yy:33-34 (и npc2, obj_asher, obj_bench, obj_save, obj_sheepFountain .yy); npc1/Step_0.gml:9-11 |
| 134 | `par_decor`: `is_static = true`; твёрдость выборкой по object index в `scr_collision_resolve` | OK — par_decor/Create_0.gml:7-9; resolve_solid → place_meeting (obj_player/Create_0.gml:81-83,102+); `instance_place(..., par_decor)` — scr_player_slope_resolve.gml:31,48 (вызывается из scr_collision_resolve) |
| 138 | `par_actor`: оба события — только `event_inherited()` | OK — par_actor/Create_0.gml:4, Step_0.gml:3 |
| 140–142 | Поля/методы `obj_actor` (move_*, move_to_point, idle-*, auto_face/auto_walk/facing_direction/__cutscene_anim_override) | OK — obj_actor/Create_0.gml:6-99; solid-набор obj_collider+par_decor+par_interactable — Step_0.gml:12-14,34-37 |
| 144 | `obj_actor` → `obj_dummy`; `obj_player` persistent, `marker_id` | OK — yy; obj_player/Create_0.gml:7,309-314 |
| 150–160 | Сводная таблица (события, родители, наследники) | OK — по objects.txt и коду; obj_player 5 событий (Create/Step/Begin/End Step/CleanUp); obj_slopeCollider Collision obj_player |
| 162–169 | Ссылки «См. также» | OK — все файлы существуют в docs_new/ (overview.md, rooms.md, systems/interaction.md, systems/save-system.md, cutscenes/action-classes.md, reference/objects-and-events.md) |

## MISSING / неточности низкого приоритета

- `par_interactable/Create_0.gml:74` — первичный вызов `__entity_state_restore()` уже в конце Create; страница это подразумевает («повторный вызов» в Other_4), но явно не фиксирует.
- Третий писатель `depth_mode = "manual"` — `__cutscene_runtime_set_value` при записи свойства `"depth"` через set_property/tween (scr_cutscene_classes.gml:727-728).
- Sources-комментарий: `scr_cutscene_classes.gml:2941-2958` покрывает только `ActionSetDepth`; snapshot/restore живут на :759 и :950-987.

## Итог

- WRONG: 2 (строки 76, 124).
- Всё остальное подтверждено; UNVERIFIABLE нет.
