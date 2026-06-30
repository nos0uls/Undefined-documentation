---
tags:
  - debug
  - runtime
---

# Debug-инструменты (Debug Tools)

Скрытая активация debug-режима, горячие клавиши для визуализации, быстрые переходы между комнатами, dev-spawn и режим призрака.

## Обзор

Debug-режим управляется глобальным флагом `global.debug`. Он включается через секретную комбинацию F12 (5 нажатий за 2 секунды) или через настройки `global.player_settings.debug_enabled`. После активации становятся доступны горячие клавиши F1–F9, dev-load из `obj_saveManager` и ручное управление флагами через `scr_toggle_debug_flag`.

Debug-спавн игрока выполняется через `global.__dev_spawn` и `global.__dev_spawn_*`. `scr_global_handle_dev_spawn` создаёт `obj_player` в центре комнаты или в заданных координатах. Этот механизм используется при загрузке сейва, переходах F5/F6 и dev-load.

## Архитектура / API

### Скрипты

| Скрипт | Описание |
|--------|----------|
| `scr_debug_activation_check` | Обрабатывает F12: 5 нажатий за 2 секунды включают `global.debug`. |
| `scr_global_debug_hotkeys` | Горячие клавиши F1–F6 и F9. Работают только при `global.debug == true`. |
| `scr_toggle_debug_flag` | Переключает bool-флаг на `obj_player` и синхронизирует его с `global`. |
| `scr_player_debug_ghost` | Переключает `ghost_mode` игрока по F8. |
| `scr_global_handle_dev_spawn` | Создаёт игрока по dev-координатам, используется после `room_goto`. |

### Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| `F12` x5 | Активировать debug-режим. |
| `F1` | Toggle `debug_show_info` — FPS, depth, имя комнаты, координаты игрока. |
| `F2` | Toggle `debug_show_colliders` — отрисовка `obj_collider` (красный) и `par_interactable` (жёлтый). |
| `F3` | Toggle `debug_show_hitbox` — хитбокс игрока и маркер взаимодействия. |
| `F4` | Сбросить `global.__init_done` и перезапустить игру через `game_restart`. |
| `F5` | Перейти к предыдущей игровой комнате с dev-spawn в центре. |
| `F6` | Перейти к следующей игровой комнате с dev-spawn в центре. |
| `F7` | Быстрое сохранение через `scr_global_quick_save`. |
| `F8` | Toggle `ghost_mode` у игрока (безколлизийный режим). |
| `F9` | Toggle `global.debug_show_music` — overlay музыкальной отладки. |

### Объекты

| Объект | Роль |
|--------|------|
| `obj_globalManager` | Draw GUI: отрисовывает debug-оверлеи, уведомления, эмоции и runtime катсцен. |
| `obj_devLoader` | UI-экран dev-load: список всех комнат с переходом и dev-spawn в центре. |
| `obj_player` | Хранит копии флагов `debug_show_*`, `ghost_mode`, `room_change_lock`. |

## Примеры

### Активация debug

```gml title="scr_debug_activation_check"
// В игре: нажмите F12 5 раз в течение 2 секунд.
// В коде: включить напрямую
global.debug = true;
global.player_settings.debug_enabled = true;
scr_saveSettings(global.player_settings);
```

### Переключение флага вручную

```gml title="scr_toggle_debug_flag"
scr_toggle_debug_flag("debug_show_colliders");
```

### Dev-spawn в центре комнаты

```gml title="scr_global_handle_dev_spawn"
global.__dev_spawn = true;
global.__dev_spawn_x = undefined; // центр по X
global.__dev_spawn_y = undefined; // центр по Y
global.__dev_spawn_facing = global.DIR.DOWN;
room_goto(rm_test_room);
// После room_goto вызовется scr_global_handle_dev_spawn
```

## Troubleshooting

!!! warning "Горячие клавиши не работают"
    `scr_global_debug_hotkeys` возвращает управление, если `global.debug == false`. Проверьте активацию через F12 или значение `global.player_settings.debug_enabled`.

!!! warning "При dev-spawn игрок не появляется"
    Убедитесь, что после `room_goto` вызывается `scr_global_handle_dev_spawn`. Если `global.__dev_spawn` сброшен до перехода, игрок создастся только стандартной логикой комнаты.

!!! note "Ghost mode отключается автоматически"
    `scr_global_transition_safety` снимает `ghost_mode` после 16 кадров безопасности. F8 включает его обратно вручную.

## См. также

- [Управление](../gameplay/controls.md) — список всех клавиш
- [Система сохранений](save-system.md) — F7, dev-spawn при загрузке
- [GML-скрипты](../code-reference/gml-scripts.md) — полный список скриптов
- [Архитектура: объекты](../architecture/objects.md) — `obj_globalManager`, `obj_devLoader`, `obj_player`
