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
- `c_speaker(name)` — выставляет `mgr.delta_current_actor` (строковый ключ актёра).
- `c_setxy(x, y)` — `ActionSetXY(mgr.delta_current_actor, x, y)`
- `c_depth(depth)` — `ActionSetDepth(mgr.delta_current_actor, depth)`
- `c_facing(dir)` — `ActionSetFacing(mgr.delta_current_actor, dir)`
- `c_autofacing(enabled)` — `ActionAutoFacingToggle(mgr.delta_current_actor, enabled)`
- `c_autowalk(enabled)` — `ActionAutoWalkToggle(mgr.delta_current_actor, enabled)`
- `c_instance(key, x, y)` — `ActionActorCreate(key, x, y, undefined)`

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
- `cutscene_set_depth(target_ref, depth)`
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

## JSON‑загрузка
- `cutscene_load_json(path)` — читает JSON (сгенерированный [редактором Undefscene](./editor.md) через Export for Engine), конвертирует секунды/px‑sec в кадры/px‑frame и создаёт `obj_cutsceneManager`.

## Примечания
Если обёртка принимает legacy значения (например, строковые имена актёров), рекомендуется мигрировать вызовы на instance id.

`cutscene_wait` и `c_wait` работают в кадрах (см. реализацию `ActionWait`).
