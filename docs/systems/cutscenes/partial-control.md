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
| **0** (`LOCKED`) | :material-cancel: | :material-cancel: | Полная блокировка (стандарт) |
| **1** (`WHITELIST`) | :material-cancel: | Whitelist | Через input API пропускается только действие `confirm`; фильтр допустимых объектов (`partial_control_whitelist`) применяет `scr_interaction`. Движение и прочий ввод остаются заблокированными |
| **2** (`FREE`) | :material-check: | :material-check: | Полная свобода, катсцена работает в фоне |

Enum `INTERACT_PARTIAL_CONTROL` объявлен в `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml`. Мусорный `control_type` из JSON (3, -1, ...) трактуется как «заблокировано» с одноразовым WARNING в логе.

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
Создаёт snapshot и сохраняет в `global.__cutscene_checkpoints` (struct).

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
    При `finish_cutscene()` вся память checkpoint-ов очищается (реассайн `global.__cutscene_checkpoints = {}`).

## Room Entry Check
!!! warning "Подсистема мертва"
    `scr_room_entry_check()` вызывается из `obj_globalManager.Step_0` при смене комнаты, но её тело зачищено до заглушки (`DELETE_CANDIDATE`): единственные писатели `global.room_flags` присваивают пустой struct, записей для спавна не создаётся. Автоматического воссоздания объектов по `room_flags` в текущей версии нет.

## См. также

- [Архитектура катсцен](architecture.md) — общая структура action-системы
- [Актёры](actors.md) — `actor_map`, `resolve_target`, работа с ключами
- [Игрок в катсцене](player_in_cutscene.md) — `can_move`, `scr_player_ui_blocking`
- [API справочник](api.md) — полный список действий и параметров
