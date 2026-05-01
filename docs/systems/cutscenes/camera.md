---
tags:
  - cutscenes
  - camera
---

# Катсцены: Камера

## Как камера работает в обычной игре
Камера центрируется на игроке в `obj_player/Step_2.gml` через `camera_set_view_pos(view_camera[0], ...)`.

## Что меняется во время катсцены
При старте катсцены менеджер выставляет `global.cutscene_camera_override = true`.
Из-за этого `obj_player/Step_2.gml` делает ранний `exit`, и камера **перестаёт автоматически следовать за игроком**.

Следовательно: чтобы камера двигалась во время катсцены, катсцена должна добавлять экшены камеры.

## Action-API (через `cutscene_*`)

### Центрирование
- `cutscene_camera_center(center_x, center_y)`
  - Мгновенно ставит камеру так, чтобы центр был в `(center_x, center_y)`.

### Панорамирование
- `cutscene_camera_pan(view_x, view_y, frames)`
  - Плавно панорамирует **позицию вида** (view pos) через tween-систему (`cutscene_runtime_tween_to`).
  - Если `frames <= 0` — мгновенная установка позиции.

### Следование (track)
- `cutscene_camera_track(target_ref, frames, offset_x=0, offset_y=0)`
  - В течение `frames` кадров каждый кадр ставит камеру в центр цели.

С практической точки зрения, это основной способ сделать «камера следует за актёром».

### Тряска
- `cutscene_camera_shake(frames, magnitude=4)`

## Builder-API (через `c_*`)
Некоторые команды камеры доступны через `c_cmd`:
- `c_pan(x, y, frames)`
- `c_pan_wait(x, y, frames)`
- `c_panobj(target_ref, frames)`
- `c_panspeed(dx, dy, frames)`
- `c_shake()` (в текущем виде трясёт фиксированно)

## Замечания
- `ActionCameraPanToObj` (через `c_panobj`) выполняет clamp в пределах комнаты.
- `ActionCameraTrack` позицию не clamp-ит.
- Устаревший `camera_panner` struct (type 0/1) **удалён** — вся логика панорамирования мигрирована на tween-систему.
- `ActionCameraPanSpeed`, `ActionCameraPan`, `ActionCameraPanToObj` создают tween через `cutscene_runtime_tween_to` и завершаются когда tween неактивен.

---

## См. также

- [Обзор катсцен](overview.md) — `global.cutscene_camera_override`
- [Архитектура](architecture.md) — `obj_cutsceneManager`, tween-система
- [API](api.md) — `cutscene_camera_pan`, `cutscene_camera_track`, `cutscene_camera_shake`
- [Игрок в катсцене](player_in_cutscene.md) — блокировка камеры игроком
- [Типовые проблемы](troubleshooting.md) — камера "застыла"
