---
tags:
  - runtime
  - rooms
---

# Переходы между комнатами (Room Transitions)

Плавные fade-переходы между игровыми комнатами, безопасный спавн игрока и синхронизация музыки при смене room.

## Обзор

Переходы реализованы через два взаимодействующих объекта: `objRoomChanger` (триггер в комнате) и `obj_changingRoomsController` (контроллер фейда). Когда игрок заходит в триггер, `objRoomChanger` создаёт контроллер, который затемняет экран, выполняет `room_goto`, перемещает игрока в целевые координаты и проявляет экран. После перехода `scr_global_transition_safety` временно включает `ghost_mode` и выталкивает игрока из коллайдеров, если он застрял. `scr_global_on_room_change` сбрасывает уведомления и переключает музыку.

Список игровых комнат для навигации F5/F6 поддерживается `scr_get_next_game_room`, которая пропускает служебные комнаты из `global.__service_menu_rooms`.

## Архитектура / API

### Скрипты

| Скрипт | Описание |
|--------|----------|
| `scr_room_fade_update` | Обновляет `fadeLevel` в `obj_changingRoomsController`. Скорость fade-in: 6.0, fade-out: 3.0 (в секундах). При достижении `fadeLevel >= 1` выполняет `room_goto(newRoom)` и перемещает `obj_player`. |
| `scr_global_transition_safety` | 16 кадров после перехода выталкивает игрока из `obj_collider`, `par_decor`, `par_interactable` и снимает `ghost_mode`. |
| `scr_global_on_room_change` | Сбрасывает уведомления, переключает музыку через `global.play_music` / `global.play_music_immediate`, включает `ghost_mode` и `room_change_lock` у игрока. |
| `scr_get_next_game_room` | Возвращает следующую/предыдущую игровую комнату, пропуская `rm_roomMenu`, `rm_savesSelect`, `rm_settings`, `rm_devLoad`. |

### Объекты

| Объект | Роль |
|--------|------|
| `objRoomChanger` | Триггер смены комнаты. В Create задаёт `pending_room`, `pending_x`, `pending_y`, `pending_glow`. В Step откладывает создание контроллера. |
| `obj_changingRoomsController` | Контроллер фейда. Поля: `newRoom`, `newX`, `newY`, `fadeLevel`, `eyesGlow`. В Step вызывает `scr_room_fade_update`. |

### Параметры `objRoomChanger`

| Переменная | Тип | Описание |
|------------|-----|----------|
| `roomName` | `room` | Целевая комната. |
| `xPosition` | `real` | Целевая X игрока. Если `0` и `0` вместе с `yPosition`, считается незаданным. |
| `yPosition` | `real` | Целевая Y игрока. |
| `eyesGlow` | `bool` | Флаг, передаваемый в контроллер. |

## Примеры

### Создание триггера в комнате

```gml title="objRoomChanger/Create_0"
roomName = rm_test_room;
xPosition = 120;
yPosition = 200;
eyesGlow = false;
```

### Ручной переход с dev-spawn

```gml title="scr_global_debug_hotkeys"
// F5/F6 используют тот же канал dev-spawn
global.__dev_spawn = true;
global.__dev_spawn_x = undefined; // центр
room_goto(scr_get_next_game_room(1));
```

### Обработка смены комнаты

```gml title="scr_global_on_room_change"
// Вызов при Room Start
global.__transition_safety_frames = 16;
scr_global_on_room_change(prev_room, room);
```

## Troubleshooting

!!! warning "Игрок застревает после перехода"
    `scr_global_transition_safety` пытается вытолкнуть игрока по спирали в течение 200 итераций. Если свободного места нет, игрок остаётся внутри коллайдера. Проверьте `xPosition`/`yPosition` триггера.

!!! warning "Fade не завершается"
    Если `newRoom` равен `undefined` или не является валидным room-индексом, контроллер уничтожается и фейд сбрасывается. Убедитесь, что `objRoomChanger` получил корректный `roomName`.

!!! note "Музыка переключается сразу при границе меню/игра"
    Внутри меню или внутри игры используется кроссфейд. При переходе между этими группами — мгновенная смена.

## См. также

- [Debug-инструменты](debug-tools.md) — F5/F6 для быстрых переходов
- [Система музыки](music.md) — `play_music`, `play_music_immediate`
- [Архитектура: комнаты](../architecture/rooms.md) — список игровых комнат
- [GML-скрипты](../code-reference/gml-scripts.md) — полный список скриптов
