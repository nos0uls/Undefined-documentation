---
title: Ввод (Input)
tags:
  - input
  - gamepad
  - settings
  - controls
---

# Ввод (Input)

Единый API ввода (`scr_inputApi`) отделяет физические клавиши от игровых действий: код опрашивает имена действий (`"confirm"`, `"run"`), а привязку к клавишам клавиатуры и кнопкам геймпада разрешает слой ввода.

## Действия и слоты биндов

`scr_input_actions_list()` возвращает единый список из **9 переназначаемых действий** — его читают UI ребинда, сброс биндов (`scr_resetInputToDefault`) и построение карты ввода (`scr_buildInputMap`):

```gml title="scripts/scr_inputApi/scr_inputApi.gml"
return ["up","down","left","right","run","confirm","back","menu","delete"];
```

Привязки хранятся в `global.player_settings` в виде **двух слотов на действие**: поля `input_<action>1` (основная клавиша) и `input_<action>2` (дополнительная). Значение `-1` означает пустой слот. `scr_buildInputMap(settings)` собирает из них `global.input_map` — структуру `действие → [слот1, слот2]`; коды прогоняются через `scr_input_normalize_key`, поэтому мусор из испорченного файла настроек не доходит до `keyboard_check`.

Контракт `input_map` — только vk-коды клавиатуры (целые `2..255`); геймпад в карту не входит и обрабатывается отдельным слоем (см. [Геймпад](#gamepad)).

### Дефолтные бинды { #defaults }

| Действие | Слот 1 | Слот 2 | Геймпад | Где используется |
|----------|--------|--------|---------|------------------|
| `up` | `vk_up` | `-1` | `gp_padu` + стик вверх | Движение (`scr_player_movement`), навигация меню |
| `down` | `vk_down` | `-1` | `gp_padd` + стик вниз | Движение, навигация меню |
| `left` | `vk_left` | `-1` | `gp_padl` + стик влево | Движение, навигация меню |
| `right` | `vk_right` | `-1` | `gp_padr` + стик вправо | Движение, навигация меню |
| `run` | `vk_shift` | `-1` | `gp_face3` или `gp_face2` | Модификатор скорости в `scr_player_movement` |
| `confirm` | `ord("Z")` | `vk_enter` | `gp_face1` (A / Cross) | Взаимодействие (`interactionWithNPCsOrObjects`), продвижение диалога, подтверждение в меню |
| `back` | `ord("X")` | `vk_shift` | `gp_face2` (B / Circle) | Отмена в меню, пропуск катсцены (`obj_cutsceneManager`) |
| `menu` | `ord("C")` | `vk_escape` | `gp_face4` или `gp_start` | Открытие/закрытие in-game меню (`scr_callMenuInit`) |
| `delete` | `ord("B")` | `-1` | `gp_select` | Удаление слота сохранения (`obj_saveManager`) |

!!! note "Дубль `vk_shift`"
    `vk_shift` по умолчанию стоит и на `run` (слот 1), и на `back` (слот 2) — Shift одновременно бег и кнопка отмены. Дубль клавиши легален: скан коллизий в `scr_input_rebind_slot` срабатывает только при явном ребинде на занятую клавишу.

## Инициализация

`obj_Init/Create_0.gml` готовит глобалы ввода: `global.input_map = scr_buildInputMap(global.player_settings)` (после `scr_loadSettings`/`scr_applySettings`), дефолты репитера `global.input_repeater_defaults`, пустое состояние `global.__input_repeat_state`, структуры `global.__gamepad_axis_prev`/`__gamepad_axis_pressed` и кэш UI-блокировки. `global.default_settings` с дефолтными биндами создаётся кодом верхнего уровня `scr_settingsManager.gml` при загрузке программы — до `obj_Init`.

## API опроса

Три функции покрывают все режимы чтения ввода. Все принимают имя действия и сами проверяют блокировку катсценой.

| Функция | Сигнатура | Поведение |
|---------|-----------|-----------|
| `scr_input_down` | `(action)` | `true`, пока клавиша или кнопка действия удерживается (`keyboard_check` + геймпад) |
| `scr_input_pressed` | `(action)` | `true` ровно один кадр при нажатии (`keyboard_check_pressed` + геймпад) |
| `scr_input_repeater` | `(action, delay = undefined, interval = undefined)` | Автоповтор нажатия при удержании — для навигации по спискам меню |

### `scr_input_repeater`

Логика как у повторения печатаемого символа:

1. Первое нажатие → `true` сразу, запускается таймер `delay`.
2. Удержание дольше `delay` → фаза частого повтора: `true` каждые `interval` миллисекунд.
3. Отпускание → сброс состояния.

Дефолты берутся из `global.input_repeater_defaults` (`{ delay: 200, interval: 120 }` мс, задаётся в `obj_Init/Create_0.gml`), время считается по `current_time`. Состояние хранится в `global.__input_repeat_state` **на пару «инстанс + действие»** — два одновременно живых UI не делят общий таймер.

### Прочие функции `scr_inputApi`

| Функция | Назначение |
|---------|------------|
| `scr_input__keys_for_action(action)` | Массив назначенных клавиш из `global.input_map` (или `[]`) |
| `scr_input_normalize_key(code)` | Нормализация кода: допустимы `-1` и целые `2..255`; `vk_lshift`/`vk_rshift` сводятся к `vk_shift`, всё остальное мусорное → `-1` |
| `scr_input_rebind(action, new_key)` | Обёртка над `scr_input_rebind_slot` для слота 1 |
| `scr_input_rebind_slot(action, slotIndex, new_key, target_settings)` | Переназначение конкретного слота — см. [Ребинд](#rebind) |
| `scr_input_keys_hint(settings, action)` | Человекочитаемая подсказка биндов вида `"Z/Enter"` для UI |
| `scr_ui_read_actions(exclude_self)` | Вне `scr_inputApi`: единое чтение ввода для меню — возвращает struct `{up, down, left, right, confirm, back, menu, delete, ui_blocking}`; навигация идёт через `scr_input_repeater`, `back`/`menu` читаются даже при UI-блокировке |

## Геймпад { #gamepad }

Геймпад читается напрямую, вне `input_map` и без ребинда — маппинг зашит в `scr_input__gamepad_down` и `scr_input__gamepad_pressed`. Опрос идёт по слотам `0..3` (`gamepad_is_connected`): учитываются все подключённые геймпады, срабатывает первый по порядку слота, сообщивший ввод.

- **Кнопки:** `gp_face1` → `confirm`, `gp_face2` → `back` и `run`, `gp_face3` → `run`, `gp_face4`/`gp_start` → `menu`, `gp_select` → `delete`, крестовина `gp_padu`/`gp_padd`/`gp_padl`/`gp_padr` → направления.
- **Левый стик:** оси `gp_axislv`/`gp_axislh` с порогом `±0.5` тоже дают `up`/`down`/`left`/`right` — для `scr_input_down` стик опрашивается напрямую каждый кадр.
- **`pressed` для стика:** одно нажатие `gamepad_button_check_pressed` не работает для осей, поэтому `scr_input_gamepad_update()` (вызывается раз в кадр из `obj_globalManager/Step_0`) считает фронты отклонения стика и складывает их в `global.__gamepad_axis_pressed` / `global.__gamepad_axis_prev`.

## Ребинд { #rebind }

Ребинд выполняется в меню настроек: `scr_settings_step_rebind(actions)` вызывается из `Step_0` `obj_settingsManager` (ветка `SETTINGS_STATE.REBIND`) со `self` = его инстанс — читает/пишет `settings_state`, `rebind_action`, `rebind_slot`, `input_delay_timer`, `local_settings`.

**Захват клавиши:** при `keyboard_check_pressed(vk_anykey)` пойманная клавиша берётся из `keyboard_lastkey`; затем `scr_input_rebind_slot(rebind_action, rebind_slot, caught, local_settings)` пишет её в слот, после чего `scr_settings_apply_and_save` применяет и сохраняет настройки, а состояние репитера действия сбрасывается.

**Специальные случаи:**

- `actions.back` или `vk_escape` — отмена ребинда без записи.
- `vk_backspace`/`vk_delete` — очистка слота. Слот 1 очищать запрещено («can't clear primary key!»), слот 2 можно очистить в `-1` (отображается как `-`).
- Запрещённые клавиши: `vk_enter` — всегда; `vk_f1`–`vk_f12` — всегда; Shift (`vk_shift`/`vk_lshift`/`vk_rshift`) — для всех действий, кроме `run` (бег должен уметь вернуться на Shift).
- `vk_lshift`/`vk_rshift`, пойманные для `run`, нормализуются в общий `vk_shift` — иначе бинд «сужался» бы до одной стороны клавиши.

**`scr_input_rebind_slot(action, slotIndex, new_key, target_settings = undefined)`:**

1. Валидирует слот (`1` или `2`) и код клавиши (`2..255`); `new_key == -1` разрешён только для слота 2.
2. Сканирует все слоты всех 9 действий на коллизии. Забрать клавишу, которая является **дефолтной для своего слота** (по `global.default_settings`), нельзя — отказ с нотификацией «can't bind to an already binded key!».
3. Коллизионные слоты освобождаются: в них возвращается дефолт, а если дефолт уже занят другим слотом — `-1`.
4. Пишет `new_key` в целевой слот. При `target_settings == undefined` (работа с `global.player_settings`) пересобирает `global.input_map` и сохраняет настройки через `scr_saveSettings`.

## Блокировка ввода

Два независимых механизма:

- **UI-блокировка** — `scr_checkUIBlocking(exclude_self, include_cutscene)`: `true`, если открыт блокирующий UI (единый список `scr_ui_objects_list()` — `obj_settingsManager`, `obj_menu`, `obj_saveManager`, `obj_inGameMenu`, `textboxTest_scribble`, p3r-меню и др., плюс `obj_sound_test` при `is_open`) или активна катсцена (`global.cutscene_active` / `global.cutscene_camera_override` при `include_cutscene`). Результат кэшируется в пределах кадра — только вызовы без `exclude_self`, с ним идёт полный пересчёт: dirty-флаги `global.__ui_blocking_dirty*` выставляет `obj_globalManager` каждый Step. Инстансы с `non_blocking = true` и вызывающий инстанс при `exclude_self` из проверки исключаются.
- **Блокировка катсценой** — `scr_input__is_cutscene_blocked_here(action)`: при `global.cutscene_active` ввод не-UI объектов подменяется виртуальным (`__cutscene_virtual_down` на инстансе; продюсеров нет — фактически читается `false`). UI-объекты из того же `scr_ui_objects_list()` продолжают видеть реальный ввод — к ним точечно добавлены `obj_cutsceneManager` и `obj_sound_test`. Режим `partial_control_type` менеджера катсцены сужает блокировку: `FREE` — ввод свободен, `WHITELIST` — пропускаются действия из `partial_control_allowed_actions` (`scr_input__partial_control_allows` разворачивает алиасы `"move"` → направления + `run` и `"interact"` → `confirm`; пустой список — только `confirm`).

Подробнее о режимах частичного контроля — в [Partial Control](../cutscenes/partial-control.md).

## Пример

```gml title="objects/obj_menu/Step_0.gml — навигация по меню"
var actions = scr_ui_read_actions(true);
var nav = scr_ui_nav_vertical(select_index, array_length(menuOptions), false, actions);
select_index = nav.index;
if (nav.moved) scr_SFXPlay("move");
if (actions.confirm) {
    scr_SFXPlay("confirm");
    menuOptions[select_index][1]();
}
```

```gml title="scripts/scr_player_movement/scr_player_movement.gml — движение и бег"
var up_key    = scr_input_down("up");
var down_key  = scr_input_down("down");
var left_key  = scr_input_down("left");
var right_key = scr_input_down("right");
current_spd = scr_input_down("run") ? run_spd : walk_spd;
```

!!! warning "Не проверено"
    Порог стика `±0.5` и маппинг `gp_*` проверены по `scr_inputApi.gml`; поведение на конкретных моделях геймпадов (раскладки, мёртвые зоны драйвера) тестами не покрыто.

## См. также

- [Partial Control](../cutscenes/partial-control.md) — режимы `LOCKED`/`WHITELIST`/`FREE` и whitelist действий в катсценах

<!-- sources: scripts/scr_inputApi/scr_inputApi.gml:1-588; scripts/scr_settings_step_rebind/scr_settings_step_rebind.gml:1-106; scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml:1-107; scripts/scr_ui_read_actions/scr_ui_read_actions.gml:1-36; scripts/scr_settingsManager/scr_settingsManager.gml:11-48,404-456; scripts/scr_key_to_string/scr_key_to_string.gml:7; objects/obj_Init/Create_0.gml:85-100,168-174; objects/obj_globalManager/Step_0.gml:14-18; objects/obj_settingsManager/Create_0.gml:62; objects/obj_settingsManager/Step_0.gml:44; objects/obj_saveManager/Step_0.gml:161; objects/obj_cutsceneManager/Step_0.gml:7; objects/obj_menu/Step_0.gml:2-16; scripts/scr_player_movement/scr_player_movement.gml:53-64; scripts/scr_callMenuInit/scr_callMenuInit.gml:7; _meta/input_actions.txt -->
