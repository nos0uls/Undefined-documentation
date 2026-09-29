---
title: Взаимодействие и интерактивные объекты
tags:
  - interaction
  - npc
  - dialogue
  - persistence
---

# Взаимодействие и интерактивные объекты

Система взаимодействия игрока с NPC и объектами мира: маркер перед игроком, единая функция `scr_interaction`, базовый класс `par_interactable` и реестр `global.entity_state` с персистентным состоянием сущностей.

## Принцип работы

Вызов взаимодействия делает **не игрок** — каждый интерактивный объект опрашивает условия в своём Step-событии и сам решает, сработал ли он. Игрок предоставляет только невидимый маркер `obj_pointMarker` — точку перед лицом персонажа:

- Маркер создаётся в `obj_player/Create_0` (persistent, живёт через смену комнат) и запоминается в `global.obj_player.marker_id`.
- Позицию маркера каждый кадр ставит `scr_player_marker_update()` (`obj_player/Step_0.gml:23`): вылет от origin игрока — `±15` px вбок (точка поднята на `6` px над origin), `-15` px вверх, `+5` px вниз по `facing_direction`.
- Интерактив в Step проверяет попадание точки маркера в свой `bbox` или маску спрайта и вызывает `scr_interaction(file, node)`.

!!! note "Контракт на маску интерактива"
    Точка маркера выступает за фут-бокс игрока на ~3 px по бокам и вверх (~6 px вниз). Маска интерактивного объекта обязана выходить к игроку не меньше этого запаса, иначе «тонкий» объект (настенная кнопка) не сработает — см. комментарий в `scr_player_marker_update`.

Условия срабатывания внутри `scr_interaction` (в порядке проверки):

1. `scr_input_pressed("confirm")` — нажатие подтверждения.
2. Маркер существует (`global.obj_player.marker_id`).
3. `is_interactable != false` у вызывающего инстанса.
4. Нет UI-блокировки (`scr_checkUIBlocking(false, false)`).
5. При активной катсцене — режим `partial_control_type` менеджера: `WHITELIST` (только объекты из `partial_control_whitelist`) или `FREE`; `LOCKED` и любые невалидные значения запрещают взаимодействие.
6. Точка маркера внутри `bbox` (`point_in_rectangle`) или маски (`position_meeting` при `_use_mask_check = true`).

При успехе объект пушит свой `id` в `global.__interacted_targets` (очередь до 32 записей, читает `ActionWaitForInteract` катсцен), открывает диалог через `readDialogue(_scriptToReadFrom, _node)` и пишет статистику в `entity_state`.

## API

### `scr_interaction(_scriptToReadFrom, _node, _use_mask_check)`

Определена в `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml` (ресурс назван по историческим причинам, рабочая функция — `scr_interaction`). Вызывается из Step интерактива, `id` внутри — сам интерактив.

| Параметр | Тип | Описание |
|----------|-----|----------|
| `_scriptToReadFrom` | `string` | Имя yarn-файла из `datafiles/Dialogues` (без пути) |
| `_node` | `string` | Имя стартовой ноды внутри yarn-файла |
| `_use_mask_check` | `bool` | `false` (дефолт) — точка маркера в `bbox`; `true` — `position_meeting` по маске спрайта. `true` используют персонажи main cast (obj_asher), чтобы зона не была шире видимого силуэта |

Возвращает `undefined`; при успехе создаёт `textboxTest_scribble` через `readDialogue`.

### Мёртвые обёртки (не вызывать)

| Функция | Файл | Статус |
|---------|------|--------|
| `interactionWithNPCsOrObjects(file, node)` | `scripts/interactionWithNPCsOrObjects/` | Пустой стаб, `DELETE_CANDIDATE`, 0 вызовов. Раньше = `scr_interaction(file, node, false)` |
| `interactionWithMainCast(file, node)` | `scripts/interactionWithMainCast/` | Пустой стаб, `DELETE_CANDIDATE`, 0 вызовов. Раньше = `scr_interaction(file, node, true)` |
| `scr_npc_pick_dialogue()` | `scripts/scr_npc_pick_dialogue/` | Пустой стаб, `DELETE_CANDIDATE`, 0 вызовов. Выбор реплики делает контент напрямую через `readDialogue` — выборочной логики по `seen_dialogues`/флагам в движке нет |

## `par_interactable` — контракт для контент-мейкера

`par_interactable` наследует `par_depth` (`is_static`, `depth_mode`, `attached_target`, auto-глубина `depth = -y`). События: `Create_0`, `Room Start` (Other_4), `Room End` (Other_5).

Поля, инициализируемые в `Create_0` (все через `variable_instance_exists` — можно задать до Create через vars-struct или переопределить в дочернем Create после `event_inherited()`):

| Поле | Дефолт | Назначение |
|------|--------|-----------|
| `is_interactable` | `true` | `false` отключает срабатывание `scr_interaction` для инстанса |
| `category` | `"generic"` | Группировка сущности (`"npc"`, `"prop"`, `"save"`...). Читателей пока нет |
| `display_name` | `"Объект"` | Человекочитаемое имя. Читателей пока нет (зарезервировано под промпт/неймплейт, аудит IF-P2-32) |
| `entity_id` | `"object_name:xstart:ystart"` | Ключ записи в `global.entity_state` (см. ниже) |
| `interaction_count` | `0` | Счётчик взаимодействий; инкрементит `scr_interaction` |
| `seen_dialogues` | `[]` | Массив ключей `"file:node"` уже показанных диалогов; пишет `scr_interaction` |

Методы, объявляемые `Create_0` на инстансе:

- `__entity_state_restore()` — читает запись `scr_entity_state_get(room_get_name(room), entity_id)` и восстанавливает `interaction_count`, `seen_dialogues`, `x`, `y` (с пересчётом `depth`). Идемпотентен; зовётся в конце Create и повторно в Room Start — повторный вызов покрывает `entity_id`, назначенный в Instance Creation Code комнаты (он выполняется после Create).
- `__entity_state_save(_custom_fields)` — пишет в реестр `{interaction_count, seen_dialogues, x, y}` плюс произвольные поля из `_custom_fields`-структуры; возвращает результат `scr_entity_state_set`.

Событие `Room End` (`Other_5`) — автосохранение: вызывает `__entity_state_save()` при выходе из комнаты, поэтому в реестр попадают и сдвиги позиции от катсцен. Если дочерний Create не вызвал `event_inherited()`, методов нет — Room Start пишет `WARN` в лог, Room End молча пропускает.

!!! warning "Не выдумывать метод `interact`"
    Отдельного переопределяемого метода `interact()`/`on_interact()` у `par_interactable` нет — реакция встраивается в Step наследника вызовом `scr_interaction` (см. рецепт ниже).

## `entity_id` — как назначается

- **Явно**: в Instance Creation Code комнаты (`entity_id = "..."`) или через vars-struct `instance_create_*` — тогда поле существует до Create.
- **Fallback** (детерминированный): `object_get_name(object_index) + ":" + string(xstart) + ":" + string(ystart)`. Стабилен между заходами в комнату и сессиями, в отличие от instance id.
- Два инстанса одного объекта в одной точке получат одинаковый id — для таких случаев `entity_id` назначается явно.

По коду и данным проекта явных назначений `entity_id` в комнатах нет — весь контент живёт на fallback-ключе.

## Реестр `global.entity_state`

Struct, ключ `"room_name:entity_id"` → запись `{interaction_count, seen_dialogues, x, y, <custom>}`. Создаётся в `obj_Init` (rm_init), целиком сериализуется в сейв (`scr_saveSave`, JSON-строкой) и восстанавливается при загрузке (`scr_saveLoad`); «новая игра» обнуляет реестр в `scr_defaultLoad`.

| Функция | Сигнатура | Возврат |
|---------|-----------|---------|
| `scr_entity_state_get` | `(room_name, entity_id)` | `struct` или `undefined`; при отсутствии `global.entity_state` пишет WARN |
| `scr_entity_state_set` | `(room_name, entity_id, state_struct)` | `bool`; при отсутствии реестра создаёт его молча |
| `scr_entity_state_clear` | `(room_name, entity_id)` | `bool` — удалена ли запись |

Writer'ы `interaction_count`/`seen_dialogues` в контенте — два: `scr_interaction` (инкремент и ключ `"file:node"` сразу при взаимодействии + `__entity_state_save()`) и автосейв `par_interactable/Other_5` на выходе из комнаты.

## Мировые флаги комнаты

Определены в `scripts/scr_entity_state/scr_entity_state.gml`, поверх того же реестра — под зарезервированной сущностью `"_room"` в поле `flags`:

| Функция | Сигнатура | Описание |
|---------|-----------|---------|
| `scr_world_flag_set` | `(room_name, flag, value) → bool` | Пишет персистентный флаг комнаты; валидирует `room_name`/`flag` как строки, `flag` дополнительно непустой |
| `scr_world_flag_get` | `(room_name, flag, _default = false) → any` | Читает флаг; при отсутствии возвращает `_default` |

Флаги персистятся вместе с сейвом через `entity_state`. Не путать с `global.room_flags` — сессионной структурой для пост-катсценных пометок, которая в сейв не входит и обнуляется при загрузке/новой игре.

!!! warning "Writer'ов в контенте нет"
    `scr_world_flag_set`/`scr_world_flag_get` — инфраструктура без прод-писателей: единственный вызов в проекте — стресс-тест `stress_entity_state` (`scr_stress_tests`). Зафиксировано в аудите как осознанное ограничение — API готов к использованию, но контент флаги пока не ставит. Аналогично пуст `scr_npc_pick_dialogue` — ветвление реплик делается внутри yarn-нод или отдельными `dialogue_node` на инстансе.

## Как сделать нового NPC

1. Создайте объект с `parentObjectId` → `par_interactable` (для типового NPC с репликой удобнее наследовать `npc1` — тогда шаги 4–5 не нужны, события унаследуются).
2. Назначьте `spriteId` (и `spriteMaskId`, если нужна отдельная маска). Флаг `solid` в `.yy` ставить не нужно: твёрдость для игрока и актёров даёт само членство в `par_interactable` — коллизии идут выборкой по object index (`place_meeting`/`resolve_solid`), GM-механика `solid` в проекте не используется (у `obj_asher` флаг выставлен избыточно, аудит F-274).
3. В `properties` объекта (Object Properties, `varType` 2 — string) объявите:
   - `dialogue_filename` — имя yarn-файла из `datafiles/Dialogues`, например `"testDialogue.yarn"`;
   - `dialogue_node` — имя стартовой ноды, например `"RM_ROAD_CURVE: NPC-1"`.
   Оба поля переопределяются на конкретном инстансе в редакторе комнаты.
4. В `Create_0`: `event_inherited();`, затем при необходимости `category = "npc";`, `display_name = "..."`, `is_interactable = true/false`.
5. В `Step_0`: `event_inherited();` (иначе не обновляется auto-глубина от `par_depth`), затем вызов с защитой от пустой конфигурации:

```gml title="Step_0.gml наследника par_interactable"
event_inherited();
if (variable_instance_exists(id, "dialogue_filename")
    && dialogue_filename != "" && dialogue_node != "") {
    scr_interaction(dialogue_filename, dialogue_node);
    // третий аргумент true — проверка по маске спрайта (для крупных персонажей)
}
```

6. Поставьте инстанс в комнату. `entity_id` по умолчанию — fallback `"объект:xstart:ystart"`; задайте явно в Instance Creation Code только если два инстанса делят объект и позицию или нужен стабильный id вне зависимости от координат.
7. Добавьте yarn-файл в `datafiles/Dialogues`; имя ноды (`title:`) должно совпадать с `dialogue_node`. Если `dialogue_filename`/`dialogue_node` пустые — NPC молчит (защита в Step наследников, см. `npc1/Step_0.gml`).

## Существующие интерактивы

| Объект | Родитель | Спрайт | `dialogue_filename` / `dialogue_node` | Особенности |
|--------|----------|--------|--------------------------------------|-------------|
| `npc1` | `par_interactable` | `npc` | `testDialogue.yarn` / `RM_ROAD_CURVE: NPC-1` | Базовый NPC: Step с guard и `scr_interaction` по `bbox` |
| `npc2` | `npc1` | `npc247` | `testDialogue.yarn` / `RM_ROAD_CURVE: NPC-2` | Событий нет — всё унаследовано; отличаются только свойства и спрайт |
| `obj_asher` | `par_interactable` | `spr_asher_default` | `testDialogue.yarn` / `Cutscene-Bridge-Demo` | Main cast: `solid`, `category="npc"`, `display_name="Asher"`, mask-check `scr_interaction(..., true)` |
| `obj_bench` | `par_interactable` | `bench1` | `testDialogueBlue.yarn` / `Blue` | `is_static = true` в Create |
| `obj_sign` | `par_decor` | `sign1` (+ `sign_collision_mask`) | — | **Не интерактивный**: наследует `par_decor`, кода взаимодействия нет, событие Create снято (`DELETE_CANDIDATE`) |
| `obj_sheepFountain` | `par_interactable` | `fountain` | `fountain.yarn` / `RM_002: FOUNTAIN` | Тот же паттерн, что у `obj_bench` |
| `obj_save` | `par_interactable` | `spr_save` | пустые по умолчанию | Своя проверка маркера + открытие `obj_saveManager` после закрытия диалога |

## См. также

- [Диалоги](dialogue.md) — `readDialogue`, `textboxTest_scribble`, Yarn-интеграция
- [Игрок](player.md) — `marker_id`, `scr_player_marker_update`, `facing_direction`
- [Ввод](input.md) — `scr_input_pressed("confirm")`, UI-блокировка
- [Система сохранений](save-system.md) — сериализация `global.entity_state` в сейв
- [Частичный контроль](../cutscenes/partial-control.md) — `partial_control_type`, whitelist интерактивов
- [Глобальное состояние](../architecture/global-state.md) — `entity_state`, `room_flags`, `flag`, `plot`

<!-- sources: objects/par_interactable/Create_0.gml; objects/par_interactable/Other_4.gml; objects/par_interactable/Other_5.gml; objects/par_interactable/par_interactable.yy; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml; scripts/interactionWithMainCast/interactionWithMainCast.gml; scripts/scr_npc_pick_dialogue/scr_npc_pick_dialogue.gml; scripts/scr_entity_state/scr_entity_state.gml; scripts/scr_player_marker_update/scr_player_marker_update.gml; scripts/readDialogue/readDialogue.gml; scripts/scr_saveSave/scr_saveSave.gml:100-107; scripts/scr_saveLoad/scr_saveLoad.gml:122-137,232-234,323-326; scripts/scr_defaultLoad/scr_defaultLoad.gml:26-32; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:4526-4605,5020-5034; scripts/scr_stress_tests/scr_stress_tests.gml:991-1012; objects/obj_Init/Create_0.gml:25-29,157,333-339; objects/obj_player/Create_0.gml:300-320; objects/obj_player/Step_0.gml:23; objects/npc1/Create_0.gml; objects/npc1/Step_0.gml; objects/npc1/npc1.yy; objects/npc2/npc2.yy; objects/obj_asher/Create_0.gml; objects/obj_asher/Step_0.gml; objects/obj_asher/obj_asher.yy; objects/obj_sign/Create_0.gml; objects/obj_sign/Step_0.gml; objects/obj_sign/obj_sign.yy; objects/obj_bench/Create_0.gml; objects/obj_bench/Step_0.gml; objects/obj_bench/obj_bench.yy; objects/obj_save/Step_0.gml; objects/obj_save/obj_save.yy; objects/obj_sheepFountain/Step_0.gml; objects/obj_sheepFountain/obj_sheepFountain.yy; objects/par_decor/Create_0.gml; objects/par_decor/par_decor.yy; objects/par_depth/Create_0.gml; audit_2026-09/07_study/S01.md:72; audit_2026-09/07_study/S08.md:124-149 -->
