# Ревью: cutscenes/action-classes.md

Код: ревизия 7ee444a ($P, read-only). Проверены `scripts/scr_cutscene_classes/scr_cutscene_classes.gml` (5035 строк, прочитан целиком), `scripts/scr_cutscene_music/scr_cutscene_music.gml` (283 строки, целиком) + вызовы из `obj_cutsceneManager`, `obj_globalManager`, `scr_inputApi`, `interactionWithNPCsOrObjects`, `scr_music_init`, `scr_global_on_room_change`, `scr_entity_state`, `cutscene_action_factory`.

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 12 | Struct-классы по паттерну Command, наследники `CutsceneAction`; классы в scr_cutscene_classes.gml, `ActionMusic*` — в scr_cutscene_music.gml; фабрика через `new Action*(...)` | OK (68 классов в scr_cutscene_classes.gml + 13 в scr_cutscene_music.gml; 77 вызовов `new Action*` в cutscene_action_factory.gml; JSON в datafiles/cutscenes/*.json) |
| 16-26 | Контракт `CutsceneAction` (64-70): `started`, `action_type`, `start`, `update`, `cleanup` | OK (scr_cutscene_classes.gml:64-70) |
| 30 | `started` ставится диспетчером/контейнерами; `ActionGoToNode` и контейнеры сбрасывают | OK (obj_cutsceneManager/Create_0.gml:83-84,195-196; classes:1853,1893,3528,3658) |
| 33 | `update` → `bool`; отдельного `is_done` нет | OK (grep `is_done` по scr_cutscene_classes/factory/manager — пусто) |
| 34 | `cleanup` один раз после завершения/прерывания; гасить записи | OK (Create_0.gml:94-99,223-226 — флаг `__cleanup_done`) |
| 35 | `reset(manager)` — опциональный, вызывается `ActionGoToNode` при обратном переходе поверх `started`/`timer`/`elapsed` | OK, неполно: сбрасываются ещё и `__cleanup_done` (classes:1853-1858) — дополнить строку |
| 39 | Резолв целей через `__cutscene_resolve_target` (ключ `actor_map`, `"player"`, instance id, object index) | OK, неполно: resolve_target принимает также алиас `"player_body"` и имя object-ассета строкой (Create_0.gml:519-532) — дополнить |
| 40 | При `instant_mode` — немедленное завершение | OK (паттерн `__cutscene_is_instant` по всему файлу) |
| 41 | Нерезолвленная цель → warning через `__cutscene_warn_unresolved` + пропуск | OK с оговоркой: большинство классов используют хелпер; `ActionFollowPath` (classes:2024) и `ActionSpawnEntity` (classes:4674) пишут собственное «ОШИБКА»-сообщение — поведение то же |
| 42 | Мгновенные — `true` из первого `update` | OK |
| 46 | Единицы — кадры и px/кадр; секунды конвертирует фабрика; исключения — `ActionScheduleAction`, `ActionAttachToTarget`, музыкальные `fade` | OK (factory: `__cutscene_json_seconds_to_frames`, `_speed_sec / max(1,_fps)`; classes:3614,3760; music-файл — `_fade_sec`) |
| 50 | `ActionWait(frames)` — `"Wait"`, `timer++`, done по frames | OK (classes:1753-1764) |
| 51 | `ActionMarkNode(_name)` — `"MarkNode"`, мгновенное | OK (classes:1770-1788) |
| 52 | `ActionGoToNode(_target_name)` — `"GoToNode"`, мгновенное | OK (classes:1802-1870) |
| 53 | `ActionSequence` — по одному за кадр; instant — цепочка с лимитом 1024; `cleanup` текущего | OK (classes:1875-1986; `__CUTSCENE_INSTANT_GUARD_LIMIT` @36) |
| 54 | `ActionFollowPath(target_ref, points_array, speed, _use_collision, auto_facing)` — шаги через `__cutscene_move_step`; cleanup = move_cleanup + возврат `auto_face` | OK (classes:1988-2107) |
| 55 | `ActionActorCreate(name, x, y, sprite_or_obj)` — `"ActorCreate"`, мгновенное | OK (classes:2109-2204) |
| 56-58 | `ActionMoveBase`/`ActionMove`/`ActionMoveRelative` — ждут `move_active==false` при наличии `move_to_point`, иначе `__cutscene_move_step`; cleanup = move_cleanup | OK (classes:2211-2304,2306-2316,2969-2979) |
| 59 | `ActionMoveRelativeDirection` — цель = `speed*frames` по направлению | OK (classes:2318-2385, `_dist = move_speed * duration_frames` @2338) |
| 60 | `ActionMoveDirect` — делегирует внутреннему `ActionMove` | OK (classes:2387-2426) |
| 61-62 | `ActionAnimate`, `ActionSetAnimationFrame` — мгновенные | OK (classes:2428-2502) |
| 63 | `ActionDialogue(_dialogue_file, _node_title, _block_queue, _auto_advance)` — ждёт `ChatterboxIsStopped`, таймаут 600; cleanup по `block_queue`/`stay_open` | OK (classes:2505-2632; `__CUTSCENE_DIALOGUE_WAIT_FRAMES=600` @44) |
| 64-79 | `RunFunction`, `SetFacing`, `WaitForDialogue`, `SetDialogueSpeed`, `WaitTyping`, `DialogueControl`, `SetPortraitNext/Now`, `ClearDialogue`, `SetProperty`, `SetDepth`, `SetXY`, `SetPositionRelative`, `SetInstantMode`, `Halt`, `Flip` | OK (classes:2644-3070; `WaitTyping` ждёт `typist.get_state()==1` @2777) |
| 80 | `ActionSpin` — ждёт конца runtime-spin, гасит `started_spin.active` | OK (classes:3072-3097) |
| 81-82 | `ActionShakeBase`, `ActionShakeObject` — ждут `shake_ref.active==false`, гасят `active`; сигнатуры | OK, косметика: в коде параметры `_magnitude_x, _magnitude_y`, в таблице `_mx, _my` (classes:3107,3137) |
| 83 | `ActionCameraShake` — cleanup только снимает `active`, откат оффсета делает агрегатный тикер | OK, косметика по `_mx/_my` (classes:3422-3445; агрегатный тикер classes:1613-1721) |
| 84-86 | `ActionPlaySFX`, `ActionEmote` (wait_for_finish → ждёт `started_emote.active`), `ActionSetEmotion` | OK (classes:3155-3261) |
| 87-89 | `ActionFadeTo/FadeIn/FadeOut` — singleton-fade по поколению `seq`; FadeIn=`FadeTo(0)`, FadeOut=`FadeTo(1)`; cleanup гасит свой fade + `alpha=0` | OK (classes:3263-3317,1156-1210) |
| 90-92 | `ActionTween`, `ActionLerp`, `ActionJump` — ждут `*_ref.active`, гасят `active` (у Lerp cleanup пустой) | OK (classes:3319-3420) |
| 93-94 | `ActionGroup` → `ActionParallel`; `ActionParallel` — все `sub_done` или `__abort_requested`; идемпотентный cleanup | OK (classes:3454-3603) |
| 95 | `ActionScheduleAction(delay_seconds, inner_action, blocking, tag)` — delay в кадрах по `game_get_speed`, blocking тикает `inner.update`; `inner.cleanup` только в blocking | OK (classes:3614-3699) |
| 96 | `ActionAttachToTarget` — при `duration>0` твин позиции, иначе мгновенное; cleanup снимает `tweening` | OK, косметика: параметры в коде `_offset_x, _offset_y` (classes:3760-3915) |
| 97-99 | `ActionDetach`, `ActionBranch`, `ActionBranchFlag` — мгновенные | OK (classes:3921-4056) |
| 100 | `ActionGuardGlobal` — `skip` сразу; `wait_until_true` ждёт условие/end-condition | OK (classes:4185-4298) |
| 101-107 | `CameraCenter`, `CameraPanBase/Pan/PanSpeed/PanToObj`, `CameraTrackBase/Track` — твины камеры, `ease_in_out`/`linear`, кламп у PanToObj; Track: `timer>=frames` | OK (classes:4300-4511) |
| 108 | `ActionCameraTrackUntilStop` — `!actor.move_active` (grace 2 кадра) | WRONG (мелочь): код `if (timer < 2) return false` — grace только на первом тике update, комментарий в коде — «1-frame grace period» (classes:4517-4522) |
| 109 | `ActionWaitForInteract` — `resolved_target` в `global.__interacted_targets` или таймаут; cleanup чистит свою цель и мёртвые id | OK (classes:4536-4604) |
| 110-113 | `SetFlag`, `SetPlot`, `SpawnEntity`, `Destroy` — мгновенные | OK (classes:4608-4710; `SpawnEntity` пишет `persistent` и spec @4661-4672; `Destroy` защищает obj_player @4696) |
| 114 | `ActionRoomChange` — ждёт уничтожения `obj_changingRoomsController` | OK (classes:4716-4805) |
| 115 | `ActionPartialControl(_control_type, whitelist_array, allowed_actions_array)` — мгновенное | OK (classes:4813-4841) |
| 116-117 | `ActionCheckpointState`, `ActionRestoreState` — мгновенные | OK (classes:4880-4930,4936-5018) |
| 121 | `__cutscene_music_call` — `method_call`/`script_execute_ext`, warning при отсутствии; `update`=true, `cleanup` не определён; фейды идут в `obj_music_ctrl` | OK (music:11-25; obj_music_ctrl/Step_0.gml:1-5) |
| 121 | — | MISSING (мелочь): в scr_cutscene_music.gml есть shorthand-обёртки `cutscene_music_pitch/pause/resume` (music:167-184), вызываемые билдером/фабрикой — на странице не упомянуты |
| 125 | `ActionMusicPlay(snd, fade, volume=1.0, persist=true)` — `play_music_immediate` при `fade<=0`, `play_music_fade`; `volume>=0 && !=1` → `set_music_volume_fade(v,0)`; пишет `global.music_persist_track` | OK (music:31-58) |
| 126-137 | `MusicStop/Volume/Pitch/Pause/Resume/IntroLoop/Duck/Unduck/PlayLayered/SetIntensity/IntroLayered/PhaseSequence` — вызовы `global.*` | OK (music:60-283; фазы — struct `{intro, calm, battle, intensity, fade}` @JSDoc) |
| 143-159 | `__cutscene_resolve_state_value`: строка+непусто, срез `global.`, без точки — `global.<name>`; `flag./flags.`, `entity./entity_state.`, `entity_state.room:eid.field` по последней точке, `stat./stats.` → `global.stat_<name>`, `<struct>.<field>`; `undefined` без исключений | OK (classes:4067-4127; диапазон в тексте точный) |
| 163-174 | `__cutscene_compare_values`: typeof+==, bool↔string «true/false/1/0», real↔string через `real(string_trim)`+try/catch, bool↔real через `!=0`, иначе `false` | OK (classes:4131-4174) |
| 180-181 | `__cutscene_resolve_target` / `__cutscene_resolve_targets` — семантика | OK (classes:86-96,236-292; без резолвера — только живой instance id @89) |
| 182-184 | `__cutscene_warn_unresolved`, `__cutscene_validate_mode`, `__cutscene_is_instant` | OK (classes:107-130,122-130,312-319) |
| 185 | `__cutscene_normalize_direction` — `l/r/u/d`, `left/right/up/down`, целое 0..3 → `global.DIR.*`; мусор → `DIR.DOWN` + warning | WRONG (мелочь): warning есть только для real вне 0..3 и нераспознанных строк; нестроковое/нечисловое значение → `DIR.DOWN` молча (classes:341-355) |
| 186 | `__cutscene_actor_apply_facing` — `facing_direction` если поле есть; спрайт из `chara_idle_sprites`/`chara_sprites`; `obj_player` → `scr_sprite_for_facing` | OK (classes:378-408; приоритет `chara_idle_sprites` @388) |
| 187 | `__cutscene_move_step` — snap без телепорта сквозь стену, `move_and_collide` по `[obj_collider, par_decor, par_interactable]`, stall 60 кадров | OK (classes:421-498; `__CUTSCENE_MOVE_STALL_LIMIT=60` @40) |
| 188 | `__cutscene_move_cleanup` — сброс `move_active`, `move_blocked`, `__cutscene_move_stall`, `__cutscene_anim_override`, `speed` | OK, неполно: при `auto_face` также `image_speed=0`, `image_index=0` (classes:503-522) |
| 189-194 | `__cutscene_sync_move_target`, `find_active_textbox` (приоритеты), `find_dialogue_ctrl`, `dialogue_is_active` (пустой chatterbox = «стартует»), `normalize_yarn_path`, `ease_value` (список алиасов) | OK (classes:529-677) |
| 195 | `__cutscene_runtime_get/set_value` — `"camera"`: `view_camera[0]` + `global.camera_x/y`, свойства x/y/view_x/view_y/camera_x/camera_y; instance/object — `variable_instance_*`; depth → `depth_mode="manual"` | OK с оговоркой: `global.camera_x/y` пишет только set (classes:714-715); get читает только `camera_get_view_*` (683-684) |
| 196 | `__cutscene_parallel_push/pop/splice/request_abort` — стек `__parallel_stack`; `insert_actions` из ветки → в ветку; `request_abort` → `__abort_requested` | OK (classes:143-234; Create_0.gml:545-558) |
| 197 | `cutscene_runtime_tween_to/fade_to/shake_object/shake_camera/spin_object/jump_to` — массивы `obj_globalManager`, `owner_id` | OK (classes:1119-1407 — все записи несут `owner_id`) |
| 198 | `cutscene_runtime_show_emote/play_sfx/set_visible/flip_x/halt` — обёртки | OK (classes:1265-1299) |
| 199 | `cutscene_runtime_step()` — из Step `obj_globalManager`, удаляет неактивные записи | OK (obj_globalManager/Step_0.gml:49; classes:1522-1527 и далее) |
| 200 | `cutscene_runtime_cleanup_owner` — деактивация по `owner_id` + singleton-fade с `alpha=0` | OK (classes:1448-1484; `alpha=0` только у активного fade @1482) |
| 201 | `__cutscene_runtime_rollback_owner_shakes` — синхронный откат `applied_x/y` | OK (classes:1493-1516) |
| 202 | `__cutscene_snapshot_instance/create_snapshot/apply_instance_snapshot` — поля снимка | OK (classes:737-909,950-987) |
| 203 | `__cutscene_cleanup_transients` — уничтожает актёров вне snapshot (кроме obj_player), чистит `actor_specs` | OK (classes:916-939) |
| 204 | `__cutscene_restore_*` — покатегорийный restore; смена типа глобала → warning+пропуск | OK (classes:993-1117) |
| 205-206 | `__cutscene_update_attachments` (позиция, xscale/yscale, depth; мёртвые → удаление); `__cutscene_attachments_remove_by_target` (+ `attached_target=noone`) | OK (classes:3703-3747,538-561; вызов из obj_cutsceneManager/Step_0.gml:20) |
| 207 | `__cutscene_cleanup_old_checkpoints` — LRU при `__CUTSCENE_MAX_CHECKPOINTS=10` по `timestamp_frames` | OK (classes:4844-4874; вытеснение при size>=10 @4851) |
| 209-210 | `__cutscene_room_entry_spawn`/`scr_room_entry_check` — заглушки DELETE_CANDIDATE; записей в `global.room_flags` никто не создаёт; комнатные флаги — `scr_world_flag_set/get` (`entity_state`, `"_room"`) | OK (classes:5020-5035; `global.room_flags` — только `={}` в obj_Init/Create_0:29, scr_defaultLoad:31, scr_saveLoad:326; scr_entity_state.gml:72-97) |
| 216-228 | `ActionDialogue` детали: reuse/создание окна, перекрытия с менеджера, валидация файла, `chatterbox=""`, try/catch; update и cleanup-семантика | OK (classes:2513-2631; `scr_layer_ensure_instances` @2534) |
| 232-233 | `ActionMarkNode`: `mark_node_reached`, `reached_nodes_limit=50`, повтор подряд игнорируется; `ActionGoToNode`: основная очередь, самопрыжок-warning, лимит 1024, диапазон `[метка..текущий]`, индекс `метка-1` | OK (Create_0.gml:24,36-56; classes:1774-1869; комментарий «лимит 2» @1775 — устаревший комментарий в коде, факт = 50) |
| 237-249 | `ActionBranchFlag`: `insert_actions(current+1)`; ключ без точки → `global.flag`, с точкой → resolver; нормализация `expected`; таблица операторов (exists/!exists/==/!=/>/<>=<=/default→==) | OK (classes:3988-4056) |
| 253-257 | `ActionGuardGlobal`: валидация `if_false`/`stop_when` с fallback, пустой ключ → вставка безусловно; wait_until_true + end-conditions; `__actions_inserted` | OK (classes:4185-4298; `end_timeout_frames` — кадры @4201) |
| 261 | `ActionLerp`: factor ∈ [0.001,1] (нечисловой → 0.1), threshold ≥ 0.01 (нечисловой → 0.5); `target_kind="camera"` без резолва; instant — запись в start | OK (classes:3352-3394) |
| 265-273 | `ActionPartialControl`: поля менеджера, `can_move` (0→false, >0→true); enum `INTERACT_PARTIAL_CONTROL` (0/1/2 LOCKED/WHITELIST/FREE); whitelist через `resolve_target` в `scr_interaction`; фильтр `scr_input__partial_control_allows`, алиасы `move`/`interact`, пустой = только `confirm`; мусорный тип → 1 warning + заблокировано | OK (classes:4813-4841; interactionWithNPCsOrObjects.gml:4-8,46-69; scr_inputApi.gml:92-137) |
| 277-286 | `ActionRoomChange` детали: нормализация комнаты, `__room_change_*` поля, reuse/создание контроллера на `__CUTSCENE_TRANSITION_DEPTH=-100000`, `__player_pos_by_manager`; update — сброс при потере перехода; пересоздание актёров в Room Start по `actor_specs`, persistent переживают | OK (classes:4716-4805; macro @62; scr_room_fade_update.gml:50-56; Other_4.gml:95-161) |
| 290-292 | `ActionMusicPlay` пишет `music_persist_track`; `scr_global_on_room_change` читает пометку; `duck_music` в `ActionMusicDuck` и `__cutscene_restore_music_state`; API — `global.duck_music` из scr_music_init, `set_music_duck` нет | OK (music:51; scr_global_on_room_change.gml:39-45 — есть доп. гарды `cutscene_active`/`==music_current`/`audio_is_playing`; classes:1059; scr_music_init.gml:563-618; `set_music_duck` отсутствует) |
| 296-299 | Контейнеры: Sequence (1/кадр, instant-бюджет 1024, сброс `started`, cleanup текущего), Parallel (`sub_done`/`sub_cleaned`/`__active_branch`/`__abort_requested`/`__cleaned`), Group (`method(context,fn)`, warning+no-op), ScheduleAction (fps-конвертация, `scheduled_actions`, tag не хранится) | OK (classes:1875-1986,3496-3603,3454-3494,3614-3699; Step-тик scheduled — Create_0.gml:118-152, чистка finish @823-836) |
| 303 | `ActionAttachToTarget`/`ActionDetach`: запись в `global.__cutscene_attachments`, твин/телепорт, `follow_depth` через `attached_target` у par_depth, `detach_on_cutscene_end` → finish_cutscene, destroy по флагу | OK (classes:3760-3943; Create_0.gml:842-861,900) |
| 307-308 | `ActionCheckpointState`: `timestamp_frames=max+1`, LRU 10; `_config` поля и legacy-JSON-строки; instances — первый инстанс; `variable_clone` глобалов. `ActionRestoreState`: дефолты опций, `on_missing` warn/fail без прерывания, порядок секций | OK (classes:4880-4930,4936-5018,775-909) |
| 312-321 | Ссылки `См. также` — overview/architecture/json-actions/partial-control/actors-and-camera/gml-dsl в cutscenes/; dialogue/music/room-transitions/input в systems/ | OK — все файлы существуют в docs_new и в `_meta/nav_plan.md` |
| 323 | sources-комментарий | OK — все перечисленные файлы читались, диапазоны соответствуют |

## Итог
- WRONG (мелочь): 2 — grace `ActionCameraTrackUntilStop` (стр. 108: фактически 1 кадр, `timer < 2`); `__cutscene_normalize_direction` (стр. 185: нестроковый/нечисловой мусор → `DIR.DOWN` без warning).
- Неполнота (мелочь): `reset`-строка — добавить `__cleanup_done`; резолвер — алиас `"player_body"` и имя object-ассета; `__cutscene_move_cleanup` — idle-кадр при `auto_face`; `__cutscene_runtime_get_value` для камеры не читает `global.camera_x/y` (их пишет только set).
- Косметика сигнатур: `_mx/_my` → `_magnitude_x/_magnitude_y` (ShakeBase/ShakeObject/CameraShake), `_ox/_oy` → `_offset_x/_offset_y` (AttachToTarget).
- MISSING (мелочь): shorthand-обёртки `cutscene_music_pitch/pause/resume` в scr_cutscene_music.gml.
- Оговорка: `__cutscene_warn_unresolved` используется не всеми классами (`ActionFollowPath`, `ActionSpawnEntity` — собственные «ОШИБКА»-сообщения).
- UNVERIFIABLE: нет.
