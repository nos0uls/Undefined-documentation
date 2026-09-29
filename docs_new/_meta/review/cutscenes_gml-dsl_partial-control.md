# Ревью: cutscenes/gml-dsl.md + cutscenes/partial-control.md

Код-ревизия: `7ee444a` (`$P`), проверка парная. Статусы: OK / WRONG (file:line) / UNVERIFIABLE / MISSING.

## gml-dsl.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 12 | `c_*` собирают `Action*`-struct'ы в очередь между `c_begin()`/`c_play()`; те же команды доступны из Yarn через `ChatterboxAddFunction` | OK — scripts/c_cmd/c_cmd.gml:9-15, 149-209 |
| 16-24 (mermaid) | `c_begin` → `global.__cutscene_build_mgr`; `c_*` → `__cutscene_builder_add` → `cutscene_add(mgr, action)` → `mgr.action_queue`; `c_play` → `start_cutscene()` | OK — c_cmd.gml:9-14; cutscene_add.gml:22-23; c_play.gml:18 |
| 26 | `c_begin(_id)` создаёт `obj_cutsceneManager` и кладёт в `global.__cutscene_build_mgr` | OK (нормальный путь; при активной катсцене возвращает активный менеджер и чистит протёкший билдер — c_begin.gml:3-17, нюанс частично покрыт строкой 27) |
| 27 | `__cutscene_builder_add` резолвит сначала `global.active_cutscene_manager`, иначе `global.__cutscene_build_mgr`; инъекция в живую очередь | OK — c_cmd.gml:1-15 |
| 28 | `c_play(_mgr)` вызывает `start_cutscene()` у найденного менеджера и очищает build-слот | OK — c_play.gml:1-24 |
| 29 | `c_end(_mgr)`: явный менеджер → build-менеджер → активная катсцена (`finish_cutscene()`) | OK — c_end.gml:5-60 |
| 31 | Единицы: кадры и px/кадр; в JSON — секунды и px/sec | OK — c_wait.gml:1-5 (frames); factory `__cutscene_json_seconds_to_frames` (cutscene_action_factory.gml:1033); `option_game_speed:60` (options/main/options_main.yy:13) |
| 33 | «Команда с пустым/`undefined` target не добавляет действие и пишет `[CUTSCENE] ПРЕДУПРЕЖДЕНИЕ` (`__cutscene_cmd_require_target`)» | WRONG (частично) — верно только для команд с `__cutscene_cmd_require_target` (c_cmd.gml:40-46). `c_halt`/`c_shakeobj` без target и одноаргументные `c_flip`/`c_visible` **добавляют** действие с `""` через `__cutscene_selected_actor` (c_cmd.gml:17-24, 260-266, 268-275, 282-288, 290-297); `""` резолвится в `noone` в рантайме (obj_cutsceneManager/Create_0.gml:504-531) |
| 36 | Вне сессии `__cutscene_builder_add` молча возвращает `noone` | OK — c_cmd.gml:11 |
| 40 | Большинство команд в `scripts/c_cmd/c_cmd.gml`; часть — в одноимённых `scripts/c_*/*.gml` | OK — отдельные файлы: c_begin, c_play, c_end, c_wait, c_speaker, c_facing, c_setxy, c_depth, c_autofacing, c_autowalk (формулировка «c_wait-соседи» уточнена при правке) |
| 44-79 (таблица) | Сигнатуры и Action-маппинги всех 36 живых `c_*`-команд | OK — сверено построчно с c_cmd.gml:215-349, c_begin/c_play/c_end/c_wait/c_speaker/c_facing/c_setxy/c_depth/c_autofacing/c_autowalk.gml. `c_flip` → `ActionFlip` через `image_xscale` (classes:3051-3065); `c_depth` → `ActionSetDepth` + `depth_mode = manual` (classes:2941-2953); `c_walkdirect`/`_speed` → `ActionMoveDirect` с `use_speed = false/true` (c_cmd.gml:308-316, classes:2387) |
| 81 | Дефолты опциональных аргументов — только в конструкторах `Action*` | OK — комментарий F-539 в c_cmd.gml:246-248 |
| 85-98 | Девять `c_*`-заглушек DELETE_CANDIDATE с указанными сигнатурами | OK — все 9 файлов подтверждены (пустые тела, метки); `c_cmd_x` вызывалась из `c_delaycmd`/`c_delaywalk`, `c_pan` — из `c_pan_wait` (комментарии в файлах; R3/C10_fixlog F-131) |
| 99 | Имен `c_move`, `c_follow_path`, `c_actor_create`, `c_parallel`, `c_branch`, `c_camera_*` нет | OK — `grep "function c_move\|c_camera…"` пуст; зачищены целиком в R3/F-131 (не переведены в стабы) |
| 105-118 | Таблица `cutscene_*`-хелперов | OK — cutscene_add.gml:6-24; c_cmd.gml:114-139; cutscene_branch.gml:6-8; cutscene_set_facing.gml:11-13; cutscene_load_json.gml:9-100+; cutscene_load_engine_settings.gml:14-40; cutscene_action_factory.gml:1-2,1243; scr_cutscene_music.gml:155-178 |
| 124 | 17 отдельных `cutscene_*`-файлов — заглушки | OK — все 17 подтверждены пустыми телами с меткой DELETE_CANDIDATE |
| 125 | 14 заглушек внутри `cutscene_add.gml` | OK — cutscene_add.gml:32-45 (ровно 14 функций) |
| 126 | `scr_cutscene_make` — заглушка `return noone` | OK — scr_cutscene_make.gml:8-10 |
| 127 | `scr_cutscene_animate` (`Script312`) — пустой стаб; живой аналог `c_animate`/`ActionAnimate` | OK — scr_cutscene_animate.gml:4-5 (функция `Script312`); NB: комментарий в коде называет живым аналогом `scripts/cutscene_animate`, но тот сам стаб — формулировка страницы корректнее |
| 131 | Регистрация одноразовая из `obj_Init/Create_0.gml`, повторный вызов → `true` | OK — obj_Init/Create_0.gml:269-270; c_cmd.gml:145-147,211-212 |
| 135-139 | Списки yarn-имён (8 + 18 + 9 + 4 + 4 = 43 регистрации) | OK — все 43 `ChatterboxAddFunction` сверены с c_cmd.gml:149-209; `c_var`/`c_var_lerp`/`c_var_lerp_to` — только yarn-алиасы (GML-функций нет, grep пуст) |
| 141 | `__cutscene_bridge_real` (мусор → 0), `__cutscene_bridge_real_opt` (→ `undefined`), `__cutscene_bridge_color` (имена + число) | OK — c_cmd.gml:48-112; цвета black/white/red/green/blue/yellow подтверждены |
| 145-153 | GML-пример | OK — API верно; `snd_wobble` существует (sounds/snd_wobble); `c_wait(30)` = полсекунды при 60 fps (options_main.yy:13) |
| 155-162 | yarn-пример = нода `Cutscene-Bridge-Demo` | OK — datafiles/Dialogues/testDialogue.yarn:30-38 (дословное совпадение) |
| 169-174 | Ссылки «См. также» | OK — все цели есть в `_meta/nav_plan.md` |
| 175 | sources: `scripts/c_cmd/c_cmd.gml:1-397` | WRONG — файл 349 строк; исправлено на `:1-349` |

## partial-control.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 13 | Три поля менеджера; переключение `ActionPartialControl`; фильтры в `scr_inputApi` и `scr_interaction` | OK — obj_cutsceneManager/Create_0.gml:312-316; scr_cutscene_classes.gml:4819-4824; scr_inputApi.gml:49-137; interactionWithNPCsOrObjects.gml:41-70 |
| 17-23 | Enum `INTERACT_PARTIAL_CONTROL` в interactionWithNPCsOrObjects.gml: `LOCKED=0`, `WHITELIST=1`, `FREE=2`; поведение режимов | OK — interactionWithNPCsOrObjects.gml:4-9; scr_inputApi.gml:94-107; scr_player_ui_blocking.gml:15-24 |
| 25 | `ActionPartialControl.start` пишет 3 поля и выставляет `can_move` (`false` при 0, `true` при >0); фриз в `start_cutscene()` только при type==0; `finish_cutscene()` сбрасывает поля и восстанавливает `can_move` из `prev_player_can_move` только если тип был 0 | OK — classes:4819-4840; Create_0.gml:644-650, 702-710 |
| 28 | Мусорный `control_type` → один WARNING (`__partial_control_warned`), ввод глушится; тот же дефолт-запрет в `scr_interaction` | OK — scr_inputApi.gml:99-107; interactionWithNPCsOrObjects.gml:44-46,66-68 |
| 34-37 | Алиасы: `"move"` → up/down/left/right/run; `"interact"` → `confirm`; прочие строки — имена из `input_map` (список `scr_input_actions_list`); пустой массив → только `confirm` | OK — scr_inputApi.gml:123-137, 27-29 |
| 39 | `partial_control_whitelist` резолвится через `mgr.resolve_target()`, сравнение с `id` инстанса | OK — interactionWithNPCsOrObjects.gml:52-64; resolve_target в Create_0.gml:504-531 |
| 43-49 | Гейт `scr_input__is_cutscene_blocked_here` вызывают `scr_input_down`/`pressed`/`repeater`; порядок проверок (не катсцена → UI-объекты → FREE → WHITELIST → LOCKED/прочее) | OK — scr_inputApi.gml:54-112, 276, 306, 359 |
| 46 | UI-список = `scr_ui_objects_list()` (общий с `scr_checkUIBlocking`) + `obj_cutsceneManager` и `obj_sound_test` точечно | OK — scr_inputApi.gml:59-73; scr_checkUIBlocking.gml:44-49 |
| 51 | Блокированный ввод подменяется виртуальным `__cutscene_virtual_down`/`__cutscene_virtual_prev`, продюсеров нет → фактически `false` | OK — scr_inputApi.gml:274-325, 359-372; вне inputApi писателей не найдено (grep) |
| 53-65 | `scr_player_ui_blocking` до `scr_player_movement` в `obj_player/Step_0`; mermaid-ветвление; `include_cutscene = false` | OK — obj_player/Step_0.gml:6,13; scr_player_ui_blocking.gml:10-26; scr_checkUIBlocking(false,false) |
| 69 | `wait_for_interact`: очередь `global.__interacted_targets` (пушат `scr_interaction`/`obj_save`, максимум 32), действие ищет свой `resolved_target` и удаляет запись | OK — classes:4526-4552, 4574-4590; interactionWithNPCsOrObjects.gml:83-90; obj_save/Step_0.gml:22-30 |
| 73 | Пустой `allowed_actions` → `confirm` держит связку WHITELIST + `wait_for_interact` рабочей | OK — scr_inputApi.gml:83-88, 126-128 |
| 74 | `timeout` в секундах → кадры; `0` = бесконечно; `timeout_action`: `"continue"` (дефолт) / `"abort_parallel"` через `__cutscene_parallel_request_abort` | OK — cutscene_action_factory.gml:1031-1037; classes:4539-4543, 4564-4571 |
| 75 | Перерезолв цели при мёртвом `resolved_target` | OK — classes:4560-4562 |
| 76 | Чистка мёртвых `id` на каждом `update()` и в `cleanup()` | OK — classes:4578-4580, 4596-4603 |
| 85-87 | JSON-поля `partial_control`: `control_type` (real, дефолт 0), `whitelist` (не-строки отбрасываются), `allowed_actions` — массив или строка `"[\"move\"]"`/`"move,interact"` | OK — cutscene_action_factory.gml:991-1026 |
| 90-92 | JSON-пример | OK — формат соответствует фабрике (`target` читается `__cutscene_json_get_target`, cutscene_load_json.gml:455-464) |
| 95 | Фабрика `f[$ "partial_control"]`, класс `ActionPartialControl` | OK — cutscene_action_factory.gml:991; classes:4813 |
| 99-103 | Ссылки «См. также» | OK — все цели есть в `_meta/nav_plan.md` |
| 105 | sources-диапазоны | OK — classes:4526-4605 (WaitForInteract), 4807-4841 (PartialControl), factory:991-1038, Create_0:312-317/585-665/695-715 — все попадают |

## Итог

- **gml-dsl.md**: 1 WRONG-по-существу (строка 33 — поведение пустого target у `c_halt`/`c_shakeobj`/`c_flip`/`c_visible`), 1 WRONG-косметика (sources `:1-397` → `:1-349`), 1 уточнение формулировки (строка 40).
- **partial-control.md**: ошибок не найдено — все утверждения подтверждены.
- MISSING/UNVERIFIABLE: нет.
