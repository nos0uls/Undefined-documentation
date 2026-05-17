---
tags:
  - cutscenes
---

# Катсцены: Обзор

## Принципы работы
- `obj_cutsceneManager` выполняет очередь `action_queue`.
- Каждый экшен имеет жизненный цикл: `start()` → `update()` → `cleanup()`.
- Резолвинг целей (`target_ref`) поддерживает instance id и строковые ключи актёров.
- Скорость: в GML используется **px/frame**, в JSON — **px/sec** (конвертируется автоматически).
- Параллельное выполнение: `cutscene_parallel([...])` ожидает завершения всех вложенных экшенов.

## Глобальное состояние
- `global.cutscene_active`: флаг активности системы.
- `global.active_cutscene_manager`: ссылка на текущий инстанс менеджера.
- `global.cutscene_camera_override`: блокировка стандартного поведения камеры игрока.
- `global.active_cutscene_id` — строковый `cutscene_id` активной катсцены.

## Возможности
- Управление музыкой внутри катсцены: смена треков, громкость, pitch, duck/unduck, пауза и возобновление (`ActionMusicPlay`, `ActionMusicStop`, `ActionMusicVolume`, `ActionMusicDuck`, `ActionMusicUnduck`).
- Относительное позиционирование актёров: `move_relative` и `set_position_relative` для сдвига от текущей позиции.
- Условное ожидание: `wait_until` — ожидание, пока `global`-переменная примет нужное значение (синтаксический сахар над `guard_global`).
- Checkpoint / Restore: сохранение и восстановление состояния катсцены (`checkpoint_state`, `restore_state`).
- Частичный контроль: `partial_control` и `wait_for_interact` для интерактивных катсцен.
- Привязка объектов: `attach_to_target` с поддержкой `depth_mode = "attached"`.
- Защита игрока: `ActionDestroy` не уничтожает `obj_player`.
- Cleanup при досрочном выходе: `finish_cutscene()` вызывает `cleanup()` для всех action'ов.

## Разделы документации

<div class="grid cards" markdown>

-   :material-sitemap: **Архитектура**
    ---
    `obj_cutsceneManager`, жизненный цикл Action-struct, JSON-загрузка
    [:material-arrow-right: Подробнее](architecture.md)

-   :material-code-braces: **API**
    ---
    Builder-API `c_*`, `cutscene_*`, Chatterbox-интеграция, музыкальные ноды, относительное позиционирование
    [:material-arrow-right: Подробнее](api.md)

-   :material-account-group: **Актёры**
    ---
    `actor_map`, `ActionActorCreate`, групповые операции
    [:material-arrow-right: Подробнее](actors.md)

-   :material-video-vintage: **Камера**
    ---
    `ActionCameraPan`, `ActionCameraTrack`, `ActionCameraShake`
    [:material-arrow-right: Подробнее](camera.md)

-   :material-account: **Игрок в катсцене**
    ---
    Блокировка движения, camera override, анимация
    [:material-arrow-right: Подробнее](player_in_cutscene.md)

-   :material-bug: **Отладка**
    ---
    Debug overlay, stuck watchdog, Wait-счётчик
    [:material-arrow-right: Подробнее](debugging.md)

-   :material-lightbulb-on: **Примеры**
    ---
    JSON-загрузка, Builder-стиль, Yarn-команды
    [:material-arrow-right: Подробнее](examples.md)

-   :material-wrench: **Типовые проблемы**
    ---
    Камера застряла, актёр не двигается, катсцена не стартует
    [:material-arrow-right: Подробнее](troubleshooting.md)

-   :material-monitor-dashboard: **Редактор Undefscene**
    ---
    Визуальный редактор катсцен на Electron + React Flow
    [:material-arrow-right: Подробнее](undefscene/overview.md)

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
