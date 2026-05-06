---
tags:
  - cutscenes
  - cutscene-api
  - yarn
---

# Катсцены: API

Интерфейсы управления катсценным движком через Builder-API (`c_*`), Action-API (`cutscene_*`) и JSON.

## Стандарты
- **`target_ref`**: instance id или строковый ключ актёра.
- **Единицы**: Builder-API использует **кадры** (длительность) и **px/frame** (скорость).
- **JSON**: использует **секунды** и **px/sec** (конвертируются при загрузке).
- **Звук**: управляется через `obj_music_ctrl`, катсцены вызывают его через `c_run` или `global.play_music`.

## Builder-API (`c_*`)
Построение очереди через активный менеджер без передачи ссылки на него в каждый вызов.

### Жизненный цикл
- `c_begin(id)`: инициализация менеджера.
- `c_play()`: запуск выполнения.
- `c_end()`: принудительное завершение.

### Основные команды
- `c_speaker(name)`: установка имени говорящего.
- `c_setxy(target, x, y)`: телепортация актёра.
- `c_facing(target, dir)`: поворот персонажа.
- `c_visible(target, bool)`: управление видимостью.
- `c_wait(frames)`: задержка выполнения.

### Камера
- `c_pan(x, y, frames)`: плавное перемещение.
- `c_panobj(target, frames)`: слежение за объектом.
- `c_shake(frames, magnitude)`: эффект тряски.

## Action-API (`cutscene_*`)
Прямое создание структур Action-struct.

- `cutscene_move(target, x, y, speed)`: перемещение.
- `cutscene_animate(target, sprite, ...)`: смена анимации.
- `cutscene_dialogue(file, node)`: запуск Yarn-диалога.
- `cutscene_parallel(actions)`: параллельное выполнение.
- `cutscene_tween(target, property, ...)`: плавная анимация свойств.

## JSON и Фабрика Экшенов
`cutscene_load_json(path)` загружает декларативные описания сцен.

### JSON actions

| Type | Поля | Результат в движке |
|------|------|--------------------|
| `camera_pan` | `x`, `y`, `seconds` | `ActionCameraPan` двигает view к координатам |
| `camera_pan_obj` | `target`, `seconds` | `ActionCameraPanToObj` двигает view к актёру |
| `camera_center` | `x`, `y` | `ActionCameraCenter` мгновенно центрирует камеру |
| `camera_track` | `target`, `seconds`, `offset_x`, `offset_y` | `ActionCameraTrack` следует за целью |
| `camera_track_until_stop` | `target`, `offset_x`, `offset_y` | `ActionCameraTrackUntilStop` следует до остановки |
| `camera_shake` | `seconds`, `magnitude` | `ActionCameraShake` трясёт экран |
| `set_facing` | `target`, `direction` | меняет `facing_direction` и idle/walk sprite |
| `auto_facing` | `target`, `enabled` | записывает `auto_face` |
| `auto_walk` | `target`, `enabled` | записывает `auto_walk` |
| `set_depth` | `target`, `depth` | записывает `depth` |
| `set_position` | `target`, `x`, `y` | переносит актёра и обновляет `target_x`, `target_y` |
| `set_property` | `kind`, `target`, `property`, `value` | записывает произвольное свойство instance или камеры |
| `tween` | `target`, `property`, `to_value`, `from_value`, `seconds`, `easing` | плавно меняет числовое свойство instance |
| `tween_camera` | `property`, `to_value`, `from_value`, `seconds`, `easing` | плавно меняет `x` или `y` камеры |

`direction` принимает `left`, `right`, `up`, `down` или числовое значение из `global.DIR`.

### Нормализация имен
Старые имена автоматически приводятся к каноническим:
- `shakeobj` → `shake_object`
- `visible` → `set_visible`
- `waittalk` → `wait_for_dialogue`
- `facing` → `set_facing`
- `autofacing` → `auto_facing`
- `autowalk` → `auto_walk`

!!! note "Таймаут диалогов"
    Если `chatterbox` не отвечает более 600 кадров (~20 сек), экшен завершается принудительно во избежание зависания сцены.

---

## См. также

- [Архитектура катсцен](architecture.md) — `obj_cutsceneManager`, жизненный цикл, target resolution
- [Актёры](actors.md) — `actor_map`, `ActionActorCreate`, `ActionActorDestroy`
- [Камера](camera.md) — `ActionCameraPan`, `ActionCameraTrack`, `ActionCameraShake`
- [Игрок в катсцене](player_in_cutscene.md) — флаги, блокировка движения, camera override
- [Отладка](debugging.md) — debug overlay, stuck watchdog
- [Примеры](examples.md) — JSON-загрузка и Builder-стиль
