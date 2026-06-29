---
tags:
  - persistent-objects
  - runtime
---

# Объекты Системы (System Objects)

Основные объекты управления инициализацией, рантаймом и игровыми системами.

| Объект | Persistent | Назначение |
|--------|-----------|------------|
| `obj_Init` | Да | **Центральная инициализация**. Создается в `rm_init` (и fallback в `GlobalRoomCreationCode`). Настраивает все стартовые глобалы: константы, настройки, input map, музыку, катсцены, инвентарь, статы, face-систему, кэш сейвов. Защищен от дубликатов через `global.__init_done`. |
| `obj_globalManager` | Да | **Runtime-менеджер**. Сопровождает игровой процесс: смена комнат, дебаг-команды (F1–F12), уведомления, DEV-LOAD спавн, рантайм катсцен (tweens/emotes/shakes/spins/jumps/fade), сброс флагов UI, переключение полноэкранного режима (Q), вызов внутриигрового меню. |
| `obj_music_ctrl` | Да | **Музыкальный контроллер**. Создается из `obj_Init` после `scr_music_init()`. Каждый кадр обновляет time-based fade громкости (`scr_global_music_update_current`), fade-out предыдущего трека и intro→loop переход. |
| `obj_menu` | Нет | Главное меню игры. Стартует музыку меню (`global.play_music(music_menu)`). |
| `obj_settingsManager` | Нет | **Меню настроек**. Работает как в отдельной комнате `rm_settings`, так и в overlay-режиме (из in-game меню). Категории: Управление, Звук, Разное, Выйти в меню. Поддерживает переназначение клавиш (rebind), мастер-громкость через `scr_menu_volume_push/pop`, grayscale shader через `scr_menu_shader_push/pop`. |
| `obj_saveManager` | Нет | **Экран выбора сохранения / DEV-LOAD**. Режимы `load` и `save`. 3 слота + dev-load опция (при `global.debug == true` и `player_settings.devload_focus == true`). Читает метаданные из `global.__save_slot_metadata_cache` (быстрый путь) или с диска (fallback). |
| `obj_inGameMenu` | Нет | Внутриигровое меню (Inventory, Status, Settings). Вызывается по C/Esc. |
| `obj_player` | Нет | **Игровой персонаж**. Наследует `par_actor` → `par_depth`. Обработка движения (grid-based), коллизий (`scr_collision_resolve()` с `obj_collider`, `par_decor`, `par_interactable`), спавн-оверрайд (`global.__next_spawn_*`), facing → sprite mapping (`scr_sprite_for_facing`), ghost_mode, room_change_lock, создает `obj_pointMarker` для взаимодействия. |
| `par_actor` | Нет | **Родительский объект для актёров** (`obj_player`, `obj_actor`). Управляет `move_active`, `move_speed`, `target_x/y`. Наследует `par_depth` для Z-сортировки. |
| `par_depth` | Нет | **Базовый объект для Z-сортировки** (isometric). Иерархия: `par_depth` → `par_actor` → `obj_player`/`obj_actor`. `par_depth` → `par_decor`/`par_interactable`/`par_entity` → `obj_collider`. |
| `par_entity` | Нет | **Родительский объект для сущностей мира** (`obj_collider`). Обеспечивает коллизию. |
| `par_decor` | Нет | **Родительский объект декораций** (`obj_lantern`, статические объекты). Наследует `par_depth`. Участвует в коллизии (`is_static = true`). |
| `par_interactable` | Нет | **Родительский объект для интерактивных объектов** (`obj_bench`, NPC). Наследует `par_depth`. Участвует в коллизии. |
| `obj_actor` | Нет | **Базовый объект для NPC и участников катсцен**. Наследует `par_actor`. Содержит tween-based movement system (`move_to_point()`): `move_active`, `move_progress`, `target_x/y`, `move_speed`, `use_collision`. Idle system: `idle_active`, `idle_timer`, `idle_delay_frames`, `chara_idle_sprites`. `auto_face` (default: true), `auto_walk` (default: false). |
| `obj_collider` | Нет | **Базовый коллайдер**. Наследует `par_entity` → `par_depth`. Объекты, блокирующие движение. |
| `obj_pointMarker` | Нет | **Невидимый маркер взаимодействия**. Создается при спавне игрока. depth = -9999. Отрисовывается только в debug-режиме (F3). Используется `interactionWithNPCsOrObjects()` для определения цели взаимодействия. |
| `obj_save` | Нет | **Интерактивный сейвпоинт в мире**. При взаимодействии запускает Yarn-диалог, заданный в `dialogue_filename` и `dialogue_node`. После диалога выполняет сохранение через `obj_saveManager`. |
| `obj_devLoader` | Нет | **UI-экран dev-load**. Показывает список всех игровых комнат, исключая служебные. При выборе комнаты устанавливает `global.__dev_spawn` и выполняет `room_goto` в центр комнаты. |
| `obj_changingRoomsController` | Нет | **Контроллер fade-перехода**. В Step вызывает `scr_room_fade_update`, выполняет `room_goto`, перемещает игрока и отвечает за `fadeLevel` / `eyesGlow`. |
| `objRoomChanger` | Нет | **Триггер смены комнаты**. Задаёт целевую комнату и координаты. При касании игрока создаёт `obj_changingRoomsController` и уничтожается. |
| `obj_cutsceneManager` | Да | **Центральный контроллер катсцен**. Persistent. Управляет `action_queue`, `actor_map`, `actor_specs`. Выполняет экшены из очереди, обрабатывает параллельные ветки, управляет partial control. Room Start/End — очищает мёртвые ссылки. |
| `textboxTest_scribble` | Нет | **Диалоговое окно**. Использует Scribble для отрисовки текста и Chatterbox для логики Yarn-диалогов. Обрабатывает опции выбора, портреты, голоса. |
| `obj_face` | Нет | **Портрет диалога**. Отрисовывает спрайт-портрет говорящего персонажа в текстбоксе. Управляется через `global.current_actor` / `global.current_emote`. |
| `obj_sound_test` | Нет | **GUI теста звука**. Имеет флаг `is_open`. Блокирует ввод через `scr_checkUIBlocking` при открытом GUI. |
| `obj_p3r_title` | Нет | **P3R title screen**. Блокирует ввод через `scr_checkUIBlocking`. |
| `obj_p3r_pause` | Нет | **P3R pause menu**. Блокирует ввод через `scr_checkUIBlocking`. |
| `obj_p3r_settings` | Нет | **P3R settings**. Блокирует ввод через `scr_checkUIBlocking`. |
| `obj_p3r_background` | Нет | Фоновый объект P3R-стиля меню. |
| `obj_p3r_transition` | Нет | Переход между P3R-экранами. |
| `obj_p3r_background_1` | Нет | Дополнительный фоновый объект P3R. |
| `obj_anim` | Нет | Объект анимации. |
| `obj_asher` | Нет | NPC Ашер. Наследует `obj_actor`. |
| `obj_bench` | Нет | Интерактивный объект (скамейка). Наследует `par_interactable`. |
| `obj_dummy` | Нет | Тестовый объект. |
| `obj_kachela` | Нет | Игровой объект (качеля). |
| `obj_lantern` | Нет | Декорация (фонарь). Наследует `par_decor`. |
| `obj_sheepFountain` | Нет | Игровой объект (фонтан). |
| `obj_sign` | Нет | Интерактивный объект (знак). Наследует `par_interactable`. |
| `obj_slopeCollider` | Нет | Коллайдер для склонов. Наследует `par_entity`. |
| `obj_tree1` / `obj_tree2` | Нет | Декорации (деревья). Наследуют `par_decor`. |
| `obj_visualObject` | Нет | Визуальный объект (без коллизии). |
| `obj_menuBGSpriteChanger` | Нет | Смена спрайта фона меню. |
| `obj_menuTest` / `obj_cutsceneTest` / `obj_dialoguetest` | Нет | Тестовые объекты для отладки. |

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
- [Катсцены: обзор](../systems/cutscenes/overview.md) — runtime катсцен, `obj_cutsceneManager`
- [Диалоговые портреты](../systems/dialogue-portraits.md) — `textboxTest_scribble`, `obj_face`
