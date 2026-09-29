# Review: docs_new/systems/music.md

Код: `Undefinedtale888` @ 7ee444a (read-only). Проверено по файлам, перечисленным в `<!-- sources -->` страницы, плюс `sounds/*/*.yy` (ls), `cutscene_action_factory`, `scr_cutscene_classes`, `obj_cutsceneManager`, `obj_Init`, `obj_globalManager`, `scr_settingsManager`, `obj_settingsManager`, `obj_p3r_pause`, `obj_inGameMenu`, `scr_settings_step_root`, `scr_global_debug_hotkeys`, `obj_sound_test`, `obj_menu`, `obj_p3r_title`, `map_emotions`, `datafiles/cutscenes/*.json`.

Легенда: OK — подтверждено; WRONG — не соответствует коду; UNVERIFIABLE — в коде не проверяемо; MISSING — есть в коде, нет на странице.

## Шапка и архитектура

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 12 | Time-based фейды, intro+loop, calm/battle, duck, phase sequences; API в `global.*` создаёт `scr_music_init()`; тик — persistent `obj_music_ctrl` | OK — scr_music_init.gml:48-50 (delta_time), obj_music_ctrl.yy:17 (persistent), Step_0.gml:3-5 |
| 18-19 | `obj_Init.Create_0` → `scr_music_init()` + `instance_create_layer` → `obj_music_ctrl` | OK — obj_Init/Create_0.gml:266, 279-281 |
| 20-21 | Step → `update_current` + `fade_previous` | OK — obj_music_ctrl/Step_0.gml:3-5 |
| 22 | Draw GUI → debug overlay (F9) | OK — Draw_64.gml:3 (`global.debug && global.debug_show_music`), scr_global_debug_hotkeys.gml:66-68 |
| 23-24 | `obj_globalManager.Step` при `room != current_room` → `scr_global_on_room_change` → `play_music`/`play_music_immediate` | OK — obj_globalManager/Step_0.gml:22-27 |
| 25 | `ActionMusic*` → `__cutscene_music_call` | OK — scr_cutscene_music.gml:11-21 |
| 30 | Повторный `scr_music_init` гасит живые инстансы до перезаписи | OK — scr_music_init.gml:11-25 |
| 31-37 | Роли файлов в таблице | OK — все файлы существуют, содержимое совпадает |
| 39 | `obj_music_ctrl`: persistent, без спрайта/родителя; Create — комментарий; Step — два тика; Draw GUI — overlay при `global.debug && global.debug_show_music` | OK — obj_music_ctrl.yy:16,17,34; Create_0.gml:1-4; Draw_64.gml:3 |
| 39 | Создаётся на слое `scr_layer_ensure_instances()` | OK — obj_Init/Create_0.gml:280 |

## Глобальное состояние (таблица `global.music_*`)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 46-62 | Все переменные `music_*` и их дефолты | OK — scr_music_init.gml:30-107 (поимённо сверено) |
| 51 | `music_volume_override`: `-1` = из настроек, `>=0` — ручная, сброс при смене трека | OK — scr_music_init.gml:52, 201, 277, 461, 655 |
| 61 | `music_default_fade` = 0.5, `music_crossfade_lead` = 0.15 | OK — scr_music_init.gml:79-80 |
| 62 | `music_phase_fade_default` 0.5 / `music_phase_stop_fade` 1.0 / `music_autorestart_fade` 0.2 | OK — scr_music_init.gml:82-86 |
| 63 | `music_default_game_track` = `music_SchoolRoutine` | OK — scr_music_init.gml:114 |
| 64 | `room_music_override` = `undefined`, таблица удалена | OK по сути, **формулировка неточна**: «обращение к ней падает громко» — чтение глобала возвращает `undefined` без ошибки (он присвоен); падает только использование как таблицы (индексация). Код: scr_music_init.gml:115-117 |
| 65 | `music_phase_manager` = struct `phases`, `phase_count`, `current_index` + методы | OK — scr_music_init.gml:793-797 |
| 66 | `__menu_volume_depth` — глубина стека push/pop | OK — scr_music_init.gml:130 |

## API `scr_music_init` (сигнатуры сверены по файлу построчно)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 74 | `play_music(snd_asset)` — кроссфейд за `music_default_fade`, no-op при том же живом треке | OK — scr_music_init.gml:177-182 (делегирует в fade), фильтр 197-199. Нюанс: no-op только при `!music_layered_mode` — на странице не уточнено (исправлено при правке) |
| 75 | `play_music_fade(snd_asset, fade_sec)` — handoff в prev, fade-in короче на `crossfade_lead` | OK — scr_music_init.gml:190-239, 203, 209 |
| 76 | `play_music_immediate` — мгновенная смена, повтор = рестарт, используется restore | OK — scr_music_init.gml:274-318; restore — scr_cutscene_classes.gml:1032,1037 |
| 77 | `stop_music(fade_sec)`, снимает паузу | OK — scr_music_init.gml:325-375, 333-335 |
| 78 | `set_music_pitch(pitch)`, min 0.01, применяется к intro/layer2 | OK — scr_music_init.gml:382-395 |
| 79 | `set_music_volume_fade(vol, fade_sec)` — override + фейд к `vol * duck`; при 0 и идущем fade-in перенацеливает | OK — scr_music_init.gml:404-447 |
| 80 | `play_music_intro_loop(intro, loop, fade)` | OK — scr_music_init.gml:457-507 |
| 81 | `play_music_intro_layered(intro, calm, battle, fade, start_intensity)`; `battle=noone` → обычный loop | OK — scr_music_init.gml:251-264 |
| 82 | `pause_music`/`resume_music` — все каналы: current, intro, prev, layer2, prev_layer2 | OK — scr_music_init.gml:513-559 |
| 83 | `duck_music(multiplier, fade_sec)` — финальная = `settings_vol * multiplier` | OK — scr_music_init.gml:569-612 |
| 84 | `unduck_music(fade_sec)` = `duck_music(1, fade_sec)` | OK — scr_music_init.gml:617-619 |
| 85 | `play_music_layered(calm, battle, fade)` — стартовая интенсивность 0 | OK — scr_music_init.gml:644-709, 693-694 |
| 86 | `set_music_layer_intensity` — no-op без layered | OK — scr_music_init.gml:718-733 (719) |
| 87 | `stop_layered_music` — fallback на `stop_music` без layered | OK — scr_music_init.gml:738-786 (739-742) |
| 88 | `play_music_phase_sequence(phases, fade)` — фаза 0; `calm` обязателен | OK — scr_music_init.gml:909-913, 849-851 |
| 89 | `music_phase_next(fade)` | OK — scr_music_init.gml:918-921 |
| 90 | Методы `music_phase_manager.*`: `set_sequence`, `play_index`, `play`, `next`, `set_intensity`, `stop`, `clear`; `play_index` диспетчер по полям фазы | OK — scr_music_init.gml:800-903 |
| 91 | `__music_get_settings_volume` = (override ≥ 0 ? override : `__music_volume`) × `duck_multiplier` | OK — scr_music_init.gml:142-150 |
| 92 | `__music_stop_intro`, `__music_stop_layer2` | OK — scr_music_init.gml:157-170, 625-636 |
| 94 | Модульные `__music_handoff_to_prev`, `__music_fade_lerp` | OK — scr_music_init.gml:930-965, 976-980 |
| — | Полнота таблицы: все `global.*`-присваивания файла покрыты | OK — пробелов нет |
| 97 | `set_music_duck` не существует — только `duck_music`/`unduck_music` | OK — `grep -r set_music_duck` по коду: 0 совпадений |

## SFX

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 101 | `scr_play_sfx(sound_or_key, [volume], [pitch], [fallback_sound])` | OK — scr_SFXPlay.gml:11 |
| 103 | строка → ключ `ui_sfx_map` (`move/confirm/back/erase/error/save`), иначе `asset_get_index` | OK — scr_SFXPlay.gml:14-25; ключи — obj_Init/Create_0.gml:108-115 |
| 104 | число → индекс ассета | OK — scr_SFXPlay.gml:26 |
| 105 | fallback → `fallback_sound`, затем `ui_snd_select` | OK — scr_SFXPlay.gml:30-39 |
| 107 | громкость = `volume * clamp(__sfx_volume,0,1)`; до init — полная | OK — scr_SFXPlay.gml:44-45 |
| 107 | `scr_SFXPlay` — legacy-алиас, `ui_snd_select` как fallback, ~70 вызовов | OK — scr_SFXPlay.gml:61-65; фактически ~77 точек (близко) |
| 109 | `ui_sfx_map`/`ui_snd_select` задаёт `obj_Init.Create_0`, все ключи → `snd_text_ch1` | OK — obj_Init/Create_0.gml:103-115 |
| 109 | `snd_text_ch1` — дефолтный voice-blip (`map_emotions` → `current_voice`) | OK — map_emotions.gml:15,33,39; scr_inventory_init.gml:58 |

## Громкости и volume push/pop

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 115 | `__current_master_volume`: пишут obj_Init (1.0), `scr_applySettings`, `obj_settingsManager`, push/pop | OK — obj_Init:45; scr_settingsManager.gml:313-314; obj_settingsManager/Create_0.gml:181-182; scr_menu_volume_guard.gml:11,30 |
| 116 | `__music_volume`: obj_Init, `scr_applySettings`, `obj_settingsManager`; читает `__music_get_settings_volume` | OK — obj_Init:46; scr_settingsManager.gml:319; obj_settingsManager:189 |
| 117 | `__sfx_volume`: те же; читает `scr_play_sfx` | OK — obj_Init:47; scr_settingsManager.gml:320; obj_settingsManager:203 |
| 119 | Источник истины — `player_settings.master_volume/music_volume/sfx_volume`, файл `player_settings.dat` | OK — scr_settingsManager.gml:13-15; obj_Init/Create_0.gml:35 |
| 119 | `scr_menu_volume_push(target=0.8)` — 80% текущего с учётом вложенности; `pop` на нуле восстанавливает `player_settings.master_volume` (не снапшот) | OK — scr_menu_volume_guard.gml:4-15, 19-33 |
| 119 | Вызывают: `obj_p3r_pause` (Create/Destroy), `obj_inGameMenu` (ручной push при overlay), `obj_settingsManager`/`scr_settings_step_root` (pop) | OK — obj_p3r_pause/Create_0.gml:5, Destroy_0.gml:13; obj_inGameMenu/Step_0.gml:82; obj_settingsManager/Create_0.gml:263; scr_settings_step_root.gml:34 |

## Ассеты `sounds/` (ls + .yy)

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 123 | Все в `audiogroup_default`, 44100 Hz, без preload; конвенция `music_*`/`mus_*`/`snd_*` | OK — все 8 `.yy` (проверены целиком) |
| 127 | `music_menu`, ogg, 42.7 c; меню-комнаты + форс в `obj_menu`, `obj_p3r_title` | OK — music_menu.yy (42.710205, ogg); on_room_change:28; obj_menu/Create_0.gml:17-18; obj_p3r_title/Create_0.gml:64-65 |
| 128 | `music_SchoolRoutine`, ogg, 138.4 c, дефолт игровых комнат | OK — .yy (138.433); scr_music_init.gml:114 |
| 129 | `mus_intro`, wav, 79.0 c, intro-фазы `obj_sound_test` | OK, но неполно — также в `datafiles/cutscenes/cutscene.json` (`play_music_intro`, `play_music_intro_layered`, строки 46, 50). Ячейку расширил |
| 130 | `mus_loop_calm_loud`, wav, 175.7 c, `volume` ассета 0.39 | OK — .yy (175.67351, volume 0.39). Неполно: также `cutscene.json` (`play_boss_music`, `boss_music_phase`) |
| 131 | `mus_loop_battle`, wav, 175.7 c | OK — .yy (175.67471). Неполно: также `cutscene.json` |
| 132 | `mus_end`, wav, 36.0 c, вызовов в коде нет | OK — .yy (36.0405); `grep mus_end` по objects/scripts/datafiles — 0 |
| 133 | `snd_text_ch1`, wav, 1.7 c — ключи `ui_sfx_map`, `ui_snd_select`, voice-blip | OK — .yy (1.7142857) |
| 134 | `snd_wobble`, wav, 0.33 c — `play_sfx` в `cutscene.json` | OK — .yy (0.329161); cutscene.json:20,59,69. Неполно: также слои в `cutscenes/tests/*.json` |

## Смена комнаты

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 138 | `obj_globalManager.Step` → `scr_global_on_room_change(current_room, room)` | OK — Step_0.gml:22-27 |
| 140 | `music_menu` для `is_menu_room`; список `__service_menu_rooms`: rm_roomMenu, rm_savesSelect, rm_settings, rm_devLoad; иначе `music_default_game_track` | OK — on_room_change.gml:19-31; obj_Init/Create_0.gml:181-186 |
| 141 | Граница меню↔игра — `play_music_immediate`; внутри — `play_music` | OK — on_room_change.gml:49-55 |
| 142 | Persist-гард: `cutscene_active` && `persist_track == music_current` && instance жив; самоочистка | OK — on_room_change.gml:39-45 |

## Катсцены

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 146 | `__cutscene_music_call(func_name, args)` — вызов по имени с разворачиванием массива + warning | OK — scr_cutscene_music.gml:11-21 |
| 150 | `ActionMusicPlay(snd, fade, volume=1.0, persist=true)` ↔ `play_music` (`sound`/`track`, `fade`/`fade_in_seconds`, `volume`, `persist_room_change`) → `play_music_fade`/`play_music_immediate` + `set_music_volume_fade`, пишет `persist_track` | OK — scr_cutscene_music.gml:32-52; factory:655-679. Уточнение: `set_music_volume_fade` вызывается только при `volume != 1.0` (строка 45) — добавлено в ячейку |
| 151 | `ActionMusicStop(fade, use_layered)` ↔ `stop_music`, `stop_boss_music` | OK — scr_cutscene_music.gml:64-77; factory:684-687, 762-767 |
| 152 | `ActionMusicVolume` ↔ `music_volume` | OK — factory:692-695 |
| 153 | `ActionMusicPitch` ↔ `music_pitch` | OK — factory:715-717 |
| 154 | `ActionMusicPause`/`Resume` ↔ `music_pause`/`music_resume` | OK — factory:722-729 |
| 155 | `ActionMusicDuck`/`Unduck` ↔ `music_duck` (`multiplier`)/`music_unduck` | OK — factory:700-710 |
| 156 | `ActionMusicPlayLayered` ↔ `play_boss_music` (`calm`, `battle`, `fade`) | OK — factory:734-757 |
| 157 | `ActionMusicSetIntensity` ↔ `crossfade_music` (`intensity`, `fade`) | OK — factory:899-902 |
| 158 | `ActionMusicIntroLoop` ↔ `play_music_intro` (`intro`/`sound`, `loop`/`track`) | OK — factory:833-857 |
| 159 | `ActionMusicIntroLayered` ↔ `play_music_intro_layered` | OK — factory:862-894 |
| 160 | `ActionMusicPhaseSequence` ↔ `boss_music_phase` (`phases[]`) | OK — factory:772-828 |
| 161 | `ActionPlaySFX(sound, volume, pitch)` ↔ `play_sfx` → `scr_play_sfx` | OK с уточнением — вызов идёт через `cutscene_runtime_play_sfx` (scr_cutscene_classes.gml:1271-1273, 3161). Ячейку дополнил |
| 163 | Живые shorthand: только `cutscene_music_pitch/pause/resume` | OK — scr_cutscene_music.gml:150-178; factory:717,723,729 |
| 165 | `persist_room_change` дефолт `true` и в конструкторе, и в JSON; снятие пометки при `false` | OK — scr_cutscene_music.gml:32,37,51; factory:673-677 |
| 165 | `finish_cutscene` делает `unduck_music(0)` и `music_persist_track = noone` | OK — obj_cutsceneManager/Create_0.gml:741-747, 756-757 |
| 167 | Snapshot `music`: `current_track, volume, pitch, paused, duck_multiplier, layered_mode, layer2_asset, layer_intensity, persist_track`; `include_music` дефолт `true` | OK — scr_cutscene_classes.gml:784, 821-836 |
| 167 | `__cutscene_restore_music_state`: `audio_exists`, `play_music_immediate`, layered → `play_music_layered` + `set_music_layer_intensity`, затем `set_music_pitch`, `duck_music`, `persist_track`, `set_music_volume_fade`, `pause_music` | OK — scr_cutscene_classes.gml:1015-1072 (порядок точный) |

## Debug overlay и прочее

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 171 | Содержимое overlay: трек, позиция/длительность, Vol→target+fade%, pitch, Duck→target, instance id+статус, intro→loop, prev, PAUSED, layered-имена и интенсивность с цветовой шкалой | OK — Draw_64.gml:25-153 |
| 173 | `obj_sound_test`: меню по `confirm`, двухфазная `play_music_phase_sequence` на `mus_intro`/`mus_loop_calm_loud`/`mus_loop_battle`, `set_music_layer_intensity`, `music_phase_next` | OK — obj_sound_test/Step_0.gml:19-48, 86-101 |
| 175-183 | Ссылки «См. также» | OK — все 7 целей существуют в `docs_new/` и в `_meta/nav_plan.md` |

## Итог

- **WRONG:** 0 (одна неточная формулировка — `room_music_override`, строка 64).
- **MISSING:** 0 (таблица API полная).
- **UNVERIFIABLE:** 0.
- Исправлено при правке страницы: формулировка про `room_music_override`; уточнение no-op `play_music` (не в layered); условие `volume != 1.0` у `ActionMusicPlay`; обёртка `cutscene_runtime_play_sfx` у `ActionPlaySFX`; расширена колонка «Использование» ассетов; в `<!-- sources -->` поправлен диапазон `scr_settingsManager.gml` и добавлен `3155-3164` (`ActionPlaySFX`).
