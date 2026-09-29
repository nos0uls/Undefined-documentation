# Review: docs_new/cutscenes/json-actions.md

Код: `Undefinedtale888` @ 7ee444a (read-only). Проверено по `scripts/cutscene_action_factory/cutscene_action_factory.gml` (1245 строк, прочитан целиком), `scripts/cutscene_load_json/cutscene_load_json.gml`, `scripts/scr_cutscene_classes/scr_cutscene_classes.gml`, `scripts/scr_cutscene_music/scr_cutscene_music.gml`, `scripts/scr_inputApi/scr_inputApi.gml`, `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml`, `objects/obj_cutsceneManager/Create_0.gml` + `Step_0.gml`, `datafiles/cutscenes/**/*.json`, `datafiles/cutscenes/cutscene_engine_settings.json`, `_meta/json_actions.txt`, `_meta/nav_plan.md`.

Легенда: OK — подтверждено; WRONG — не соответствует коду; UNVERIFIABLE — в коде не проверяемо; MISSING — есть в коде, нет на странице.

## Полнота покрытия

| Утверждение | Вердикт |
|-------------|---------|
| Все типы `###` страницы покрывают ключи фабрики | OK — фабрика регистрирует 82 ключа = 79 уникальных типов + 3 фабричных алиаса (`destroy_entity`, `destroy` → `actor_destroy`, фабрика:52-53; `emote` → `show_emote`, фабрика:918). Все 79 заголовков страницы соответствуют ключам; `###`-секций у алиасов нет и не нужно — они перечислены в таблице алиасов и в описаниях `actor_destroy` (стр. 427) / `show_emote` (стр. 490) |
| Список `_meta/json_actions.txt` совпадает с фабрикой | OK — эталонный список полон |

## Алиасы типов (стр. 60-75)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 62 | `type` приводится к нижнему регистру и прогоняется через нормализатор до фабрики | OK — load_json.gml:206, 223-225 (`string_lower` + `string_trim`) |
| 66-73 | Legacy-алиасы normalize: `shakeobj`, `visible`, `instant_mode`, `waittalk`/`wait_talk`, `depth`, `facing`, `autofacing`, `autowalk` | OK — load_json.gml:226-233, все 8 на месте |
| 74-75 | Фабричные алиасы `destroy_entity`/`destroy` → `actor_destroy`, `emote` → `show_emote` | OK — фабрика:52-53, 918; уровень «фабрика» указан верно — normalize их не трогает |
| — | Отсутствие `f["waittalk"]`/`f["instant_mode"]` | OK — комментарии фабрики:170-172, 988-989 подтверждают normalize-only уровень |

## Формат файла и общие правила (стр. 14-58)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 16-28 | Скелет: `schema_version`, `cutscene_id`, `settings`, `actions` обязателен | OK — load_json.gml:144-149 (не-массив `actions` → ошибка + destroy менеджера); `schema_version` реально присутствует в datafiles (cutscene.json) |
| 33 | `cutscene_id` пишется в `manager.cutscene_id` и `global.active_cutscene_id` | OK — load_json.gml:~126 (`_mgr.cutscene_id`), obj_cutsceneManager/Create_0.gml:643 |
| 34 | `schema_version` загрузчиком не читается | OK — в load_json.gml ключ не встречается |
| 35 | `settings.fps` валиден в `1..240`, иначе `default_fps` из engine-настроек | OK — load_json.gml:99-106 (диапазон + WARNING), 118-119 (`default_fps`); значение 60 в cutscene_engine_settings.json |
| 36, 39-40 | `settings.skippable` bool, default `true`, `false` запрещает пропуск по `back` | OK — load_json.gml:95, 108-111 (`get_bool(..., true)`), 132 (`_mgr.skippable`); Create_0.gml:34; Step_0.gml:6-7 |
| 42 | `start` (debug, только первым элементом) / `end` (останавливает разбор) — не действия фабрики | OK — load_json.gml:151-158, 174-175; в фабрике ключей нет |
| 48 | `target` приоритетнее `target_ref`; строка — ключ actor_map (регистрозависимо) / `"player"`/`"player_body"` (регистронезависимо) / имя object-ассета; число — instance id или object-индекс; `null` → `noone`; пустая строка/noone отклоняют | OK — load_json.gml:455-463 (`target` иначе `target_ref`, `undefined` → `noone`), Create_0.gml:501-541 (`resolve_target`), примеры отклонений — фабрика:15, 49, 370 |
| 49 | `seconds`/`duration`/`time` — синонимы в этом порядке; у `wait`/`spin`/`shake_object` явный `frames` приоритетнее | OK — `__cutscene_json_get_seconds`/`__cutscene_json_get_frames` в load_json.gml; фабрика:9, 960, 968 |
| 50 | Строки-числа парсятся, NaN/±infinity → дефолт; `0` как координата проверяется по наличию ключа у перечисленных типов | OK — get_real: load_json.gml:298-320; проверки ключей: move:19, set_position:371, jump:932, actor_create:36, spawn_entity:1058, camera_center:228, camera_pan:237, room_change:1205 |
| 51 | Булевы: `true`/`false`, `1`/`0`, строки `"true/false/yes/no/on/off/1/0"` | OK — `__cutscene_json_get_bool`, load_json.gml:~359-372 |
| 52 | Цвет: `c_*`-индекс, имя или hex `#RRGGBB`/`RRGGBB` | OK — `__cutscene_json_get_color`, load_json.gml |
| 53 | Направление (`set_facing`, `move_relative_direction`): имена/`r/l/u/d` или число `global.DIR.*` | **WRONG (частично)** — число работает только в `set_facing` (`__cutscene_json_parse_direction`, load_json.gml:241-263). У `move_relative_direction` `direction` читается через `get_string` (фабрика:394): real → `string(2)` = `"2"` → `__cutscene_normalize_direction` → WARNING + `DOWN` (classes:346-355). Исправлено: числовой вариант ограничен `set_facing` |
| 54 | Easing: `linear` (default), `ease_in`/`in`, `ease_out`/`out`, `ease_in_out`/`in_out`/`ease` | OK — `__cutscene_ease_by_name` в classes; нераспознанное → linear (fallthrough) |
| 55 | Свойства камеры: `x`/`y`/`view_x`/`view_y`/`camera_x`/`camera_y` | OK — `set_property`/`tween` kind-camera маппинг (фабрика:456-464, 523-558; ActionSetProperty/ActionTween в classes) |
| 56 | Dot-нотация: `flag.x`/`flags.x` → `global.flag[$ "x"]`, `stat.hp` → `global.stat_hp`, `entity_state.rm:eid[.field]`, `struct.field`, префикс `global.` срезается; без точки — `global.flag[key]` (branch_flag) / целая global (guard_global) | OK — `__cutscene_resolve_state_value`, classes:4067-4130; ActionBranchFlag чтение `global.flag` для простого ключа — classes:~4005-4008 |
| 58 | Невалидные обязательные поля → `noone` + лог `[CUTSCENE] FACTORY: action '<type>' rejected — …` | OK — формат подтверждён по всему файлу фабрики (15, 34, 49, 78, 99, ...) |

## Движение и анимация (стр. 77-406)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 79-89 | `move`: target обязателен; `x`,`y` обязательны по ключу; `speed_px_sec` default 60 с fallback на `speed`; `collision` false; → `ActionMove` | OK — фабрика:13-28 |
| 95-105 | `follow_path`: points непустой `{x,y}`/`[x,y]`; speed_px_sec 60; collision false; autofacing true | OK — фабрика:55-72 |
| 111-120 | `move_relative`: dx/dy default 0; speed_px_sec 60; collision false | OK — фабрика:378-387 |
| 128 | `move_relative_direction`: движение `speed * seconds` px | OK — classes:2337-2340 (`lengthdir_*(_dist)`, `_dist = move_speed * duration_frames`) |
| 133 | `direction` тип `string/real`, «как у set_facing» | **WRONG** — поле читается `get_string` (фабрика:394): JSON-число превращается в строку и деградирует в `DOWN` с warning. Исправлено на `string` с оговоркой |
| 142-156 | `move_direct`: `x`/`y` отсутствие → текущая координата; `value` 60; `use_speed` false → `value` в кадрах, переопределяется seconds/`frames`; при `use_speed:true` — px/кадр без конвертации | OK — фабрика:405-427 |
| 162-172 | `jump`: x/y по ключу; seconds 0.5; height 16; easing linear | OK — фабрика:929-940 |
| 178-185 | `set_position`: x/y по ключу; → `ActionSetXY` | OK — фабрика:368-375 |
| 191-198 | `set_position_relative`: dx/dy 0 | OK — фабрика:431-437 |
| 204-211 | `set_depth`: обязателен, `0` валиден, отсутствие/нечисло отклоняет | OK — фабрика:440-452 |
| 217-224 | `set_facing`: direction обязателен; «нераспознанное отклоняет действие» | OK с нюансом — отклоняются нераспознанные **строки** и отсутствие ключа (фабрика:486-489); число вне `0..3` проходит `parse_direction` и деградирует в `DOWN` + warning в `ActionSetFacing`→`__cutscene_normalize_direction` (classes:341-345, 2697). Формулировка уточнена |
| 230-237 | `auto_facing` → `ActionSetProperty(target,"auto_face",enabled)`, default true | OK — фабрика:466-471 |
| 243-250 | `auto_walk` → `ActionSetProperty(target,"auto_walk",enabled)`, default true | OK — фабрика:473-478 |
| 256-265 | `animate`: sprite опционален, неразрешённое имя → warning + пропуск; image_index/image_speed не задаются без ключей; `image_speed > 0` → `__cutscene_anim_override` | OK — фабрика:496-507 (`get_real_opt`); classes:2438-2456. Нюанс: `image_speed: 0` явно снимает override (`= (image_speed > 0)`) — на странице не уточнено, но не противоречит |
| 271-280 | `set_animation_frame`: image_index 0, image_speed 1, pause false | OK — фабрика:511-518 |
| 286-295 | `set_property`: kind `instance`/`camera` (camera без target); property обязателен; value default undefined | OK — фабрика:456-464 |
| 301-315 | `tween`: property/prop обязателен; to_value/end_value 0; приоритет `frames` → секунды → `duration_frames`; `duration_frames` = **секунды**; easing linear; from_value/start_value_override | OK — фабрика:523-558; особое утверждение `duration_frames`=секунды подтверждено комментарием фабрики:533-536 и кодом:544-547 |
| 321-331 | `lerp`: target `"camera"` (любой регистр) → камера; factor 0.1 кламп `0.001..1`; threshold 0.5 мин `0.01` | OK — фабрика:560-580 (`string_lower(_target)=="camera"`:578); клампы — ActionLerp, classes:3352+ |
| 337-346 | `spin`: speed 10 = итоговый угол, размазанный на длительность; frames 60 приоритетнее секунд | OK — фабрика:955-962; classes:3085-3088 (`spin_speed / duration_frames` за кадр) |
| 352-359 | `flip`: flipped true → отрицательный `image_xscale` | OK — фабрика:948-953; `cutscene_runtime_flip_x`, classes:1281-1287 |
| 365-371 | `halt` → `ActionHalt` / `cutscene_runtime_halt` | OK — фабрика:942-946; classes:1289-1299 |
| 377-389 | `shake_object`: frames 20, magnitude 4, mag_x/y = magnitude, decay false, frequency 1 | OK — фабрика:964-975 |
| 395-402 | `set_visible` → `ActionSetProperty(target,"visible",…)`, default true | OK — фабрика:977-982 |

## Актёры (стр. 408-519)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 410-419 | `actor_create`: key/actor_key/actor_name первое непустое; x/y по ключу; sprite_or_object/actor_sprite; имя sprite → `default_actor_object` со спрайтом; copy_from/copy_target | OK — фабрика:30-45; `default_actor_object`="obj_actor" в cutscene_engine_settings.json; копируемые поля — ActionActorCreate, classes:2109+ |
| 425-433 | `actor_destroy`: алиасы destroy_entity/destroy; снимает с actor_map/actor_specs; `obj_player` защищён | OK — фабрика:47-53; ActionDestroy, classes:4684+ (warning + пропуск для игрока) |
| 439-449 | `spawn_entity`: object/actor_sprite обязателен; x/y по ключу; key/actor_name; depth 0 с warning; у par_depth-наследников depth=-y; persistent false | OK — фабрика:1052-1075 |
| 455-468 | `attach_to_target`: parent/parent_ref обязателен; offsets 0; follow_* true; duration_seconds 0=телепорт; detach_on_cutscene_end true | OK — фабрика:1100-1118; семантика duration — ActionAttachToTarget, classes:3760+ |
| 474-482 | `detach`: destroy_after_detach false; `keep_world_position` игнорируется с warning | OK — фабрика:1120-1130 |
| 488-500 | `show_emote`: алиас emote; seconds 1; offset_y -24; scale 1; wait false; fallback `default_emote_sprite` → `chara_question_o`/`chara_question_c` | OK — фабрика:906-918; `cutscene_runtime_resolve_emote_sprite`, classes:1219-1250 |
| 506-515 | `set_emotion`: emotion `default`; apply_to_sprite/portrait true; портрет через consume-once `global.__actor_forced_emotion` | OK — фабрика:920-927; classes:3240-3243; потребитель — scr_parse_emote.gml:11 |

## Камера (стр. 521-634)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 523-531 | `camera_track`: seconds 0 → кламп до 1 кадра в классе; offsets 0; клампа к комнате нет | OK — фабрика:208-216; `max(1, round(frames))` в ActionCameraTrackBase, classes:~4505; комментарий «без клампа» classes:~4479-4482 |
| 537-544 | `camera_track_until_stop`: ждёт `move_active == false`, grace 2 кадра | OK — фабрика:218-224; ActionCameraTrackUntilStop |
| 550-556 | `camera_center`: x/y обязательны, координаты ЦЕНТРА view | OK — фабрика:226-232; classes:4300 (`center − half_w/h`) |
| 562-569 | `camera_pan`: x/y — позиция ЛЕВОГО ВЕРХНЕГО угла, seconds 1, ease_in_out внутри | OK — фабрика:234-243; ActionCameraPan(view_x,view_y) с `__CUTSCENE_EASE_IN_OUT`, classes:4374-4384 |
| 575-583 | `camera_pan_speed`: x/y — **скорость px/кадр**, хотя бы одно обязательно; `speed`/`speed_px_sec` игнорируются с warning; seconds 1 | OK — фабрика:245-262 (комментарий 246-247; reject 253-256; warning 248-252) — особое утверждение подтверждено |
| 589-596 | `camera_pan_obj`: seconds 1; единственный камерный экшен с клампом к комнате | OK — фабрика:264-270; кламп — ActionCameraPanToObj, classes:4399+ |
| 602-612 | `camera_shake`: seconds 1; magnitude 4; mag_x/y=magnitude; decay false; frequency 1 | OK — фабрика:617-626 |
| 618-630 | `tween_camera`: схема `tween` с kind=camera; `duration_frames` = секунды | OK — фабрика:582-615 (600-605) |

## Диалог (стр. 636-736)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 638-649 | `dialogue`: file обязателен с `.yarn`; node any default undefined; block_queue true; auto_advance false (перекрывается `manager.dialogue_auto_advance`); подмена файла на `dialogue_default_file`; таймаут `__CUTSCENE_DIALOGUE_WAIT_FRAMES` (~10 сек) | OK — фабрика:157-164; `__CUTSCENE_DIALOGUE_WAIT_FRAMES`=600 (classes:44); подмена файла — ActionDialogue, classes:~2570-2575 |
| 655-668 | `wait_for_dialogue`: алиасы waittalk/wait_talk; dialogue_controller опционален; stay_open-замечание | OK — фабрика:166-172 |
| 670-676 | `set_dialogue_speed`: speed 1.0, символы/сек, на менеджере | OK — фабрика:174-177 |
| 682-688 | `wait_typing` без полей | OK — фабрика:179-181 |
| 690-698 | `dialogue_control`: prevent_skip/stay_open/auto_advance default false | OK — фабрика:183-188 |
| 704-711 | `set_portrait_next`: emotion `neutral`; ключ нормализуется (lower+trim) | OK — фабрика:190-195; classes:2835 |
| 717-724 | `set_portrait_now`: emotion `neutral`; пишет current_emotion + ресурсы через `map_emotions` | OK — фабрика:197-202; ActionSetPortraitNow, classes:2847+ |
| 730-732 | `clear_dialogue` без полей | OK — фабрика:204-206 |

## Музыка и звук (стр. 738-934)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 740 | music-действия через `__cutscene_music_call`; отсутствующая функция — warning | OK — scr_cutscene_music.gml:11-21 |
| 742-750 | `play_sfx`: sound обязателен непустой; volume/pitch 1 | OK — фабрика:642-648 |
| 756-769 | `play_music`: sound/track (sound приоритетнее); fade 0.5, `0` = мгновенная смена; fade_in_seconds переопределяет; volume 1.0 применяется при `!=1 && >=0`; **persist_room_change default `true`**, `global.music_persist_track`/`noone` | OK — фабрика:655-680 (persist:670-677); ActionMusicPlay — scr_cutscene_music.gml:24-52 — особое утверждение подтверждено |
| 775-782 | `stop_music`: fade 1.0, fade_out_seconds переопределяет; `ActionMusicStop(fade,false)` | OK — фабрика:683-688 |
| 788-795 | `music_volume`: volume 1, fade 0.5 | OK — фабрика:691-696 |
| 801-808 | `music_duck`: multiplier 0.3, fade 0.3 | OK — фабрика:699-704 |
| 814-820 | `music_unduck`: fade 0.3 | OK — фабрика:707-711 |
| 826-832 | `music_pitch`: pitch 1.0 через `cutscene_music_pitch` | OK — фабрика:714-718 |
| 838-848 | `music_pause`/`music_resume` без полей | OK — фабрика:721-730 |
| 854-862 | `play_boss_music`: calm/calm_asset обязателен; battle/battle_asset опционален; fade 0.5 | OK — фабрика:733-758 |
| 868-874 | `stop_boss_music`: fade 1.0; `ActionMusicStop(fade,true)` → layered-путь с откатом | OK — фабрика:761-768 |
| 880-887 | `boss_music_phase`: phases [], struct-элементы {intro,calm,battle,intensity,fade}, не-struct пропускаются; fade 0.5 | OK — фабрика:771-829 |
| 893-901 | `play_music_intro`: intro/sound и loop/track обязательны; fade 0.5 | OK — фабрика:832-858 |
| 907-917 | `play_music_intro_layered`: intro и calm обязательны; battle опционален; fade 0.5; start_intensity 0 | OK — фабрика:861-895 |
| 923-930 | `crossfade_music`: intensity 0.5; fade 1.0 | OK — фабрика:898-903 |

## Управление потоком (стр. 936-1071)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 938-945 | `wait`: frames приоритетнее; секундные ключи; default 0 кадров | OK — фабрика:6-11 |
| 951-957 | `mark_node`: name default `""`; пишет в `manager.reached_nodes` | OK — фабрика:144-147; `mark_node_reached`/`reached_nodes` (лимит 50) — Create_0.gml:24-53 |
| 963-971 | `goto`: target обязателен непустой; поиск только в главной очереди; прыжок назад переигрывает диапазон; лимит обратных переходов 1024; самопрыжок no-op | OK — фабрика:149-155; ActionGoToNode, classes:~1790-1860 (лимит:1839-1842) |
| 977-985 | `parallel`: actions обязателен; элемент = action или массив (sequence); `__cutscene_parallel_splice`; `abort_parallel` обрывает ветки | OK — фабрика:272-296; classes:162-234 |
| 994-1004 | `branch`: condition по умолчанию `""`; строка → script-ассет; не-callable/не-bool → ветка false с warning; whitelist.branch_conditions advisory | OK — фабрика:298-333; ActionBranch, classes:3945+ |
| 1014-1023 | `branch_flag`: key обязателен; operator `==`, список `exists/!exists/==/!=/>/</>=/<=`; неизвестный → `==` с warning; value default `"true"` | OK — фабрика:335-366 — особое утверждение подтверждено |
| 1031-1040 | `run_function`: function/function_name/fn; script-ассет или callable из global; не-callable отклоняется; args array или `"a,b,c"`; менеджер дописывается в конец args; whitelist.run_functions advisory | OK — фабрика:74-142 (global callable:103-113; строка args:126-140); менеджер в args — classes:~2653-2658 |
| 1046-1055 | `schedule_action`: delay_seconds 0; blocking false → `manager.scheduled_actions`, true → дотикивает inner; tag `""`; action обязателен-struct, провал разбора отклоняет | OK — фабрика:1078-1098; ActionScheduleAction, classes:3614+ |
| 1061-1067 | `set_instant`: enabled true; алиас instant_mode | OK — фабрика:984-989 |

## Состояние и мир (стр. 1073-1174)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 1075-1082 | `set_flag`: key обязателен; value 0; пишет `global.flag[$ key]` | OK — фабрика:1040-1045; ActionSetFlag, classes:4608+ |
| 1088-1094 | `set_plot`: value 0; пишет `global.plot` | OK — фабрика:1047-1050 |
| 1100-1114 | `guard_global`: var `""`=всегда истинно; equals `""`; if_false `skip`/`wait_until_true` (неизвестное → skip+warning); stop_when `none`/`global_var`/`node_reached`/`timeout`; end_var/end_equals/end_node/end_timeout | OK — фабрика:1133-1157; `__cutscene_validate_mode` в ActionGuardGlobal, classes:4185+ |
| 1122-1123 | `set_global` отсутствует в фабрике | OK — ключа нет; MISSING-проверка пройдена |
| 1125-1137 | `checkpoint_state`: лимит 10 с LRU; include_* default true; include_globals/instances — массив или legacy-строка с JSON; пустой checkpoint_id → ERROR в start | OK — фабрика:1159-1181; `__CUTSCENE_MAX_CHECKPOINTS`=10 + LRU по timestamp, classes:4843-4874; разбор include_* — classes:843-884; валидация id — classes:4891-4894 |
| 1143-1153 | `restore_state`: cleanup_transients/restore_camera/restore_music true; on_missing `warn`, `fail` → ERROR; runtime-эффекты гасятся до отката | OK — фабрика:1183-1198; ActionRestoreState, classes:4936+ (`cutscene_runtime_cleanup_owner`) |
| 1159-1170 | `room_change`: room обязателен; player_x/player_y по ключу; actors `{key:{x,y}}` или `[x,y]`, битые записи с warning; same-room → no-op с WARNING | OK — фабрика:1200-1241; same-room — ActionRoomChange, classes:4716+ |

## Ввод (стр. 1176-1207)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 1178-1188 | `partial_control`: control_type default 0; `0`=LOCKED, `1`=WHITELIST, `2`=FREE; мусор → заблокировано+warning; whitelist — строки ключей; allowed_actions — массив или строка (`"move,interact"` / JSON-строка); группы `move`→up/down/left/right/run, `interact`→confirm; пустой → только confirm; `>0` возвращает `can_move`, `0` снимает | OK — фабрика:991-1026; enum — interactionWithNPCsOrObjects.gml:4-8; разбор строки — фабрика:1007-1018; группы и confirm-дефолт — scr_inputApi.gml:114-137; мусорный тип — scr_inputApi.gml:99-107; can_move — classes:4825-4838 — особое утверждение подтверждено |
| 1194-1203 | `wait_for_interact`: target обязателен; timeout секунды→кадры, `0`=бесконечно; timeout_action/interact_action `continue`, `abort_parallel` обрывает parallel; неизвестное → continue+warning | OK — фабрика:1028-1038; `__cutscene_validate_mode` в classes:4540-4544; abort — classes:4567-4569, 4584-4586 |

## UI и прочее (стр. 1209-1235)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 1211-1218 | `fade_in`: seconds 0.5; color c_black; alpha → 0 | OK — фабрика:628-633; ActionFadeIn = fade к 0 |
| 1224-1231 | `fade_out`: seconds 0.5; color c_black; alpha → 1 | OK — фабрика:635-640 |

## Примеры

| Утверждение | Вердикт |
|-------------|---------|
| Все примеры с титулом `datafiles/cutscenes/...` существуют и совпадают по типу и значениям полей | OK — 73 цитирования проверены программно (subset-матч каждого JSON-блока по дереву actions соответствующего файла); включая перекрёстные (`stop_music.json` для `play_music`, `play_boss_music.json` для `stop_boss_music`, `sequence.json` для `parallel`) |
| `lerp` (стр. 333), `goto` (стр. 973), `branch_flag` (стр. 1025) помечены как синтетические | OK — в datafiles этих типов нет (проверено по списку tests/ + cutscene*.json), пометка корректна |

## Ссылки и nav

| Утверждение | Вердикт |
|-------------|---------|
| Ссылки «См. также» (стр. 1239-1248) ведут на существующие страницы nav-плана | OK — все 10 файлов существуют на диске и в `_meta/nav_plan.md` |

## Итог

- **WRONG**: 2 (обе — семантика `direction`): стр. 53 и стр. 133. Уточнение-нюанс: стр. 224.
- **UNVERIFIABLE**: 0.
- **MISSING**: 0 — покрытие полное.
- Правки на странице: строки 53, 133, 224 (уточнение границ принимаемых значений `direction`; структура не изменена).
