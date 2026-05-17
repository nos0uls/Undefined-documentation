---
tags:
  - cutscenes
---

# Катсцены: Интеграция игрока

Правила взаимодействия игрового персонажа с катсценным движком.

## Блокировка управления
При запуске сцены менеджер автоматически выставляет `obj_player.can_move = false`. Это отключает обработку пользовательского ввода, но сохраняет возможность управления игроком через экшены (движение, анимация).

`obj_player` наследует `par_actor` → `par_depth` и использует `scr_collision_resolve()` для коллизии с `obj_collider`, `par_decor`, `par_interactable`.

## Состояние камеры
Флаг `global.cutscene_camera_override = true` отключает стандартное центрирование камеры на игроке в `Step_2`. Для слежения за игроком во время сцены необходимо явно добавить экшен `cutscene_camera_track`.

## Конфликты анимаций
Во время активной сцены скрипты автоматической анимации игрока (`scr_player_animation`) игнорируются, передавая полный контроль над спрайтами экшенам `animate` и `set_facing`.

## Резолвинг игрока
В командах и JSON-файлах для обращения к игроку зарезервированы ключи:
- `"player"`
- `"player_body"`
- Прямой `instance id` объекта `obj_player`.

---

## См. также

- [Обзор катсцен](overview.md) — `global.active_cutscene_manager`, флаги активности
- [Архитектура](architecture.md) — `start_cutscene()`, `finish_cutscene()`, блокировка `can_move`
- [Камера](camera.md) — `global.cutscene_camera_override`, экшены камеры
- [API](api.md) — `cutscene_add`, Action-классы
- [Типовые проблемы](troubleshooting.md) — камера "застыла", строковые ключи актёров

