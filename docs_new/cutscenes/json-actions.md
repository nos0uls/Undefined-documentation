---
title: JSON-действия катсцен — справочник
tags:
  - cutscenes
  - cutscene-json
  - data-formats
  - reference
---

# JSON-действия катсцен — справочник

Полный список типов `type`, которые разбирает фабрика `cutscene_action_factory` из массива `actions` JSON-катсцены. Для каждого типа — поля, значения по умолчанию и создаваемый `Action*`-класс.

## Формат файла

Корень JSON — объект; массив `actions` обязателен:

```json title="Скелет JSON-катсцены"
{
  "schema_version": 1,
  "cutscene_id": "my_cutscene",
  "settings": { "fps": 60, "skippable": true },
  "actions": [
    { "type": "start", "debug": true },
    { "type": "wait", "seconds": 1 },
    { "type": "end" }
  ]
}
```

| Поле верхнего уровня | Тип | Описание |
|----------------------|-----|----------|
| `cutscene_id` | string | Идентификатор сцены, пишется в `manager.cutscene_id` и `global.active_cutscene_id` |
| `schema_version` | real | Маркер экспортёра; загрузчиком не читается |
| `settings.fps` | real | FPS для конвертации секунд в кадры; валиден диапазон `1..240`, иначе берётся `default_fps` из `cutscene_load_engine_settings()` |
| `settings.skippable` | bool | `false` запрещает пропуск сцены кнопкой `back` (см. `obj_cutsceneManager/Step_0`); по умолчанию `true` |
| `actions` | array | Список действий — объектов с полем `type` |

!!! info "settings.skippable — не действие"
    `skippable` — поле объекта `settings` верхнего уровня, а не элемент `actions`. Сюжетные сцены ставят `"settings": { "skippable": false }`, чтобы `back` не пропускал катсцену.

Служебные элементы `actions` — не действия фабрики: `{"type": "start", "debug": true}` (работает только первым элементом — включает `manager.debug_enabled`) и `{"type": "end"}` (останавливает разбор; всё после него не выполняется).

## Общие правила полей

Поля читаются типизированными хелперами `__cutscene_json_get_*` из `cutscene_load_json.gml`:

- **Цель** (`target` / `target_ref`, `target` приоритетнее): строка — ключ `actor_map` (регистрозависимо), зарезервированные `"player"`/`"player_body"` (регистронезависимо) или имя object-ассета; число — instance id или object-индекс. JSON `null` нормализуется в `noone` — `"target": null` отклоняется как «нет цели». Пустая строка и `noone` везде, где цель обязательна, отклоняют действие с записью в лог.
- **Время**: `seconds`, `duration`, `time` — синонимы длительности в секундах (проверяются в этом порядке); конвертируются в кадры через `settings.fps`. Где фабрика вызывает `__cutscene_json_get_frames` (`wait`, `spin`, `shake_object`), явный `frames` имеет приоритет над секундными ключами.
- **Числа**: строки-числа (`"120"`) парсятся; нечисловые строки, `NaN` и `±infinity` дают значение по умолчанию. Там, где `0` — валидное значение координаты (`move`, `set_position`, `jump`, `actor_create`, `spawn_entity`, `camera_center`, `camera_pan`, `room_change`), обязательность проверяется по наличию ключа, а не по значению.
- **Булевы**: принимаются `true`/`false`, `1`/`0`, строки `"true"/"false"/"yes"/"no"/"on"/"off"/"1"/"0"`.
- **Цвет** (`fade_in`/`fade_out`): индекс `c_*`-цвета, имя (`"black"`, `"white"`, `"red"`, …, `"gray"`/`"grey"`, `"dkgray"`, `"ltgray"`, …) или hex `"#RRGGBB"`/`"RRGGBB"`.
- **Направление**: `"right"`/`"r"`, `"left"`/`"l"`, `"up"`/`"u"`, `"down"`/`"d"`; число `global.DIR.*` (`RIGHT=0`, `LEFT=1`, `UP=2`, `DOWN=3`) принимает только `set_facing` — у `move_relative_direction` поле `direction` читается строкой (`__cutscene_json_get_string`), поэтому JSON-число превращается в строку `"2"` и деградирует в `DOWN` с warning.
- **Easing** (`tween`, `tween_camera`, `jump`): `"linear"` (по умолчанию), `"ease_in"`/`"in"`, `"ease_out"`/`"out"`, `"ease_in_out"`/`"in_out"`/`"ease"`.
- **Свойства камеры** (`set_property`/`tween`/`lerp` с `kind:"camera"`, `tween_camera`): `"x"`, `"y"`, `"view_x"`, `"view_y"`, `"camera_x"`, `"camera_y"` — левый верхний угол view.
- **Dot-нотация состояния** (`branch_flag.key`, `guard_global.var`/`end_var`): резолвер `__cutscene_resolve_state_value` понимает `"flag.x"`/`"flags.x"` → `global.flag[$ "x"]`, `"stat.hp"` → `global.stat_hp`, `"entity_state.rm:eid[.field]"` → запись `global.entity_state`, `"struct.field"` → `global[$ struct][$ field]`; префикс `global.` срезается. Ключ без точки читается как `global.flag[key]` (в `branch_flag`) или целая global-переменная (в `guard_global`).

Действие с невалидными обязательными полями не создаётся — фабрика возвращает `noone` и пишет `[CUTSCENE] FACTORY: action '<type>' rejected — …` в лог.

## Алиасы типов

`type` приводится к нижнему регистру и прогоняется через `__cutscene_json_normalize_action_type` до обращения к фабрике:

| Legacy-имя | Канонический тип | Уровень |
|------------|------------------|---------|
| `shakeobj` | `shake_object` | normalize |
| `visible` | `set_visible` | normalize |
| `instant_mode` | `set_instant` | normalize |
| `waittalk`, `wait_talk` | `wait_for_dialogue` | normalize |
| `depth` | `set_depth` | normalize |
| `facing` | `set_facing` | normalize |
| `autofacing` | `auto_facing` | normalize |
| `autowalk` | `auto_walk` | normalize |
| `destroy_entity`, `destroy` | `actor_destroy` | фабрика (`f[$ "destroy_entity"] = f[$ "actor_destroy"]`) |
| `emote` | `show_emote` | фабрика |

## Движение и анимация

### `move`

Ведёт актёра к абсолютной точке; блокирует очередь до прибытия или остановки коллизией. Создаёт `ActionMove`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `x`, `y` | real | да (ключи) | — |
| `speed_px_sec` | real | нет | `60` (fallback на `speed`) |
| `speed` | real | нет | `60` — читается, только если `speed_px_sec` отсутствует или `< 0` |
| `collision` | bool | нет | `false` |

```json title="datafiles/cutscenes/tests/move_basic.json"
{ "type": "move", "target": "test_actor", "x": 200, "y": 100, "speed_px_sec": 120 }
```

### `follow_path`

Ведёт актёра по массиву точек; блокирует до последней. Создаёт `ActionFollowPath`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `points` | array | да (непустой) | элементы `{x,y}` или `[x,y]`; нераспознанные пропускаются с warning |
| `speed_px_sec` | real | нет | `60` |
| `collision` | bool | нет | `false` |
| `autofacing` | bool | нет | `true` — поворачивает актёра по ходу пути; исходный `auto_face` восстанавливается в `cleanup` |

```json title="datafiles/cutscenes/tests/move_path.json"
{ "type": "follow_path", "target": "test_actor", "speed_px_sec": 120, "points": [{ "x": 100, "y": 100 }, { "x": 150, "y": 100 }, { "x": 150, "y": 150 }] }
```

### `move_relative`

Сдвиг актёра на `(dx, dy)` от текущей позиции; блокирует до прибытия. Создаёт `ActionMoveRelative`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `dx`, `dy` | real | нет | `0` |
| `speed_px_sec` | real | нет | `60` |
| `collision` | bool | нет | `false` |

```json title="datafiles/cutscenes/tests/move_relative.json"
{ "type": "move_relative", "target": "test_actor", "dx": 50, "dy": -30, "speed_px_sec": 120 }
```

### `move_relative_direction`

Движение в заданном направлении `speed * seconds` пикселей; блокирует до остановки. Создаёт `ActionMoveRelativeDirection`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `direction` | string | нет | `"right"` — только имена/буквы (`r/l/u/d` тоже); JSON-число строкифицируется и деградирует в `DOWN` с warning |
| `speed_px_sec` | real | нет | `60` |
| `seconds` / `duration` / `time` | real | нет | `1` — длительность движения |
| `collision` | bool | нет | `false` |

```json title="datafiles/cutscenes/tests/move_rel_dir.json"
{ "type": "move_relative_direction", "target": "test_actor", "direction": "right", "speed_px_sec": 120, "seconds": 0.5 }
```

### `move_direct`

Движение к точке либо с фиксированной скоростью, либо за фиксированное время. Создаёт `ActionMoveDirect` (внутри — `ActionMove`).

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `x`, `y` | real | нет | отсутствующая ось = текущая координата |
| `value` | real | нет | `60` — при `use_speed:false` это кадры движения |
| `use_speed` | bool | нет | `false` |
| `seconds` / `duration` / `time`, `frames` | real | нет | переопределяют `value` при `use_speed:false` |
| `collision` | bool | нет | `false` |

!!! warning "Единицы `value` при `use_speed: true`"
    При `"use_speed": true` поле `value` — скорость в **px/кадр** (передаётся в `ActionMove` без конвертации), а не px/сек, как `speed_px_sec` у остальных move-действий. `60` px/кадр при 60 fps — это 3600 px/сек.

```json title="datafiles/cutscenes/tests/move_direct.json"
{ "type": "move_direct", "target": "test_actor", "x": 220, "y": 100, "value": 60, "use_speed": false }
```

### `jump`

Прыжок актёра к точке по дуге; блокирует до приземления. Создаёт `ActionJump`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `x`, `y` | real | да (ключи) | — |
| `seconds` / `duration` / `time` | real | нет | `0.5` |
| `height` | real | нет | `16` — высота дуги в px |
| `easing` | string | нет | `"linear"` |

```json title="datafiles/cutscenes/tests/jump.json"
{ "type": "jump", "target": "test_actor", "x": 180, "y": 100, "seconds": 0.5, "height": 20 }
```

### `set_position`

Мгновенный телепорт актёра в точку (пишет также `target_x`/`target_y`, где они есть). Создаёт `ActionSetXY`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `x`, `y` | real | да (ключи) | — |

```json title="datafiles/cutscenes/tests/set_position.json"
{ "type": "set_position", "target": "test_actor", "x": 123, "y": 456 }
```

### `set_position_relative`

Мгновенный сдвиг актёра на `(dx, dy)`. Создаёт `ActionSetPositionRelative`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `dx`, `dy` | real | нет | `0` |

```json title="datafiles/cutscenes/tests/set_position_relative.json"
{ "type": "set_position_relative", "target": "test_actor", "dx": 25, "dy": -15 }
```

### `set_depth`

Пишет `depth` актёра. Создаёт `ActionSetDepth`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `depth` | real | да | — (отсутствие/нечисло отклоняет действие; `0` валиден) |

```json title="datafiles/cutscenes/tests/set_depth.json"
{ "type": "set_depth", "target": "test_actor", "depth": -500 }
```

### `set_facing`

Мгновенно разворачивает актёра: пишет `facing_direction` и меняет спрайт по `chara_sprites`/`chara_idle_sprites`. Создаёт `ActionSetFacing`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `direction` | string/real | да | — (`"right"/"left"/"up"/"down"`, короткие `r/l/u/d`, число `0..3`; нераспознанная строка отклоняет действие, число вне `0..3` деградирует в `DOWN` с warning) |

```json title="datafiles/cutscenes/tests/set_facing.json"
{ "type": "set_facing", "target": "test_actor", "direction": "left" }
```

### `auto_facing`

Включает/выключает авто-поворот актёра по направлению движения. Создаёт `ActionSetProperty(target, "auto_face", enabled)`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `enabled` | bool | нет | `true` |

```json title="datafiles/cutscenes/tests/auto_facing.json"
{ "type": "auto_facing", "target": "test_actor", "enabled": true }
```

### `auto_walk`

Включает/выключает авто-анимацию ходьбы актёра. Создаёт `ActionSetProperty(target, "auto_walk", enabled)`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `enabled` | bool | нет | `true` |

```json title="datafiles/cutscenes/tests/auto_walk.json"
{ "type": "auto_walk", "target": "test_actor", "enabled": false }
```

### `animate`

Меняет `sprite_index` и опционально `image_index`/`image_speed` актёра. Создаёт `ActionAnimate`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `sprite` | string | нет | — (неразрешённое имя пропускается с warning, `sprite_index` не трогается) |
| `image_index` | real | нет | не задаётся — поле остаётся как есть |
| `image_speed` | real | нет | не задаётся; `> 0` включает `__cutscene_anim_override` |

```json title="datafiles/cutscenes/tests/animate.json"
{ "type": "animate", "target": "test_actor", "sprite": "spr_Chara_walking_R" }
```

### `set_animation_frame`

Ставит конкретный кадр без смены спрайта (freeze-поза). Создаёт `ActionSetAnimationFrame`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `image_index` | real | нет | `0` |
| `image_speed` | real | нет | `1` |
| `pause` | bool | нет | `false` — `true` обнуляет `image_speed` после установки кадра |

```json title="datafiles/cutscenes/tests/set_animation_frame.json"
{ "type": "set_animation_frame", "target": "test_actor", "image_index": 2, "image_speed": 0, "pause": true }
```

### `set_property`

Пишет произвольное instance-поле цели или свойство камеры. Создаёт `ActionSetProperty`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `kind` | string | нет | `"instance"`; `"camera"` — камера, `target` не нужен |
| `target` / `target_ref` | string/id | да для `kind != "camera"` | — |
| `property` | string | да | — |
| `value` | any | нет | `undefined` |

```json title="datafiles/cutscenes/tests/set_property.json"
{ "type": "set_property", "target": "test_actor", "property": "custom_test_value", "value": 42, "kind": "instance" }
```

### `tween`

Плавно меняет числовое свойство цели или камеры; блокирует до конца. Создаёт `ActionTween`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `kind` | string | нет | `"instance"`; `"camera"` — `target` не нужен |
| `target` / `target_ref` | string/id | да для `kind != "camera"` | — |
| `property` / `prop` | string | да | — |
| `to_value` / `end_value` | real | нет | `0` |
| `frames` | real | нет | приоритет над секундными ключами |
| `seconds` / `duration` / `time` | real | нет | `1` сек, если нет `frames` |
| `duration_frames` | real | нет | **секунды**, несмотря на имя — так экспортирует Undefscene |
| `easing` / `ease_name` | string | нет | `"linear"` |
| `from_value` / `start_value_override` | real | нет | стартовое значение; без него — текущее свойство цели |

```json title="datafiles/cutscenes/tests/tween.json"
{ "type": "tween", "target": "test_actor", "property": "x", "to_value": 200, "seconds": 0.5, "easing": "linear" }
```

### `lerp`

Покадровое `lerp(cur, to_value, factor)` до тех пор, пока разница не станет `<= threshold`. Создаёт `ActionLerp`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | строка `"camera"` (любой регистр) переключает на камеру |
| `property` / `prop` | string | да | — |
| `to_value` / `end_value` | real | нет | `0` |
| `factor` | real | нет | `0.1` — клампится в `0.001..1` |
| `threshold` | real | нет | `0.5` — минимум `0.01` |

```json title="Синтетический пример (в datafiles/cutscenes не встречается)"
{ "type": "lerp", "target": "test_actor", "property": "image_alpha", "to_value": 0, "factor": 0.2 }
```

### `spin`

Вращает `image_angle` актёра; блокирует до конца. Создаёт `ActionSpin`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `speed` | real | нет | `10` — итоговый угол в градусах, равномерно размазанный на длительность |
| `frames` | int | нет | `60` кадров; приоритет над секундными ключами |
| `seconds` / `duration` / `time` | real | нет | — |

```json title="datafiles/cutscenes/tests/spin.json (вложенный action)"
{ "type": "spin", "target": "test_actor", "speed": 90, "frames": 60 }
```

### `flip`

Зеркалит спрайт по горизонтали через `image_xscale`. Создаёт `ActionFlip`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `flipped` | bool | нет | `true` — `true` даёт отрицательный `image_xscale` |

```json title="datafiles/cutscenes/tests/flip.json"
{ "type": "flip", "target": "test_actor", "flipped": true }
```

### `halt`

Мгновенно останавливает движение актёра (`cutscene_runtime_halt`). Создаёт `ActionHalt`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |

```json title="datafiles/cutscenes/tests/halt.json"
{ "type": "halt", "target": "test_actor" }
```

### `shake_object`

Трясёт актёра; блокирует до конца. Создаёт `ActionShakeObject`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `frames` | int | нет | `20` кадров; приоритет над секундными ключами |
| `seconds` / `duration` / `time` | real | нет | — |
| `magnitude` | real | нет | `4` |
| `magnitude_x`, `magnitude_y` | real | нет | = `magnitude` |
| `decay` | bool | нет | `false` — затухание амплитуды |
| `frequency` | real | нет | `1` |

```json title="datafiles/cutscenes/tests/shake_object.json"
{ "type": "shake_object", "target": "shake_actor", "seconds": 0.5, "magnitude": 4 }
```

### `set_visible`

Управляет `visible` актёра. Создаёт `ActionSetProperty(target, "visible", visible)`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `visible` | bool | нет | `true` |

```json title="datafiles/cutscenes/tests/set_visible.json"
{ "type": "set_visible", "target": "test_actor", "visible": false }
```

## Актёры

### `actor_create`

Создаёт актёра в мире и регистрирует его в `actor_map`/`actor_specs` под ключом. Создаёт `ActionActorCreate`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `key` / `actor_key` / `actor_name` | string | да (первое непустое) | — |
| `x`, `y` | real | да (ключи) | — |
| `sprite_or_object` / `actor_sprite` | string/id | нет | имя object-ассета создаёт этот объект; имя sprite — `obj_actor` (точнее `default_actor_object` из engine-настроек) с этим спрайтом; без поля — объект по умолчанию |
| `copy_from` / `copy_target` | string/id | нет | — источник внешности: спрайт, кадр, масштаб, `facing_direction`, `auto_face`, `auto_walk` (depth не копируется) |

```json title="datafiles/cutscenes/tests/actor_create.json"
{ "type": "actor_create", "key": "test_actor", "x": 100, "y": 100, "actor_sprite": "spr_Dummy" }
```

### `actor_destroy`

Уничтожает инстанс цели и снимает её с `actor_map`/`actor_specs`. Создаёт `ActionDestroy`. Алиасы: `destroy_entity`, `destroy`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |

`obj_player` и его наследники защищены от уничтожения — действие пишет warning и пропускает удаление.

```json title="datafiles/cutscenes/tests/spawn_entity.json (алиас destroy_entity)"
{ "type": "destroy_entity", "target": "spawned_test" }
```

### `spawn_entity`

Создаёт произвольный object-инстанс (`instance_create_depth`). Создаёт `ActionSpawnEntity`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `object` / `actor_sprite` | string | да (имя object-ассета) | — |
| `x`, `y` | real | да (ключи) | — |
| `key` / `actor_name` | string | нет | `""` — при непустом ключе инстанс регистрируется в `actor_map` |
| `depth` | real | нет | `0` (с warning; у наследников `par_depth` игнорируется — их `depth = -y`) |
| `persistent` | bool | нет | `false` |

```json title="datafiles/cutscenes/tests/spawn_entity.json"
{ "type": "spawn_entity", "object": "obj_actor", "x": 100, "y": 100, "key": "spawned_test", "depth": 0, "persistent": false }
```

### `attach_to_target`

Привязывает актёра к родителю: позиция = `parent + offset` каждый кадр. Создаёт `ActionAttachToTarget`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | кого привязываем |
| `parent` / `parent_ref` | string/id | да | к кому привязываем |
| `offset_x`, `offset_y` | real | нет | `0` |
| `follow_facing` | bool | нет | `true` — копировать `image_xscale` родителя |
| `follow_scale` | bool | нет | `true` — копировать `image_yscale` |
| `follow_depth` | bool | нет | `true` — у `par_depth`-наследников через `attached_target`, иначе прямой записью `depth` |
| `duration_seconds` | real | нет | `0` — `0` = мгновенный телепорт к точке привязки, `> 0` = плавный подлёт за N секунд |
| `detach_on_cutscene_end` | bool | нет | `true` — авто-отвязка при `finish_cutscene` |

```json title="datafiles/cutscenes/tests/attach_detach.json"
{ "type": "attach_to_target", "target": "child_actor", "parent_ref": "parent_actor", "offset_x": 20, "offset_y": 0, "follow_facing": true, "follow_scale": true, "follow_depth": true }
```

### `detach`

Снимает привязку актёра; позиция сохраняется. Создаёт `ActionDetach`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `destroy_after_detach` | bool | нет | `false` — уничтожить инстанс после отвязки |
| `keep_world_position` | — | — | игнорируется с warning (позиция и так сохраняется) |

```json title="datafiles/cutscenes/tests/attach_detach.json"
{ "type": "detach", "target": "child_actor", "destroy_after_detach": false }
```

### `show_emote`

Показывает спрайт-эмоцию над актёром. Создаёт `ActionEmote`. Алиас: `emote`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `sprite` | string/id | нет | `undefined` — fallback: `default_emote_sprite` из engine-настроек, затем `chara_question_o`/`chara_question_c` |
| `seconds` / `duration` / `time` | real | нет | `1` |
| `offset_x` | real | нет | `0` |
| `offset_y` | real | нет | `-24` |
| `scale` | real | нет | `1` |
| `wait` | bool | нет | `false` — `true` блокирует очередь до конца эмоции |

```json title="datafiles/cutscenes/tests/emote.json"
{ "type": "show_emote", "target": "test_actor", "sprite": "spr_StatHeart", "seconds": 1.0, "wait": false }
```

### `set_emotion`

Ставит эмоциональное состояние актёра: idle-спрайт через `map_emotions` и/или портрет следующей реплики. Создаёт `ActionSetEmotion`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `emotion` | string | нет | `"default"` |
| `apply_to_sprite` | bool | нет | `true` — меняет `sprite_index` на idle-спрайт эмоции |
| `apply_to_portrait` | bool | нет | `true` — пишет в consume-once карту `global.__actor_forced_emotion` |

```json title="datafiles/cutscenes/tests/set_emotion.json"
{ "type": "set_emotion", "target": "test_actor", "emotion": "happy", "apply_to_sprite": false, "apply_to_portrait": true }
```

## Камера

### `camera_track`

Камера следует за целью заданное время; блокирует до конца таймера. Создаёт `ActionCameraTrack`. Клампа к границам комнаты нет — как у follow-камеры игрока.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `seconds` / `duration` / `time` | real | нет | `0` (клампится до 1 кадра в классе) |
| `offset_x`, `offset_y` | real | нет | `0` — смещение точки слежения |

```json title="datafiles/cutscenes/tests/camera_track.json"
{ "type": "camera_track", "target": "test_actor", "seconds": 0.5 }
```

### `camera_track_until_stop`

Камера следует за целью, пока та не остановится (`move_active == false`; grace-период 2 кадра). Создаёт `ActionCameraTrackUntilStop`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `offset_x`, `offset_y` | real | нет | `0` |

```json title="datafiles/cutscenes/tests/camera_track_until_stop.json"
{ "type": "camera_track_until_stop", "target": "test_actor" }
```

### `camera_center`

Мгновенно центрирует view на точке. Создаёт `ActionCameraCenter`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `x`, `y` | real | да (ключи) | — координаты ЦЕНТРА view, не левого верхнего угла |

```json title="datafiles/cutscenes/tests/camera_center.json"
{ "type": "camera_center", "x": 400, "y": 300 }
```

### `camera_pan`

Плавно ведёт view к абсолютной позиции (easing `ease_in_out` внутри класса); блокирует до конца. Создаёт `ActionCameraPan`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `x`, `y` | real | да (ключи) | — целевая позиция ЛЕВОГО ВЕРХНЕГО угла view |
| `seconds` / `duration` / `time` | real | нет | `1` |

```json title="datafiles/cutscenes/tests/camera_pan.json"
{ "type": "camera_pan", "x": 50, "y": 80, "seconds": 0.5 }
```

### `camera_pan_speed`

Панорамирует view с фиксированной скоростью (linear); блокирует до конца. Создаёт `ActionCameraPanSpeed`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `x`, `y` | real | хотя бы одно | `0` — **скорость в px/кадр по оси, не координата** |
| `seconds` / `duration` / `time` | real | нет | `1` |
| `speed`, `speed_px_sec` | — | — | игнорируются с warning |

```json title="datafiles/cutscenes/tests/camera_pan_speed.json"
{ "type": "camera_pan_speed", "x": 1, "y": 1, "seconds": 1.0 }
```

### `camera_pan_obj`

Плавно центрирует view на цели с клампом к границам комнаты (единственный камерный экшен с клампом). Создаёт `ActionCameraPanToObj`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `seconds` / `duration` / `time` | real | нет | `1` |

```json title="datafiles/cutscenes/tests/camera_pan_obj.json"
{ "type": "camera_pan_obj", "target": "test_actor", "seconds": 0.5 }
```

### `camera_shake`

Трясёт экран; блокирует до конца. Создаёт `ActionCameraShake`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `seconds` / `duration` / `time` | real | нет | `1` |
| `magnitude` | real | нет | `4` |
| `magnitude_x`, `magnitude_y` | real | нет | = `magnitude` |
| `decay` | bool | нет | `false` |
| `frequency` | real | нет | `1` |

```json title="datafiles/cutscenes/tests/camera_shake.json"
{ "type": "camera_shake", "seconds": 0.5, "magnitude": 4 }
```

### `tween_camera`

Плавно меняет числовое свойство камеры (`x`, `y`, …); блокирует до конца. Создаёт `ActionTween("camera", prop, …, "camera")` — эквивалент `tween` с `kind:"camera"`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `property` / `prop` | string | да | — |
| `to_value` / `end_value` | real | нет | `0` |
| `frames` | real | нет | приоритет над секундными ключами |
| `seconds` / `duration` / `time` | real | нет | `1` сек |
| `duration_frames` | real | нет | **секунды**, несмотря на имя |
| `easing` / `ease_name` | string | нет | `"linear"` |
| `from_value` / `start_value_override` | real | нет | текущее значение |

```json title="datafiles/cutscenes/tests/tween_camera.json"
{ "type": "tween_camera", "property": "x", "to_value": 100, "seconds": 0.5, "easing": "linear" }
```

## Диалог

### `dialogue`

Открывает yarn-диалог в `textboxTest_scribble`. Создаёт `ActionDialogue`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `file` | string | да | — обязано содержать `.yarn`; иначе действие отклоняется |
| `node` | any | нет | `undefined` — стартовая нода файла |
| `block_queue` | bool | нет | `true` — `false` запускает диалог неблокирующе (`non_blocking`), действие завершается сразу |
| `auto_advance` | bool | нет | `false` — перекрывается `manager.dialogue_auto_advance`, если тот задан через `dialogue_control` |

Несуществующий файл подменяется `dialogue_default_file` менеджера с warning. При `block_queue` действие ждёт `ChatterboxIsStopped`; если chatterbox не появился за `__CUTSCENE_DIALOGUE_WAIT_FRAMES` (~10 сек при 60 fps), действие пропускается по таймауту.

```json title="datafiles/cutscenes/tests/dialogue.json"
{ "type": "dialogue", "file": "testDialogue.yarn", "node": "Intro-dialogue-CUT" }
```

### `wait_for_dialogue`

Ждёт закрытия диалогового окна. Создаёт `ActionWaitForDialogue`. Алиасы: `waittalk`, `wait_talk`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `dialogue_controller` | id | нет | `undefined` — авто-поиск контроллера менеджера или любого `textboxTest_scribble` |

```json title="datafiles/cutscenes/tests/wait_for_dialogue.json"
{ "type": "wait_for_dialogue" }
```

!!! warning "stay_open и wait_for_dialogue"
    При `stay_open: true` окно считается активным, пока не закрыто — закрывайте такой диалог явно через `clear_dialogue`.

### `set_dialogue_speed`

Ставит скорость печати текста (символов в секунду) — персистентно на менеджере, применяется ко всем последующим диалогам. Создаёт `ActionSetDialogueSpeed`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `speed` | real | нет | `1.0` |

```json title="datafiles/cutscenes/tests/dialogue_speed.json"
{ "type": "set_dialogue_speed", "speed": 40.0 }
```

### `wait_typing`

Ждёт завершения анимации печати текущей реплики (`typist.get_state() == 1`). Создаёт `ActionWaitTyping`. Полей нет.

```json title="datafiles/cutscenes/tests/wait_typing.json"
{ "type": "wait_typing" }
```

### `dialogue_control`

Ставит флаги поведения диалогового окна — на активный контроллер и на менеджер (для следующих диалогов). Создаёт `ActionDialogueControl`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `prevent_skip` | bool | нет | `false` — запрет скипа печати по `confirm` |
| `stay_open` | bool | нет | `false` — окно остаётся открытым после конца реплики |
| `auto_advance` | bool | нет | `false` — диалог пролистывается сам |

```json title="datafiles/cutscenes/tests/dialogue_control.json"
{ "type": "dialogue_control", "prevent_skip": true, "stay_open": true, "auto_advance": false }
```

### `set_portrait_next`

Задаёт эмоцию портрета для следующей реплики (consume-once карта `global.__actor_forced_emotion`, забирает `scr_parse_emote`). Создаёт `ActionSetPortraitNext`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — ключ нормализуется (нижний регистр + trim) |
| `emotion` | string | нет | `"neutral"` |

```json title="datafiles/cutscenes/tests/portrait_next.json"
{ "type": "set_portrait_next", "target": "test_actor", "emotion": "neutral" }
```

### `set_portrait_now`

Мгновенно меняет портрет: `current_emotion` актёра/`obj_face` и ресурсы рта/голоса контроллера диалога через `map_emotions`. Создаёт `ActionSetPortraitNow`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `emotion` | string | нет | `"neutral"` |

```json title="datafiles/cutscenes/tests/portrait_now.json"
{ "type": "set_portrait_now", "target": "test_actor", "emotion": "happy" }
```

### `clear_dialogue`

Уничтожает контроллер менеджера и все живые `textboxTest_scribble`. Создаёт `ActionClearDialogue`. Полей нет.

```json title="datafiles/cutscenes/tests/clear_dialogue.json"
{ "type": "clear_dialogue" }
```

## Музыка и звук

Все music-действия идут через глобальные `play_music_*`/`set_music_*`-функции (`__cutscene_music_call`); отсутствующая функция — warning, не ошибка.

### `play_sfx`

Проигрывает звуковой эффект. Создаёт `ActionPlaySFX`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `sound` | string/id | да | — непустое значение обязательно |
| `volume` | real | нет | `1` |
| `pitch` | real | нет | `1` |

```json title="datafiles/cutscenes/tests/play_sfx.json"
{ "type": "play_sfx", "sound": "snd_text_ch1", "volume": 1.0, "pitch": 1.0 }
```

### `play_music`

Переключает музыку на трек с кроссфейдом. Создаёт `ActionMusicPlay`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `sound` / `track` | string/id | да | — имя sound-ассета (`asset_get_index` + проверка `asset_sound`) |
| `fade` | real | нет | `0.5` сек — `0` даёт мгновенную смену |
| `fade_in_seconds` | real | нет | переопределяет `fade` |
| `volume` | real | нет | `1.0` — применяется только при `!= 1` и `>= 0` |
| `persist_room_change` | bool | нет | `true` — трек помечается в `global.music_persist_track` и не затирается музыкой следующей комнаты |

!!! info "persist_room_change"
    Дефолт `true`: галочка «остаётся при переходе» в редакторе включена изначально, и старые JSON без поля получают то же поведение. Чтобы трек погас при смене комнаты, задайте `"persist_room_change": false` явно. `play_music` без persist снимает чужую пометку (`global.music_persist_track = noone`).

```json title="datafiles/cutscenes/tests/stop_music.json"
{ "type": "play_music", "sound": "snd_wobble", "fade": 0.1, "volume": 0.5 }
```

### `stop_music`

Останавливает музыку с фейдом. Создаёт `ActionMusicStop(fade, false)`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `fade` | real | нет | `1.0` сек |
| `fade_out_seconds` | real | нет | переопределяет `fade` |

```json title="datafiles/cutscenes/tests/stop_music.json"
{ "type": "stop_music", "fade": 0.0 }
```

### `music_volume`

Плавно меняет громкость текущего трека. Создаёт `ActionMusicVolume`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `volume` | real | нет | `1` |
| `fade` | real | нет | `0.5` сек |

```json title="datafiles/cutscenes/tests/music_volume.json"
{ "type": "music_volume", "volume": 0.4, "fade": 0.2 }
```

### `music_duck`

Приглушает музыку относительным множителем. Создаёт `ActionMusicDuck`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `multiplier` | real | нет | `0.3` |
| `fade` | real | нет | `0.3` сек |

```json title="datafiles/cutscenes/tests/music_duck_unduck.json"
{ "type": "music_duck", "multiplier": 0.2, "fade": 0.2 }
```

### `music_unduck`

Снимает приглушение. Создаёт `ActionMusicUnduck`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `fade` | real | нет | `0.3` сек |

```json title="datafiles/cutscenes/tests/music_duck_unduck.json"
{ "type": "music_unduck", "fade": 0.2 }
```

### `music_pitch`

Ставит pitch текущего трека. Создаёт `ActionMusicPitch` (фабрика вызывает wrapper `cutscene_music_pitch`).

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `pitch` | real | нет | `1.0` |

```json title="datafiles/cutscenes/tests/music_pitch.json"
{ "type": "music_pitch", "pitch": 1.5 }
```

### `music_pause`

Ставит музыку на паузу (включая intro/layer/prev-каналы). Создаёт `ActionMusicPause` (через `cutscene_music_pause`). Полей нет.

```json title="datafiles/cutscenes/tests/music_pause_resume.json"
{ "type": "music_pause" }
```

### `music_resume`

Снимает музыку с паузы. Создаёт `ActionMusicResume` (через `cutscene_music_resume`). Полей нет.

```json title="datafiles/cutscenes/tests/music_pause_resume.json"
{ "type": "music_resume" }
```

### `play_boss_music`

Запускает два слоя синхронно — calm + battle. Создаёт `ActionMusicPlayLayered`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `calm` / `calm_asset` | string/id | да | — спокойный слой |
| `battle` / `battle_asset` | string/id | нет | — боевой слой |
| `fade` | real | нет | `0.5` сек |

```json title="datafiles/cutscenes/tests/play_boss_music.json"
{ "type": "play_boss_music", "calm": "snd_wobble", "battle": "snd_text_ch1", "fade": 0.1 }
```

### `stop_boss_music`

Останавливает layered-музыку (гасит оба слоя; без слоёв откатывается на обычный `stop_music`). Создаёт `ActionMusicStop(fade, true)`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `fade` | real | нет | `1.0` сек |

```json title="datafiles/cutscenes/tests/play_boss_music.json"
{ "type": "stop_boss_music", "fade": 0.0 }
```

### `boss_music_phase`

Запускает фазовую последовательность музыки через `ActionMusicPhaseSequence` (`play_music_phase_sequence`).

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `phases` | array | нет | `[]` — элементы-struct `{intro, calm, battle, intensity, fade}`; не-struct элементы молча пропускаются |
| `fade` | real | нет | `0.5` сек — переход по умолчанию |

```json title="datafiles/cutscenes/cutscene.json"
{ "type": "boss_music_phase", "phases": [ { "calm": "mus_loop_calm_loud", "battle": "mus_loop_battle", "intensity": 0.25, "fade": 0.4 } ], "fade": 0.4 }
```

### `play_music_intro`

Играет intro один раз, затем переходит на зацикленный трек. Создаёт `ActionMusicIntroLoop`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `intro` / `sound` | string/id | да | — трек интро |
| `loop` / `track` | string/id | да | — зацикленная часть |
| `fade` | real | нет | `0.5` сек |

```json title="datafiles/cutscenes/cutscene.json"
{ "type": "play_music_intro", "intro": "mus_intro", "loop": "mus_loop_calm_loud", "fade": 0.5 }
```

### `play_music_intro_layered`

Играет intro, затем переходит на layered loop (calm + battle). Создаёт `ActionMusicIntroLayered`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `intro` | string/id | да | — |
| `calm` | string/id | да | — |
| `battle` | string/id | нет | — |
| `fade` | real | нет | `0.5` сек |
| `start_intensity` | real | нет | `0` — стартовое соотношение слоёв `0..1` |

```json title="datafiles/cutscenes/cutscene.json"
{ "type": "play_music_intro_layered", "intro": "mus_intro", "calm": "mus_loop_calm_loud", "battle": "mus_loop_battle", "fade": 0.5, "start_intensity": 0.2 }
```

### `crossfade_music`

Меняет соотношение calm/battle слоёв текущего layered-трека. Создаёт `ActionMusicSetIntensity`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `intensity` | real | нет | `0.5` — `0` = calm, `1` = battle |
| `fade` | real | нет | `1.0` сек |

```json title="datafiles/cutscenes/tests/crossfade_music.json"
{ "type": "crossfade_music", "intensity": 0.8, "fade": 0.3 }
```

## Управление потоком

### `wait`

Пауза очереди. Создаёт `ActionWait`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `frames` | int | нет | приоритет над секундными ключами |
| `seconds` / `duration` / `time` | real | нет | `0` кадров — действие завершается сразу |

```json title="datafiles/cutscenes/tests/zero_wait.json"
{ "type": "wait", "seconds": 0 }
```

### `mark_node`

Отмечает именованную точку в `manager.reached_nodes` — цель для `goto` и `guard_global` со `stop_when: "node_reached"`. Создаёт `ActionMarkNode`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `name` | string | нет | `""` |

```json title="datafiles/cutscenes/tests/mark_node.json"
{ "type": "mark_node", "name": "checkpoint_alpha" }
```

### `goto`

Переводит `current_action_index` на `mark_node` с указанным именем. Создаёт `ActionGoToNode`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` | string | да (непустое) | — имя метки |

Прыжок ищется только в основной очереди (метки внутри `parallel`/sequence недостижимы). Прыжок назад переигрывает действия диапазона (сброс `started`, таймеров, `reset()`); лимит обратных переходов — 1024, дальше переход отменяется как вероятный бесконечный цикл. Самопрыжок — no-op с warning.

```json title="Синтетический пример (в datafiles/cutscenes не встречается)"
{ "type": "goto", "target": "system_start" }
```

### `parallel`

Выполняет ветки одновременно; действие завершается, когда закончились все ветки. Создаёт `ActionParallel`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `actions` | array | да | — элемент: action-объект (одна ветка) или массив action-объектов (ветка-sequence) |

Вложенный `branch`/`guard_global` вставляет продолжение в свою ветку, а не в главную очередь (`__cutscene_parallel_splice`). `wait_for_interact` с `abort_parallel` обрывает соседние ветки.

```json title="datafiles/cutscenes/tests/sequence.json"
{ "type": "parallel", "actions": [
  [{ "type": "move", "target": "test_actor", "x": 150, "y": 100, "speed_px_sec": 120 }, { "type": "move", "target": "test_actor", "x": 150, "y": 150, "speed_px_sec": 120 }],
  [{ "type": "wait", "seconds": 0.5 }]
]}
```

### `branch`

Вставляет в очередь `true_actions` или `false_actions` по результату `condition`. Создаёт `ActionBranch`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `condition` | string/bool | нет | `""` — строка трактуется как имя script-ассета и вызывается; не-callable/не-bool → ветка false с warning |
| `true_actions` | array | нет | `[]` |
| `false_actions` | array | нет | `[]` |

Строки вне `whitelist.branch_conditions` из engine-настроек логируются, но допускаются (advisory-режим).

```json title="datafiles/cutscenes/tests/branch_true.json"
{ "type": "branch", "condition": "scr_test_branch_true", "true_actions": [
  { "type": "set_position", "target": "test_actor", "x": 111, "y": 222 }
], "false_actions": [
  { "type": "set_position", "target": "test_actor", "x": 999, "y": 999 }
]}
```

### `branch_flag`

Ветвление по значению флага/состояния. Создаёт `ActionBranchFlag`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `key` | string | да (непустой) | — `global.flag[key]` или dot-путь (`flag.x`, `stat.hp`, `entity_state.rm:eid[.field]`, `struct.field`, `global.*` срезается) |
| `operator` | string | нет | `"=="`; допустимы `exists`, `!exists`, `==`, `!=`, `>`, `<`, `>=`, `<=`; неизвестный → `==` с warning |
| `value` | any | нет | `"true"` — сравнение толерантно к строкам/bool из JSON (`__cutscene_compare_values`); `>`,`<`,`>=`,`<=` приводят оба операнда к real |
| `true_actions`, `false_actions` | array | нет | `[]` |

```json title="Синтетический пример (в datafiles/cutscenes не встречается)"
{ "type": "branch_flag", "key": "flag.met_asher", "operator": "==", "value": true,
  "true_actions": [ { "type": "dialogue", "file": "asher.yarn", "node": "Met" } ],
  "false_actions": [ { "type": "dialogue", "file": "asher.yarn", "node": "FirstMeet" } ] }
```

### `run_function`

Вызывает GML-функцию на старте действия. Создаёт `ActionRunFunction`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `function` / `function_name` / `fn` | string | да | — имя script-ассета или callable-значения из `global`; не-script ассет и не-callable глобал отклоняются |
| `args` | array/string | нет | `[]` — массив элементов или строка `"a,b,c"` (числовые части парсятся в real) |

К `args` в конец всегда добавляется менеджер катсцены: вызов идёт как `fn(arg0..argN, manager)`. Имена вне `whitelist.run_functions` из engine-настроек логируются, но допускаются (advisory-режим).

```json title="datafiles/cutscenes/tests/move_basic.json"
{ "type": "run_function", "function": "scr_test_assert_position", "args": ["test_actor", 200, 100, 2] }
```

### `schedule_action`

Запускает вложенное действие с задержкой. Создаёт `ActionScheduleAction`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `delay_seconds` | real | нет | `0` |
| `blocking` | bool | нет | `false` — `false`: inner уходит в `manager.scheduled_actions` и тикает фоном (fire-and-forget); `true`: действие дотикивает inner до его завершения |
| `tag` | string | нет | `""` |
| `action` | object | да | — action-объект, разбирается рекурсивно той же фабрикой; провал разбора отклоняет весь `schedule_action` |

```json title="datafiles/cutscenes/tests/schedule_action.json"
{ "type": "schedule_action", "delay_seconds": 0.3, "blocking": true, "action": { "type": "set_position", "target": "test_actor", "x": 175, "y": 100 } }
```

### `set_instant`

Включает instant-режим менеджера: тикающие действия (wait, move, tween и т.п.) завершаются мгновенно. Создаёт `ActionSetInstantMode`. Алиас: `instant_mode`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `enabled` | bool | нет | `true` |

```json title="datafiles/cutscenes/tests/set_instant.json"
{ "type": "set_instant", "enabled": true }
```

## Состояние и мир

### `set_flag`

Пишет `global.flag[$ key] = value`. Создаёт `ActionSetFlag`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `key` | string | да (непустой) | — ключ без точек; значения с dot-путём читаются `branch_flag`/`guard_global` как `flag.<key>` |
| `value` | any | нет | `0` |

```json title="datafiles/cutscenes/tests/set_flag.json"
{ "type": "set_flag", "key": "test_flag_a", "value": 7 }
```

### `set_plot`

Пишет `global.plot` — счётчик прогресса сюжета. Создаёт `ActionSetPlot`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `value` | real | нет | `0` |

```json title="datafiles/cutscenes/tests/set_plot.json"
{ "type": "set_plot", "value": 42 }
```

### `guard_global`

Условный блок / ожидание по global-переменной (dot-нотация `a.b` — см. общие правила). Создаёт `ActionGuardGlobal`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `var` | string | нет | `""` — пустой = условие всегда истинно, `actions` вставляются сразу |
| `equals` | any | нет | `""` — сравнение через `__cutscene_compare_values` |
| `if_false` | string | нет | `"skip"`; `"wait_until_true"` — ждать истинности каждый кадр; неизвестное → `skip` с warning |
| `actions` | array | нет | `[]` — вставляются в очередь при истинном условии |
| `stop_when` | string | нет | `"none"`; для `wait_until_true`: `"global_var"`, `"node_reached"`, `"timeout"` — прервать ожидание без вставки actions |
| `end_var` | string | нет | `""` — переменная для `stop_when: "global_var"` |
| `end_equals` | any | нет | `""` |
| `end_node` | string | нет | `""` — имя метки для `stop_when: "node_reached"` (см. `mark_node`) |
| `end_timeout` | real | нет | `0` — секунды для `stop_when: "timeout"` |

```json title="datafiles/cutscenes/tests/guard_timeout.json"
{ "type": "guard_global", "var": "__test_guard_timeout", "equals": true, "if_false": "wait_until_true", "stop_when": "timeout", "end_timeout": 0.5, "actions": [
    { "type": "actor_create", "key": "should_not_exist", "x": 100, "y": 100, "actor_sprite": "spr_Dummy" }
]}
```

!!! note "Типа `set_global` нет"
    Отдельного действия `set_global` фабрика не регистрирует: флаги сюжета пишет `set_flag` (`global.flag`), прогресс — `set_plot` (`global.plot`), произвольную global-переменную меняйте через `run_function`. Читать состояние могут `branch_flag` и `guard_global` через dot-нотацию.

### `checkpoint_state`

Сохраняет snapshot состояния катсцены в `global.__cutscene_checkpoints` (лимит 10, вытеснение LRU). Создаёт `ActionCheckpointState`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `checkpoint_id` | string | нет | `""` — пустой отклоняется в `start` с ошибкой |
| `include_actors` | bool | нет | `true` |
| `include_player` | bool | нет | `true` |
| `include_camera` | bool | нет | `true` |
| `include_music` | bool | нет | `true` |
| `include_globals` | array/string | нет | `""` — JSON-массив или legacy-строка с JSON внутри |
| `include_instances` | array/string | нет | `""` — то же |

```json title="datafiles/cutscenes/tests/checkpoint_restore.json"
{ "type": "checkpoint_state", "checkpoint_id": "test_checkpoint_1", "include_actors": true, "include_player": true, "include_camera": true, "include_music": false }
```

### `restore_state`

Восстанавливает состояние из checkpoint: актёры, игрок, камера, музыка, globals, инстансы; живые runtime-эффекты (tween/jump/shake/spin/fade) этой сцены гасятся до отката. Создаёт `ActionRestoreState`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `checkpoint_id` | string | нет | `""` |
| `cleanup_transients` | bool | нет | `true` — уничтожить актёров, созданных после checkpoint |
| `restore_camera` | bool | нет | `true` |
| `restore_music` | bool | нет | `true` |
| `on_missing` | string | нет | `"warn"`; `"fail"` пишет ERROR вместо WARNING; действие завершается в любом случае |

```json title="datafiles/cutscenes/tests/checkpoint_restore.json"
{ "type": "restore_state", "checkpoint_id": "test_checkpoint_1", "cleanup_transients": true, "restore_camera": true, "restore_music": false }
```

### `room_change`

Блокирующая смена комнаты с фейдом через `obj_changingRoomsController`: `update` завершается после затухания; позиции применяет Room Start менеджера. Создаёт `ActionRoomChange`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `room` | string | да | — имя room-ассета |
| `player_x`, `player_y` | real | да (ключи) | — точка спавна игрока в новой комнате |
| `actors` | object | нет | `{}` — `{ "ключ_актёра": {x,y} }` или `[x,y]`; записи без `x`/`y` пропускаются с warning |

!!! warning "Переход в текущую комнату"
    `room_change` в текущую комнату — no-op: контроллер затухает без `room_goto`, действие пишет WARNING «same-room завершение без перехода» и сбрасывает параметры.

```json title="datafiles/cutscenes/tests/room_change.json"
{ "type": "room_change", "room": "rm_cutsceneTest", "player_x": 160, "player_y": 120 }
```

## Ввод

### `partial_control`

Переключает уровень контроля игрока во время катсцены (`manager.partial_control_*`). Создаёт `ActionPartialControl`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `control_type` | real | нет | `0` — `0` = `LOCKED` (игрок подчинён сцене), `1` = `WHITELIST`, `2` = `FREE` (полная свобода, катсцена в фоне); мусорное значение = всё заблокировано + warning |
| `whitelist` | array | нет | `[]` — строки-ключи/`target_ref` объектов, с которыми можно взаимодействовать в режиме `1` (проверяет `scr_interaction` через `resolve_target`) |
| `allowed_actions` | array/string | нет | `[]` — имена действий ввода, пропускаемых в режиме `1`; принимает также строку `"move,interact"` или `"[\"move\"]"` |

Алиасы-группы в `allowed_actions`: `"move"` покрывает `up`/`down`/`left`/`right`/`run`, `"interact"` — `confirm`; остальные строки сравниваются с именами действий `input_map` напрямую. Пустой `allowed_actions` = только `confirm` (иначе `wait_for_interact` без таймаута был бы софтлоком). При `control_type > 0` игроку возвращается `can_move`, при `0` — снимается. Подробности — в [Частичный контроль](partial-control.md).

```json title="datafiles/cutscenes/cutscene.json"
{ "type": "partial_control", "control_type": 1, "whitelist": ["obj_cutsceneTest", "obj_player"] }
```

### `wait_for_interact`

Ждёт, пока игрок взаимодействует с целью — цель ищется в `global.__interacted_targets` (очередь пишут обработчики взаимодействий). Создаёт `ActionWaitForInteract`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `target` / `target_ref` | string/id | да | — |
| `timeout` | real | нет | `0` — секунды; `0` = ждать бесконечно |
| `timeout_action` | string | нет | `"continue"`; `"abort_parallel"` обрывает ближайшую `parallel`-группу по таймауту; неизвестное → `continue` с warning |
| `interact_action` | string | нет | `"continue"`; `"abort_parallel"` обрывает соседние ветки при успешном взаимодействии |

```json title="datafiles/cutscenes/tests/wait_for_interact.json"
{ "type": "wait_for_interact", "target": "test_actor", "timeout": 1, "timeout_action": "abort_parallel", "interact_action": "continue" }
```

## UI и прочее

### `fade_in`

Проявление экрана из затемнения (alpha → 0); блокирует до конца. Создаёт `ActionFadeIn`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `seconds` / `duration` / `time` | real | нет | `0.5` |
| `color` | string/real | нет | `c_black` — имя цвета или `"#RRGGBB"` |

```json title="datafiles/cutscenes/tests/fade_in.json"
{ "type": "fade_in", "seconds": 0.5 }
```

### `fade_out`

Затемнение экрана (alpha → 1); блокирует до конца. Создаёт `ActionFadeOut`.

| Поле | Тип | Обяз. | По умолчанию |
|------|-----|-------|--------------|
| `seconds` / `duration` / `time` | real | нет | `0.5` |
| `color` | string/real | нет | `c_black` |

```json title="datafiles/cutscenes/tests/fade_out.json"
{ "type": "fade_out", "seconds": 0.5 }
```

## См. также

- [Катсцены — обзор](overview.md) — способы задать сцену, запуск, `settings`
- [Архитектура менеджера](architecture.md) — очередь, `resolve_target`, `actor_map`, Room Start
- [Action-классы](action-classes.md) — реализация `Action*`-структур
- [Частичный контроль](partial-control.md) — режимы `partial_control` и ввод во время сцены
- [Актёры и камера](actors-and-camera.md) — движение, привязки, camera-действия
- [Рецепты](cookbook.md) — готовые схемы сцен
- [GML и `c_*`-DSL](gml-dsl.md) — командный слой и Yarn-интеграция
- [Форматы данных](../architecture/data-formats.md) — схемы JSON и `cutscene_engine_settings.json`
- [Диалоги](../systems/dialogue.md) — Chatterbox, `textboxTest_scribble`, yarn-файлы
- [Музыка](../systems/music.md) — `play_music_*`, layered-треки

<!-- sources: scripts/cutscene_action_factory/cutscene_action_factory.gml:1-1245; scripts/cutscene_load_json/cutscene_load_json.gml:7-538; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:64-5035 (ActionWait:1753, ActionMarkNode:1770, ActionGoToNode:1802, ActionFollowPath:1988, ActionActorCreate:2109, ActionMoveBase:2211, ActionMoveRelativeDirection:2318, ActionMoveDirect:2387, ActionAnimate:2428, ActionSetAnimationFrame:2472, ActionDialogue:2505, ActionRunFunction:2644, ActionSetFacing:2686, ActionWaitForDialogue:2701, ActionSetDialogueSpeed:2741, ActionWaitTyping:2767, ActionDialogueControl:2788, ActionSetPortraitNext:2815, ActionSetPortraitNow:2847, ActionClearDialogue:2897, ActionSetInstantMode:3028, ActionHalt:3037, ActionFlip:3055, ActionSpin:3072, ActionShakeBase:3107, ActionEmote:3175, ActionSetEmotion:3216, ActionTween:3319, ActionLerp:3352, ActionJump:3396, ActionCameraShake:3422, ActionParallel:3496, ActionScheduleAction:3614, ActionAttachToTarget:3760, ActionDetach:3921, ActionBranch:3945, ActionBranchFlag:3988, __cutscene_resolve_state_value:4067, ActionGuardGlobal:4185, ActionCameraCenter:4300, ActionCameraPanToObj:4399, ActionCameraTrackBase:4457, ActionWaitForInteract:4536, ActionSetFlag:4608, ActionSetPlot:4626, ActionSpawnEntity:4637, ActionDestroy:4684, ActionRoomChange:4716, ActionPartialControl:4813, ActionCheckpointState:4880, ActionRestoreState:4936); scripts/scr_cutscene_music/scr_cutscene_music.gml:1-283; scripts/scr_inputApi/scr_inputApi.gml:81-137; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml:1-70; objects/obj_cutsceneManager/Create_0.gml:500-535; datafiles/cutscenes/cutscene.json; datafiles/cutscenes/tests/*.json -->
