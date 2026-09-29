---
title: Актёры и камера
tags:
  - cutscenes
  - actors
  - camera
  - objects
---

# Актёры и камера

Актёр катсцены — инстанс, зарегистрированный в `actor_map` менеджера под строковым ключом и адресуемый из действий через `target`. Камера — это `view_camera[0]`: пока играет катсцена, ею владеют camera-действия, а follow-камера игрока отключена флагом `global.cutscene_camera_override`.

## Объекты актёров

Иерархия: `par_depth` (Z-сортировка `depth = -y`, `depth_mode`, `attached_target`, `is_static`) → `par_actor` (тонкий родитель, события наследуются) → `obj_actor` (движение, facing, idle) → `obj_dummy` (наследник `obj_actor` со спрайтом `spr_Dummy`, тестовый/заглушечный актёр).

`obj_actor` — дефолтный объект актёра: `cutscene_engine_settings.json` → `default_actor_object` (дефолт `"obj_actor"`), финальный fallback: asset `obj_actor` напрямую.

## Создание актёров: `actor_create`

!!! warning "`cutscene_actor_create`: заглушка"
    Скрипт-обёртка `cutscene_actor_create()` помечена `DELETE_CANDIDATE`: тело зачищено, функция ничего не делает. Рабочий путь: JSON-экшен `actor_create` (фабрика создаёт `ActionActorCreate` напрямую) или `new ActionActorCreate(name, x, y, sprite_or_obj)` из кода.

| Поле JSON | Тип | Обязательное | Описание |
|-----------|-----|--------------|----------|
| `key` / `actor_key` / `actor_name` | string | да | Ключ в `actor_map`; первое непустое из трёх |
| `x`, `y` | real | да | Координаты спавна; без любого из ключей действие отклоняется |
| `sprite_or_object` / `actor_sprite` | string | нет | Имя object- или sprite-ассета |
| `copy_from` / `copy_target` | ref | нет | Источник внешности: ключ актёра, `"player"` или instance id; при двух заданных ключах приоритет у `copy_target` |

Логика `ActionActorCreate.start` (`scr_cutscene_classes.gml`):

1. `sprite_or_object`/`actor_sprite` резолвится в object-ассет или sprite-ассет: имя объекта → спавнится этот объект; имя спрайта → спавнится дефолтный объект актёра с подставленным `sprite_index`; ключ отсутствует или имя не резолвится в object/sprite-ассет → дефолтный объект.
2. Инстанс создаётся через `instance_create_depth(x, y, -y, obj)`: глубина сразу соответствует сортировке `depth = -y`.
3. Если `copy_from`/`copy_target` резолвится в живой инстанс (через `__cutscene_resolve_copy_source`: тот же `resolve_target`, плюс прямой instance id), копируются `sprite_index`, `image_index`, `image_speed`, `image_xscale`, `image_yscale`, `image_blend`, `image_alpha`, `visible`, а также `facing_direction`, `auto_face`, `auto_walk` (только если поля объявлены у источника). **`depth` не копируется**: isometric sorting пересчитает его из `y`. Явно заданный спрайт перекрывает скопированный.
4. Инстанс регистрируется: `actor_map[key] = inst`, `actor_specs[key] = {sprite, x, y, copy}`: `actor_specs` нужен для пересоздания актёра после `room_change` (см. [архитектуру](architecture.md)).

Для произвольных объектов (не «болванок» актёров) есть `spawn_entity`: поля `object`/`actor_sprite` (имя объекта, обязательно хотя бы одно), `x`, `y` (обязательные), `key`/`actor_name`, `depth`, `persistent`. Объект спавнится как есть, ключ тоже попадает в `actor_map`. Для наследников `par_depth` поле `depth` игнорируется: их Create перезаписывает глубину выражением `-y`.

## Поля `obj_actor`

| Поле | Источник | Default |
|------|----------|---------|
| `move_active` | `Create_0` / `move_to_point` | `false` |
| `target_x`, `target_y` | `Create_0` / `move_to_point` | `x`, `y` инстанса |
| `move_speed` | `Create_0` / `move_to_point` | `2` (px/кадр, нижний предел `__CUTSCENE_MIN_MOVE_SPEED = 0.1`) |
| `move_blocked` | `Step_0` при остановке о препятствие | `false` |
| `use_collision` | `Create_0` / `move_to_point` | `false` |
| `auto_face` | `Create_0` / `auto_facing` | `true` |
| `auto_walk` | `Create_0` / `auto_walk` | `false`: поле семантически inert, пишется, никем не читается |
| `facing_direction` | `Create_0` / `set_facing` / Step при движении | `global.DIR.DOWN` (`3`) |
| `idle_delay_frames` | `Create_0` / `set_idle_config` | `30` |
| `idle_anim_speed` | `Create_0` / `set_idle_config` | `0` (стоп-кадр) |
| `chara_idle_sprites` | `set_idle_sprites` | `undefined` |
| `chara_sprites` | внешнее поле, в Create не создаётся | отсутствует |
| `__cutscene_anim_override` | `Create_0` / `animate` / `set_animation_frame` | `false` |
| `actor_id` | внешнее поле, движок не выставляет | отсутствует |

### Спрайты по направлению и idle

Пока `move_active` и `auto_face`, `Step_0` выбирает walking-спрайт по доминирующей оси движения (`abs(dx) >= abs(dy)` → горизонталь) и параллельно пишет `facing_direction`:

1. `chara_sprites` (struct с полями `up`/`down`/`left`/`right`, значения обязаны быть sprite-ассетами, строковые имена не пройдут проверку `sprite_exists`) — приоритетная таблица; заполняется внешним кодом (`run_function` с whitelisted-скриптом, код комнаты/инстанса). Из JSON напрямую её не собрать.
2. Fallback Чары срабатывает, только если объявлено поле `actor_id` и `actor_id == "player"`: `spr_Chara_walking_R/L/D/U`. Движок это поле нигде не выставляет (единственный читатель: `obj_actor/Step_0`), поэтому fallback срабатывает лишь на актёрах, которым его присвоили вручную.

Когда актёр стоит (`move_active == false`), через `idle_delay_frames` кадров подставляется idle-спрайт из `chara_idle_sprites` (задаётся методом `set_idle_sprites(up, down, left, right)`): спрайт выбирается по текущему walking-спрайту сравнением `sprite_index` с полями `chara_sprites` либо с `spr_Chara_walking_*` напрямую (вторая проверка не смотрит на `actor_id`, она по факту текущего спрайта). Отсутствующее направление оставляет текущий кадр. `idle_anim_speed = 0`: стоп-кадр на нулевом кадре.

`__cutscene_anim_override = true` (ставят `animate` при `image_speed > 0` и `set_animation_frame`) отключает всю авто-подстановку (ни walking, ни idle) для pose-hold. Актёр без `chara_sprites`, `actor_id` и явного `actor_sprite` остаётся с `sprite_index` по умолчанию объекта (у `obj_actor` его нет, инстанс невидим).

`set_facing` проходит через `__cutscene_actor_apply_facing`: пишет `facing_direction`, затем ищет спрайт в `chara_idle_sprites`/`chara_sprites`; спрайты Чары подставляются только цели с `object_index == obj_player` (иначе любой актёр без таблиц «превращался» бы в игрока при повороте).

## Движение и коллизии

`move_to_point(tx, ty, spd, collision)` взводит `move_active`, движение идёт в `Step_0` покадрово. При `collision: true` проверяется единый solid-набор проекта: `obj_collider` + `par_decor` + `par_interactable` (та же проходимость, что у игрока), включая `collision_line` до точки шага против туннелирования. Остановка о препятствие ставит `move_blocked = true` и пишет warning: это видимый в логе «не дошёл», а не успешное прибытие.

## Привязка: `attach_to_target` / `detach`

`attach_to_target` (`ActionAttachToTarget`) крепит актёра к родителю: каждый кадр `__cutscene_update_attachments` ставит `target.x = parent.x + offset_x`, `target.y = parent.y + offset_y`. Запись живёт в глобальном реестре `global.__cutscene_attachments` между действиями.

| Поле JSON | Default | Описание |
|-----------|---------|----------|
| `target` / `target_ref` | — (обяз.) | Кого крепим |
| `parent` / `parent_ref` | — (обяз.) | К кому крепим |
| `offset_x`, `offset_y` | `0` | Смещение относительно родителя |
| `follow_facing` | `true` | Копировать `image_xscale` родителя |
| `follow_scale` | `true` | Копировать `image_yscale` родителя |
| `follow_depth` | `true` | Глубина родителя: у `par_depth`-наследников через `attached_target`, у прочих прямой записью `depth` |
| `duration_seconds` | `0` | `> 0`: позиция дотвинивается за указанное время, иначе телепорт |
| `detach_on_cutscene_end` | `true` | Снять привязку в `finish_cutscene` |

`detach` снимает запись (поле `destroy_after_detach: true` дополнительно уничтожает инстанс); позиция при отвязке всегда сохраняется; поле `keep_world_position`, которое пишет экспортёр, не читается и логируется как мёртвое. При уничтожении любой из сторон запись удаляется с warning.

## Камера

Все camera-действия работают с `view_camera[0]` (макрос `__CUTSCENE_VIEW_CAMERA`) и синхронно пишут `global.camera_x`/`global.camera_y`. Стартующие tween-ы идут через общий рантайм `cutscene_runtime_tween_to`, поэтому `camera_pan`-подобные действия прерываются корректно (cleanup гасит твины).

| JSON type | Поля | Поведение |
|-----------|------|-----------|
| `camera_center` | `x`, `y` (обяз.) | Мгновенно ставит центр вида в точку; клампа к комнате нет |
| `camera_pan` | `x`, `y` (обяз.), `seconds` (`1`) | Твин к абсолютной позиции **верхнего левого угла** вида, `ease_in_out` |
| `camera_pan_speed` | `x`, `y` (хотя бы одно обяз.), `seconds` (`1`) | `x`/`y`: скорости в px/кадр (не координаты!), `linear`; ключ `speed`/`speed_px_sec` игнорируется с warning; без обоих `x`/`y` действие отклоняется |
| `camera_pan_obj` | `target` (обяз.), `seconds` (`1`) | Центр на цели; единственное действие с клампом к границам комнаты |
| `camera_track` | `target` (обяз.), `seconds` (`0`), `offset_x`, `offset_y` | Покадровое следование за целью (центр + offset), завершается по таймеру; без клампа к границам комнаты |
| `camera_track_until_stop` | `target` (обяз.), `offset_x`, `offset_y` | То же, завершается когда у цели `move_active == false` (grace 1 кадр); у цели без `move_active`: сразу после grace |
| `camera_shake` | `seconds` (`1`), `magnitude` (`4`), `magnitude_x`, `magnitude_y`, `decay`, `frequency` (`1`) | Тряска вида вокруг текущей позиции |
| `tween_camera` | `property`/`prop`, `to_value`/`end_value`, `frames`/`seconds`/`duration_frames`, `easing`/`ease_name`, `from_value`/`start_value_override` | Твин одной координаты камеры; свойства: `x`/`view_x`/`camera_x`, `y`/`view_y`/`camera_y` |

Тот же канал камеры открывают общие действия: `tween`/`set_property` с `kind: "camera"` (не требуют `target`) и `lerp` с `target: "camera"`. Из кода и Yarn: `c_tween_camera(_property, _to_value, _frames, _easing, _from_value)`: в отличие от JSON-полей, `_frames` здесь задаётся **в кадрах**, а не в секундах.

!!! warning "`duration_frames`: это секунды"
    В `tween`/`tween_camera` ключ `duration_frames` так экспортирует Undefscene и читается как секунды, несмотря на имя. Не путать с `frames` (действительно кадры, имеет приоритет).

### `global.cutscene_camera_override`

Инициализируется в `obj_Init` (`false`), взводится `start_cutscene()`; перед этим менеджер запоминает прежнее значение и позицию вида (`prev_cutscene_camera_override`, `prev_camera_view_x/y`). Пока флаг взведён:

- `obj_player/Step_2` выходит сразу: follow-камера игрока не перезаписывает вид;
- `scr_checkUIBlocking` считает override UI-блокировкой ввода.

`finish_cutscene()` возвращает `prev`-значение флага и восстанавливает вид: при снятом override центр ставится на игроке, иначе сохранённая позиция. `scr_saveLoad` при загрузке сейва тоже сбрасывает флаг в `false`.

!!! warning "Мёртвые обёртки"
    `cutscene_camera_center`, `cutscene_camera_pan`, `cutscene_camera_track`, `cutscene_camera_shake`, `cutscene_actor_destroy` — зачищенные заглушки (`DELETE_CANDIDATE`, тела пустые). Использовать JSON-экшены или конструкторы `ActionCamera*`.

## См. также

- [Обзор катсцен](overview.md): способы задать сцену, глобальное состояние
- [Архитектура менеджера](architecture.md): `actor_map`/`actor_specs`, пересоздание при `room_change`, `finish_cutscene`
- [JSON-действия](json-actions.md): поля `actor_create`, `attach_to_target`, camera-экшенов
- [Классы действий](action-classes.md): `ActionActorCreate`, `ActionCamera*`, `ActionAttachToTarget`
- [GML и `c_*`-DSL](gml-dsl.md): `c_tween_camera` и команды билдера
- [Рецепты](cookbook.md): готовые JSON-сцены с актёрами и камерой
- [Иерархия объектов](../architecture/object-hierarchy.md): `par_depth`, `depth_mode`, `attached_target`

<!-- sources: objects/obj_actor/Create_0.gml:1-99; objects/obj_actor/Step_0.gml:1-137; objects/obj_actor/obj_actor.yy; objects/par_actor/par_actor.yy; objects/par_actor/Create_0.gml; objects/par_actor/Step_0.gml; objects/obj_dummy/obj_dummy.yy; objects/par_depth/Create_0.gml:10-28; objects/par_depth/Step_0.gml:2-35; scripts/cutscene_actor_create/cutscene_actor_create.gml:1-5; scripts/cutscene_action_factory/cutscene_action_factory.gml:30-53, 208-270, 523-640, 906-990, 1052-1131, 1200-1241; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:33-59, 294-310, 375-408, 2109-2304, 2428-2503, 3210-3261, 3700-3915, 4300-4524, 4635-4710; scripts/cutscene_load_json/cutscene_load_json.gml:455-534; scripts/cutscene_load_engine_settings/cutscene_load_engine_settings.gml:105-122; scripts/c_cmd/c_cmd.gml:178-232; objects/obj_cutsceneManager/Create_0.gml:287-298, 426-535, 659-738, 838-918; objects/obj_player/Step_2.gml:1-17; objects/obj_Init/Create_0.gml:154; scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml:78; scripts/scr_saveLoad/scr_saveLoad.gml:311; scripts/scr_layer_ensure_instances/scr_layer_ensure_instances.gml; datafiles/cutscenes/test_actors.json; datafiles/cutscenes/tests/attach_detach.json -->
