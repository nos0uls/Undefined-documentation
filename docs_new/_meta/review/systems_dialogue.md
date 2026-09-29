# Фактчек `systems/dialogue.md` — ревизия кода 7ee444a

Код: `$P` (только чтение). Страница: `docs_new/systems/dialogue.md`. Ссылки проверены по `_meta/nav_plan.md` — все целевые файлы существуют.

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 13 | Пайплайн: yarn из `datafiles/Dialogues/` → Chatterbox, окно `textboxTest_scribble` → Scribble, портрет `obj_face`, эмоуты — глобальная система | OK (`Step_0.gml:166-183`; `Draw_64.gml:169`; `obj_face/Step_2.gml`; `scr_emote_system.gml`) |
| 19 | Mermaid: `ActionDialogue → readDialogue` | **WRONG** — `ActionDialogue` не зовёт `readDialogue`: он сам создаёт/подхватывает `textboxTest_scribble` (`scr_cutscene_classes.gml:2520-2535`). Зовут `readDialogue` только `scr_interaction` (`interactionWithNPCsOrObjects.gml:94`) и `obj_save` (`obj_save/Step_0.gml:33`) |
| 24-26 | Mermaid: Export → scr_saveSave → Import в scr_saveLoad | OK (`scr_saveSave.gml:129-136`, `scr_saveLoad.gml:272-285`) |
| 29 | В катсценах окно создаёт и контролирует `ActionDialogue` | OK (`scr_cutscene_classes.gml:2505-2632`) |
| 34-41 | Сигнатура `readDialogue(_filename, _nodename)`, параметры, возврат instance/noone | OK (`readDialogue.gml:8-24`) |
| 43 | Создание на слое через `scr_layer_ensure_instances` в (0,0); выставляются `is_dialogue_requested`, `dialogue_filename`, `dialogue_node`; блокировка через `scr_player_ui_blocking` | OK (`readDialogue.gml:13-19`; `scr_player_ui_blocking.gml:10-15`; `scr_checkUIBlocking.gml:53`) |
| 45 | Вызывается из `scr_interaction` и `obj_save/Step_0`; пример `obj_save` в `rm_road_curve` → `fountain.yarn`, нода `RM_002: FOUNTAIN` | OK (`interactionWithNPCsOrObjects.gml:94`; `obj_save/Step_0.gml:33`; `rm_road_curve.yy:65-66`; `fountain.yarn:5`) |
| 49 | Файлы: `testDialogue.yarn`, `testDialogueBlue.yarn`, `testChoices.yarn`, `fountain.yarn`; нода `title:`/`---`/`===`; `__PrivCrochet_*` метаданные | OK (4 файла в `datafiles/Dialogues/`; `testDialogue.yarn:1-15`) |
| 51-62 | Цитата из `testDialogue.yarn` (нода `Bench`) | **WRONG** — последняя строка приврата: в файле `Chara [chara:question]: Ha-ha,[delay, 1000] funny. At least don't eat your brother for the god's sake, I guess.` + строка `Chara [chara]: How about we go grab a lunch...`, а не `Chara [chara]: Ha-ha, funny.` (`testDialogue.yarn`, нода Bench) |
| 64 | Speaker-строка `DisplayName [code:emotion]:`, парсит `scr_parse_emote` | OK (`scr_parse_emote.gml:1-23`) |
| 65 | Максимум 4 опции, warning один раз | OK, с нюансом: флаг `options_overflow_warned` сбрасывается при исчезновении опций (`Draw_64.gml:44-47, 218-224`) — «один раз на экран опций» |
| 66 | `<<jump>>`, `<<wait>>` стандартные; `c_*` зарегистрированы в `cutscene_register_chatterbox_functions()` в `obj_Init/Create_0`, ~40 функций | OK (`__ChatterboxCompile.gml:92,162`; `c_cmd.gml:141-209` — 44 вызова `ChatterboxAddFunction`; `obj_Init/Create_0.gml:268-269`) |
| 67 | `[wave]`, `[delay,мс]`, `[c_red]…[/c]` — Scribble; литеральная `[` → `[[` | OK (`Draw_64.gml:62-66, 359-362`) |
| 68 | `$var` и `visited()` в глобальном scope Chatterbox, попадают в сейв | OK — visited-счётчики лежат в `__variablesMap` (`ChatterboxGetVisited.gml:12-20`, `__ChatterboxClassNode.gml:40`), Export копирует карту без констант (`ChatterboxVariablesExport.gml:6-18`) |
| 72 | Непersistent, без спрайта; события Create_0, Step_1, Step_0, Draw_64, CleanUp_0; логика в Step | OK (`textboxTest_scribble.yy`: `persistent:false`, `spriteId:null`, eventType 0/3(num 1)/3(num 0)/8(num 64)/12(num 0)) |
| 76 | Create_0 создаёт `obj_face` при отсутствии | OK (`Create_0.gml:8-11`) |
| 77 | `typist.in(char_speed/fps, 0)`, `char_speed=21`; `typist.sound(global.current_voice, 2000, 1, 1)`; `execution_scope(id)` + `function_per_char` | OK (`Create_0.gml:20-28, 90-91`) |
| 78 | Дефолты `actor_prev`/`emotion_prev`/`display_name_prev`, `mouth_*_prev`, `sound_prev`; `talk_chance=0.6`, `talk_hold_frames=6` (30-FPS экв.), `talk_max_consecutive=7`, `talk_pause_symbols=3` | OK (`Create_0.gml:102-130`) |
| 79 | `typing_done`, `prevent_skip`, `stay_open`, `auto_advance`, `auto_advance_delay=30`; `non_blocking` не объявлено | OK (`Create_0.gml:135-143`; `non_blocking` ставится в `scr_cutscene_classes.gml:2541`) |
| 80 | Layout-константы двух пресетов, слоты 1–4 опций, nameplate, `__cache_*` | OK (`Create_0.gml:150-283`) |
| 84 | Step_1 обнуляет `global.current_sprite` при опциях | OK (`Step_1.gml:15-17`) |
| 90 | Запрос: `ChatterboxIsLoaded` → `file_exists("Dialogues/"+name)` → `ChatterboxLoadFromFile` → `ChatterboxCreate` → `FindNode` → `ChatterboxJump`; промах → `show_debug_message` + `_request_failed` + destroy в конце Step | OK (`Step_0.gml:155-194, 333-339`; макрос `CHATTERBOX_INCLUDED_FILES_SUBDIRECTORY="Dialogues"` в `__ChatterboxConfigMacros.gml:10`) |
| 91 | `apply_current_dialogue_state()`: последняя content-строка, forced-эмоция consume-once из `global.__actor_forced_emotion`, обновление `mouth_*`/`sound`/`text`/`text_plain` | OK (`Step_0.gml:6-118`). Нюанс: forced забирается после первого парсинга по актёру строки, затем строка перепарсивается (`Step_0.gml:41-56`) |
| 92-96 | Ввод confirm: опции → `ChatterboxSelect`; печать → `typist.skip()` если `!prevent_skip`; допечатано+waiting → `ChatterboxContinue`; затем `apply_current_dialogue_state()` + `typist.reset()` | OK (`Step_0.gml:203-246`) |
| 97 | Навигация: 1–3 опции циклически, up/down для 3; для 4 — `nav_map` (0=левый, 1=правый, 2=нижний, 3=верхний) | OK (`Step_0.gml:265-327`) |
| 98 | `ChatterboxIsStopped` или `_request_failed` и `!stay_open` → `instance_destroy`; `can_move` снимает `scr_player_ui_blocking` | OK (`Step_0.gml:333-339`) |
| 102 | Бокс `spr_dialogue_box` = `gui_width-100` × `gui_height/3`, внизу; пресет по `sprite_exists(global.current_sprite)` | OK (`Draw_64.gml:22-36, 123`) |
| 103 | Nameplate `textbox_menuingame` + `display_name_prev` шрифтом `ft_menuFont`; скрыт у narrator/при опциях/`nameplate_visible=false`; auto-fit с `nameplate_min_width` | OK (`Create_0.gml:232-248`; `Draw_64.gml:53-118`) |
| 104 | Портрет `global.current_sprite` по `portrait_*` пресета | OK (`Draw_64.gml:137-143`) |
| 105 | `scribble(text)` + `.scale()` + `.line_spacing("107%")` + `.padding(0,0,0,0)` + `.wrap(w,h)`; кэш по сигнатуре; `textScribble.draw(x,y,typist)`; маркер `>` без портрета после допечатки | OK (`Draw_64.gml:165-207`; `marker_visible_with_portrait=false` в `Create_0.gml:161`) |
| 106 | Опции: основной текст не рисуется; собственный word-wrap с пробниками Scribble; шаг строки = разность высот пробников; выбранная `c_red`, остальные `c_white` | OK (`Draw_64.gml:187, 212-394`) |
| 107 | `ft_menuFont`; `scribble_font_set_default`/`draw_get_font` сохраняются и восстанавливаются | OK (`Draw_64.gml:14-15, 155, 400-403`) |
| 111 | CleanUp_0: уничтожает `obj_face`, если это последний `textboxTest_scribble` | OK (`CleanUp_0.gml:2-4`, `instance_number <= 1`) |
| 117 | `non_blocking`: не объявлено, `ActionDialogue` ставит `= !block_queue`; `scr_checkUIBlocking_raw` пропускает инстанс | OK (`scr_cutscene_classes.gml:2541`; `scr_checkUIBlocking.gml:90`) |
| 118 | `auto_advance=false`; ставят `ActionDialogue`/`ActionDialogueControl`; ждёт `auto_advance_delay`=30 и эмулирует confirm; на опциях не действует | OK (`Create_0.gml:138-143`; `scr_cutscene_classes.gml:2540-2542, 2799-2801`; `Step_0.gml:211-218`) |
| 119 | `stay_open=false`; `ActionDialogueControl`; окно переиспользуется `ActionDialogue`, закрывается `ActionClearDialogue` | OK (`Create_0.gml:137`; `scr_cutscene_classes.gml:2544, 2624, 2798-2803, 2897-2919`) |
| 120 | `prevent_skip=false`; `ActionDialogueControl`; confirm не вызывает `typist.skip()` | OK (`Create_0.gml:136`; `Step_0.gml:234-236`; `scr_cutscene_classes.gml:2543, 2797`) |
| 121 | `char_speed=21`; `ActionSetDialogueSpeed`; менеджер хранит `dialogue_char_speed` | OK (`Create_0.gml:24`; `scr_cutscene_classes.gml:2741-2758, 2548-2553`) |
| 125 | `obj_Init/Create_0` зовёт `ChatterboxLoadFromFile("testDialogue.yarn")` и `cutscene_register_chatterbox_functions()`; остальные файлы подгружает окно | OK (`obj_Init/Create_0.gml:268-273`; `Step_0.gml:163-168`) |
| 126 | `ChatterboxVariablesExport()` → строка (переменные без констант), `scr_saveSave` пишет отдельной строкой, формат v3+ | OK (`ChatterboxVariablesExport.gml`; `scr_saveSave.gml:128-136`) |
| 127 | `scr_saveLoad`: непустая JSON → `ChatterboxVariablesImport`; отсутствующая/битая → `ResetAll`+`ClearVisitedAll`; восстановление при любом `_change_room`; `false` использует тестовый стенд | **Частично WRONG** — сброс делается только при пустой/не-`{` секции; битый JSON с `{` уходит в Import и падает в try/catch с warn (`scr_saveLoad.gml:272-286`). `scr_saveLoad(false)` зовёт `scr_stress_tests.gml:770` — подтверждено |
| 128 | `scr_defaultLoad` сбрасывает теми же `ResetAll`+`ClearVisitedAll` | OK (`scr_defaultLoad.gml:35-40`) |
| 132-136 | `obj_face`: `Draw_64=exit`; Step_2 выбирает кадр; активный окно = не stopped или `stay_open`; опции/нет окна/невалидный `mouth_closed` → `global.current_sprite=noone`; `talk_open_now` → `mouth_open` | OK (`obj_face/Draw_64.gml:1`; `Step_2.gml:1-57`) |
| 141-143 | Сигнатура и возврат `scr_parse_emote` | OK (`scr_parse_emote.gml:23`, defaults опущены — допустимо) |
| 145-150 | Правила разбора `code:emotion`, narrator, наследование emotion, приоритет display_name, forced | OK (`scr_parse_emote.gml:48-137`) |
| 154 | `map_emotions` static-карта: `narrator.default` (noone-спрайты, `snd_text_ch1`), `chara.default`/`chara.question` (`chara_question_c`/`o`); неизвестный actor/emotion → default; `actor_display_name`: `chara` → `"Chara"` | OK (`map_emotions.gml:12-44, 69-81`; `actor_display_name.gml:8-19`). Уточнение: неизвестный actor → ветка `narrator`, неизвестная emotion → `actor.default` |
| 156 | `ActionSetPortraitNext`/`ActionSetEmotion` пишут `global.__actor_forced_emotion[actor]`; окно забирает consume-once; `ActionSetPortraitNow` перезаписывает `mouth_*_prev`/`sound_prev` | OK (`scr_cutscene_classes.gml:2827-2835, 3239-3244, 2877-2886`; `Step_0.gml:46-56`). Нюанс формулировки: запись забирается по актёру уже распарсенной строки — фраза «перед парсингом строки» не совсем точна |
| 160 | Per-char callback: пунктуация пропускается, `talk_chance`, hold на `talk_hold_frames`, пауза `talk_pause_symbols` после `talk_max_consecutive`; `update_talk_animation_state()` выставляет `talk_open_now` | OK (`Create_0.gml:31-91`; `Step_0.gml:124-149`) |
| 164 | `global.global_emote_system={active_emotes:[]}` в `obj_Init`; `emote_step()` в `obj_globalManager/Step_0`; `emote_draw_gui(camx,camy,scale,ox,oy)` в `Draw_64`; формула позиции | OK (`obj_Init/Create_0.gml:262`; `obj_globalManager/Step_0.gml:48`; `Draw_64.gml:160`; `scr_emote_system.gml:208-209`) |
| 167-176 | Таблица `emote_show(_target,_sprite,_duration,_offset_x,_offset_y,_scale)` | OK (`scr_emote_system.gml:24-65`: object index → `instance_find(t,0)`; строка с префиксом `spr_`; `EMOTE_MIN_DURATION_FRAMES=1`; дефолты 60/0/-24/1; scale ≥ 0.1) |
| 178 | `emote_step` декрементит `frames_left`, крутит `image_index`, удаляет по таймеру/гибели цели; `emote_hide_all_for`/`emote_hide_all` — пустые заглушки DELETE_CANDIDATE | OK (`scr_emote_system.gml:73-78, 149-176`) |
| 180 | `cutscene_runtime_show_emote` — общий вход для `c_emote`, `ActionEmote`, JSON `show_emote`/`emote`; fallback `default_emote_sprite` из settings (`"chara_question_o"`), затем жёсткий `chara_question_c` | OK с уточнением (`c_cmd.gml:250-253`; `scr_cutscene_classes.gml:3198`; `cutscene_action_factory.gml:906-918`; `cutscene_runtime_resolve_emote_sprite` 1219-1249 — жёсткие fallback'и `__CUTSCENE_EMOTE_FALLBACK_A="chara_question_o"` и `B="chara_question_c"`, строки 53-54; `cutscene_engine_settings.json:7`) |
| 184 | `seen_dialogues` на `par_interactable`; ключ `"<файл>:<нода>"` без дублей, `interaction_count++`, `__entity_state_save()` → `global.entity_state`; restore при спавне | OK (`interactionWithNPCsOrObjects.gml:94-110`; `par_interactable/Create_0.gml:29-74`; `scr_entity_state.gml`; сейв — `scr_saveSave.gml:100-104`) |
| 189 | Troubleshooting: `noone` при открытом окне; промахи файла/ноды — debug message без фатала | OK (`readDialogue.gml:10-24`; `Step_0.gml:171, 187`) |
| 192 | `>4` опций — первые 4, warning один раз | OK с нюансом (флаг сбрасывается при исчезновении опций — `Draw_64.gml:45-47`) |
| 195 | `ChatterboxLoadFromFile` только для незагруженных; повторная загрузка инвалидирует chatterbox'ы | OK (`Step_0.gml:156-169`) |
| 198 | `[[` — escape; `display_name` экранируется; пустая опция → `[[error]` | OK (`Draw_64.gml:66, 362`) |
| 202-208 | Ссылки «См. также» | OK — все файлы в `nav_plan.md` существуют |
| 210 | Sources comment | OK — перечисленные файлы/диапазоны соответствуют прочитанному |

## Итог
- **WRONG**: 3 (mermaid-стрелка `ActionDialogue→readDialogue`; цитата ноды `Bench`; формулировка про «битую» секцию сейва).
- **Уточнения**: reset-флаг warning'а опций; consume-once forced-эмоции; цепочка fallback-спрайтов эмоутов.
- Остальное подтверждено кодом.
