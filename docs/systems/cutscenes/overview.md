---
tags:
  - cutscenes
---

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

## Разделы документации

<div class="grid cards" markdown>

-   :fontawesome-solid-sitemap:{ .lg .middle } **Архитектура**
    ---
    `obj_cutsceneManager`, жизненный цикл Action-struct, JSON-загрузка
    ---
    [:octicons-arrow-right-24: Подробнее](architecture.md)

-   :fontawesome-solid-code:{ .lg .middle } **API**
    ---
    Builder-API `c_*`, `cutscene_*`, Chatterbox-интеграция
    ---
    [:octicons-arrow-right-24: Подробнее](api.md)

-   :fontawesome-solid-users:{ .lg .middle } **Актёры**
    ---
    `actor_map`, `ActionActorCreate`, групповые операции
    ---
    [:octicons-arrow-right-24: Подробнее](actors.md)

-   :fontawesome-solid-video:{ .lg .middle } **Камера**
    ---
    `ActionCameraPan`, `ActionCameraTrack`, `ActionCameraShake`
    ---
    [:octicons-arrow-right-24: Подробнее](camera.md)

-   :fontawesome-solid-user:{ .lg .middle } **Игрок в катсцене**
    ---
    Блокировка движения, camera override, анимация
    ---
    [:octicons-arrow-right-24: Подробнее](player_in_cutscene.md)

-   :fontawesome-solid-bug:{ .lg .middle } **Отладка**
    ---
    Debug overlay, stuck watchdog, Wait-счётчик
    ---
    [:octicons-arrow-right-24: Подробнее](debugging.md)

-   :fontawesome-solid-lightbulb:{ .lg .middle } **Примеры**
    ---
    JSON-загрузка, Builder-стиль, Yarn-команды
    ---
    [:octicons-arrow-right-24: Подробнее](examples.md)

-   :fontawesome-solid-wrench:{ .lg .middle } **Типовые проблемы**
    ---
    Камера застряла, актёр не двигается, катсцена не стартует
    ---
    [:octicons-arrow-right-24: Подробнее](troubleshooting.md)

-   :fontawesome-solid-desktop:{ .lg .middle } **Редактор Undefscene**
    ---
    Визуальный редактор катсцен на Electron + React Flow
    ---
    [:octicons-arrow-right-24: Подробнее](undefscene/overview.md)

</div>

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
