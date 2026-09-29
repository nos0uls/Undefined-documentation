---
title: UI и меню
tags:
  - ui
  - menu
  - settings
---

# UI и меню

Экраны меню Undefinedtale-888: главное меню (`obj_menu`), in-game меню (`obj_inGameMenu`), настройки (`obj_settingsManager`), всплывающие уведомления и механизм блокировки ввода `scr_checkUIBlocking`. Все меню читают ввод через единый слой `scr_ui_read_actions` и рисуются в Draw GUI.

## Общие строительные блоки

| Скрипт | Назначение |
|--------|------------|
| `scr_ui_read_actions(exclude_self = false)` | Возвращает структуру `actions` с полями `up`/`down`/`left`/`right` (через `scr_input_repeater`), `confirm`/`delete` (через `scr_input_pressed`), `back`/`menu` и `ui_blocking`. `back` и `menu` читаются всегда — открытое меню можно закрыть той же клавишей; остальные поля глушатся, пока `scr_checkUIBlocking` возвращает `true`. |
| `scr_ui_nav_vertical(index, count, wrap, actions)` | Вертикальная навигация по списку; `wrap = true` — кольцевая. Возвращает `{ index, moved }`. |
| `scr_ui_list_controller(index, count, rows_per_col, columns, actions)` | Навигация по сетке из нескольких колонок; `left`/`right` сдвигают индекс на `rows_per_col`. Навигация всегда кольцевая по всему списку. |
| `scr_menu_shader_push()` / `scr_menu_shader_pop()` | Счётчик вложенности `global.__menu_shader_depth`: первый `push` выключает автодроу `application_surface` (меню рисует его вручную с `shd_grayscale`), последний `pop` восстанавливает сохранённое состояние. |
| `scr_menu_volume_push(target = 0.8)` / `scr_menu_volume_pop()` | Стек `global.__menu_volume_depth`: `push` приглушает `audio_master_gain` до `0.8` текущей громкости, `pop` на нулевой глубине возвращает `global.player_settings.master_volume`. Pop без парного push — no-op. |

Звуки навигации во всех меню — `scr_SFXPlay("move" | "confirm" | "back" | "error")` (см. [Аудио](music.md)).

## Главное меню — `obj_menu`

Живёт в `rm_roomMenu` вместе с `obj_menuBGSpriteChanger`. Пункты — массив пар `[строка Scribble, функция]` в `menuOptions`:

| Пункт | Действие |
|-------|----------|
| `Играть` | `room_goto(rm_savesSelect)` — экран выбора сейва |
| `Настройки` | `room_goto(rm_settings)` |
| `Выход` | `game_end()` |

- `select_index` по умолчанию `0`; если `global.menu_return_focus == 1` (выставляют пути выхода из настроек), фокус ставится на «Настройки» и флаг сбрасывается.
- Навигация в `Step_0`: `scr_ui_nav_vertical(select_index, count, false, actions)` — без заворота на концах. Ветки `back` нет: из главного меню «назад» вести некуда.
- `Draw_64`: шрифт `ft_menuFont`, выделенный пункт `#762828`, строки по `y = 430 + 90·i`, футер `ft_menuFont_small` серым с текстом версии `UNDEF DEV. CONSOLE VER. 0.888` в правом нижнем углу.
- Музыка: при создании вызывается `global.play_music(music_menu)`, если этот трек ещё не играет.

### Фон меню — `obj_menuBGSpriteChanger`

Размещён в `rm_roomMenu`, `rm_savesSelect` и `rm_settings`; позиция и масштаб берутся из расстановки инстанса в комнате. Циклически показывает кадры `backgrounds = [_1, _2, _3]`, интервал `bg_switch_seconds = 2.5` секунды переводится в кадры через `game_get_speed(gamespeed_fps)` — не через измеренный `fps`. Спрайт рисуется через `draw_sprite_ext` под `shd_grayscale`.

## In-game меню — `obj_inGameMenu`

### Открытие

`scr_callMenuInit()` вызывается каждый шаг из `obj_globalManager/Step_0` и создаёт меню на `instance_create_depth(0, 0, -1000, obj_inGameMenu)`, когда выполнены все условия:

1. `!global.is_menu_room(room)` — не в служебной комнате;
2. `scr_input_pressed("menu")` — действие `menu` (по умолчанию `C`/`Esc`, см. [Ввод](input.md));
3. `!scr_checkUIBlocking()` — нет другого UI-блокера.

При открытии игрок замораживается: `obj_player.can_move = false`, `image_speed = 0`, `image_index = 0`. В `Create_0` меню делает `scr_menu_shader_push()` и ставит `shader_guard_owned = true` — `Destroy_0` снимает guard при любом уничтожении, но не трогает чужой push (флаг обнуляется до `instance_destroy` на всех штатных выходах).

### Экраны

Корневой список — `menu_options = ["ITEM", "STAT", "OPT"]`; текущий экран хранится в `current_option` (`-1` — корень, `1` — ITEM, `2` — STAT). Кольцевая навигация вверх/вниз по корню, `back`/`menu` закрывает меню.

- **ITEM** (`current_option = 1`): список `global.inventory` с пропуском пустых слотов (`undefined`); навигация по `item_selOption` перескакивает через пустоту. Confirm на предмете открывает ряд действий `item_options = ["USE","INFO","DROP"]` (`item_use` = `1..3`, `heart_x` = `0/42/90`):
    - `USE` — вызывает `item.use()`; если вернул `true`, слот очищается;
    - `INFO` — `global.show_notification(item.description)`;
    - `DROP` — подэкран `drop_confirming` с выбором `YES`/`NO` (`drop_confirm_selection`); при `YES` предмет удаляется, ссылки `global.equipped_weapon`/`equipped_armor` на него обнуляются и вызывается `scr_stats_recalc()`. Пустой инвентарь показывает `NO ITEMS YET.`.
- **STAT** (`current_option = 2`): шесть строк `stat_text` — `player_name`, `stat_lv`, `stat_hp`, `stat_atk`, `stat_def`, `stat_gold`; массив пересобирается в Draw, потому что `use()` предметов может менять HP уже после открытия меню.
- **OPT**: не вкладка, а переход — меню делает `scr_menu_shader_pop()`, уничтожается и создаёт `obj_settingsManager` на слое `Instances` с `overlay_mode = true` и `return_to_ingame_menu = true` (с `scr_menu_volume_push()`). Индекс пункта задан макросом `#macro INGAME_MENU_OPT_INDEX 2` — при перестановке `menu_options` его нужно обновить синхронно.

### Отрисовка и указатель

`Draw_64` рисует `application_surface` через `shd_grayscale`, затем UI в цвете. Масштаб мир→GUI единый: `s = min(gui_w/view_w, gui_h/view_h)` с letterbox-центрированием — все координаты заданы в view-единицах и домножаются на `s`. Окно списка предметов анимировано: `height` интерполируется `66 ↔ 176`, `yBox` — `88 ↔ 32`. Сердце-указатель `spr_StatHeart` движется через `menu_move_heart()` (lerp по `menu_heartpos`), цель вычисляется в `Step_0` от текущего экрана.

Возврат фокуса после закрытия настроек — одноразовый `global.ingame_menu_return_index` (инициализируется `-1` в `obj_Init`): `obj_settingsManager` пишет туда `INGAME_MENU_OPT_INDEX`, а новый `obj_inGameMenu` клэмпит значение в `sel_option`.

!!! note "Мёртвый файл"
    `objects/obj_inGameMenu/Alarm_0.gml` не привязан к событию объекта и нигде не планируется — уничтожение меню делает `Destroy_0`.

## Настройки — `obj_settingsManager`

Менеджер существует в двух режимах: инстанс комнаты `rm_settings` (приход из главного меню) и оверлей поверх игры, создаваемый из `obj_inGameMenu`. Поля `overlay_mode` и `return_to_ingame_menu` выставляет создающий код после `Create`.

### Машина состояний

`settings_state` принимает значения `global.SETTINGS_STATE` (`scr_constants`): `ROOT`, `CATEGORY`, `REBIND`, `CONFIRM_RESET`. `Step_0` читает `actions`, сливает `menu` в `back` (кроме `REBIND`, где клавиши ловятся сырыми через `keyboard_lastkey`), глушит весь ввод на `input_delay_timer` кадров и диспетчит:

| Состояние | Обработчик | Что делает |
|-----------|------------|------------|
| `ROOT` | `scr_settings_step_root` | Навигация по `settings_categories`; confirm открывает категорию или «Выйти в меню», back → `handle_back()` |
| `CATEGORY` | `scr_settings_step_category` | Навигация по пунктам категории; `left`/`right` — слот бинда (в «Управление») или `handle_setting_change(±1)` |
| `REBIND` | `scr_settings_step_rebind` | Ловит `keyboard_lastkey` как новый бинд |
| `CONFIRM_RESET` | `scr_settings_step_confirm_reset` | Диалог подтверждения `controls` / `full_reset` |

Обработчики выполняются с `self` = инстанс менеджера и вызывают его методы из `Create_0`: `get_option_count`, `handle_select`, `handle_setting_change`, `handle_back`, `apply_and_save_settings`.

### Категории

`settings_categories`: `Управление`, `Звук`, `Разное`, `Выйти в меню`.

- **Управление**: строки — `scr_input_actions_list()` (9 действий) плюс «Назад»; два слота `input_<action>1/2`, `left`/`right` переключают `selected_col`. Confirm входит в `REBIND` для `rebind_action`/`rebind_slot`. Правила ребинда: слот 1 нельзя очистить (Backspace/Delete → `error` и уведомление), слот 2 очищается в `-1`; запрещены `vk_enter`, `vk_f1..vk_f12` и Shift для всех действий кроме `run` (для `run` боковые `vk_lshift`/`vk_rshift` нормализуются в `vk_shift`); запрещённая клавиша даёт уведомление. Занятая клавиша отклоняется с уведомлением только если она дефолтна для чужого слота; прочие коллизии `scr_input_rebind_slot` освобождает, возвращая слот к дефолту или `-1`. Детали — в [Ввод](input.md).
- **Звук**: `master_volume`, `music_volume`, `sfx_volume` — шаг `0.1`, клэмп `0..1`. Изменение применяется сразу (`audio_master_gain`, `global.set_music_volume_fade` для музыки), а запись файла отложена до выхода из меню.
- **Разное**: раскладка берётся из единого источника `scr_settings_misc_items()` — `borderless`, `debug`, `reset_controls`, `full_reset`, затем условные `playtime` (при `__total_playtime_seconds > 0`) и `devload` (при `global.debug`), последним всегда `back`. `borderless` переключает `fullscreen_borderless` (поле `fullscreen` принудительно `false` — нативный полный экран не используется); `debug` нельзя включить при `global.clean_state` (уведомление; выключение не блокируется); `playtime` — readonly, confirm показывает уведомление со `scr_format_playtime`; `devload` переключает `devload_focus` (стартовый фокус на кнопке DEV-LOAD в `obj_saveManager` в режиме загрузки).
- **Выйти в меню**: сохраняет настройки, уничтожает `obj_player`, снимает volume/shader-стеки (`scr_menu_volume_pop`, `scr_menu_shader_pop`), ставит `global.menu_return_focus = 1` и уходит в `rm_roomMenu` — минуя `handle_back`.

### Применение и сохранение

Редактируется локальная копия `local_settings = scr_settings_deep_copy(global.player_settings)` — все ключи из `global.default_settings` (`scr_settingsManager.gml`). `scr_settings_apply_and_save(local_settings, mode)` принимает `mode` = `"apply"`, `"save"` или `"both"`, обновляет `global.player_settings` и вызывает `scr_applySettings` (окно borderless через `window_set_showborder`/`window_set_size`/`window_set_position`, громкости, `global.debug`, пересборка `global.input_map`) и/или `scr_saveSettings` (текстовый файл `ключ=значение` в `global.settings_file`).

`handle_back()` из корня: `apply_and_save_settings()` → ветвление по режиму — `return_to_ingame_menu` пересоздаёт `obj_inGameMenu` с фокусом на OPT; `overlay_mode` размораживает игрока; комнатный режим уходит в `rm_roomMenu`. Затем `scr_menu_volume_pop()`, `scr_menu_shader_pop()`, `shader_guard_owned = false` и `instance_destroy()`. `Destroy_0` — страховка: снимает shader-guard, если меню уничтожено извне.

!!! note "Горячая клавиша Q"
    `scr_global_toggle_fullscreen` (Q, только при `global.debug`) переключает borderless и синхронизирует `local_settings` открытого менеджера — вызывается из `obj_globalManager`, а не из меню.

## Уведомления

`global.show_notification(text)` (определена в `obj_Init/Create_0`) пишет в единственный слот `obj_globalManager`: `notification_text`, `notification_active = true`, `notification_timer = notification_duration`. Очереди нет — новый вызов перезаписывает текущее уведомление и сбрасывает таймер. `scr_global_handle_notifications()` декрементит таймер по `delta_time` (FPS-независимо, `notification_duration = 1` секунда) и вызывается из `obj_globalManager/Step_0`; `scr_global_on_room_change` сбрасывает слот при смене комнаты. Рисуется в `Draw_64` менеджера: жёлтый текст `ft_inGameFont` по центру view.

Вызывают её, в частности, `INFO` предмета, отказы ребинда, блокировка debug-переключателя и `obj_p3r_title`.

## Блокировка ввода — `scr_checkUIBlocking`

Единый список UI-объектов возвращает `scr_ui_objects_list()`:

```gml title="scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml"
return [
    textboxTest_scribble,      // диалог
    obj_settingsManager,       // настройки
    obj_menu,                  // главное меню
    obj_saveManager,           // экран сейвов
    obj_inGameMenu,            // in-game меню
    obj_p3r_title, obj_p3r_pause, obj_p3r_settings, // P3R-прототип
    obj_changingRoomsController // переход между комнатами
];
```

`scr_checkUIBlocking(exclude_self = false, include_cutscene = true)` возвращает `true`, если существует инстанс хотя бы одного объекта из списка (пропускаются инстансы с `non_blocking = true` и вызывающий инстанс при `exclude_self`), открыт `obj_sound_test.is_open` либо при `include_cutscene` активны `global.cutscene_active` / `cutscene_camera_override`. Результат кэшируется в `global.__ui_blocking_cache*`: dirty-флаги каждый Step выставляет `obj_globalManager`, поэтому пересчёт идёт раз в кадр; вызовы с `exclude_self` не кэшируются. Тот же список читает слой ввода (`scr_input__is_cutscene_blocked_here`) — перечисленные объекты продолжают видеть реальный ввод во время катсцены.

Игрок и интерактивные объекты проверяют блокировку перед движением и взаимодействием (см. [Игрок](player.md), [Взаимодействие](interaction.md)).

## Комнаты меню — `is_menu_room`

`global.__service_menu_rooms` (`obj_Init/Create_0`) = `rm_roomMenu`, `rm_savesSelect`, `rm_settings`, `rm_devLoad`. `global.is_menu_room(_room)` принимает комнату или её имя. Эффекты флага:

| Потребитель | Поведение в меню-комнате |
|-------------|--------------------------|
| `scr_callMenuInit` | In-game меню не открывается |
| `obj_globalManager/Step_0` | Счётчики `__save_playtime_seconds`/`__total_playtime_seconds` не тикают |
| `scr_global_on_room_change` | Целевой трек — `music_menu`; на границе меню↔игра трек меняется мгновенно (`play_music_immediate`), внутри — кроссфейдом |
| `scr_global_quick_save` | Быстрый сейв заблокирован |
| `scr_get_next_game_room` | Комнаты пропускаются при перечислении «игровых» |

`rm_init` и `SCREENSHOTS` в список не входят — это служебные тупики без меню-семантики; их отсекает dev-фильтр `scr_room_is_dev_navigation_excluded`.

## Тюнинг-константы

Значения из Create/Draw UI-объектов; полная карта тюнинга диалогового окна — в файлах `textboxTest_scribble` (см. [Диалоги](dialogue.md)).

| Параметр | Значение | Где задано |
|----------|----------|------------|
| Интервал смены фона меню | `bg_switch_seconds = 2.5` с | `obj_menuBGSpriteChanger/Create_0` |
| Автоповтор навигации (задержка/интервал) | `global.input_repeater_defaults = { delay: 200, interval: 120 }` мс | `obj_Init/Create_0` |
| Глушение ввода после ребинда/сброса | `input_delay_timer = 15` кадров (отмена confirm-диалога — `10`) | `scr_settings_step_*` |
| Длительность уведомления | `notification_duration = 1` с | `obj_globalManager/Create_0` |
| Приглушение звука в меню | `scr_menu_volume_push(0.8)` | `scr_menu_volume_guard` |
| Шаг ползунков громкости | `±0.1`, клэмп `0..1` | `obj_settingsManager` `handle_setting_change` |
| Рамка настроек | `1200 × 900`, `start_y = 325`, `line_height = 80` (корень) / `60` (категория) | `obj_settingsManager/Draw_64` |
| Затемнение под настройками | `c_black`, `alpha = 0.7` | `obj_settingsManager/Draw_64` |
| Цвет выделения (меню/настройки) | `#762828`; заголовок `#FF9F9F`; слоты биндов `#B0B0B0` | `obj_menu`, `obj_settingsManager` |
| Цвет выделения in-game меню | `select_color = make_colour_rgb(255,15,15)` | `obj_inGameMenu/Create_0` |
| Анимация окна предметов | `height 66↔176`, `yBox 88↔32`, lerp `0.18/0.25` | `obj_inGameMenu/Step_0` |
| Сердце-указатель | lerp `0.35`; `heart_x = 0/42/90` для USE/INFO/DROP | `obj_inGameMenu` |
| Палитра P3R | `global.P3R_COLORS` (~20 ключей: `bg_*`, `accent_*`, `text_*`, `border_*`, `crt_*`) | `scr_p3r_palette` |

## P3R-прототип

Семейство `obj_p3r_title` / `obj_p3r_pause` / `obj_p3r_settings` / `obj_p3r_background` / `obj_p3r_transition` — экспериментальные меню в стилистике с твинами (TweenGMS) и палитрой `scr_p3r_palette`. Боевым UI не являются: созданы под `DevRoom1`, где триггер `obj_menuTest` открывает title по `K` и pause по `L`. Используют `scr_p3r_menu_state_create`/`scr_p3r_menu_nav` (обёртка над `scr_ui_nav_vertical`); guard'ы `scr_menu_shader_*`/`scr_menu_volume_*` поднимает только `obj_p3r_pause` — title/settings обходятся без них. Title, pause и settings включены в список UI-блокеров, чтобы не пропускать ввод игрока.

## См. также

- [Ввод](input.md) — действия `menu`/`confirm`/`back`, ребинд, `scr_input_repeater`
- [Инвентарь и статы](inventory-and-stats.md) — `global.inventory`, `use()` предметов, `scr_stats_recalc`
- [Система сохранений](save-system.md) — `obj_saveManager`, экран `rm_savesSelect`
- [Аудио](music.md) — `scr_menu_volume_*`, `set_music_volume_fade`, `music_menu`
- [Комнаты](../architecture/rooms.md) — `rm_roomMenu`, `rm_settings`, `rm_savesSelect`
- [Глобальное состояние](../architecture/global-state.md) — `player_settings`, `menu_return_focus`, `ui_blocking` кэш
- [Переходы между комнатами](room-transitions.md) — `obj_changingRoomsController`
- [Диалоги](dialogue.md) — `textboxTest_scribble` как UI-блокер

<!-- sources: objects/obj_menu/Create_0.gml; objects/obj_menu/Step_0.gml; objects/obj_menu/Draw_64.gml; objects/obj_menuBGSpriteChanger/Create_0.gml:1-12; objects/obj_menuBGSpriteChanger/Step_0.gml; objects/obj_menuBGSpriteChanger/Draw_0.gml; objects/obj_inGameMenu/Create_0.gml; objects/obj_inGameMenu/Step_0.gml; objects/obj_inGameMenu/Draw_64.gml; objects/obj_inGameMenu/Destroy_0.gml; objects/obj_inGameMenu/Alarm_0.gml; objects/obj_settingsManager/Create_0.gml; objects/obj_settingsManager/Step_0.gml; objects/obj_settingsManager/Draw_64.gml; objects/obj_settingsManager/Destroy_0.gml; scripts/scr_settings_step_root/scr_settings_step_root.gml; scripts/scr_settings_step_category/scr_settings_step_category.gml; scripts/scr_settings_step_rebind/scr_settings_step_rebind.gml; scripts/scr_settings_step_confirm_reset/scr_settings_step_confirm_reset.gml; scripts/scr_settingsManager/scr_settingsManager.gml:11-48,262-437; scripts/scr_callMenuInit/scr_callMenuInit.gml; scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml; scripts/scr_ui_read_actions/scr_ui_read_actions.gml; scripts/scr_ui_nav_vertical/scr_ui_nav_vertical.gml; scripts/scr_ui_list_controller/scr_ui_list_controller.gml; scripts/scr_menu_shader_guard/scr_menu_shader_guard.gml; scripts/scr_menu_volume_guard/scr_menu_volume_guard.gml; scripts/scr_global_handle_notifications/scr_global_handle_notifications.gml; scripts/scr_global_on_room_change/scr_global_on_room_change.gml; scripts/scr_global_quick_save/scr_global_quick_save.gml:10-25; scripts/scr_constants/scr_constants.gml:21-26; scripts/scr_inputApi/scr_inputApi.gml:27-47,304-390; scripts/scr_p3r_palette/scr_p3r_palette.gml; scripts/scr_p3r_menu_init/scr_p3r_menu_init.gml; scripts/scr_p3r_menu_nav/scr_p3r_menu_nav.gml; objects/obj_Init/Create_0.gml:97-99,166-167,181-195,284-292; objects/obj_globalManager/Create_0.gml:18-21; objects/obj_globalManager/Step_0.gml:11-15,46,63-74; objects/obj_globalManager/Draw_64.gml:48-58; objects/obj_menuTest/Create_0.gml; objects/obj_menuTest/Step_0.gml; objects/obj_p3r_title/Create_0.gml:1-30; objects/obj_p3r_pause/Create_0.gml:1-30; objects/obj_p3r_settings/Create_0.gml:1-20; objects/obj_saveManager/Create_0.gml:1-25; rooms/rm_roomMenu/rm_roomMenu.yy; rooms/rm_settings/rm_settings.yy; rooms/rm_savesSelect/rm_savesSelect.yy; rooms/DevRoom1/DevRoom1.yy; scripts/scr_layer_ensure_instances/scr_layer_ensure_instances.gml; scripts/scr_global_toggle_fullscreen/scr_global_toggle_fullscreen.gml; scripts/scr_get_next_game_room/scr_get_next_game_room.gml; objects/obj_saveManager/Step_0.gml:18-49; objects/obj_inGameMenu/obj_inGameMenu.yy; objects/obj_p3r_title/Step_0.gml; objects/obj_p3r_pause/Step_0.gml; objects/obj_p3r_settings/Step_0.gml -->
