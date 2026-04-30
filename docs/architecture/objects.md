# Объекты Системы (System Objects)

В проекте используется несколько ключевых объектов, которые управляют инициализацией, runtime-состоянием и игровыми системами.

| Объект | Persistent | Назначение |
|--------|-----------|------------|
| `obj_Init` | Да | **Центральная инициализация**. Создается в `rm_init` (и fallback в `GlobalRoomCreationCode`). Настраивает ВСЕ стартовые глобалы: константы, настройки, input map, музыку, катсцены, инвентарь, статы, face-систему, кэш сейвов. Защищен от дублей через `global.__init_done`. |
| `obj_globalManager` | Да | **Runtime-менеджер**. Живет всю игру. Следит за сменой комнат, debug-хоткеи (F1–F12), уведомления, DEV-LOAD спаун, runtime катсцен (tweens/emotes/shakes/spins/jumps/fade), сброс флагов UI, переключение полноэкранного режима (Q), вызов in-game меню. |
| `obj_music_ctrl` | Да | **Музыкальный контроллер**. Создается из `obj_Init` после `scr_music_init()`. Каждый кадр обновляет time-based fade громкости (`scr_global_music_update_current`), fade-out предыдущего трека и intro→loop переход. |
| `obj_menu` | Нет | Главное меню игры. Стартует музыку меню (`global.play_music(music_menu)`). |
| `obj_settingsManager` | Нет | **Меню настроек**. Работает как в отдельной комнате `rm_settings`, так и в overlay-режиме (из in-game меню). Категории: Управление, Звук, Разное, Выйти в меню. Поддерживает переназначение клавиш (rebind), мастер-громкость через `scr_menu_volume_push/pop`, grayscale shader через `scr_menu_shader_push/pop`. |
| `obj_saveManager` | Нет | **Экран выбора сохранения / DEV-LOAD**. Режимы `load` и `save`. 3 слота + dev-load опция (при `global.debug == true` и `player_settings.devload_focus == true`). Читает метаданные из `global.__save_slot_metadata_cache` (быстрый путь) или с диска (fallback). |
| `obj_inGameMenu` | Нет | Внутриигровое меню (Inventory, Status, Settings). Вызывается по C/Esc. |
| `obj_player` | Нет | **Игровой персонаж**. Обработка движения (grid-based), коллизий (`collision()` с xplus/yplus unstuck), спавн-оверрайд (`global.__next_spawn_*`), facing → sprite mapping (`scr_sprite_for_facing`), ghost_mode, room_change_lock, создает `obj_pointMarker` для взаимодействия. |
| `obj_actor` | Нет | **Базовый объект для NPC и участников катсцен**. Содержит tween-based movement system (`move_to_point()`): `move_active`, `move_progress`, `target_x/y`, `move_speed`, `use_collision`. Idle system: `idle_active`, `idle_timer`, `idle_delay_frames`, `chara_idle_sprites`. `auto_face` (default: true), `auto_walk` (default: false). |
| `obj_pointMarker` | Нет | **Невидимый маркер взаимодействия**. Создается при спавне игрока. depth = -9999. Отрисовывается только в debug-режиме (F3). Используется `interactionWithNPCsOrObjects()` для определения цели взаимодействия. |

## Детали по объектам

### `obj_Init` vs `obj_globalManager`

| Аспект | `obj_Init` | `obj_globalManager` |
|--------|-----------|-------------------|
| **Когда создается** | `rm_init` (или fallback `GlobalRoomCreationCode`) | В конце `obj_Init.Create` (или fallback) |
| **Persistent** | Да | Да |
| **Главная роль** | Однократный холодный старт | Runtime каждый кадр (Step) |
| **Музыка** | Вызывает `scr_music_init()`, создает `obj_music_ctrl` | Нет (только `scr_global_on_room_change` выбирает трек) |
| **Глобалы** | Инициализирует ВСЕ `global.*` | Использует, не создает новые |
| **Катсцены** | Регистрирует Yarn-функции (`cutscene_register_chatterbox_functions`) | Runtime update (`cutscene_runtime_step()`, `emote_step()`) |

---

## См. также

- [Инициализация](initialization.md) — `obj_Init`, `global.__init_done`
- [Глобальное состояние](global-state.md) — `global.input_map`, UI blocking
- [Комнаты](rooms.md) — `rm_init`, `global.rooms_by_name`
- [Система ввода](../systems/input.md) — `scr_buildInputMap()`
- [Система музыки](../systems/music.md) — `obj_music_ctrl`
- [Катсцены: обзор](../systems/cutscenes/overview.md) — runtime катсцен
