---
title: Классы действий катсцен (Action*)
tags:
  - cutscenes
  - cutscene-api
  - reference
  - gml
---

# Классы действий катсцен (Action*)

Все действия катсцены — struct-классы по паттерну Command, наследники `CutsceneAction`. Большинство классов объявлено в `scripts/scr_cutscene_classes/scr_cutscene_classes.gml`; музыкальные действия (`ActionMusic*`) живут в `scripts/scr_cutscene_music/scr_cutscene_music.gml`. JSON-экшены из `datafiles/cutscenes/*.json` фабрика `cutscene_action_factory` конструирует через `new Action*(...)` — соответствие типов см. в [JSON-экшенах](json-actions.md).

## Контракт `CutsceneAction`

Базовый конструктор (`scr_cutscene_classes.gml:64-70`):

```gml title="scripts/scr_cutscene_classes/scr_cutscene_classes.gml" linenums="64"
function CutsceneAction() constructor {
    started = false;
    action_type = "Base";
    start = function(manager) {};
    update = function(manager) { return true; };
    cleanup = function(manager) {};
}
```

| Член | Тип | Назначение |
|------|-----|------------|
| `started` | `bool` | Флаг «start уже вызван». Ставится диспетчером/контейнерами перед первым `start`; `ActionGoToNode` и контейнеры сбрасывают его для переигровки. |
| `action_type` | `string` | Читаемое имя действия для логов и поиска меток (`"MarkNode"`, `"Dialogue"` и т.д.). |
| `start(manager)` | `function` | Одноразовая инициализация: резолв целей, запись состояния на менеджер/инстансы, запуск runtime-эффектов. |
| `update(manager)` | `function` → `bool` | Вызывается каждый кадр; `true` — действие завершено. Отдельного метода `is_done` нет: готовность — это возвращаемое значение `update`. |
| `cleanup(manager)` | `function` | Вызывается один раз после завершения или при прерывании. Действия с runtime-эффектами обязаны гасить свои записи (`tween_ref.active = false` и т.п.). |
| `reset(manager)` | `function` (опционально) | Точка расширения: вызывается `ActionGoToNode` при обратном переходе поверх сброса `started`/`__cleanup_done`/`timer`/`elapsed`, если метод реализован. |

Правила, которые выдерживают все наследники:

- `manager` — инстанс `obj_cutsceneManager`; цели резолвятся через `__cutscene_resolve_target(manager, target)` (`"player"`/`"player_body"`, строка-ключ `actor_map`, имя object-ассета, instance id, object index).
- При `manager.instant_mode == true` (`__cutscene_is_instant`) действия обязаны завершаться немедленно: движение — телепортом, эффекты — без регистрации записи, ожидания — `return true`.
- Нерезолвленная цель в `start` — warning и пропуск, а не runtime-ошибка. Большинство классов используют `__cutscene_warn_unresolved`; `ActionFollowPath` и `ActionSpawnEntity` пишут собственное сообщение.
- Мгновенные действия возвращают `true` из первого же `update`; блокирующие тикают до условия.

## Сводная таблица классов

Единицы: конструкторы принимают **кадры** и **px/кадр** (секунды/px-в-секунду конвертирует JSON-фабрика; исключения — `ActionScheduleAction`, `ActionAttachToTarget`, музыкальные `fade` — в секундах).

| Класс (сигнатура конструктора) | `action_type` | `update` | `cleanup` |
|-------------------------------|---------------|----------|-----------|
| `ActionWait(frames)` | `"Wait"` | `timer++`, done по `frames` | — |
| `ActionMarkNode(_name)` | `"MarkNode"` | мгновенное | — |
| `ActionGoToNode(_target_name)` | `"GoToNode"` | мгновенное | — |
| `ActionSequence(actions_array)` | `"Sequence"` | тикает под-действия по очереди (по одному за кадр; в instant — цепочкой с лимитом 1024/кадр) | `cleanup` текущего под-действия |
| `ActionFollowPath(target_ref, points_array, speed, _use_collision, auto_facing)` | `"FollowPath"` | шаги к точкам пути через `__cutscene_move_step` | `__cutscene_move_cleanup` + возврат `auto_face` |
| `ActionActorCreate(name, x, y, sprite_or_obj)` | `"ActorCreate"` | мгновенное | — |
| `ActionMoveBase(_target, _speed, _use_collision)` | `"MoveBase"` | ждёт `move_active==false` у актёра с `move_to_point`, иначе шагает сам | `__cutscene_move_cleanup` |
| `ActionMove(target_ref, _target_x, _target_y, speed, use_collision)` | `"Move"` | как у базы, цель — абсолютные координаты | как у базы |
| `ActionMoveRelative(_target, _dx, _dy, _speed_pf, _use_collision)` | `"MoveRelative"` | как у базы, цель — позиция в `start` + offset | как у базы |
| `ActionMoveRelativeDirection(target_ref, direction_ref, speed, frames, _use_collision)` | `"MoveRelativeDirection"` | то же, цель = `speed*frames` по направлению | `__cutscene_move_cleanup` |
| `ActionMoveDirect(target_ref, _x, _y, frames_or_speed, use_speed, _use_collision)` | `"MoveDirect"` | делегирует внутреннему `ActionMove` | `cleanup` внутреннего |
| `ActionAnimate(target_ref, _sprite, image_index_set, image_speed_set)` | `"Animate"` | мгновенное | — |
| `ActionSetAnimationFrame(target_ref, _image_index, _image_speed, _pause)` | `"SetAnimationFrame"` | мгновенное | — |
| `ActionDialogue(_dialogue_file, _node_title, _block_queue, _auto_advance)` | `"Dialogue"` | ждёт `ChatterboxIsStopped` (таймаут 600 кадров на появление chatterbox) | уничтожает `dialogue_controller`, если `block_queue` и не `stay_open` |
| `ActionRunFunction(_func_ref, arg_array)` | `"RunFunction"` | мгновенное | — |
| `ActionSetFacing(target_ref, direction)` | `"SetFacing"` | мгновенное | — |
| `ActionWaitForDialogue(dialogue_controller_ref)` | `"WaitForDialogue"` | ждёт стоп chatterbox контроллера (таймаут 600 на появление) | — |
| `ActionSetDialogueSpeed(speed)` | `"SetDialogueSpeed"` | мгновенное | — |
| `ActionWaitTyping()` | `"WaitTyping"` | ждёт `typist.get_state() == 1` | — |
| `ActionDialogueControl(prevent_skip, stay_open, auto_advance)` | `"DialogueControl"` | мгновенное | — |
| `ActionSetPortraitNext(target, emotion)` | `"SetPortraitNext"` | мгновенное | — |
| `ActionSetPortraitNow(target, emotion)` | `"SetPortraitNow"` | мгновенное | — |
| `ActionClearDialogue()` | `"ClearDialogue"` | мгновенное | — |
| `ActionSetProperty(target_ref, _property_name, value, _target_kind)` | `"SetProperty"` | мгновенное | — |
| `ActionSetDepth(target_ref, depth_value)` | `"SetDepth"` | мгновенное | — |
| `ActionSetXY(target_ref, _x, _y)` | `"SetXY"` | мгновенное | — |
| `ActionSetPositionRelative(_target, _dx, _dy)` | `"SetPositionRelative"` | мгновенное | — |
| `ActionSetInstantMode(enabled)` | `"SetInstantMode"` | мгновенное | — |
| `ActionHalt(target_ref)` | `"Halt"` | мгновенное | — |
| `ActionFlip(target_ref, flipped)` | `"Flip"` | мгновенное | — |
| `ActionSpin(target_ref, speed, frames)` | `"Spin"` | ждёт конца runtime-spin | гасит `started_spin.active` |
| `ActionShakeBase(_frames, _magnitude, _magnitude_x, _magnitude_y, _decay, _frequency)` | `"ShakeBase"` | ждёт `shake_ref.active == false` | гасит `shake_ref.active` |
| `ActionShakeObject(target_ref, frames, _magnitude, _magnitude_x, _magnitude_y, _decay, _frequency)` | `"ShakeObject"` | как у базы | как у базы |
| `ActionCameraShake(frames, _magnitude, _magnitude_x, _magnitude_y, _decay, _frequency)` | `"CameraShake"` | как у базы | снимает `active` (откат оффсета делает агрегатный тикер) |
| `ActionPlaySFX(_sound_or_key, _volume, _pitch)` | `"PlaySFX"` | мгновенное | — |
| `ActionEmote(target_ref, _sprite, _duration, _ox, _oy, _scale, _wait_for_finish)` | `"Emote"` | мгновенное; при `wait_for_finish` ждёт `started_emote.active == false` | — |
| `ActionSetEmotion(target_ref, emotion, apply_to_sprite, apply_to_portrait)` | `"SetEmotion"` | мгновенное | — |
| `ActionFadeTo(target_alpha, frames, color)` | `"FadeTo"` | ждёт конца singleton-fade своего поколения `seq` | гасит свой активный fade и сбрасывает `alpha = 0` |
| `ActionFadeIn(frames, color)` | `"FadeIn"` | `ActionFadeTo(0, …)` | как у базы |
| `ActionFadeOut(frames, color)` | `"FadeOut"` | `ActionFadeTo(1, …)` | как у базы |
| `ActionTween(target_ref, _property_name, to_value, frames, easing, from_value, _target_kind)` | `"Tween"` | ждёт `tween_ref.active == false` | гасит `tween_ref.active` |
| `ActionLerp(target_ref, _property_name, to_value, factor, threshold, _target_kind)` | `"Lerp"` | покадровый `lerp` до `threshold`, затем точная запись | — |
| `ActionJump(target_ref, _x, _y, frames, height, easing)` | `"Jump"` | ждёт `jump_ref.active == false` | гасит `jump_ref.active` |
| `ActionGroup(_targets, _context, _generator_fn)` | `"Group"` | делегирует собранному `ActionParallel` | `cleanup` параллели |
| `ActionParallel(actions_array)` | `"Parallel"` | тикает все ветки; done, когда все `sub_done` или `__abort_requested` | `cleanup` незавершённых веток (идемпотентно) |
| `ActionScheduleAction(delay_seconds, inner_action, blocking, tag)` | `"ScheduleAction"` | ждёт delay (кадры = `delay_seconds * fps`), запускает `inner`; blocking — тикает `inner.update` | `inner.cleanup` только в blocking-режиме |
| `ActionAttachToTarget(target_ref, parent_ref, _offset_x, _offset_y, follow_facing, follow_scale, follow_depth, duration_seconds, detach_on_cutscene_end)` | `"AttachToTarget"` | при `duration > 0` — твин позиции к родителю; иначе мгновенное | снимает флаг `tweening` при прерывании твина |
| `ActionDetach(target_ref, destroy_after_detach)` | `"Detach"` | мгновенное | — |
| `ActionBranch(condition_func, true_actions, false_actions)` | `"Branch"` | мгновенное | — |
| `ActionBranchFlag(flag_key, operator, expected_val, true_actions, false_actions)` | `"BranchFlag"` | мгновенное | — |
| `ActionGuardGlobal(var_name, equals_value, inner_actions, _if_false, _stop_when, _end_var, _end_equals, _end_node, _end_timeout_frames)` | `"GuardGlobal"` | `skip` — сразу; `wait_until_true` — ждёт условие или end-condition | — |
| `ActionCameraCenter(_center_x, _center_y)` | `"CameraCenter"` | мгновенное | — |
| `ActionCameraPanBase(_frames)` | `"CameraPanBase"` | ждёт оба camera-твина | гасит `tween_x`/`tween_y` |
| `ActionCameraPan(view_x, view_y, frames)` | `"CameraPan"` | как у базы, цель — абсолютные координаты, `ease_in_out` | как у базы |
| `ActionCameraPanSpeed(_speed_x, _speed_y, frames)` | `"CameraPanSpeed"` | как у базы, цель — `speed*frames`, `linear` | как у базы |
| `ActionCameraPanToObj(_target, frames)` | `"CameraPanToObj"` | ждёт твины к центру цели (кламп к комнате) | гасит `tween_x`/`tween_y` |
| `ActionCameraTrackBase(_target, _offset_x, _offset_y)` | `"CameraTrackBase"` | каждый кадр центрирует view на цели; done по `should_finish` | — |
| `ActionCameraTrack(target_ref, frames, offset_x, offset_y)` | `"CameraTrack"` | `should_finish`: `timer >= frames` | — |
| `ActionCameraTrackUntilStop(target_ref, offset_x, offset_y)` | `"CameraTrackUntilStop"` | `should_finish`: `!actor.move_active` (grace 1 кадр, `timer < 2`) | — |
| `ActionWaitForInteract(target_ref, timeout_frames, timeout_action, interact_action)` | `"WaitForInteract"` | ждёт `resolved_target` в `global.__interacted_targets` или таймаут | чистит очередь от своей цели и мёртвых id |
| `ActionSetFlag(key, value)` | `"SetFlag"` | мгновенное | — |
| `ActionSetPlot(value)` | `"SetPlot"` | мгновенное | — |
| `ActionSpawnEntity(object_name, x, y, key, depth_val, persistent_flag)` | `"SpawnEntity"` | мгновенное | — |
| `ActionDestroy(target_ref)` | `"Destroy"` | мгновенное | — |
| `ActionRoomChange(target_room_ref, px, py, actor_pos_struct)` | `"RoomChange"` | ждёт уничтожения `obj_changingRoomsController` | — |
| `ActionPartialControl(_control_type, whitelist_array, allowed_actions_array)` | `"PartialControl"` | мгновенное | — |
| `ActionCheckpointState(_checkpoint_id, _config)` | `"CheckpointState"` | мгновенное | — |
| `ActionRestoreState(_checkpoint_id, _options)` | `"RestoreState"` | мгновенное | — |

### Музыкальные классы (`scr_cutscene_music.gml`)

Все музыкальные действия мгновенные: `start` дёргает глобальную функцию движка через `__cutscene_music_call(name, args)` — безопасный вызов `global.<name>` с развёртыванием массива аргументов (`method_call`/`script_execute_ext`) и warning при отсутствии функции. `update` всегда `true`, `cleanup` не определён. Блокировки очереди нет — фейды идёт в `obj_music_ctrl` независимо. Там же живут shorthand-обёртки `cutscene_music_pitch`, `cutscene_music_pause`, `cutscene_music_resume` — возвращают готовые действия для билдера/фабрики.

| Класс | `action_type` | Вызов в `start` |
|-------|---------------|-----------------|
| `ActionMusicPlay(snd_asset, fade_sec, volume = 1.0, persist_room_change = true)` | `"MusicPlay"` | `play_music_immediate(snd)` при `fade <= 0`, иначе `play_music_fade(snd, fade)`; при `volume >= 0 && volume != 1` — `set_music_volume_fade(volume, 0)`; пишет `global.music_persist_track` |
| `ActionMusicStop(fade_sec, use_layered = false)` | `"MusicStop"` | `stop_layered_music(fade)` или `stop_music(fade)` |
| `ActionMusicVolume(vol, fade_sec)` | `"MusicVolume"` | `set_music_volume_fade(vol, fade)` |
| `ActionMusicPitch(pitch)` | `"MusicPitch"` | `set_music_pitch(pitch)` |
| `ActionMusicPause()` | `"MusicPause"` | `pause_music()` |
| `ActionMusicResume()` | `"MusicResume"` | `resume_music()` |
| `ActionMusicIntroLoop(intro_asset, loop_asset, fade_sec)` | `"MusicIntroLoop"` | `play_music_intro_loop(intro, loop, fade)` |
| `ActionMusicDuck(multiplier, fade_sec)` | `"MusicDuck"` | `duck_music(mult, fade)` |
| `ActionMusicUnduck(fade_sec)` | `"MusicUnduck"` | `unduck_music(fade)` |
| `ActionMusicPlayLayered(calm_asset, battle_asset, fade_sec)` | `"MusicPlayLayered"` | `play_music_layered(calm, battle, fade)` |
| `ActionMusicSetIntensity(intensity, fade_sec = 1.0)` | `"MusicSetIntensity"` | `set_music_layer_intensity(intensity, fade)` |
| `ActionMusicIntroLayered(intro, calm, battle, fade, start_intensity)` | `"MusicIntroLayered"` | `play_music_intro_layered(...)` |
| `ActionMusicPhaseSequence(phases, fade_sec)` | `"MusicPhaseSequence"` | `play_music_phase_sequence(phases, fade)`; фазы — struct `{intro, calm, battle, intensity, fade}` |

## Хелперы уровня файла

### `__cutscene_resolve_state_value(var_path)`

Резолвер значений состояния мира (`scr_cutscene_classes.gml:4067-4127`). Используется `ActionBranchFlag` (ключи с точкой) и `ActionGuardGlobal` (поля `var`/`end_var`).

Правила разбора:

1. Вход обязан быть непустой строкой; ведущий префикс `global.` срезается.
2. Без точки — чтение `global.<name>` (например, `"plot"`, `"interact"`).
3. С точкой — по префиксу:

| Форма пути | Результат |
|------------|-----------|
| `flag.<key>` / `flags.<key>` | `global.flag[$ key]` |
| `entity.<key>` / `entity_state.<key>` | `global.entity_state[$ key]` |
| `entity_state.<room:eid>.<field>` | поле `field` записи сущности — путь режется по **последней** точке, т.к. ключ сущности сам содержит `:` |
| `stat.<name>` / `stats.<name>` | `global.stat_<name>` (например, `stat.hp` → `global.stat_hp`) |
| `<struct>.<field>` | `global[$ struct][$ field]`, если `global.<struct>` — struct |

Неразрешённый путь возвращает `undefined` (без исключений).

### `__cutscene_compare_values(actual, expected)`

Сравнение с толерантностью к JSON-типам (`scr_cutscene_classes.gml:4131-4174`):

| `actual` | `expected` | Результат |
|----------|------------|-----------|
| любой | любой | `true` при совпадении `typeof` и `==` |
| `bool` | `string` | `"true"`/`"false"` (без учёта регистра), `"1"`/`"0"` после trim |
| `real` | `string` | `real(string_trim(expected)) == actual`; нечисловая строка → `catch` → `false` |
| `string` | `bool` | симметрично: `"true"`/`"false"`/`"1"`/`"0"` |
| `string` | `real` | `real(string_trim(actual)) == expected` с `try/catch` |
| `bool` | `real` | `(expected != 0) == actual` |
| `real` | `bool` | `(actual != 0) == expected` |
| иначе | | `false` |

### Прочие хелперы файла

| Хелпер | Назначение |
|--------|------------|
| `__cutscene_resolve_target(_manager, _target)` | Резолв одной цели через `manager.resolve_target`; без резолвера принимает только живой instance id |
| `__cutscene_resolve_targets(_manager, _target)` | Мульти-резолв: массив целей, object index → все инстансы, строка → ключ `actor_map`, затем имя object-ассета → все инстансы |
| `__cutscene_warn_unresolved(action, role, target)` | Warning «цель не найдена» — только из одноразовых точек (`start`), не из покадровых |
| `__cutscene_validate_mode(value, allowed, fallback, owner, param)` | Валидация строкового режима по списку; невалидное → warning + fallback |
| `__cutscene_is_instant(_manager)` | Читает `manager.instant_mode` |
| `__cutscene_normalize_direction(_dir)` | `l/r/u/d`, `left/right/up/down` или целое `0..3` → `global.DIR.*`; real вне `0..3` и нераспознанная строка → warning + `DIR.DOWN`; нестроковые/нечисловые типы → `DIR.DOWN` молча |
| `__cutscene_actor_apply_facing(_inst, _dir)` | Пишет `facing_direction` (если поле есть) и спрайт из `chara_idle_sprites`/`chara_sprites`; для `obj_player` — `scr_sprite_for_facing` |
| `__cutscene_move_step(_actor, _tx, _ty, _spd, _use_collision, _apply_move_state)` | Один шаг движения: snap в пределах шага (без телепорта сквозь стену), `move_and_collide` по `[obj_collider, par_decor, par_interactable]`, stall-таймаут 60 кадров → «точка недостижима» |
| `__cutscene_move_cleanup(_actor)` | Сброс `move_active`, `move_blocked`, `__cutscene_move_stall`, `__cutscene_anim_override`, `speed`; при `auto_face` ещё `image_speed`/`image_index` в 0 |
| `__cutscene_sync_move_target(_inst)` | `target_x/y := x/y` после телепортов |
| `__cutscene_find_active_textbox()` | «Самое живое» окно `textboxTest_scribble`: с `is_dialogue_requested` → с идущим chatterbox → с любым chatterbox → первое |
| `__cutscene_find_dialogue_ctrl(_manager)` | `manager.dialogue_controller`, иначе `__cutscene_find_active_textbox()` |
| `__cutscene_dialogue_is_active(_ctrl)` | Активность диалога: пустой `chatterbox` = «стартует» → `true`; иначе `!ChatterboxIsStopped` |
| `__cutscene_normalize_yarn_path(_file)` | `\\` → `/`, срезает префиксы `datafiles/` и `Dialogues/` |
| `__cutscene_ease_value(_t, _easing)` | `"linear"`, `"ease_in"`/`"in"`, `"ease_out"`/`"out"`, `"ease_in_out"`/`"in_out"`/`"ease"` (квадратичные) |
| `__cutscene_runtime_get/set_value(_kind, _target, _property, ...)` | Чтение/запись свойства по `kind`: `"camera"` — свойства `x`/`y`/`view_x`/`view_y`/`camera_x`/`camera_y` через `view_camera[0]` (get — `camera_get_view_*`, set — `camera_set_view_pos` + `global.camera_x/y`); `"instance"`/`"object"` — `variable_instance_*`; запись `depth` переводит `depth_mode` в `"manual"` |
| `__cutscene_parallel_push/pop/splice/request_abort` | Стек активных `ActionParallel` на менеджере (`__parallel_stack`): `insert_actions` из действия внутри ветки вставляет продолжение в неё, `request_abort` ставит `__abort_requested` верхней группе |
| `cutscene_runtime_tween_to / fade_to / shake_object / shake_camera / spin_object / jump_to` | Регистрация runtime-эффектов в массивах `obj_globalManager` (`cutscene_runtime_*`); записи несут `owner_id` активной катсцены |
| `cutscene_runtime_show_emote / play_sfx / set_visible / flip_x / halt` | Обёртки над `emote_show`, `scr_play_sfx` и прямой записью полей |
| `cutscene_runtime_step()` | Тикер всех runtime-эффектов (вызывается из Step `obj_globalManager`); сам удаляет неактивные записи |
| `cutscene_runtime_cleanup_owner(_owner)` | Деактивирует все эффекты катсцены по `owner_id` + гасит её singleton-fade с `alpha = 0` |
| `__cutscene_runtime_rollback_owner_shakes(_owner)` | Синхронный откат `applied_x/y` шейков владельца (нужен перед restore-state) |
| `__cutscene_snapshot_instance / __cutscene_create_snapshot / __cutscene_apply_instance_snapshot` | Снимок полей инстанса (позиция, `sprite_index`, `image_*`, `depth`, `visible`, `depth_mode`, `facing_direction`, `auto_face`, `auto_walk`, move-поля) и полного состояния сцены (actors, player, camera, music, globals, instances) |
| `__cutscene_cleanup_transients(_manager, _snapshot)` | Уничтожает актёров `actor_map`, которых нет в snapshot (кроме `obj_player`), и очищает `actor_specs` |
| `__cutscene_restore_actor/camera/music/global/instance_states` | Покатегорийный restore из snapshot; типы глобалов проверяются — смена типа → warning и пропуск |
| `__cutscene_update_attachments()` | Покадровое ведение привязок `global.__cutscene_attachments` (позиция, `image_xscale/yscale`, depth); мёртвые target/parent → удаление записи |
| `__cutscene_attachments_remove_by_target(_inst)` | Удаление записи привязки + сброс `attached_target` |
| `__cutscene_cleanup_old_checkpoints()` | LRU-вытеснение старейшего checkpoint при достижении `__CUTSCENE_MAX_CHECKPOINTS = 10` (по `timestamp_frames`) |

!!! note "Мёртвый код"
    `__cutscene_room_entry_spawn` и `scr_room_entry_check` в конце файла — зачищенные заглушки (`DELETE_CANDIDATE`): записей в `global.room_flags` никто не создаёт, тела пусты. Для комнатных флагов предназначены `scr_world_flag_set/get` (`entity_state`, сущность `"_room"`).

## Детали сложных классов

### `ActionDialogue`

`start` готовит контроллер диалога:

1. Если `manager.dialogue_controller` не существует:
   - есть живой `textboxTest_scribble` — забирает `instance_find(textboxTest_scribble, 0)` под контроль катсцены (при нескольких окнах — warning, берётся первое); создание второго окна поверх чужого не допускается;
   - окон нет — создаёт `instance_create_layer(0, 0, scr_layer_ensure_instances(), textboxTest_scribble)` (окно рисуется в Draw GUI, мировые координаты не важны).
2. На контроллер пишутся `auto_advance`, `non_blocking = !block_queue`; затем перекрывающие значения с менеджера, если поля есть: `dialogue_auto_advance` → `auto_advance`, `dialogue_prevent_skip` → `prevent_skip`, `dialogue_stay_open` → `stay_open`, `dialogue_char_speed` → `char_speed` + `typist.in(speed / fps, 0)`.
3. Файл валидируется: не-строка или строка без `.yarn` → warning и `manager.dialogue_default_file`; путь нормализуется `__cutscene_normalize_yarn_path`; если ни `Dialogues/<file>`, ни `<file>` не существуют — снова warning и дефолтный файл.
4. Контроллеру выставляются `dialogue_filename`, `dialogue_node`, `chatterbox = ""` (сброс остановленного диалога при переиспользовании окна `stay_open`), `is_dialogue_requested = true`.
5. Подготовка обёрнута в `try/catch`: при исключении `manager.dialogue_controller` уничтожается, действие завершается как пропущенное.

`update`: при `block_queue == false` или instant-режиме — сразу `true`. Иначе ждёт: пока `chatterbox` пуст (`""`/`noone`/`undefined`) — до `__CUTSCENE_DIALOGUE_WAIT_FRAMES = 600` кадров (~10 с при 60 fps), затем `TIMEOUT`-лог и пропуск; дальше — `ChatterboxIsStopped(_ctrl.chatterbox)`.

`cleanup`: при `block_queue == false` окно остаётся жить и доигрывать диалог (его уничтожит сам `textboxTest_scribble` по окончании речи или `finish_cutscene`). При `stay_open == true` окно тоже не трогается — его переиспользует следующий `ActionDialogue` или закроет `ActionClearDialogue`. Иначе `manager.dialogue_controller` уничтожается — в том числе когда это «чужое» окно, принятое под контроль в `start`.

### `ActionMarkNode` и `ActionGoToNode`

- `ActionMarkNode` — служебная метка: `start` вызывает `manager.mark_node_reached(node_name)` (менеджер пишет имя в `reached_nodes` с лимитом `reached_nodes_limit = 50`; повтор подряд игнорируется). Без метода у менеджера — warning. Метки читаются `ActionGoToNode` и `ActionGuardGlobal` (`stop_when = "node_reached"`).
- `ActionGoToNode` — переход курсора очереди, а не прыжок актёра. `start` ищет в `manager.action_queue` действие с `action_type == "MarkNode"` и `node_name == target_name` — только в **основной** очереди (метки внутри `parallel`/`sequence` недостижимы: warning, переход пропущен). Самопрыжок (метка == текущий индекс) — warning, no-op. Прыжок назад: инкремент `manager.__goto_back_jumps`, при превышении 1024 — warning и отмена (защита от бесконечных циклов `goto → goto`); действиям диапазона `[метка..текущий]` сбрасываются `started`, `__cleanup_done`, числовые `timer`/`elapsed`, и вызывается `reset(manager)`, если реализован. Индекс ставится в `метка - 1` — диспетчер после `cleanup` инкрементирует до метки.

### `ActionBranchFlag`

`start` читает значение и вставляет выбранную ветку через `manager.insert_actions(current_action_index + 1, actions)`:

- Ключ без точки — `global.flag[$ key]`; с точкой — `__cutscene_resolve_state_value` (`flag.*`, `stat.*`, `entity_state.*`, `struct.field`, `global.*`).
- Для числовых операторов `expected` нормализуется один раз: строка → `real(string_trim(...))` в `try/catch`; нечисловая строка → `undefined` → сравнение `false` (без исключения в `start` менеджера).

| `operator` | Семантика |
|------------|-----------|
| `exists` | ключ/путь существует и значение ≠ `undefined` |
| `!exists` | ключа нет или значение `undefined` |
| `==` | `__cutscene_compare_values(actual, expected)` (bool↔real и строковые `true/false/1/0` учитываются) |
| `!=` | отрицание `==` |
| `>`, `<`, `>=`, `<=` | строгое числовое: `is_real(actual) && is_real(expected_норм)` |
| прочее/пустое | деградирует до `==` |

### `ActionGuardGlobal`

Условный фильтр/ожидание по глобальной переменной. `if_false` валидируется в `["skip", "wait_until_true"]` (fallback `skip`), `stop_when` — в `["none", "global_var", "node_reached", "timeout"]` (fallback `none`); невалидные строки дают warning через `__cutscene_validate_mode`. Пустой `global_key` = условие не задано → `actions` вставляются безусловно.

- `skip`: `start` проверяет условие один раз и вставляет `actions` при истине; `update` сразу `true`.
- `wait_until_true`: `update` каждый кадр проверяет условие (`__cutscene_resolve_state_value` + `__cutscene_compare_values`) и инкрементирует `timer`. End-condition: `global_var` — `end_var` (тот же резолвер) равен `end_equals`; `node_reached` — `end_node` есть в `manager.reached_nodes`; `timeout` — `timer >= end_timeout_frames`. Сработавший end-condition завершает действие **без** вставки `actions`.
- Вставка защищена флагом `__actions_inserted` (сбрасывается в `start`): `start` и `update` в одном тике не вставят ветку дважды.

### `ActionLerp`

Покадровое приближение свойства без runtime-твина: `lerp_factor` зажат в `[0.001, 1]` (нечисловой → `0.1`), `snap_threshold` — минимум `0.01` (нечисловой → `0.5`). `update` читает текущее значение через `__cutscene_runtime_get_value` (нечисловое → завершение), пишет `lerp(cur, end, factor)`; при `|next - end| <= snap_threshold` — точная запись `end_value` и `true`. Поддерживает `target_kind = "camera"` (тогда `target` не резолвится — работа идёт с `view_camera[0]`); при instant-режиме — одноразовая запись цели в `start`.

### `ActionPartialControl`

Пишет на менеджер `partial_control_type`, `partial_control_whitelist`, `partial_control_allowed_actions` и дёргает `obj_player.can_move` (`0` → `false`, `> 0` → `true`). Значения `control_type` — enum `INTERACT_PARTIAL_CONTROL` (`interactionWithNPCsOrObjects.gml`):

| `control_type` | Имя | Поведение |
|----------------|-----|-----------|
| `0` | `LOCKED` | Игрок подчинён катсцене: движение и взаимодействие заблокированы |
| `1` | `WHITELIST` | Взаимодействие только с объектами из `whitelist` (проверяет `scr_interaction`, каждая запись резолвится через `manager.resolve_target`); ввод фильтруется по `allowed_actions` |
| `2` | `FREE` | Полная свобода: движение и любое взаимодействие, катсцена идёт в фоне |

Фильтр ввода (`scr_input__partial_control_allows` в `scr_inputApi.gml`): записи `allowed_actions` сравниваются с именами действий `input_map`; алиасы-группы `"move"` (покрывает `up`/`down`/`left`/`right`/`run`) и `"interact"` (покрывает `confirm`) разворачиваются. **Пустой `allowed_actions` — legacy-дефолт: пропускается только `confirm`** — без него `wait_for_interact` никогда бы не срабатывал. Мусорный `control_type` вне `0/1/2` — однократный warning и трактовка как «заблокировано».

### `ActionRoomChange`

Блокирующая смена комнаты с фейдом. `start`:

1. Нормализует `target_room` (строка → `asset_get_index`, проверка `asset_room`); `room_exists` обязателен, иначе warning и пропуск.
2. Пишет на менеджер параметры перехода для Room Start: `__room_change_target_room`, `__room_change_player_x/y`, `__room_change_actor_positions`, `__room_change_in_progress = true`. Позиции актёров — `actor_pos_struct` (ключ → `{x,y}`); не-struct приводится к `{}`.
3. Берёт или создаёт `obj_changingRoomsController`: существующий контроллер переиспользуется с warning и перезаписью `newRoom/newX/newY` (иначе чужой фейд ушёл бы в чужую комнату); новый создаётся на `__CUTSCENE_TRANSITION_DEPTH = -100000` — выше всех `par_depth`-объектов (`depth = -y`), чтобы фейд рисовался поверх сцены.
4. Ставит контроллеру `__player_pos_by_manager = true`: при катсценном переходе позицию игрока пишет только Room Start менеджера (`Other_4`), дублирующая запись `scr_room_fade_update` гасится флагом.

`update` ждёт уничтожения контроллера (конец fade-in). Если при этом `__room_change_in_progress` ещё взведён — переход не состоялся (контроллер умер в fade-out без `room_goto`, в т.ч. same-room случай): warning и сброс всех `__room_change_*` полей, чтобы устаревшие координаты не отравили следующий переход.

Пересоздание актёров в новой комнате — не работа действия: её выполняет Room Start менеджера по `actor_specs` (только не-persistent актёры; persistent-инстансы, например созданные `ActionSpawnEntity` с `persistent = true`, переживают смену комнаты сами).

### Музыкальные действия и `persist_room_change`

`ActionMusicPlay` — единственный музыкальный класс с состоянием после `start`: помимо запуска трека (`play_music_immediate` при `fade <= 0`, иначе `play_music_fade`) он пишет `global.music_persist_track = persist_room_change ? snd : noone`. `scr_global_on_room_change` читает эту пометку: persist-трек не перезаписывается музыкой новой комнаты; явный не-persist вызов снимает чужую пометку (`noone`).

Приглушение вызывается как `duck_music` — и в `ActionMusicDuck` (`__cutscene_music_call("duck_music", [mult, fade])`), и в `__cutscene_restore_music_state` (`duck_music(duck_multiplier, 0)`). Реальный API движка — `global.duck_music(multiplier, fade_sec)` из `scr_music_init.gml`; идентификатора `set_music_duck` в проекте нет.

### Контейнеры: `ActionSequence`, `ActionParallel`, `ActionGroup`, `ActionScheduleAction`

- `ActionSequence` — последовательность под-действий как одно действие. В обычном режиме за кадр завершает одно под-действие и стартует следующее; в instant-режиме крутит цепочку до конца с бюджетом `__CUTSCENE_INSTANT_GUARD_LIMIT = 1024` на кадр (остаток дорабатывает на следующем тике, warning в лог). Перед прогоном сбрасывает `started` у всех под-действий (переиспользование через `insert_actions`). `cleanup` вызывает `cleanup` только текущего действия.
- `ActionParallel` — параллельные ветки: каждая тикается до `true`, `sub_done[i]` защищает завершённую ветку от повторного update, `sub_cleaned[i]` — от двойного cleanup (ветки чистятся сразу при завершении, не в конце группы). `__active_branch` показывает индекс тикающей ветки — по нему `manager.insert_actions` через `__cutscene_parallel_splice` вставляет продолжение внутрь ветки (sequence-ветка — за текущим действием, одиночная оборачивается в `ActionSequence`). `__cutscene_parallel_request_abort` ставит `__abort_requested` — группа досрочно чистит оставшиеся ветки и возвращает `true`. `cleanup` идемпотентен (`__cleaned`).
- `ActionGroup` — генерирует действие на каждую цель из `__cutscene_resolve_targets` через `_generator_fn` (callable оборачивается в `method(context, fn)`; невызываемый генератор → warning и no-op) и гонит их как `ActionParallel`.
- `ActionScheduleAction` — отложенный запуск `inner_action`: `delay_seconds` конвертируется в кадры через `game_get_speed(gamespeed_fps)` в `start`. `blocking = false` — fire-and-forget: `inner` уходит в `manager.scheduled_actions` (тикает Step менеджера, чистится `finish_cutscene`), действие завершается сразу. `blocking = true` — очередь ждёт `inner.update`. Параметр `tag` принимается для совместимости сигнатуры, но не хранится.

### `ActionAttachToTarget` / `ActionDetach`

`ActionAttachToTarget` регистрирует запись в `global.__cutscene_attachments` (`{target_inst, parent_inst, offset_*, follow_*, detach_on_cutscene_end, tweening, owner_inst}`), предварительно удаляя старую привязку цели. При `duration_seconds > 0` позиция твинится в `update` (конечная точка пересчитывается по текущей позиции родителя), иначе телепорт + немедленное применение `follow_facing` (`image_xscale`) и `follow_scale` (`image_yscale`). `follow_depth`: для наследников `par_depth` пишется `attached_target` (их depth ведёт `par_depth/Step`), для прочих целей depth копирует `__cutscene_update_attachments` напрямую. `detach_on_cutscene_end` обрабатывает `finish_cutscene`; прерванный твин снимает флаг `tweening` в `cleanup`. `ActionDetach` удаляет запись (`__cutscene_attachments_remove_by_target`, заодно сбрасывает `attached_target`) и при `destroy_after_detach` уничтожает инстанс.

### `ActionCheckpointState` / `ActionRestoreState`

- `ActionCheckpointState` пишет snapshot (`__cutscene_create_snapshot`) в `global.__cutscene_checkpoints[id]` с монотонным `timestamp_frames = max(existing) + 1` и прогоняет LRU-чистку (`__CUTSCENE_MAX_CHECKPOINTS = 10`). `_config`: `include_actors/player/camera/music` (bool, дефолт `true`), `include_globals` и `include_instances` — массив строк **или** legacy-строка с JSON-массивом внутри (`json_parse` под `try/catch`). Секция `instances` снимает только **первый** инстанс каждого объекта (`instance_find(obj, 0)`); ссылочные значения глобалов клонируются через `variable_clone`.
- `ActionRestoreState`: `options` — `cleanup_transients`, `restore_camera`, `restore_music` (дефолт `true`), `on_missing` (`"warn"` по умолчанию; `"fail"` пишет ERROR-лог, но сцену не прерывает — `update` всегда `true`). Порядок: `cutscene_runtime_cleanup_owner(manager)` + `__cutscene_runtime_rollback_owner_shakes(manager)` (живые эффекты этой катсцены не должны доехать до старых целей после отката) → `__cutscene_cleanup_transients` → секции `actors` / `player` / `camera` / `music` / `globals` / `instances`.

## См. также

- [Обзор катсцен](overview.md) — жизненный цикл `obj_cutsceneManager`, очередь действий
- [Архитектура катсцен](architecture.md) — `actor_map`, `insert_actions`, instant_mode, watchdog
- [JSON-экшены](json-actions.md) — соответствие `"type"` ↔ `Action*`-классам
- [Частичный контроль](partial-control.md) — `partial_control` в JSON и вводе
- [Актёры и камера](actors-and-camera.md) — `obj_actor`, facing, camera-действия
- [GML DSL катсцен](gml-dsl.md) — `c_*`-команды и Chatterbox-функции
- [Диалоги](../systems/dialogue.md) — `textboxTest_scribble`, Chatterbox, портреты
- [Музыка](../systems/music.md) — `global.duck_music` и остальной API `obj_music_ctrl`
- [Смена комнат](../systems/room-transitions.md) — `obj_changingRoomsController`, `scr_global_on_room_change`
- [Ввод](../systems/input.md) — `input_map`, фильтр `partial_control`

<!-- sources: scripts/scr_cutscene_classes/scr_cutscene_classes.gml:1-5035; scripts/scr_cutscene_music/scr_cutscene_music.gml:1-283; scripts/scr_inputApi/scr_inputApi.gml:49-137; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml:1-70; scripts/scr_music_init/scr_music_init.gml:562-618; scripts/scr_global_on_room_change/scr_global_on_room_change.gml:33; objects/obj_cutsceneManager/Create_0.gml:8-61,293-316,428-430,501-545,704-705 -->
