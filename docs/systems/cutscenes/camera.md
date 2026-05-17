---
tags:
  - cutscenes
  - camera
---

# Катсцены: Камера

Управление поведением камеры во время выполнения сцен.

## Механика оверрайда
В обычном режиме камера следует за игроком (`obj_player`). При старте катсцены активируется `global.cutscene_camera_override = true`, что отключает стандартное слежение.

## API Управления

### Панорамирование (`cutscene_camera_pan`)
Плавное перемещение в заданную точку через tween-систему.
- При `frames <= 0` перемещение происходит мгновенно.

| JSON type | Поля | Поведение |
|-----------|------|-----------|
| `camera_pan` | `x`, `y`, `seconds` | Двигает view к верхнему левому углу камеры |
| `camera_pan_speed` | `x`, `y`, `speed` | Двигает view со скоростью (linear easing) |
| `camera_pan_obj` | `target`, `seconds` | Двигает view к актёру или `player` |
| `camera_center` | `x`, `y` | Ставит центр камеры в точку |

`ActionCameraPanSpeed` использует linear easing и перемещает камеру на фиксированное расстояние за кадр.

### Центрирование (`cutscene_camera_center`)
Мгновенная установка камеры по координатам.

### Слежение (`cutscene_camera_track`)
Динамическое следование за целью (`target_ref`) в течение заданного времени. Это основной способ фиксации камеры на актёре.

| JSON type | Поля | Поведение |
|-----------|------|-----------|
| `camera_track` | `target`, `seconds`, `offset_x`, `offset_y` | Следует за целью заданное время |
| `camera_track_until_stop` | `target`, `offset_x`, `offset_y` | Следует за целью до остановки |

Оба класса наследуют `ActionCameraTrackBase` и переопределяют `should_finish()`:
- `ActionCameraTrack` — завершается по таймеру.
- `ActionCameraTrackUntilStop` — завершается когда `move_active` цели становится `false`.

### Тряска (`cutscene_camera_shake`)
Эффект дрожания экрана с заданной интенсивностью и длительностью.

| JSON type | Поля | Поведение |
|-----------|------|-----------|
| `camera_shake` | `seconds`, `magnitude` | Смещает экран вокруг текущей позиции камеры |

## Особенности
- `ActionCameraPanToObj` учитывает границы комнаты (clamp).
- Плавные движения используют унифицированную tween-систему.
- Базовые классы: `ActionCameraPanBase`, `ActionCameraTrackBase`, `ActionShakeBase`.
- После завершения сцены контроль возвращается игроку автоматически.

---

## См. также

- [Обзор катсцен](overview.md) — `global.cutscene_camera_override`
- [Архитектура](architecture.md) — `obj_cutsceneManager`, tween-система
- [API](api.md) — `cutscene_camera_pan`, `cutscene_camera_track`, `cutscene_camera_shake`
- [Игрок в катсцене](player_in_cutscene.md) — блокировка камеры игроком
- [Типовые проблемы](troubleshooting.md) — камера "застыла"
