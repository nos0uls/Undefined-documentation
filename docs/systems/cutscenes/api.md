# Катсцены: API

## Канон
- **`target_ref`**: канонический формат — **instance id** или строковый actor key, резолвится менеджером.
- **Единицы скорости**: **px/frame** в builder-API. Длительности в builder — **кадры**.
- **JSON‐загрузка**: в JSON длительности в **секундах**, скорости в **px/sec**, при загрузке конвертируются в кадры/px‐per‐frame.
- **Music** — отдельная система (`obj_music_ctrl` + `scr_global_music_*`). Cutscene-ядро не владеет музыкой; из катсцен музыка управляется через `c_run`/`c_sfx` или прямые вызовы `global.play_music(...)`.

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
- `c_cmd("shake", frames=60, magnitude=4)` — `ActionCameraShake(frames, magnitude)`. Дефолты 60/4 применяются, если аргументы не переданы. `ActionCameraShake` теперь корректно восстанавливает позицию камеры на cleanup и не накапливает дрейф (Phase 1 fix).

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

### Tween / Lerp
- `c_tween(target, property, to_value, frames, easing="linear", from_value=undefined)` — `ActionTween` для instance.
- `c_tween_camera(property, to_value, frames, easing="linear", from_value=undefined)` — `ActionTween` для камеры.
- `c_var_lerp_instance(target, property, from, to, frames, easing="linear")` — алиас `c_tween` с явным `from`.
- `c_lerp(target, property, from, to, frames, easing="linear")` — **короткий алиас** для `c_var_lerp_instance` (также доступен из Yarn как `<<c_lerp ...>>`).
- `c_var_lerp_to_instance(target, property, to, frames, easing="linear")` — tween от текущего значения до `to`.

> Legacy-алиасы `c_snd_play`, `c_lerp_var_instance`, `c_lerpvar_instance`, `c_wait_talk` удалены — используйте `c_soundplay`/`c_var_lerp_instance`/`c_waittalk` или короткий `c_lerp`.

### JSON Action Factory
`cutscene_init_action_factory()` создаёт глобальную фабрику `global.__cutscene_action_factory` — struct с mapping `action_type -> constructor(map, fps)`.
Используется `cutscene_load_json` для декларативного создания Action-struct из JSON.

#### Нормализация action type
Алиасы legacy-имен приводятся к canonical в `__cutscene_json_normalize_action_type()` до поиска в factory:

| Legacy | Canonical |
| ------ | --------- |
| `shakeobj` | `shake_object` |
| `visible` | `set_visible` |
| `instant_mode` | `set_instant` |
| `waittalk`, `wait_talk` | `wait_for_dialogue` |
| `depth` | `set_depth` |
| `facing` | `set_facing` |
| `autofacing` | `auto_facing` |
| `autowalk` | `auto_walk` |

#### Поддерживаемые JSON action types
Помимо очевидных (`move`, `wait`, `dialogue`, `parallel`, и т.д.) factory регистрирует:

- `camera_pan` — `ActionCameraPan(x, y, frames)` (конвертирует seconds → frames через `_fps`).
- `camera_shake` — `ActionCameraShake(frames, magnitude=4)`.
- `camera_pan_obj` — `ActionCameraPanToObj(target, frames)`.
- `camera_track` — `ActionCameraTrack(target, frames, offset_x, offset_y)`.
- `camera_track_until_stop` — `ActionCameraTrackUntilStop(target, offset_x, offset_y)`.
- `auto_facing` — `ActionSetProperty(target, "auto_face", enabled)`.
- `auto_walk` — `ActionSetProperty(target, "auto_walk", enabled)`.
- `set_facing` — принимает строковые направления (`"right"`, `"left"`, `"up"`, `"down"`, `"r"`, `"l"`, `"u"`, `"d"`) через `__cutscene_json_parse_direction`.
- `emote` — alias к `show_emote`.
- `actor_create` — поддерживает `copy_from`/`copy_target`: внешний вид (sprite/scale/blend/depth/facing) копируется из источника в новый actor.

## JSON‑загрузка
- `cutscene_load_json(path)` — читает JSON (сгенерированный [редактором Undefscene](./undefscene/overview.md) через Export for Engine), конвертирует секунды/px‑sec в кадры/px‑frame и создаёт `obj_cutsceneManager`.
- **Нормализация пути**: `\` → `/`, удаляется префикс `datafiles/` (если есть). Файл ищется сначала как есть, затем в `datafiles/`, затем fallback.
- Для парсинга использует `global.__cutscene_action_factory` (инициализируется `cutscene_init_action_factory()`).

!!! note "ActionDialogue — safety timeout"
    `ActionDialogue` имеет встроенный safety timeout: если `chatterbox` не инициализировался в течение **600 кадров** (~20 сек при 30 FPS), action автоматически завершается с сообщением в лог. Это предотвращает бесконечное зависание катсцены при битом `.yarn` файле.

!!! note "ActionDialogue — нормализация пути"
    При запуске диалога `ActionDialogue` нормализует путь к `.yarn` файлу: удаляет префиксы `datafiles/` и `Dialogues/`, проверяет существование файла по трём путям (`datafiles/Dialogues/`, `Dialogues/`, корень). Если файл не найден — fallback на `dialogue_default_file` менеджера.

## Runtime ownership и диагностика

Runtime-эффекты (tweens, jumps, spins, shakes) хранятся в массивах на `obj_globalManager` и обрабатываются `cutscene_runtime_step()` каждый кадр. Каждый entry помечен `owner_id` — id активной катсцены на момент создания.

- `cutscene_runtime_cleanup_owner(owner)` — принудительно деактивирует все entries с `owner_id == owner`. Вызывается автоматически в `finish_cutscene()`, чтобы прерванная катсцена не оставляла сиротливых tweens в очереди.
- `__cutscene_runtime_remove_at(arr, index, item)` — внутренний helper, используемый `cutscene_runtime_step` для swap-remove с гарантией `entry.active = false`.

### Debug watchdog

`obj_cutsceneManager` ведёт счётчик кадров, в течение которых текущий action уже ждёт завершения. Если счётчик превышает порог (`debug_stuck_warning_frames`, по умолчанию 600), в `show_debug_message` пишется предупреждение с `action_type` и именем катсцены. Счётчик сбрасывается при:

- переходе к следующему action,
- `start_cutscene()`,
- `finish_cutscene()`,
- invalid action struct в очереди.

В debug overlay (`Draw_64.gml`) строка `Wait: N/N frames` показывает текущее значение; когда порог превышен — цвет меняется с жёлтого на красный.

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
