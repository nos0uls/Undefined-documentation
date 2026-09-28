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
- **Звук**: управляется через `obj_music_ctrl`, катсцены вызывают его через музыкальные Action-классы (`ActionMusicPlay` и др.) или `global.play_music*`.

## Builder-API (`c_*`)
Построение очереди через активный менеджер без передачи ссылки на него в каждый вызов.

### Жизненный цикл
- `c_begin(id)`: инициализация менеджера.
- `c_play()`: запуск выполнения.
- `c_end()`: принудительное завершение.

!!! note "Живые команды"
    Реально существующие `c_*` команды (все определены в `scripts/c_cmd/c_cmd.gml` и отдельных `scripts/c_*/`): `c_begin`, `c_play`, `c_play_json`, `c_end`, `c_wait`, `c_waittalk`, `c_setxy`, `c_facing`, `c_speaker`, `c_depth`, `c_autofacing`, `c_autowalk`, `c_dialogue`, `c_animate`, `c_sprite`, `c_tween`, `c_tween_camera`, `c_fadein`, `c_fadeout`, `c_sfx`, `c_soundplay`, `c_emote`, `c_jump`, `c_halt`, `c_flip`, `c_spin`, `c_shakeobj`, `c_visible`, `c_instant`, `c_walk`, `c_walkdirect`, `c_walkdirect_speed`, `c_var_instance`, `c_var_lerp_instance`, `c_var_lerp_to_instance`, `c_lerp`.

!!! warning "Заглушки (не вызывать)"
    Команды-заглушки с пустым телом и пометкой `DELETE_CANDIDATE`: `c_pan`, `c_panobj`, `c_panspeed`, `c_pan_wait`, `c_shake`, `c_instance`, `c_delaycmd`, `c_delaywalk`, `c_cmd_x`. Имен `c_move`, `c_follow_path`, `c_actor_create`, `c_actor_destroy`, `c_parallel`, `c_branch`, `c_camera_track`, `c_camera_track_until_stop`, `c_camera_center`, `c_run`, `c_move_group`, `c_walk_group`, `c_var_group`, `c_tween_group` в проекте нет — для parallel/branch/камеры используйте JSON-экшены или Action-классы напрямую.

### Основные команды
- `c_speaker(name)`: установка имени говорящего.
- `c_setxy(target, x, y)`: телепортация актёра.
- `c_facing(target, dir)`: поворот персонажа.
- `c_visible(target, bool)`: управление видимостью.
- `c_wait(frames)`: задержка выполнения.

### Камера
- `c_tween_camera(property, to_value, frames, easing, from_value)`: плавное изменение числового свойства камеры.
- Остальные камерные `c_*` команды удалены (заглушки) — в JSON используйте `camera_pan`, `camera_pan_obj`, `camera_center`, `camera_track`, `camera_track_until_stop`, `camera_shake`.

## Action-API (`cutscene_*`)
Прямое создание структур Action-struct и управление менеджером.

Живые wrapper-функции:

- `cutscene_add(manager, action)` — добавляет Action-struct в очередь менеджера (`scripts/cutscene_add`).
- `cutscene_branch(condition_func, true_actions, false_actions)` — возвращает `ActionBranch`.
- `cutscene_set_facing(target_ref, direction)` — возвращает `ActionSetFacing`.
- `cutscene_music_pitch(pitch)` / `cutscene_music_pause()` / `cutscene_music_resume()` — возвращают музыкальные Action-классы (`scripts/scr_cutscene_music`).
- `cutscene_play_json(path)` / `cutscene_stop_active()` / `cutscene_is_active()` / `cutscene_dialogue_is_active()` — управление JSON-катсценой (определены в `scripts/c_cmd/c_cmd.gml`).
- `cutscene_load_json(path)` / `cutscene_load_engine_settings()` — загрузка сцены и настроек движка.

!!! warning "Обёртки-заглушки и удалённые имена"
    Часть shorthand-обёрток зачищена до заглушек (`DELETE_CANDIDATE`, пустые тела — ресурсы на месте, но вызывать их бессмысленно): `cutscene_move`, `cutscene_set_xy`, `cutscene_animate`, `cutscene_set_depth`, `cutscene_auto_facing_toggle`, `cutscene_auto_walk_toggle`, `cutscene_dialogue`, `cutscene_parallel`, `cutscene_camera_center`, `cutscene_camera_pan`, `cutscene_camera_shake`, `cutscene_camera_track`, `cutscene_actor_create`, `cutscene_actor_destroy`, `cutscene_follow_path`, `cutscene_run_function`, `cutscene_wait`.

    Следующие имена удалены из проекта полностью (ресурсов нет): `cutscene_set_dialogue_speed`, `cutscene_wait_typing`, `cutscene_dialogue_control`, `cutscene_wait_for_dialogue`, `cutscene_set_portrait_next`, `cutscene_set_portrait_now`, `cutscene_clear_dialogue`, `cutscene_tween`, `cutscene_tween_camera`, `cutscene_set_animation_frame`, `cutscene_fade_in`, `cutscene_fade_out`, `cutscene_play_sfx`, `cutscene_emote`, `cutscene_jump`, `cutscene_halt`, `cutscene_flip`, `cutscene_spin`, `cutscene_shake_object`, `cutscene_set_visible`, `cutscene_set_instant`, `cutscene_set_property` и мёртвые `cutscene_music_*` (кроме pitch/pause/resume).

    Вместо обёрток создавайте Action-классы напрямую (`new ActionMove(...)`, `new ActionDialogue(...)`, `new ActionMusicPlay(...)` и т.д.) или используйте JSON-экшены — фабрика `cutscene_action_factory` конструирует их через `new`.

## JSON и Фабрика Экшенов
`cutscene_load_json(path)` загружает декларативные описания сцен.

### JSON actions

Основные типы (выборочно — полный список типов смотрите в `f[$ ...]`-таблице `cutscene_action_factory.gml`):

| Type | Поля | Результат в движке |
|------|------|--------------------|
| `camera_pan` | `x`, `y`, `seconds` | `ActionCameraPan` двигает view к координатам |
| `camera_pan_obj` | `target`, `seconds` | `ActionCameraPanToObj` двигает view к актёру с clamp к границам комнаты |
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
| `tween` | `target`, `property`, `to_value`, `from_value`, `seconds`, `easing`, `kind` | плавно меняет числовое свойство instance. Фабрика читает `kind` (`"instance"` по умолчанию); `kind:"camera"` работает без `target` — для камеры предпочтителен отдельный `tween_camera` |
| `tween_camera` | `property`, `to_value`, `from_value`, `seconds`, `easing` | плавно меняет числовое свойство камеры (`kind="camera"`). Для камеры используйте именно `tween_camera`, а не `tween` |
| `attach_to_target` | `target`, `parent`, `offset_x`, `offset_y`, `follow_facing`, `follow_scale`, `follow_depth`, `duration_seconds`, `detach_on_cutscene_end` | привязывает актёра к родителю (`parent_ref` — fallback-алиас для `parent`) |
| `detach` | `target`, `destroy_after_detach` | отсоединяет актёра от родителя (`target_ref` — legacy алиас) |
| `spin` | `target`, `speed`, `seconds` | вращает актёра |
| `set_visible` | `target`, `visible` | управляет видимостью актёра |
| `schedule_action` | `delay_seconds`, `action`, `blocking`, `tag` | отложенное выполнение вложенного действия |
| `checkpoint_state` | `checkpoint_id`, `include_actors`, `include_player`, `include_camera`, `include_music`, `include_globals` (массив или JSON-строка), `include_instances` (массив или JSON-строка) | сохранение состояния катсцены |
| `restore_state` | `checkpoint_id`, `cleanup_transients`, `restore_camera`, `restore_music`, `on_missing` | восстановление состояния катсцены |
| `set_flag` | `key`, `value` | установка глобального флага |
| `set_plot` | `value` | изменение `global.plot` |
| `spawn_entity` | `object`, `key`, `x`, `y`, `depth`, `persistent` | создание объекта в мире |
| `destroy_entity` | `target` | удаление объекта |
| `partial_control` | `control_type`, `whitelist` | частичный контроль игрока (см. ниже) |
| `wait_for_interact` | `target`, `timeout`, `timeout_action`, `interact_action` | ожидание взаимодействия |
| `room_change` | `room` (string), `player_x`, `player_y`, `actors` (object: ключ → `{x,y}` или `[x,y]`) | `ActionRoomChange` — блокирующая смена комнаты с фейдом |
| `set_dialogue_speed` | `speed` | скорость печати текста |
| `wait_typing` | — | ожидание завершения анимации печати |
| `dialogue_control` | `prevent_skip`, `stay_open`, `auto_advance` | управление поведением диалога |
| `set_portrait_next` | `target`, `emotion` | установка портрета для следующей реплики |
| `set_portrait_now` | `target`, `emotion` | мгновенная смена портрета |
| `clear_dialogue` | — | очистка диалогового окна |
| `fade_in` | `seconds`, `color` | `ActionFadeIn` — затухание из чёрного (по умолчанию `color = c_black`) |
| `fade_out` | `seconds`, `color` | `ActionFadeOut` — затемнение до чёрного (по умолчанию `color = c_black`) |
| `play_sfx` | `sound`, `volume`, `pitch` | `ActionPlaySFX` — проигрывание звукового эффекта |
| `emote` | `target`, `sprite`, `seconds`, `offset_x`, `offset_y`, `scale`, `wait` | `ActionEmote` — показ эмоции над персонажем |
| `flip` | `target`, `flipped` | отражение спрайта по горизонтали (`image_xscale`) |
| `jump` | `target`, `x`, `y`, `seconds`, `height`, `easing` | `ActionJump` — прыжок к координатам с дугой |
| `halt` | `target` | `ActionHalt` — остановка движения актёра |
| `camera_pan_speed` | `x`, `y`, `seconds` | `ActionCameraPanSpeed` — панорамирование со скоростью (linear easing) |
| `branch` | `condition` (string), `true_actions` (array), `false_actions` (array) | `ActionBranch` — ветвление по результату функции/скрипта |
| `branch_flag` | `key` (string), `operator` (string), `value` (any), `true_actions` (array), `false_actions` (array) | `ActionBranchFlag` — ветвление по значению флага/состояния (см. ниже) |
| `guard_global` | `var` (string), `equals` (any), `if_false` (`skip` or `wait_until_true`), `actions` (array), `stop_when` (`none`, `timeout`, `global_var`, `node_reached`), `end_var` (string), `end_equals` (any), `end_node` (string), `end_timeout` (real) | `ActionGuardGlobal` — условный блок или ожидание глобальной переменной |

`direction` принимает `left`, `right`, `up`, `down` или числовое значение из `global.DIR`.

### Загрузчик и формат файла

`cutscene_load_json(path)` читает файл целиком через `buffer_load`/`buffer_read`, срезает UTF-8 BOM (сигнатура `EF BB BF`) и нормализует префиксы `./` и `datafiles/` в начале пути (в рантайме каталога `datafiles/` нет — Included Files лежат в корне рабочей директории). Парсинг — нативный `json_parse`: корень обязан быть объектом (struct), `actions` — массивом; вложенные объекты приходят как `struct`/`array`, ручной `destroy` не нужен.

Служебные элементы списка: `{"type": "start", "debug": true}` включает отладку катсцены (не является действием), `{"type": "end"}` завершает список — действия после него не выполняются. `settings.fps` валидируется в диапазоне 1..240; при отсутствии/невалидности берётся `default_fps` из настроек движка.

Настройки движка загружает `cutscene_load_engine_settings()` из единственного канонического файла `cutscenes/cutscene_engine_settings.json` (в проекте — `datafiles/cutscenes/cutscene_engine_settings.json`; корневой дубль удалён). Функция кэширует результат в `static` и возвращает struct «только для чтения»; принудительное перечитывание — через `_force_reload = true`.

### `branch_flag`

Ветвление по значению флага или состояния мира. `key` без точки читается из `global.flag[key]`; ключ с точкой резолвится через общий резолвер `__cutscene_resolve_state_value`:

| Форма ключа | Источник |
|-------------|----------|
| `"met_asher"` | `global.flag["met_asher"]` |
| `"flag.x"` / `"flags.x"` | `global.flag[$ "x"]` |
| `"stat.hp"` / `"stats.hp"` | `global.stat_hp` |
| `"entity_state.rm:eid"` / `"entity.rm:eid"` | запись `global.entity_state["rm:eid"]` |
| `"entity_state.rm:eid.field"` | поле `field` записи сущности |
| `"struct_name.field"` | `global[$ struct_name][$ field]` |
| `"global.name"` (любой) | префикс `global.` срезается |

| `operator` | Семантика |
|------------|-----------|
| `==`, `!=` | Сравнение через `__cutscene_compare_values` (толерантно к строкам/булям из JSON) |
| `>`, `<`, `>=`, `<=` | Числовое сравнение (оба операнда приводятся к real) |
| `exists` | Ключ/путь существует и значение не `undefined` |
| `!exists` | Ключа нет или значение `undefined` |

Неизвестный оператор деградирует до `==` с WARNING в логе. Ветки `true_actions`/`false_actions` — массивы вложенных action-объектов; выбранная ветка вставляется в очередь после текущего действия.

```json title="Пример branch_flag"
{
  "type": "branch_flag",
  "key": "flag.met_asher",
  "operator": "==",
  "value": true,
  "true_actions": [ { "type": "dialogue", "file": "asher.yarn", "node": "Met" } ],
  "false_actions": [ { "type": "dialogue", "file": "asher.yarn", "node": "FirstMeet" } ]
}
```

### `room_change`

Блокирующая смена комнаты: создаёт `obj_changingRoomsController` с фейдом, `update()` завершается после затухания. `room`, `player_x`, `player_y` обязательны; `actors` — необязательный объект позиций актёров.

!!! warning "Переход в текущую комнату"
    `room_change` в текущую комнату — no-op: контроллер затухает без `room_goto`, action пишет WARNING «same-room завершение без перехода» и сбрасывает сохранённые параметры. Телепортации игрока и перезапуска комнаты не происходит.

### `partial_control`

`control_type` — enum `INTERACT_PARTIAL_CONTROL`: `0` LOCKED (стандарт), `1` WHITELIST, `2` FREE. При `1` через input API во время катсцены пропускается только действие `confirm` — `wait_for_interact` без него становился бы софтлоком; конкретные допустимые объекты проверяет `scr_interaction` по `whitelist` (массив строк-ключей актёров). Тип `2` сохраняет семантику полной свободы. Подробности — в [Частичный контроль](partial-control.md).

### `checkpoint_state` — формат полей

Поля `include_globals` и `include_instances` принимают **и обычный JSON-массив, и legacy-строку с JSON внутри** — фабрика берёт значение через `get_value` и разбирает строку через `json_parse`.

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
    Если `chatterbox` не отвечает более 600 кадров (~10 сек при 60 fps), экшен завершается принудительно во избежание зависания сцены.

## Dialogue Control

`dialogue_control` управляет поведением активного диалогового окна (`textboxTest_scribble`). Флаги применяются к текущему контроллеру и сохраняются в `obj_cutsceneManager` для новых диалогов.

| Поле | Тип | Описание |
|------|-----|----------|
| `prevent_skip` | bool | `true` — блокирует `confirm` для скипа печати текста. Подтверждение всё ещё продвигает допечатанную реплику. |
| `stay_open` | bool | `true` — `textboxTest_scribble` не уничтожается при `ChatterboxIsStopped`. Окно остаётся открытым до явного `clear_dialogue`. |
| `auto_advance` | bool | `true` — каждый кадр автоматически вызывает `confirm`, диалог проходит самостоятельно. |

```json title="Пример dialogue_control"
{
  "type": "dialogue_control",
  "prevent_skip": true,
  "stay_open": false,
  "auto_advance": false
}
```

!!! warning "stay_open и ActionWaitForDialogue"
    При `stay_open = true` `ActionWaitForDialogue` считает диалог активным, пока окно не закрыто. Закрывайте такой диалог вручную через `clear_dialogue`.

## Branch и Guard Global

### Branch

`branch` выполняет **одну** из двух веток в зависимости от результата `condition`.

- `condition` — имя GML-скрипта, функции, метода или callable-переменной. **Не выражение**.
- Возвращаемое значение приводится к `bool`.
- Ветка вставляется в `action_queue` менеджера и выполняется последовательно.

```json title="Пример branch"
{
  "type": "branch",
  "condition": "scr_check_player_has_key",
  "true_actions": [
    { "type": "dialogue", "file": "npc.yarn", "node": "HasKey" }
  ],
  "false_actions": [
    { "type": "dialogue", "file": "npc.yarn", "node": "NoKey" }
  ]
}
```

### Guard Global

`guard_global` — условный блок. Поля `var` и `end_var` поддерживают ту же dot-нотацию, что и `key` в `branch_flag` (`flag.x`, `stat.hp`, `entity_state.rm:eid[.field]`, `struct_name.field`; префикс `global.` срезается). Режим `if_false` определяет поведение при ложном условии:

- `skip` (по умолчанию) — пропускает `actions`, если условие ложно.
- `wait_until_true` — приостанавливает катсцену и ждёт, пока условие станет истинным.

При `wait_until_true` можно задать `stop_when` — условие прекращения ожидания без выполнения `actions`:

| `stop_when` | Описание |
|-------------|----------|
| `none` | Ждать бесконечно (по умолчанию). |
| `timeout` | Прервать ожидание через `end_timeout` секунд. |
| `global_var` | Прервать, когда `global[end_var] == end_equals`. |
| `node_reached` | Прервать, когда катсцена достигнет ноды `end_node` через `mark_node`. |

```json title="Пример guard_global: wait_until_true с timeout"
{
  "type": "guard_global",
  "var": "global.door_opened",
  "equals": true,
  "if_false": "wait_until_true",
  "stop_when": "timeout",
  "end_timeout": 5.0,
  "actions": [
    { "type": "dialogue", "file": "npc.yarn", "node": "DoorOpened" }
  ]
}
```

```json title="Пример guard_global: skip"
{
  "type": "guard_global",
  "var": "global.has_key",
  "equals": true,
  "if_false": "skip",
  "actions": [
    { "type": "dialogue", "file": "npc.yarn", "node": "HasKey" }
  ]
}
```

!!! note "set_flag vs guard_global"
    `set_flag` пишет в `global.flag[$ key]` (аргумент `key` — без точек). `guard_global` читает переменную через резолвер состояния: для флага сюжета используйте путь `"flag.<key>"`, например `"var": "flag.met_asher"`.

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

Живыми wrapper-функциями остались только `cutscene_music_pitch(pitch)`, `cutscene_music_pause()` и `cutscene_music_resume()` — они возвращают `ActionMusicPitch`/`ActionMusicPause`/`ActionMusicResume`. Остальные shorthand-обёртки удалены: из кода создавайте Action-классы напрямую через `new` (фабрика JSON-экшенов делает то же самое):

| Вызов | Описание |
|-------|----------|
| `new ActionMusicPlay(snd_asset, fade_sec, volume = 1.0)` | Смена трека |
| `new ActionMusicStop(fade_sec)` | Остановка с затуханием |
| `new ActionMusicVolume(vol, fade_sec)` | Плавное изменение громкости |
| `new ActionMusicDuck(multiplier, fade_sec)` | Относительное приглушение |
| `new ActionMusicUnduck(fade_sec)` | Снятие duck |
| `new ActionMusicPlayLayered(calm_asset, battle_asset, fade_sec)` | Запуск calm + battle |
| `new ActionMusicSetIntensity(intensity, fade_sec)` | Смена интенсивности |
| `new ActionMusicIntroLoop(intro_asset, loop_asset, fade_sec)` | Intro + loop |
| `new ActionMusicIntroLayered(intro_asset, calm_asset, battle_asset, fade_sec, start_intensity)` | Intro + layered loop |
| `new ActionMusicPhaseSequence(phases, fade_sec)` | Фазовая последовательность |

!!! note "Кроссфейд и немедленный старт"
    Если `fade <= 0`, `play_music` вызывает `global.play_music_immediate()`. При `fade > 0` — `global.play_music_fade()`.

!!! note "Action-классы музыки"
    Все музыкальные action-классы реализованы в `scripts/scr_cutscene_music/scr_cutscene_music.gml`. Они не блокируют очередь катсцены — инициируют команду в `obj_music_ctrl`, а фейды обрабатываются независимо.

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
| `wait_until` | `condition_var` (string), `condition_equals` (string), `timeout_seconds` (real) | ждёт, пока глобальная переменная станет равна значению |

!!! warning "Только в редакторе Undefscene"
    `wait_until` — синтаксический сахар **уровня редактора**: компилятор Undefscene превращает ноду в `guard_global` с `if_false: "wait_until_true"`. Runtime-фабрика `cutscene_action_factory` тип `wait_until` **не регистрирует** — рукописный JSON с `"type": "wait_until"` будет отброшен как неизвестный. Вручную пишите `guard_global` с `if_false: "wait_until_true"` и нужным `stop_when`.

---

## См. также

- [Архитектура катсцен](architecture.md) — `obj_cutsceneManager`, жизненный цикл, target resolution
- [Актёры](actors.md) — `actor_map`, `ActionActorCreate`, `ActionActorDestroy`
- [Камера](camera.md) — `ActionCameraPan`, `ActionCameraTrack`, `ActionCameraShake`
- [Игрок в катсцене](player_in_cutscene.md) — флаги, блокировка движения, camera override
- [Отладка](debugging.md) — debug overlay, stuck watchdog
- [Примеры](examples.md) — JSON-загрузка и Builder-стиль
