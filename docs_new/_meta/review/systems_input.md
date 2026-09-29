# Review: systems/input.md

Фактчек по коду ревизии 7ee444a. Источники: `scripts/scr_inputApi/scr_inputApi.gml`, `scripts/scr_settingsManager/scr_settingsManager.gml`, `scripts/scr_settings_step_rebind/scr_settings_step_rebind.gml`, `scripts/scr_checkUIBlocking/scr_checkUIBlocking.gml`, `scripts/scr_ui_read_actions/scr_ui_read_actions.gml`, `objects/obj_Init/Create_0.gml`, `objects/obj_globalManager/Step_0.gml`, `objects/obj_settingsManager/{Create_0,Step_0}.gml`, `objects/obj_saveManager/Step_0.gml`, `objects/obj_cutsceneManager/Step_0.gml`, `objects/obj_menu/Step_0.gml`, `scripts/scr_callMenuInit/scr_callMenuInit.gml`, `scripts/scr_player_movement/scr_player_movement.gml`, `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml`, `scripts/scr_key_to_string/scr_key_to_string.gml`, `_meta/input_actions.txt`.

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 12 | `scr_inputApi` отделяет физические клавиши от имён действий | OK — scr_inputApi.gml (общая архитектура: keyboard_check по input_map + отдельный gp-слой) |
| 16 | `scr_input_actions_list()` — единый список из 9 действий; читают UI ребинда, `scr_resetInputToDefault`, `scr_buildInputMap` | OK — scr_inputApi.gml:27-29; obj_settingsManager/Create_0.gml:62; scr_settingsManager.gml:410,444. Доп.: четвёртый потребитель — скан коллизий в scr_input_rebind_slot (scr_inputApi.gml:489) |
| 19 | `return ["up","down","left","right","run","confirm","back","menu","delete"]` | OK — scr_inputApi.gml:28 (дословно) |
| 22 | Два слота `input_<action>1`/`input_<action>2`; `-1` = пустой слот; `scr_buildInputMap` → `global.input_map` вида `действие → [слот1, слот2]` через `scr_input_normalize_key` | OK — scr_settingsManager.gml:442-456; scr_inputApi.gml:41-47 |
| 24 | Контракт `input_map` — только vk-коды 2..255; геймпад отдельным слоем | OK — scr_inputApi.gml:3-6 |
| 30–33 | `up`/`down`/`left`/`right`: стрелки, слот 2 = `-1`; `gp_pad*` + стик | OK — scr_settingsManager.gml:24-31; scr_inputApi.gml:186-201 |
| 34 | `run`: `vk_shift` / `-1`; геймпад `gp_face3` или `gp_face2` | OK — scr_settingsManager.gml:36-37; scr_inputApi.gml:209,250 |
| 35 | `confirm`: `ord("Z")` / `vk_enter`; `gp_face1`; используется в `interactionWithNPCsOrObjects` | OK — scr_settingsManager.gml:34-35; scr_inputApi.gml:203,244; interactionWithNPCsOrObjects.gml:25; textboxTest_scribble/Step_0.gml:203 |
| 36 | `back`: `ord("X")` / `vk_shift`; `gp_face2`; пропуск катсцены в `obj_cutsceneManager` | OK — scr_settingsManager.gml:42-43; scr_inputApi.gml:206,247; obj_cutsceneManager/Step_0.gml:7 |
| 37 | `menu`: `ord("C")` / `vk_escape`; `gp_face4` или `gp_start`; `scr_callMenuInit` | OK — scr_settingsManager.gml:44-45; scr_inputApi.gml:212,253; scr_callMenuInit.gml:7 |
| 38 | `delete`: `ord("B")` / `-1`; `gp_select`; `obj_saveManager` | OK — scr_settingsManager.gml:46-47; scr_inputApi.gml:215,256; obj_saveManager/Step_0.gml:161 |
| 40–41 | Дубль `vk_shift` (run1 + back2) легален; скан коллизий срабатывает только при ребинде | OK — scr_settingsManager.gml:38-43; коллизии проверяются только в scr_input_rebind_slot:489-553 |
| 45 | Инициализация: `input_map` после `scr_loadSettings`/`scr_applySettings`, repeater defaults, `__input_repeat_state`, `__gamepad_axis_*`, кэш UI-блокировки; `default_settings` — top-level код до `obj_Init` | OK — obj_Init/Create_0.gml:85,87,94,97-100,171-174; scr_settingsManager.gml:7-11 |
| 49 | Три функции опроса; все проверяют блокировку катсценой | OK — scr_inputApi.gml:276,306,359 (все три зовут `scr_input__is_cutscene_blocked_here`) |
| 53–55 | Сигнатуры `scr_input_down(action)`, `scr_input_pressed(action)`, `scr_input_repeater(action, delay=undefined, interval=undefined)` | OK — scr_inputApi.gml:274,304,348 |
| 59–63 | Логика репитера: pressed → true сразу + таймер delay; удержание → фаза interval; отпускание → сброс | OK — scr_inputApi.gml:404-430 |
| 65 | Дефолты `{delay:200, interval:120}` мс из `global.input_repeater_defaults` (obj_Init); время по `current_time`; состояние на пару «инстанс + действие» | OK — obj_Init/Create_0.gml:97; scr_inputApi.gml:351-352 (`argument_count`+`is_real`), :386-401 (ключ `string(id)` внутри мапы по действию) |
| 71 | `scr_input__keys_for_action` → массив клавиш из `input_map` или `[]` | OK — scr_inputApi.gml:11-19 |
| 72 | `scr_input_normalize_key`: `-1` и целые 2..255; `vk_lshift`/`vk_rshift` → `vk_shift`; мусор → `-1` | OK — scr_inputApi.gml:41-47 |
| 73 | `scr_input_rebind` — обёртка над `scr_input_rebind_slot` слота 1 | OK — scr_inputApi.gml:443-445 (в коде помечен DELETE_CANDIDATE, 0 вызовов — страница это не отражает, но и не утверждает обратное) |
| 74 | `scr_input_rebind_slot(action, slotIndex, new_key, target_settings)` | OK — scr_inputApi.gml:453 |
| 75 | `scr_input_keys_hint` → `"Z/Enter"` | OK — scr_inputApi.gml:574-588 |
| 76 | `scr_ui_read_actions(exclude_self)` → `{up,down,left,right,confirm,back,menu,delete,ui_blocking}`; навигация через `scr_input_repeater`; `back`/`menu` при блокировке | OK — scr_ui_read_actions.gml:4-35 |
| 80 | Опрос слотов `0..3` через `gamepad_is_connected`; «срабатывает первый подключённый геймпад» | OK с уточнением — scr_inputApi.gml:182-218,152-169: опрашиваются ВСЕ подключённые геймпады по слотам 0..3; срабатывает первый по порядку слота, сообщивший ввод (не «только первый подключённый»). Формулировка двусмысленна — уточнена |
| 82 | Маппинг кнопок: face1→confirm, face2→back+run, face3→run, face4/start→menu, select→delete, gp_pad*→направления | OK — scr_inputApi.gml:186-216 (down) и :230-258 (pressed — маппинг идентичен) |
| 83 | Стик: `gp_axislv`/`gp_axislh`, порог ±0.5; «для down стик проверяется каждый кадр напрямую» | OK с уточнением — scr_inputApi.gml:188,192,196,200 (`<-0.5`/`>0.5`). «down» — это `scr_input_down` (удержание), а не действие "down"; двусмысленность устранена |
| 84 | `pressed` для стика через фронты `scr_input_gamepad_update()` из `obj_globalManager/Step_0` в `__gamepad_axis_pressed`/`__gamepad_axis_prev` | OK — obj_globalManager/Step_0.gml:18; scr_inputApi.gml:141-175,261-266 |
| 88 | `scr_settings_step_rebind` из `Step_0` `obj_settingsManager`, `self` = его инстанс; поля `settings_state`, `rebind_action`, `rebind_slot`, `local_settings` | OK с уточнением — obj_settingsManager/Step_0.gml:44 (ветка `SETTINGS_STATE.REBIND`); сигнатура `scr_settings_step_rebind(actions)`; также читает/пишет `input_delay_timer` (rebind.gml:25,49,103) — дополнено |
| 90 | `keyboard_check_pressed(vk_anykey)` → `keyboard_lastkey` → `scr_input_rebind_slot(...)` → `scr_settings_apply_and_save` → сброс репитера действия | OK — scr_settings_step_rebind.gml:11-13,78-98 |
| 94 | Отмена ребинда: `actions.back` или `vk_escape`, без записи | OK — scr_settings_step_rebind.gml:20-28 |
| 95 | `vk_backspace`/`vk_delete` — очистка слота; слот 1 запрещён («can't clear primary key!»); слот 2 → `-1` («-») | OK — scr_settings_step_rebind.gml:33-52; отображение «-» — scr_key_to_string.gml:7 (`key <= 0 → "-"`) |
| 96 | Запреты: `vk_enter` и `vk_f1`–`vk_f12` — всегда; Shift (`vk_shift`/`vk_lshift`/`vk_rshift`) — кроме `run` | OK — scr_settings_step_rebind.gml:59-66 |
| 97 | `vk_lshift`/`vk_rshift` для `run` нормализуются в `vk_shift` | OK — scr_settings_step_rebind.gml:62 (`_is_shift_key && rebind_action == "run"` → `caught = vk_shift`) |
| 101 | Валидация слота (1/2) и кода (2..255); `-1` только для слота 2 | OK — scr_inputApi.gml:458-478 |
| 102 | Скан всех слотов 9 действий; дефолтную для слота клавишу забрать нельзя («can't bind to an already binded key!») | OK — scr_inputApi.gml:489-517 (целевой слот исключается из скана :495 — тривиально, т.к. перезаписывается) |
| 103 | Коллизионные слоты освобождаются: дефолт, или `-1` если дефолт занят | OK — scr_inputApi.gml:519-552 |
| 104 | Запись в слот; при `target_settings == undefined` — пересборка `input_map` + `scr_saveSettings` | OK — scr_inputApi.gml:555-563 (то же в ветке очистки :471-474) |
| 110 | `scr_checkUIBlocking(exclude_self, include_cutscene)`; список `scr_ui_objects_list()` (settingsManager, menu, saveManager, inGameMenu, textboxTest_scribble, p3r-меню и др.) + `obj_sound_test` при `is_open`; кэш в пределах кадра, dirty-флаги от `obj_globalManager`; `non_blocking`/`exclude_self` исключаются | OK — scr_checkUIBlocking.gml:15-107; scr_ui_objects_list:51-63 (полный список: + obj_p3r_title/pause/settings, obj_changingRoomsController); obj_globalManager/Step_0.gml:14-15. Уточнения: кэшируются только вызовы без `exclude_self` (с ним — raw-пересчёт, :16-19); `include_cutscene` также учитывает `global.cutscene_camera_override` (:78) — дополнено |
| 111 | `scr_input__is_cutscene_blocked_here(action)`: при `global.cutscene_active` не-UI ввод подменяется виртуальным (`__cutscene_virtual_down`; продюсеров нет → `false`); UI из `scr_ui_objects_list()` видят реальный ввод; `partial_control_type`: FREE — свободен, WHITELIST — `partial_control_allowed_actions` (алиасы `move`→направления+run, `interact`→confirm; пустой — только `confirm`) | OK — scr_inputApi.gml:54-137; писателей `__cutscene_virtual_down` вне scr_inputApi нет (grep по `*.gml`). Неполнота: к списку точечно добавлены `obj_cutsceneManager` и `obj_sound_test` (:66-67) — дополнено |
| 113 | Ссылка `../cutscenes/partial-control.md` | OK — docs_new/cutscenes/partial-control.md существует (nav_plan.md:42) |
| 117–126 | Пример `obj_menu/Step_0.gml` | OK — obj_menu/Step_0.gml:2-16 (`count` в коде — переменная, в примере инлайн `array_length(menuOptions)` — эквивалентно) |
| 128–134 | Пример `scr_player_movement` | OK — scr_player_movement.gml:53-64 (дословно) |
| 136–137 | `!!! warning "Не проверено"` про геймпад — корректный дисклеймер | OK |
| 139–141 | «См. также» — partial-control.md | OK |
| 143 | sources-комментарий | OK — все файлы и диапазоны существуют и покрывают утверждения страницы |

## MISSING / неточности низкого приоритета

- Строка 80 — «срабатывает первый подключённый геймпад»: опрашиваются все слоты 0..3; срабатывает первый по порядку слота, давший ввод. Уточнено.
- Строка 83 — «для down стик проверяется каждый кадр напрямую»: `down` = `scr_input_down`, не действие `"down"`. Уточнено.
- Строка 88 — не указан параметр `actions` и поле `input_delay_timer`. Дополнено.
- Строка 110 — не указано, что вызовы с `exclude_self` не кэшируются, и что `include_cutscene` учитывает `cutscene_camera_override`. Дополнено.
- Строка 111 — помимо `scr_ui_objects_list()` от блокировки катсцены точечно освобождены `obj_cutsceneManager` и `obj_sound_test`. Дополнено.
- Строка 73 — `scr_input_rebind` помечен DELETE_CANDIDATE (0 вызовов); страница не обязана это фиксировать (API существует и работает), оставлено без изменений.
- `scr_input_rebind_slot` при скане коллизий пропускает целевой слот (scr_inputApi.gml:495) — деталь тривиальна, в доке опущена обоснованно.

## Итог

- WRONG: 0.
- UNVERIFIABLE: 0.
- Неточности/неполноты: 5 мест (строки 80, 83, 88, 110, 111) — исправлены на странице без смены структуры.
