# Катсцены: Обзор

## Область
Эта документация описывает катсцен-движок проекта (скрипты `c_*` и `cutscene_*`, `scr_cutscene_classes`, объект `obj_cutsceneManager`, тестовые катсцены).

## Как устроена катсцена (кратко)
- `obj_cutsceneManager` выполняет `action_queue` — массив Action-struct с жизненным циклом `start()`/`update()`/`cleanup()`.
- Цели экшенов (`target_ref`) обычно передаются как **instance id** (канонический формат), но также поддерживаются строковые ключи актёров: `"actor:<key>"` и просто `<key>`.
- Скорость движения в `ActionMove` измеряется в **px/frame**.
- Для JSON‑загрузки используется `cutscene_load_json()`: в JSON длительности задаются в **секундах**, скорости — в **px/sec**, при загрузке всё переводится в кадры/px‑per‑frame.
- `cutscene_parallel([...])` позволяет запускать несколько экшенов одновременно и ждать, пока завершатся все.

## Глобальное состояние
- `global.active_cutscene_manager` — инстанс текущего менеджера.
- `global.active_cutscene_id` — строковый `cutscene_id` активной катсцены.
- `global.cutscene_active` — булевый флаг активности катсцены.
- `global.cutscene_camera_override` — отключает стандартное ведение камеры игроком (см. `camera.md`).

---

## См. также

- [Архитектура катсцен](architecture.md) — `obj_cutsceneManager`, жизненный цикл
- [API](api.md) — `cutscene_add`, Action-классы, JSON-загрузка
- [Актёры](actors.md) — `actor_map`, `ActionActorCreate`, групповые операции
- [Камера](camera.md) — `ActionCameraPan`, `ActionCameraTrack`, `ActionCameraShake`
- [Игрок в катсцене](player_in_cutscene.md) — блокировка движения, camera override
- [Отладка](debugging.md) — debug overlay, stuck watchdog
- [Примеры](examples.md) — JSON-загрузка и Builder-стиль
- [Типовые проблемы](troubleshooting.md)
- [Редактор Undefscene](undefscene/overview.md) — визуальный редактор
