---
tags:
  - cutscenes
---

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
- статус перемещения актёров (`move_active`)
- список следующих экшенов (preview)
- секция `Paths:`
    - Показывает актёров из `actor_map`, у которых есть активное перемещение.
    - Визуализирует путь до целевой точки (`target_x`, `target_y`) с цветовой индикацией старта (lime) и конца (red).
    - Оптимизировано: отрисовка путей теперь корректно очищается после завершения перемещения.

### Досрочный выход (ESC/X)
При нажатии `back` (`ESC`/`X`) `finish_cutscene()` вызывает `cleanup()` для:
- текущего выполняющегося action'а
- всех оставшихся action'ов в очереди
- всех `background_actions`
- всех `scheduled_actions`
- очистку `global.__cutscene_attachments` (auto-detach при `detach_on_cutscene_end`)
- очистку `global.__cutscene_checkpoints`

Это исправляет баг, при котором `move_active` оставался `true` после выхода из катсцены, блокируя управление игроком.

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

---

## См. также

- [Обзор катсцен](overview.md) — `obj_cutsceneManager`, `action_queue`
- [Архитектура](architecture.md) — `debug_stuck_warning_frames`
- [API](api.md) — `cutscene_add`, Action-классы
- [Типовые проблемы](troubleshooting.md) — камера "застыла", строковые ключи