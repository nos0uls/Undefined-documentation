# Ревью: systems/room-transitions.md

Код: ревизия 7ee444a ($P, read-only). Проверено по исходникам, указанным в `<!-- sources -->` страницы.

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 12 | `objRoomChanger` — триггер, запускает persistent `obj_changingRoomsController`: фейд, `room_goto`, позиция игрока | OK |
| 12 | Побочные эффекты (музыка, антизастревание) — `obj_globalManager` через `scr_global_on_room_change` / `scr_global_transition_safety` | OK (objects/obj_globalManager/Step_0.gml:22-32,61) |
| 18 | `objRoomChanger`: спрайт `spr_rmChanger`, `visible:false`, `persistent:false` | OK (objects/objRoomChanger/objRoomChanger.yy:17,42-46) |
| 18 | При касании снимает параметры, на следующем Step создаёт контроллер | OK (Collision_obj_player.gml:20-27; Step_0.gml:2-25) |
| 19 | Контроллер живёт до конца затухания и самоуничтожается | OK (scr_room_fade_update.gml:63-67) |
| 28 (mermaid) | `RC->>RC: снимок pending_*, room_change_lock = true` | WRONG: `room_change_lock` ставится игроку (`other.room_change_lock`, Collision_obj_player.gml:12), стрелка должна быть RC→P |
| 29-30 (mermaid) | Step: `instance_create_depth(__CUTSCENE_TRANSITION_DEPTH)`, затем `instance_destroy()` | OK (Step_0.gml:19,25; macro = -100000, scr_cutscene_classes.gml:62) |
| 31-33 (mermaid) | Fade-in ~0.17 c, `fadeLevel += 6.0 * dt` | OK (scr_room_fade_update.gml:12-14,33) |
| 34-35 (mermaid) | `fadeLevel >= 1` → `room_goto(newRoom)`; `x=newX, y=newY` | OK (scr_room_fade_update.gml:34,48,55-56) |
| 36-38 (mermaid) | GM: `room != current_room` → `scr_global_on_room_change`; `transition_ghost`, `room_change_lock`, `__transition_entry_*`; `__transition_safety_frames = 16` | OK (Step_0.gml:22-27; scr_global_on_room_change.gml:63-78) |
| 39-42 (mermaid) | Fade-out ~0.33 c, `fadeLevel -= 3.0 * dt`; `fadeLevel <= 0` → destroy | OK (scr_room_fade_update.gml:14,60,63-67) |
| 43 (mermaid) | `scr_global_transition_safety`: unstuck, снять ghost | OK (scr_global_transition_safety.gml:5-73) |
| 52 | `room_name` — asset, фильтр `GMRoom` | OK (objRoomChanger.yy:33-35, varType 5) |
| 53-54 | `x_position`/`y_position`: `-1` = ось не настроена → позиция триггера; `0` валидна | OK (objRoomChanger.yy:31-32; Collision_obj_player.gml:20-21) |
| 55 | `eyes_glow`: спрайт игрока под `shd_Chara_Eyes` поверх затемнения | OK (objRoomChanger.yy:36; Draw_0.gml:20-32) |
| 59 | Create: `pending_change = false`, снимок не делается (property-overrides + ICC позже) | OK (Create_0.gml:2-8) |
| 60 | Collision: выходы по `instance_exists(obj_changingRoomsController)` и `other.room_change_lock` | OK (Collision_obj_player.gml:2-9) |
| 60 | «взводит `room_change_lock`» — без уточнения чей | WRONG (мелочь): ставится `other.room_change_lock` — флаг игрока (Collision_obj_player.gml:12); уточнить |
| 60 | Копирует `pending_x/y/room/glow`, `pending_change = true` | OK (Collision_obj_player.gml:20-27) |
| 61 | Step: повторный гард на контроллера (ActionRoomChange/сейв), самоуничтожение; создание на `__CUTSCENE_TRANSITION_DEPTH` (-100000); перепись `newX/newY/newRoom/eyesGlow` | OK (Step_0.gml:5-25; scr_cutscene_classes.gml:62) |
| 68 | `persistent: true`; события Create, Step, Draw | OK (obj_changingRoomsController.yy:5-8,17) |
| 70 | Поля Create: `newX/newY/newRoom`, `fadeLevel = 0.1`, `eyesGlow`, `__fade_prev_room = room` | OK (Create_0.gml:1-13) |
| 72 | Step → `scr_room_fade_update()`, контракт self | OK (Step_0.gml:2; scr_room_fade_update.gml:4-7) |
| 76 | Скорости 6.0/3.0 доли/сек через `delta_time`, ~0.17/~0.33 с | OK (scr_room_fade_update.gml:12-14) |
| 77 | `__fade_prev_room`: при внешней смене `newRoom = room`, фейд затухает на месте | OK (scr_room_fade_update.gml:22-30) |
| 78 | `fadeLevel >= 1` → валидация `is_real` + `room_exists`, иначе `[ROOM FADE] ERROR`, сброс, destroy; `room_goto`; перенос игрока | OK (scr_room_fade_update.gml:38-57) |
| 79 | `__player_pos_by_manager` вешает `ActionRoomChange`; позицию ставит Room Start `obj_cutsceneManager` | OK (scr_cutscene_classes.gml:4767; obj_cutsceneManager/Other_4.gml:96-104) |
| 80 | `room == newRoom` → затухание; `fadeLevel <= 0` → `eyesGlow = false`, destroy | OK (scr_room_fade_update.gml:59-67) |
| 82 | Draw: чёрный `draw_rectangle(0,0,room_width,room_height)` с `alpha=fadeLevel`; `eyesGlow` → спрайт под шейдером | OK (Draw_0.gml:11-32; фактический вызов с 5-м аргументом `false` — filled; уточнить подпись) |
| 82 | Захват/возврат draw-state (font/color/alpha/halign/valign) | OK (Draw_0.gml:4-8,36-40) |
| 86 | `obj_globalManager` Step: `room != current_room` → `scr_global_on_room_change(current_room, room)`, обновление `current_room` (Step_0.gml:22-32); контракт self, `notification_*` | OK (Step_0.gml:22-32; scr_global_on_room_change.gml:5-13) |
| 90 | Сброс `notification_active/text/timer` | OK (scr_global_on_room_change.gml:11-13) |
| 91 | Трек: `music_menu` для menu-комнат (`global.is_menu_room`), иначе `global.music_default_game_track`; граница меню↔игра — `play_music_immediate`, внутри — `play_music` | OK (scr_global_on_room_change.gml:19-56; scr_music_init.gml:114,177,274; obj_Init/Create_0.gml:189) |
| 92 | `transition_ghost = true`, `ghost_mode = true`, `room_change_lock = true`, `__transition_entry_x/y`, `global.__transition_safety_frames = 16` (кадры) | OK (scr_global_on_room_change.gml:63-78) |
| 94 | `scr_global_transition_safety` каждый Step из `obj_globalManager` | OK (Step_0.gml:61) |
| 96 | `place_meeting` по `obj_collider`, `par_decor`, `par_interactable` | OK (scr_global_transition_safety.gml:9-11) |
| 97 | Кольца радиус 1–32 px, шаг 45°, ближайшая к `__transition_entry_*`; `[TRANSITION] WARNING` с дистанцией | OK (scr_global_transition_safety.gml:19-56) |
| 98 | На нуле: `transition_ghost = false`, `ghost_mode = debug_ghost` (F8-призрак переживает) | OK (scr_global_transition_safety.gml:64-73) |
| 100 | `room_change_lock` снимает `scr_player_room_lock` (Step `obj_player`), пока пересечение с `objRoomChanger` | OK (scr_player_room_lock.gml:7-13; obj_player/Step_0.gml:9) |
| 104 | Persistent-объекты: 9 перечисленных | OK — grep `"persistent":true` по objects/*/*.yy даёт ровно этот список |
| 105 | `global.music_persist_track` ставит `ActionMusicPlay` с `persist_room_change`; гард `cutscene_active` + совпадение с `music_current`; снимает `finish_cutscene` | OK (scr_cutscene_music.gml:32,51; scr_global_on_room_change.gml:39-45 — гард также требует `music_instance != -1` и `audio_is_playing`, «играющим» покрыто; obj_cutsceneManager/Create_0.gml:756-757 внутри `finish_cutscene` @669) |
| 106 | `Other_5` (Room End): `__transition_actor_snapshot` — позиции + исходный persistent; актёры со spec → переходный persistent; `Other_4` возвращает флаг и пересоздаёт погибших | OK (obj_cutsceneManager/Other_5.gml:15-28; Other_4.gml:47-93,117-153) |
| 110 | `par_interactable/Other_4` → `__entity_state_restore()` (entity_id финальный), `Other_5` → `__entity_state_save()` | OK (par_interactable/Other_4.gml:1-11; Other_5.gml:1-8; Create_0.gml:41-74) |
| 111 | `obj_cutsceneManager/Other_4`: восстановление актёров + `__room_change_*` после `ActionRoomChange`; `Other_5`: снапшот | OK (Other_4.gml:95-161; Other_5.gml) |
| 115 | `clean_state`: init `false` в `obj_Init/Create_0`; `true` только в `scr_resetGameToDefault`; удаляет слоты + `game_state.dat`, сбрасывает настройки, `game_end()` в том же кадре | OK (obj_Init/Create_0.gml:23; scr_resetGameToDefault.gml:5-42; `global.game_state_file = "game_state.dat"` @69) |
| 119 | `obj_globalManager/Other_3`: при `clean_state` выход до записи `game_state.dat` | OK (Other_3.gml:4-9) |
| 120 | `obj_settingsManager` блокирует debug-пункт при `clean_state && !debug`, текст «Debug заблокирован в режиме тестера» | OK (obj_settingsManager/Create_0.gml:136-140; Draw_64.gml:115) |
| 127 | `[ROOM FADE] ERROR` при невалидном `newRoom` | OK (scr_room_fade_update.gml:38-42) |
| 130 | 16 кадров unstuck, радиус 32 px к точке входа, `[TRANSITION] WARNING` | OK (scr_global_transition_safety.gml) |
| 133 | Гард `instance_exists` в Collision и Step; второй триггер самоуничтожается | OK (Collision_obj_player.gml:2-4; Step_0.gml:9-12) |
| 137-143 | Ссылки `player.md`, `music.md`, `../cutscenes/architecture.md`, `interaction.md`, `save-system.md`, `../architecture/global-state.md`, `../architecture/rooms.md` | OK — все файлы существуют в docs_new и в `_meta/nav_plan.md` |
| 145 | sources-комментарий | OK — все перечисленные файлы читались; диапазоны соответствуют |

## Итог
- WRONG: 2 (mermaid-стрелка `room_change_lock` → игрок, а не RC; та же неточность в тексте стр. 60 — флаг игрока `other.room_change_lock`).
- Мелочь: `draw_rectangle` в подписи без 5-го аргумента `false` (filled) — уточнено.
- UNVERIFIABLE / MISSING: нет.
