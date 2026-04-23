# Катсцены: Интеграция игрока

## Цели
- Игрок должен быть доступен как цель экшенов (обычно — instance id).
- Во время катсцены ввод игрока должен быть заблокирован (если явно не разрешено обратное).

## Канонические флаги
Активная катсцена определяется через:
  - `global.active_cutscene_manager` (instance)
  - `global.active_cutscene_id` (string)
  - `global.cutscene_active` (bool)
  - `global.cutscene_camera_override` (bool)

## Блокировка движения
`obj_cutsceneManager.start_cutscene()` сохраняет предыдущее значение `obj_player.can_move` и выставляет `false`.
`obj_cutsceneManager.finish_cutscene()` восстанавливает значение.

## Камера и катсцены
Во время катсцены `global.cutscene_camera_override = true`, и `obj_player/Step_2.gml` перестаёт центрировать камеру на игроке.

Следовательно:
- если нужно, чтобы камера следовала за игроком/актёром — добавляй экшены камеры (см. `camera.md`).

## Предотвращение конфликтов анимации/направления
В скриптах игрока делаем ранний `exit`, пока катсцена активна.

