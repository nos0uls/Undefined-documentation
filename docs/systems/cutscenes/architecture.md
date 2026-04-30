# Катсцены: Архитектура

## Основная идея
Катсцена — это **очередь экшенов (Action-struct)**, которые выполняются менеджером `obj_cutsceneManager`.

## Менеджер `obj_cutsceneManager`

### Основные поля
- `action_queue` — массив экшенов.
- `current_action_index` — индекс текущего экшена.
- `is_running`, `is_paused` — состояние выполнения.

### Реестр актёров
- `actor_map` — struct-словарь: `ключ -> instance id`. Итерация по `variable_struct_get_names(actor_map)`.

### Камера
- `global.cutscene_camera_override` — флаг, который отключает стандартное ведение камеры игроком.
- `prev_camera_view_x`, `prev_camera_view_y` — позиция камеры до старта катсцены.
- Камера управляется через tween-систему (`cutscene_runtime_tween_to`) внутри Action-классов камеры.

### Отложенные команды
- `delayed_commands` — список команд, которые будут выполнены через N кадров.
- `background_actions` — список экшенов, которые выполняются параллельно с основной очередью.

## Жизненный цикл

### Создание
Канон: `c_begin(id)` для создания билд‑менеджера.

### Старт
`c_play(mgr)` вызывает `start_cutscene()`:
- выставляет `is_running = true`.
- заполняет глобальные флаги:
  - `global.active_cutscene_manager`
  - `global.active_cutscene_id`
  - `global.cutscene_active`
- сохраняет и блокирует движение игрока через `obj_player.can_move` (если поле есть).
- включает `global.cutscene_camera_override = true`.

### Выполнение
В `Step` менеджер:
- обновляет `camera_panner` (если есть).
- выполняет `delayed_commands` и добавляет `background_actions`.
- выполняет текущий экшен из `action_queue`:
  - если экшен не стартовал — вызывает `start(manager)`.
  - каждый кадр вызывает `update(manager)` до `true`.
  - затем вызывает `cleanup(manager)` и переходит к следующему.

### Завершение
`finish_cutscene()`:
- очищает глобальные флаги.
- восстанавливает `obj_player.can_move`.
- уничтожает актёров из `actor_map`.
- восстанавливает `global.cutscene_camera_override` и возвращает камеру.
- уничтожает инстанс менеджера.

## Target resolution (`resolve_target`)
`resolve_target(_ref)` поддерживает:
- instance id (если `instance_exists(_ref)`)
- asset объекта (берётся `instance_find(obj_asset, 0)`)
- строку `"player"` или `"player_body"` (разрешаются в `obj_player`)
- строковые ключи актёров, зарегистрированные в `actor_map`

Практический вывод:
- строки поддерживаются, но для максимально предсказуемого поведения в экшенах предпочтительнее передавать instance id напрямую.

---

## См. также

- [Обзор катсцен](overview.md) — `obj_cutsceneManager`, `action_queue`
- [API](api.md) — `cutscene_add`, `ActionMove`, Action-классы
- [Актёры](actors.md) — `actor_map`, `ActionActorCreate`, `ActionGroup`
- [Камера](camera.md) — `cutscene_runtime_tween_to`, camera override
- [Игрок в катсцене](player_in_cutscene.md) — блокировка движения
- [Отладка](debugging.md) — debug overlay, stuck watchdog