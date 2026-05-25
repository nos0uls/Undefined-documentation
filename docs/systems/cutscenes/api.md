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
| `tween_camera` | `property`, `to_value`, `from_value`, `seconds`, `easing` | плавно меняет `x` или `y` камеры (legacy, рекомендуется `tween` с `kind=camera`) |
| `attach_to_target` | `target_ref`, `parent_ref`, `offset_x`, `offset_y`, `follow_facing`, `follow_scale`, `follow_depth`, `duration_seconds`, `detach_on_cutscene_end` | привязывает актёра к родителю |
| `detach` | `target_ref`, `keep_world_position`, `destroy_after_detach` | отсоединяет актёра от родителя |
| `spin` | `target`, `speed`, `seconds` | вращает актёра |
| `set_visible` | `target`, `visible` | управляет видимостью актёра |
| `schedule_action` | `delay_seconds`, `action`, `blocking`, `tag` | отложенное выполнение вложенного действия |
| `checkpoint_state` | `checkpoint_id`, `include_actors`, `include_player`, `include_camera`, `include_music`, `include_globals` (JSON-строка), `include_instances` (JSON-строка) | сохранение состояния катсцены |
| `restore_state` | `checkpoint_id`, `cleanup_transients`, `restore_camera`, `restore_music`, `on_missing` | восстановление состояния катсцены |
| `set_flag` | `key`, `value` | установка глобального флага |
| `set_plot` | `value` | изменение `global.plot` |
| `spawn_entity` | `object`, `key`, `x`, `y`, `depth`, `persistent` | создание объекта в мире |
| `destroy_entity` | `target` | удаление объекта |
| `partial_control` | `control_type`, `whitelist` | частичный контроль игрока |
| `wait_for_interact` | `target`, `timeout`, `timeout_action` | ожидание взаимодействия |
| `set_dialogue_speed` | `speed` | скорость печати текста |
| `wait_typing` | — | ожидание завершения анимации печати |
| `dialogue_control` | `prevent_skip`, `stay_open`, `auto_advance` | управление поведением диалога |
| `set_portrait_next` | `target`, `emotion` | установка портрета для следующей реплики |
| `set_portrait_now` | `target`, `emotion` | мгновенная смена портрета |
| `clear_dialogue` | — | очистка диалогового окна |
| `set_depth` | `target` (string), `depth` (real) | `ActionSetDepth` — устанавливает depth и переключает `depth_mode` в `manual` |
| `spin` | `target` (string), `speed` (real), `seconds` (real) | `ActionSpin` — вращает актёра |
| `set_visible` | `target` (string), `visible` (bool) | `ActionSetProperty` — управляет видимостью |

`direction` принимает `left`, `right`, `up`, `down` или числовое значение из `global.DIR`.

### `checkpoint_state` — формат полей

Поля `include_globals` и `include_instances` передаются как **JSON-строки**, а не массивы. Runtime парсит их через `json_parse`.

```json title="Пример checkpoint_state"
{
  "type": "checkpoint_state",
  "checkpoint_id": "save_1",
  "include_actors": true,
  "include_globals": "[\"global.lives\", \"global.score\"]",
  "include_instances": "[\"inst_1\", \"inst_2\"]"
}
```

### `parallel` — формат веток

Каждый элемент массива `actions` — это либо один action-объект, либо массив объектов (sequence). Пустые ветки допустимы и игнорируются.

```json title="Пример parallel"
{
  "type": "parallel",
  "actions": [
    { "type": "move", "target": "player", "x": 100, "y": 200, "speed_px_sec": 120 },
    [
      { "type": "wait", "seconds": 0.5 },
      { "type": "camera_shake", "seconds": 1, "magnitude": 4 }
    ]
  ]
}
```

### Базовые классы

Для устранения дублирования кода созданы базовые Action-классы:

| Базовый класс | Наследники | Общая логика |
|---------------|------------|-------------|
| `ActionMoveBase` | `ActionMove`, `ActionMoveRelative` | tween-based перемещение, коллизия, `move_active` |
| `ActionCameraPanBase` | `ActionCameraPan`, `ActionCameraPanSpeed` | расчёт целевых координат, tween-система |
| `ActionCameraTrackBase` | `ActionCameraTrack`, `ActionCameraTrackUntilStop` | слежение за целью, `offset_x/y`, `resolver` |
| `ActionShakeBase` | `ActionCameraShake`, `ActionShakeObject` | амплитуда, частота, decay |

!!! note "ActionCameraPanSpeed"
    `ActionCameraPanSpeed` использует linear easing и перемещает камеру на фиксированное расстояние за кадр. Зарегистрирован в `cutscene_action_factory`.

### Нормализация имен
Неканонические имена автоматически приводятся к каноническим:
- `shakeobj` → `shake_object`
- `visible` → `set_visible`
- `waittalk` → `wait_for_dialogue`
- `facing` → `set_facing`
- `autofacing` → `auto_facing`
- `autowalk` → `auto_walk`

!!! note "Таймаут диалогов"
    Если `chatterbox` не отвечает более 600 кадров (~20 сек), экшен завершается принудительно во избежание зависания сцены.

## Музыка в катсценах

| Type | Поля | Результат в движке |
|------|------|--------------------|
| `play_music` | `sound` (string), `volume` (real, 0..1), `fade` (real, sec) | `ActionMusicPlay` — смена трека с кроссфейдом |
| `stop_music` | `fade` (real, sec) | `ActionMusicStop` — остановка с затуханием |
| `music_volume` | `volume` (real, 0..1), `fade` (real, sec) | `ActionMusicVolume` — плавное изменение громкости |
| `music_duck` | `multiplier` (real, 0..1), `fade` (real, sec) | `ActionMusicDuck` — относительное приглушение |
| `music_unduck` | `fade` (real, sec) | `ActionMusicUnduck` — снятие duck |
| `music_pitch` | `pitch` (real) | `ActionMusicPitch` — установка скорости воспроизведения (playback rate). `1.0` = нормальная скорость |
| `music_pause` | — | `ActionMusicPause` — пауза |
| `music_resume` | — | `ActionMusicResume` — возобновление |
| `play_boss_music` | `calm` (string), `battle` (string), `fade` (real, sec) | `ActionMusicPlayLayered` — запуск calm + battle |
| `stop_boss_music` | `fade` (real, sec) | `ActionMusicStop` — остановка с затуханием |
| `boss_music_phase` | `phases` (JSON array), `fade` (real, sec) | `ActionMusicPhaseSequence` — фазовая последовательность |
| `play_music_intro` | `intro` (string), `loop` (string), `fade` (real, sec) | `ActionMusicIntroLoop` — intro + loop |
| `play_music_intro_layered` | `intro` (string), `calm` (string), `battle` (string), `fade` (real, sec), `start_intensity` (real, 0..1) | `ActionMusicIntroLayered` — intro + layered loop |
| `crossfade_music` | `intensity` (real, 0..1), `fade` (real, sec) | `ActionMusicSetIntensity` — смена соотношения calm/battle |

**GML-эквиваленты**

| Функция | Action-класс | Описание |
|---------|-------------|----------|
| `cutscene_music_play(snd_asset, fade_sec = 0.5)` | `ActionMusicPlay` | Смена трека |
| `cutscene_music_stop(fade_sec = 1.0)` | `ActionMusicStop` | Остановка с затуханием |
| `cutscene_music_volume(vol, fade_sec = 0.5)` | `ActionMusicVolume` | Плавное изменение громкости |
| `cutscene_music_duck(multiplier = 0.3, fade_sec = 0.3)` | `ActionMusicDuck` | Относительное приглушение |
| `cutscene_music_unduck(fade_sec = 0.3)` | `ActionMusicUnduck` | Снятие duck |
| `cutscene_music_pitch(pitch)` | `ActionMusicPitch` | Установка скорости воспроизведения. `1.0` = нормальная скорость |
| `cutscene_music_pause()` | `ActionMusicPause` | Пауза |
| `cutscene_music_resume()` | `ActionMusicResume` | Возобновление |
| `cutscene_music_layered(calm_asset, battle_asset, fade_sec = 0.5)` | `ActionMusicPlayLayered` | Запуск calm + battle |
| `cutscene_music_intensity(intensity, fade_sec = 1.0)` | `ActionMusicSetIntensity` | Смена интенсивности |
| `cutscene_music_intro_loop(intro_asset, loop_asset, fade_sec = 0.5)` | `ActionMusicIntroLoop` | Intro + loop |
| `cutscene_music_intro_layered(intro_asset, calm_asset, battle_asset, fade_sec = 0.5, start_intensity = 0)` | `ActionMusicIntroLayered` | Intro + layered loop |
| `cutscene_music_phase_sequence(phases, fade_sec = 0.5)` | `ActionMusicPhaseSequence` | Фазовая последовательность |

!!! note "Кроссфейд и немедленный старт"
    Если `fade <= 0`, `play_music` вызывает `global.play_music_immediate()`. При `fade > 0` — `global.play_music_fade()`.

!!! note "Action-классы музыки"
    Все музыкальные action-классы реализованы как отдельные классы в `scr_cutscene_classes.gml`. Они не блокируют очередь катсцены — инициируют команду в `obj_music_ctrl`, а фейды обрабатываются независимо.

## Относительное позиционирование

| Type | Поля | Результат в движке |
|------|------|--------------------|
| `move_relative` | `target` (string), `dx` (real, px), `dy` (real, px), `speed_px_sec` (real), `collision` (bool) | `ActionMoveRelative` — движение на offset от текущей позиции |
| `set_position_relative` | `target` (string), `dx` (real, px), `dy` (real, px) | `ActionSetPositionRelative` — мгновенный сдвиг |

**GML-эквиваленты**

- `new ActionMoveRelative(target, dx, dy, speed_pf, collision)` — двигает актёра на `(dx, dy)` от позиции на момент старта.
- `new ActionSetPositionRelative(target, dx, dy)` — мгновенно сдвигает актёра.

!!! note "Скорость и коллизия"
    `speed_px_sec` конвертируется в `px/frame` при загрузке JSON. `collision = true` включает `move_and_collide` с `obj_collider`.

## `wait_until`

| Type | Поля | Результат в движке |
|------|------|--------------------|
| `wait_until` | `condition_var` (string), `condition_equals` (string), `timeout_seconds` (real) | `ActionGuardGlobal` с `if_false: "wait_until_true"` |

!!! info "Синтаксический сахар"
    `wait_until` не имеет отдельного Action-класса. При компиляции JSON нода превращается в `guard_global` с `if_false: "wait_until_true"` и пустым `actions`. В GML это эквивалентно `new ActionGuardGlobal(var_name, equals, [], "wait_until_true", "none", "", "", "", 0)` (при `timeout_seconds = 0`). Таймаут конвертируется во фреймы и передаётся в `end_timeout_frames`.

---

## См. также

- [Архитектура катсцен](architecture.md) — `obj_cutsceneManager`, жизненный цикл, target resolution
- [Актёры](actors.md) — `actor_map`, `ActionActorCreate`, `ActionActorDestroy`
- [Камера](camera.md) — `ActionCameraPan`, `ActionCameraTrack`, `ActionCameraShake`
- [Игрок в катсцене](player_in_cutscene.md) — флаги, блокировка движения, camera override
- [Отладка](debugging.md) — debug overlay, stuck watchdog
- [Примеры](examples.md) — JSON-загрузка и Builder-стиль
