# Катсцены: API

## Канон
- **`target_ref`**: канонический формат — **instance id**.
- **Единицы скорости**: **px/frame**.
- **JSON‑загрузка**: в JSON длительности в **секундах**, скорости в **px/sec**, при загрузке конвертируются в кадры/px‑per‑frame.

## Builder-API (`c_*`)
Builder-слой предназначен для построения очереди через активный менеджер (build manager) без передачи `mgr` в каждый вызов.

### Менеджер сборки
- `c_begin(id)` — создаёт менеджер `obj_cutsceneManager` и сохраняет в `global.__cutscene_build_mgr`.
- `c_play(mgr=noone)` — запускает `start_cutscene()` (если `mgr` не передан, берёт `global.__cutscene_build_mgr`).
- `c_end(mgr=noone)` — принудительно вызывает `mgr.finish_cutscene()`.

Канон запуска: `c_begin` + `c_play`.

### Команды (через `c_cmd`)
`c_cmd` — stateless роутер: actor-specific команды требуют **явный `target` как первый аргумент**.

- `c_speaker(name)` — выставляет `dialogue_controller.speaker_name`.
- `c_setxy(target, x, y)` — `ActionSetXY(target, x, y)`
- `c_depth(target, depth)` — `ActionSetProperty(target, "depth", depth)`
- `c_facing(target, dir)` — `ActionRunFunction(...)` с применением направления и спрайта.
- `c_autofacing(target, enabled)` — `ActionSetProperty(target, "auto_face", enabled)`
- `c_autowalk(target, enabled)` — `ActionSetProperty(target, "auto_walk", enabled)`
- `c_visible(target, visible)` — `ActionSetProperty(target, "visible", visible)`
- `c_instance(key, x, y)` — `ActionActorCreate(key, x, y, undefined)`
- `c_sprite(target, sprite, image_index, image_speed)` — `ActionAnimate(target, sprite, image_index, image_speed)`

### Камера (через `c_cmd`)
- `c_pan(view_x, view_y, frames)` — `ActionCameraPan(view_x, view_y, frames)`
- `c_panobj(target_ref, frames)` — `ActionCameraPanToObj(target_ref, frames)`
- `c_panspeed(dx, dy, frames)` — `ActionCameraPanSpeed(dx, dy, frames)`
- `c_pan_wait(view_x, view_y, frames)` — `c_pan(...)` + `c_wait(frames)`
- `c_shake()` — добавляет `ActionCameraShake(30, 4)` (фиксировано)

### Ожидание
- `c_wait(frames)` — добавляет `ActionWait(frames)`.

### Отложенные команды
- `c_delaycmd(delay_frames, cmd, arg0)` — помещает команду в `mgr.delayed_commands`.
- `c_delaywalk(delay_frames, dir, speed, time_frames)` — планирует background-движение через `ActionMove`.

## Action-API (`cutscene_*`)
Обёртки `cutscene_*` обычно возвращают Action-struct из `scr_cutscene_classes`.

- `cutscene_add(manager, action)`
- `cutscene_start(manager)`
- `cutscene_wait(frames)`
- `cutscene_move(target_ref, x, y, speed_px_per_frame, use_collision=false)`
- `cutscene_animate(target_ref, sprite, frame=0, image_speed=0)`
- `cutscene_set_facing(target_ref, dir)`
- `cutscene_dialogue(filename, node)`

Дополнительно (присутствует в коде):
- `cutscene_create(id)`
- `cutscene_actor_create(key, x, y, sprite_or_object, copy_from_object=undefined)`
- `cutscene_actor_destroy(target_ref)`
- `cutscene_set_xy(target_ref, x, y)`
- `cutscene_set_depth(target_ref, depth)` — **унифицировано в `ActionSetProperty`** (`cutscene_set_visible`, `cutscene_auto_facing_toggle`, `cutscene_auto_walk_toggle` аналогично).
- `cutscene_auto_facing_toggle(target_ref, enabled)`
- `cutscene_auto_walk_toggle(target_ref, enabled)`
- `cutscene_parallel(actions_array)`
- `cutscene_branch(condition_func, true_actions, false_actions=[])`
- `cutscene_run_function(func, args=[])`
- `cutscene_camera_center(center_x, center_y)`
- `cutscene_camera_pan(view_x, view_y, frames)`
- `cutscene_camera_track(target_ref, frames, offset_x=0, offset_y=0)`
- `cutscene_camera_shake(frames, magnitude=4)`
- `cutscene_follow_path(target_ref, points_array, speed_px_per_frame, use_collision=false)`

### Групповые команды (`c_*_group`)
Доступны с `ActionGroup` для применения одного экшена к нескольким target-ам:
- `c_move_group(targets[], x, y, speed, use_collision=false)`
- `c_walk_group(targets[], dir, speed, frames, use_collision=false)`
- `c_var_group(targets[], property, value)` — `ActionSetProperty`
- `c_tween_group(targets[], property, to_value, frames, easing="linear", from_value=undefined)`

### JSON Action Factory
`cutscene_init_action_factory()` создаёт глобальную фабрику `global.__cutscene_action_factory` — struct с mapping `action_type -> constructor(map, fps)`.
Используется `cutscene_load_json` для декларативного создания Action-struct из JSON.

## JSON‑загрузка
- `cutscene_load_json(path)` — читает JSON (сгенерированный [редактором Undefscene](./undefscene/overview.md) через Export for Engine), конвертирует секунды/px‑sec в кадры/px‑frame и создаёт `obj_cutsceneManager`.
- Для парсинга использует `global.__cutscene_action_factory` (инициализируется `cutscene_init_action_factory()`).

## Примечания
### Chatterbox-интеграция
Все `ChatterboxAddFunction`-обёртки теперь **stateless** и требуют явный `target`:
- `c_walk(target, dir, speed, frames)`
- `c_walkdirect(target, x, y, frames)`
- `c_walkdirect_speed(target, x, y, speed)`
- `c_setxy(target, x, y)`
- `c_depth(target, depth)`
- `c_facing(target, dir)`
- `c_autofacing(target, enabled)`
- `c_autowalk(target, enabled)`
- `c_sprite(target, sprite, ...)`

Если обёртка принимает legacy значения (например, строковые имена актёров), рекомендуется мигрировать вызовы на instance id.

`cutscene_wait` и `c_wait` работают в кадрах (см. реализацию `ActionWait`).
