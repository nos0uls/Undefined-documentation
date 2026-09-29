# Фактчек: getting-started/project-structure.md + conventions.md

Дата: 2026-09 (ревизия кода `7ee444a`, ветка `audit-fixes-2026-09` — совпадает с заявленной на странице).
Источник истины: `$P = Undefinedtale888/` (только чтение). Формат вердиктов: OK / WRONG (file:line) / UNVERIFIABLE / MISSING.

## project-structure.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| L10 | Состав по ветке `audit-fixes-2026-09` | OK (`git rev-parse` → `audit-fixes-2026-09`, HEAD `7ee444a`) |
| L16 | `.yyp`: список ресурсов, `RoomOrder` (первой `rm_init`), Included Files | WRONG — ключ в JSON называется `RoomOrderNodes` (`Undefinedtale888.yyp:769`); первой идёт `rm_init` (`:770`), `IncludedFiles` есть (`:104`) |
| L17 | `Undefinedtale888.resource_order` в `.gitignore` | OK (`Undefinedtale888/.gitignore:59` — `*.resource_order`) |
| L18 | `guide.md` — стандарты: именование, JSDoc, диалоги, локализация, чек-листы | OK (`guide.md` целиком: разделы «Правила именования», «Обязательные элементы», «Диалоги», «Локализация», «Система проверок») |
| L19 | `README.md` — установка, запуск, Yarn, локализация, деплой | OK (`README.md:1-60` + далее про билды) |
| L20 | `УПРАВЛЕНИЕ.txt` — таблица игровых и debug-клавиш | OK (`УПРАВЛЕНИЕ.txt:1-30`) |
| L21 | `cutscene_system_research.md` — исследование движка катсцен | OK (файл есть, 28 КБ) |
| L22 | `audit/`, `audit_2026-09/` — рабочие материалы аудитов | OK (каталоги существуют) |
| L28 | `objects/` — 53 объекта; перечисленные системные/родители/`o_SharedTweener`/без префикса | OK (53 каталога; все названные имена существуют: `obj_Init`, `obj_globalManager`, `obj_music_ctrl`, `obj_cutsceneManager`, `par_depth/actor/decor/entity/interactable`, `o_SharedTweener`, `bush`, `npc1`, `pinkBench`, `textboxTest_scribble`) |
| L29 | `scripts/` — 359 скриптов, один ресурс = один `.gml`; `scr_*`/`c_*`/`cutscene_*` | OK (359 каталогов = 359 `.gml`; `scr_*` 74, `c_*` 20, `cutscene_*` 23) |
| L29 | `Chatterbox*`/`__Chatterbox*` ~103 | OK (63 + 40 = 103 ровно) |
| L29 | `scribble*`/`__scribble_*` ~117 | WRONG — фактически 110 (67 `scribble_*` + 43 `__scribble_*`, `ls scripts/`) |
| L29 | `TGMX_*` (12) | OK (12 каталогов `TGMX_0..TGMX_System`, `TGMX_Experimental`) |
| L30 | `rooms/` — 16 комнат; перечисленные имена; `RoomCreationCode.gml` у части комнат | OK (16; все имена существуют; `RoomCreationCode.gml` у `rm_devLoad` и `SCREENSHOTS`) |
| L32 | `sounds/` — 8 ресурсов; `mus_intro`, `music_menu`, `music_SchoolRoutine`, `snd_text_ch1`, `snd_wobble` | OK (8; все имена существуют) |
| L33 | `sprites/` — 79; `spr_Chara_walking_*` рядом с `bush2`, `npc`, `kachela` | OK (79; имена существуют) |
| L34 | `fonts/` — 11; `ft_menuFont`, `ft_p3r_title`, `Montserrat`, `scribble_fallback_font` | OK (11; имена существуют) |
| L35 | `shaders/` — `shd_grayscale`, `shd_p3r_*`, `__shd_scribble*` | OK (14 шейдеров: `shd_grayscale`, `shd_p3r_glow/gradient/water`, `shd_Chara_Eyes`, 9 `__shd_scribble*`) |
| L36 | `animcurves/` — 3 кривые | OK (ровно перечисленные) |
| L37 | `tilesets/` — 5 тайлсетов | OK (ровно перечисленные) |
| L38 | `notes/` — только `TGMX_Documentation`, `TGMX_Terms_of_Use`, `TGMX_Update_Log` | OK (3 каталога) |
| L39 | `options/` — перечисленные подкаталоги | OK (11 каталогов, совпадают) |
| L45 | `obj_Init` persistent, единственный инстанс в `rm_init`, объявляет `global.*`, создаёт `obj_globalManager` и `obj_music_ctrl` | OK (`obj_Init.yy:15 persistent:true`; в `rm_init.yy` ровно 1 `$GMRInstance` — `obj_Init`; `Create_0.gml:275,279-280,321-322` — `ChatterboxLoadFromFile` и `instance_create_layer(..., scr_layer_ensure_instances(), obj_music_ctrl/obj_globalManager)`; `global.*` объявляются там же) |
| L46 | `obj_globalManager` persistent, создаётся из `obj_Init` на слое `scr_layer_ensure_instances()`; смена комнат, debug-хоткеи, уведомления, шаг катсцен и эмоутов | OK (`obj_globalManager.yy:19`; `Create_0.gml:322`; `Step_0.gml:26,31,40,43,46,48-49` — `scr_global_on_room_change`, `scr_global_debug_hotkeys`, `scr_global_handle_notifications`, `emote_step`, `cutscene_runtime_step`) |
| L47 | `obj_player` наследник `par_actor` → `par_depth`; `obj_collider`/`obj_slopeCollider` под `par_entity` | OK (`obj_player.yy → par_actor`; `par_actor.yy → par_depth`; `obj_collider.yy`/`obj_slopeCollider.yy → par_entity`; `par_entity.yy → null`) |
| L48 | `obj_cutsceneManager` — очередь действий; `obj_actor`; `obj_cutsceneTest` | OK (`obj_actor.yy → par_actor`; очередь `_mgr.action_queue` в `cutscene_add.gml:23`) |
| L49 | UI-объекты: `obj_menu`, `obj_inGameMenu`, `obj_settingsManager`, `obj_saveManager`, `obj_devLoader`, `obj_face`, `textboxTest_scribble`, `obj_p3r_*` | OK (все существуют в `objects/`) |
| L53 | `obj_Init` грузит `.yarn` через `ChatterboxLoadFromFile`; `textboxTest_scribble` и `readDialogue` двигают диалог по нодам | WRONG-частично — `readDialogue` не вызывает Chatterbox: он создаёт `textboxTest_scribble` и передаёт `dialogue_filename`/`dialogue_node` (`readDialogue.gml:11-18`); само окно ведёт диалог (`textboxTest_scribble/Step_0.gml:175,225,239` — `ChatterboxCreate/Select/Continue`). Формулировка уточнена |
| L54 | Scribble: скрипты/шейдеры/`scribble_fallback_font`/лицензия; обёртки `draw_text_scribble`, `string_width_scribble`; используется в текстбоксе и `obj_p3r_*` | OK (`draw_text_scribble.gml:23`, `string_width_scribble.gml:10`, `draw_text_scribble_ext`, `string_width_scribble_ext`; `datafiles/scribble_license.txt`; scribble в `textboxTest_scribble/*`, `obj_p3r_*/Draw_64.gml`, также `obj_menu/Draw_64.gml`) |
| L55 | TGMX 1.0.8; `o_SharedTweener` persistent, лениво создаётся `SharedTweener()`; `TweenFire` только в `obj_p3r_title/pause/settings/transition`; решение по мокапам | OK (`notes/TGMX_Documentation.md:2` — «TweenGMX 1.0.8»; `TGMX_System.gml:477-493` — `SharedTweener()` с `instance_create_depth(...,o_SharedTweener)`; `o_SharedTweener.yy:21 persistent:true`; `grep TweenFire` вне библиотеки — только `obj_p3r_pause/settings/title/transition`; `audit_2026-09/fix/DESIGN_DECISIONS.md:21-23` — F-223 «TGMX используется только плейсхолдерами obj_p3r_*») |
| L61 | `Dialogues/` — 4 Yarn: `fountain`, `testDialogue`, `testDialogueBlue`, `testChoices` | OK (ровно эти 4 файла) |
| L62 | `cutscenes/` — `cutscene.json`, `cutscene1.json`, `cutscene_demo_888.yarn`, `test_*.json`, `cutscene_engine_settings.json` | OK (все файлы существуют; `test_*.json` — 5 шт.) |
| L63 | `cutscenes/tests/` — ~90 JSON-тестов + `stress/` | OK (81 JSON в `tests/` + 8 в `tests/stress/` = 89 ≈ ~90) |
| L64 | `scribble_license.txt` | OK |
| L66 | Поля `cutscene_engine_settings.json`; читается один раз за сессию | OK (`schema_version`, `default_fps`, `strict_mode_default`, `default_actor_object`, `default_emote_sprite`, `whitelist.run_functions/branch_conditions`, `debug.*` — все есть; `cutscene_load_engine_settings.gml` — `static _cached_settings`, чтение 1 раз до `_force_reload`) |
| L68-69 | Included Files регистрируются в `.yyp` | OK (`Undefinedtale888.yyp:104+` — массив `IncludedFiles`) |
| L71-72 | `cutscene_load_json` срезает `./` и `datafiles/` перед `file_exists`; пути от рабочей директории | OK (`cutscene_load_json.gml:22-34,36`) |

MISSING (существенное): в таблице корня нет строки про `.gitattributes`/`.gitignore` (правила LF, `*.resource_order` в ignore) — добавлена строка.

## conventions.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| L11 | Стандарт в `guide.md`; ниже — фактическое с расхождениями | OK |
| L17-27 | Таблица префиксов, все примеры | OK (все имена ресурсов существуют: `obj_player`, `obj_Init`, `obj_cutsceneManager`, `obj_inGameMenu`, `par_*`, `scr_inputApi`, `scr_player_movement`, `scr_saveLoad`, `scr_settingsManager`, `c_begin/play/wait/pan/speaker`, `cutscene_load_json/actor_create/camera_pan`, `rm_*`, `spr_Chara_walking_D`, `spr_p3r_cursor`, `spr_rmChanger`, `snd_text_ch1`, `snd_wobble`, `mus_intro`, `mus_end`, `music_menu`, `music_SchoolRoutine`, `ft_menuFont`, `ft_dialogueTest`, `ft_p3r_title`, `shd_grayscale`, `shd_p3r_glow`, `shd_Chara_Eyes`) |
| L30 | Исключения: `bush`, `npc1`, `npc2`, `pinkBench`, `sand`, `screenshot`, `textboxTest_scribble`, `spr_pinkBench`, `objRoomChanger`; комнаты `DevRoom1`, `SCREENSHOTS`, `roomForDialogueTesting`; `mus_`/`music_`; спрайты `bush2`, `npc`, `kachela`; `guide.md` предписывает `fnt_`/`snd_`/`shd_`/`tls_`; фактически `ft_*`, `grassTile`, `ts_main` | OK (все имена в `ls`; `guide.md:15,18-20` — `snd_`/`shd_`/`fnt_`/`tls_`) |
| L36 | `_param`/`_tmp`: `cutscene_load_json(_path)`, `var _buf`, `var _normalized_path` | OK (`cutscene_load_json.gml:7,20,41`) |
| L37 | Примеры обоих стилей: `menu_cursor_target_y`, `can_move`, `move_active`, `dialogueFile` | WRONG частично — `dialogueFile` в коде не существует (это пример из `guide.md:113`); фактический идентификатор — `dialogue_filename` (snake_case). Заменено на реальный camelCase `itemType` (`constructorsForInventory.gml:8,27`) |
| L38 | `global.game_state`, `global.input_map`, `global.player_settings` | OK (`scr_game_state.gml`, `obj_Init/Create_0.gml`, `scr_inputApi.gml`) |
| L39 | `global.__cutscene_build_mgr`, `global.__music_volume`, `global.__init_done` | OK (`c_begin.gml`, `scr_music_init.gml`, `obj_Init/Create_0.gml`) |
| L40 | `__cutscene_resolve_target`, `#macro __CUTSCENE_EPSILON`, `__shd_scribble*`, `__Chatterbox*` | OK (`scr_cutscene_classes.gml:29`) |
| L41 | `SAVE_FORMAT_VERSION 3`, `MANAGER_DEPTH -10000`, `ITEMTYPE.WEAPON` | OK (`scr_saveSave.gml:7`, `scr_constants.gml:4`, `constructorsForInventory.gml:27`) |
| L42 | `ITEMTYPE`, `PLAYER_AXIS_FSM` | OK (`currentENUMS.gml:4`, `scr_player_process_mutually_exclusive_inputs.gml:4`) |
| L45 | `__ChatterboxClassInstruction`, `__scribble_class_typist`, `__cutscene_get_resolver`, `global.__cutscene_checkpoints` | OK (скрипты существуют; `scr_cutscene_classes.gml`) |
| L51 | Feather-стиль, ~83 проектных файла | OK (`grep -lE '/// @(function\|desc\|description)'` по не-библиотечным `scripts/` = 83) |
| L53-60 | Цитата заголовка `readDialogue` | WRONG-минор — цитата усечена: в файле `@description` занимает 3 строки (`readDialogue.gml:1-8`). Приведено дословно |
| L63 | Второй стиль `@summary`/`@returns`/`@since`, ~9 файлов | OK (ровно 9 файлов с `/// @summary`; уточнено до «9 файлов») |
| L65-70 | Цитата заголовка `cutscene_load_json` | WRONG-минор — пропущены строки-продолжения `@param` (`cutscene_load_json.gml:1-7`). Приведено дословно |
| L73 | `guide.md` предписывает `@summary`/`@param`/`@returns`/`@since`; старый код — `@function`/`@desc`/`@return` | OK (`guide.md:35-39,80`; `@desc` — 82 файла) |
| L77 | `#region` в 52 файлах | OK (`grep -l '#region'` по `scripts/`+`objects/` = 52) |
| L79-81 | Регионы в `scr_cutscene_classes`, `scr_music_init`, `cutscene_action_factory`, `scr_settings_step_root`, `scr_saveLoad` | OK (`scr_cutscene_classes.gml:2464,2960,3001`; `scr_music_init.gml:6,110` и др.; у трёх файлов `#region` есть) |
| L85 | Нет `AGENTS.md`/`.windsurf/`/`.devin/rules/` | OK (`find` по репозиторию — пусто; `.windsurf` упомянут в `.gitignore`, на диске отсутствует) |
| L87 | `///` обязательны, «блокирующая ошибка» | OK (`guide.md:241`) |
| L88 | Инициализация в `Create`, освобождение в `Clean Up`, `ds_*` явно | OK (`guide.md:42-50,245` — в оригинале «Cleanup», имя события GMS — Clean Up) |
| L89 | Guard clauses: `noone`/`false` + `show_debug_message`; примеры `cutscene_load_json`, `cutscene_add` | WRONG-минор — `cutscene_add` возвращает void и логирует только при `global.debug` (`cutscene_add.gml:6-18`). Формулировка уточнена |
| L90 | Глобалы в `obj_Init`; исключение `global.default_settings` телом скрипта | OK (`scr_settingsManager.gml:8-11` — комментарий «единственная "скрытая" точка» + присвоение в теле; `:50` — «единое место инициализации») |
| L91 | Тексты не хардкодить | OK (`guide.md:77`) |
| L92 | Магические числа → константы | OK (`guide.md:81,221`; макросы подтверждены) |
| L93 | Аудит по `obj_`/`spr_`/`snd_`/`rm_`/`scr_`/`shd_`/`fnt_`/`tls_` | OK (`guide.md:215`) |
| L96 | Метки аудита `(F-535)`, `(E-V03)`, `(F-055)` в комментариях | OK (`cutscene_load_json.gml:20,54`, `scr_cutscene_classes.gml:4811`, `scr_inputApi.gml:52,116`) |
| L100 | `.gitattributes`: LF для `*.gml`/`*.yy`/`*.yyp`/`*.json`; корневой `* text=auto` | OK (`Undefinedtale888/.gitattributes` целиком; корневой `.gitattributes` — `* text=auto`) |
| L101 | UTF-8, комментарии на русском | OK |
| L102 | BOM `EF BB BF` срезается по байтам до `buffer_read`; `buffer_text` → `U+FEFF` | OK (`cutscene_load_json.gml:48-58` — `buffer_peek` 0xEF/0xBB/0xBF + `buffer_seek(3)`, комментарий E-V03) |

## Итог исправлений

project-structure.md:
- L16: `RoomOrder` → `RoomOrderNodes`, `Included Files` → `IncludedFiles`.
- L29: `~117` → `110` (точное), `~103` → `103`.
- L53: уточнена роль `readDialogue` (открывает окно; диалог ведёт `textboxTest_scribble`).
- Добавлена строка `.gitattributes`/`.gitignore` в таблицу корня.

conventions.md:
- L37: `dialogueFile` → `itemType` (реальный camelCase из кода).
- L54-59, L66-70: цитаты JSDoc приведены дословно (добавлены пропущенные строки).
- L63: «~9 файлов» → «9 файлов».
- L89: уточнён пример `cutscene_add` (ранний возврат, лог при `global.debug`).
