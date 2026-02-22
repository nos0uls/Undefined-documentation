# Катсцены: Отладка

## Встроенный debug overlay
В `obj_cutsceneManager` есть debug overlay в `Draw_64.gml`.

### Как включить
- У менеджера есть поле `debug_enabled`.
- В тестовой катсцене пример:
  - `mgr.debug_enabled = true;`

### Что показывает overlay
- ID катсцены (`cutscene_id`)
- текущий индекс и длину очереди (`current_action_index`, `action_queue`)
- тип текущего экшена (`action_type`)
- список следующих экшенов (preview)
- секция `Paths:`
  - показывает актёров из `actor_map`, у которых есть `move_active` и он равен `true`.

## World-debug (Draw)
В `obj_cutsceneManager/Draw_0.gml` добавлена отрисовка в world‑координатах (только когда `debug_enabled = true`).

Что рисуется:
- линия пути от текущей позиции к целевой (`target_x/target_y`)
- точка старта (лайм) и точка конца (красная)
- подпись над спрайтом: `player` или `actor: <ключ>`
- подписи разводятся по разным смещениям, чтобы меньше пересекались

## Debug messages
Некоторые экшены пишут в лог через `show_debug_message`, например когда цель не найдена.

Рекомендация: привязывать такие отрисовки к `debug_enabled`, чтобы не попадало в прод.

## Preview‑control (через файлы)
В `obj_cutsceneManager` есть поддержка управления проигрыванием через файлы:
- `preview_control.json` — входящая команда
- `preview_status.json` — текущий статус

Формат `preview_control.json`:
```json
{ "command": "play", "speed": 1 }
```

Команды:
- `play`, `pause`, `stop`, `step`

Поле `speed` — множитель скорости (например 0.5, 1, 2, 4).

Формат `preview_status.json`:
```json
{
  "cutscene_id": "test",
  "is_running": true,
  "is_paused": false,
  "current_action_index": 3,
  "queue_length": 10,
  "speed": 1,
  "current_action_type": "Move"
}
```
