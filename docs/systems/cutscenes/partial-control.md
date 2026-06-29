---
tags:
  - cutscenes
  - cutscene-api
  - gameplay
  - controls
---

# Частичный контроль и изменения мира

Механизмы передачи управления игроку во время сцен и сохранения последствий в игровом мире.

## Частичный контроль игрока
Экшен `partial_control` позволяет временно разблокировать определенные действия игрока, не завершая катсцену.

| Тип | Движение | Взаимодействие | Описание |
|-----|----------|----------------|-----------|
| **0** | :material-cancel: | :material-cancel: | Полная блокировка (стандарт) |
| **1** | :material-check: | Whitelist | Свободное движение, взаимодействие только с разрешенными объектами |
| **2** | :material-check: | :material-check: | Полная свобода, катсцена работает в фоне |

## Ожидание взаимодействия (`wait_for_interact`)
Приостанавливает выполнение очереди до тех пор, пока игрок не провзаимодействует с указанным объектом. Часто используется в связке с `partial_control type 1`.

**Параметры:**
- `target`: объект, с которым ожидается взаимодействие (actor key или object)
- `timeout`: таймаут в секундах (0 = безлимитно)
- `timeout_action`: поведение при таймауте - `"continue"` (продолжить ветку, по умолчанию) или `"abort_parallel"` (прервать parallel)
- `interact_action`: поведение при взаимодействии - `"continue"` (продолжить, по умолчанию) или `"abort_parallel"` (прервать parallel)

**Работа в parallel ветках:**
Механизм использует очередь `global.__interacted_targets` (массив) вместо флага. Каждое взаимодействие добавляет ID объекта в очередь. `ActionWaitForInteract` ищет свой target в этой очереди и удаляет его при совпадении. Это безопасно для parallel веток — несколько `wait_for_interact` могут ждать разные цели одновременно без race condition.

## Изменение состояния мира
Экшены для перманентного влияния на игру:
- `set_flag`: установка глобальных флагов прогресса.
- `set_plot`: изменение основной переменной сюжета.
- `spawn_entity`: создание объектов, которые должны остаться после сцены.
- `destroy_entity`: удаление объектов из мира.

## Checkpoint / Restore

Система сохранения и восстановления состояния катсцены.

### ActionCheckpointState
Создаёт snapshot и сохраняет в `global.__cutscene_checkpoints` (ds_map).

**Параметры:**
- `checkpoint_id` (string) — уникальный ID. Не может быть пустым.
- `include_actors` (bool) — сохранить `actor_map`
- `include_player` (bool) — сохранить `obj_player`
- `include_camera` (bool) — сохранить позицию камеры
- `include_music` (bool) — сохранить текущий трек
- `include_globals` (array) — список имён глобальных переменных
- `include_instances` (array) — список ID инстансов

### ActionRestoreState
Восстанавливает snapshot по `checkpoint_id`.

**Параметры:**
- `checkpoint_id` (string)
- `cleanup_transients` (bool) — уничтожить актёров, созданные после checkpoint
- `restore_camera` (bool)
- `restore_music` (bool)
- `on_missing` (string) — `"warn"`, `"ignore"`, `"fail"`

!!! warning "Лимит checkpoint-ов"
    Максимум **10** checkpoint-ов в памяти (`__CUTSCENE_MAX_CHECKPOINTS`). При превышении — авто-очистка самого старого (LRU по `timestamp_frames`).

!!! warning "Cleanup при завершении катсцены"
    При `finish_cutscene()` вся память checkpoint-ов очищается (`ds_map_clear`).

## Room Entry Check
Механизм `scr_room_entry_check()` автоматически воссоздает объекты при повторном входе в комнату, если соответствующие флаги были установлены в катсцене. Это обеспечивает "постоянство" изменений.

## См. также

- [Архитектура катсцен](architecture.md) — общая структура action-системы
- [Актёры](actors.md) — `actor_map`, `resolve_target`, работа с ключами
- [Игрок в катсцене](player_in_cutscene.md) — `can_move`, `scr_player_ui_blocking`
- [API справочник](api.md) — полный список действий и параметров
