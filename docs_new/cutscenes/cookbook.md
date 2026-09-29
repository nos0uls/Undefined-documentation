---
title: Рецепты катсцен
tags:
  - cutscenes
  - cutscene-json
  - actors
  - camera
  - dialogue
  - room-transitions
  - music
  - how-to
  - troubleshooting
---

# Рецепты катсцен

Готовые JSON-сцены для `datafiles/cutscenes/`. Все поля проверены по фабрике `cutscene_action_factory` и тестовым файлам `datafiles/cutscenes/tests/`; полный список типов и полей см. в [JSON-действиях](json-actions.md). Время везде задаётся в секундах (конвертация по `settings.fps`, дефолт `60`).

## Спавн актёра и движение

`actor_create` регистрирует инстанс в `actor_map` под ключом `key`, дальше ключ адресует его во всех `target`. `actor_sprite` со sprite-ассетом ставит спрайт на дефолтный `obj_actor`; с object-ассетом (`"obj_dummy"`) спавнится сам объект.

```json title="spawn + move + facing"
{
  "cutscene_id": "spawn_and_move",
  "settings": { "fps": 60 },
  "actions": [
    { "type": "actor_create", "key": "guard", "x": 320, "y": 240, "actor_sprite": "spr_Dummy" },
    { "type": "wait", "seconds": 0.5 },
    { "type": "move", "target": "guard", "x": 420, "y": 240, "speed_px_sec": 120, "collision": true },
    { "type": "set_facing", "target": "guard", "direction": "left" },
    { "type": "actor_destroy", "target": "guard" }
  ]
}
```

`collision: true` заставляет актёра останавливаться о `obj_collider`/`par_decor`/`par_interactable`; `direction` принимает `right`/`left`/`up`/`down` (краткие `r`/`l`/`u`/`d` и числа тоже). Поля `actor_create`, `move`, `set_facing`, `actor_destroy` описаны в [json-actions.md](json-actions.md).

## Диалог с эмоцией

`dialogue` блокирует очередь до конца реплики (`block_queue: true` по умолчанию). `set_emotion` задаёт эмоцию портрета и спрайта перед репликой, `show_emote`: спрайт-реакцию над головой актёра (алиас `emote`).

```json title="dialogue + emotion + emote"
{ "type": "set_emotion", "target": "guard", "emotion": "happy" },
{ "type": "show_emote", "target": "guard", "sprite": "chara_question_o", "seconds": 1.0, "wait": true },
{ "type": "dialogue", "file": "testDialogue.yarn", "node": "Intro-dialogue-CUT", "block_queue": true }
```

`file` обязан содержать `.yarn`; файл ищется сначала в `Dialogues/` (префикс подставляется сам), затем в корне Included Files; при промахе подставляется дефолтный yarn менеджера с warning. `node` задаёт `title:` ноды в файле. Поля `set_emotion`, `show_emote`, `dialogue` описаны в [json-actions.md](json-actions.md); про диалоговую подсистему см. [Диалоги](../systems/dialogue.md).

## Параллельные действия: `parallel`

`parallel` исполняет ветки одновременно и завершается, когда завершены все. Элемент `actions`: либо struct одиночного действия, либо массив (последовательность внутри ветки).

```json title="parallel: камера следит за бегущим актёром"
{ "type": "parallel", "actions": [
    [
      { "type": "move", "target": "guard", "x": 600, "y": 240, "speed_px_sec": 180 }
    ],
    [
      { "type": "camera_track_until_stop", "target": "guard" }
    ],
    { "type": "show_emote", "target": "player", "sprite": "spr_StatHeart", "seconds": 1.0 }
] }
```

`camera_track_until_stop` держит камеру на актёре, пока у него `move_active`: трек заканчивается вместе с `move`. Поля `parallel` и `camera_track_until_stop` описаны в [json-actions.md](json-actions.md).

## Ветвление по флагу: `branch_flag`

Читает `global.flag[key]` (dot-путь вида `"flag.x"`, `"stat.hp"`, `"entity_state.*"` резолвится глубже) и вставляет `true_actions` или `false_actions` в очередь сразу за текущим действием. Операторы: `==`, `!=`, `>`, `<`, `>=`, `<=`, `exists`, `!exists`; неизвестный оператор деградирует в `==` с warning.

```json title="branch_flag по мировому флагу"
{ "type": "set_flag", "key": "guard_met", "value": 1 },
{ "type": "branch_flag", "key": "guard_met", "operator": "==", "value": 1,
  "true_actions": [
    { "type": "dialogue", "file": "testDialogue.yarn", "node": "Bench" }
  ],
  "false_actions": [
    { "type": "dialogue", "file": "testDialogue.yarn", "node": "Intro-dialogue-CUT" }
  ]
}
```

Поля `set_flag` и `branch_flag` описаны в [json-actions.md](json-actions.md); про хранилище флагов см. [глобальное состояние](../architecture/global-state.md).

## Частичный контроль: игрок ходит по сцене

`partial_control` с `control_type: 1` (WHITELIST) возвращает игроку ввод из `allowed_actions`, а `wait_for_interact` ждёт активации конкретного объекта. `timeout` страхует от софтлока; значение `timeout_action: "abort_parallel"` (и `interact_action` тоже) по событию обрывает соседние ветки `parallel`: в примере стоит `"continue"`.

```json title="partial_control + wait_for_interact"
{ "type": "partial_control", "control_type": 1,
  "whitelist": ["guard"], "allowed_actions": ["move", "interact"] },
{ "type": "wait_for_interact", "target": "guard", "timeout": 30, "timeout_action": "continue" },
{ "type": "partial_control", "control_type": 0 },
{ "type": "dialogue", "file": "testDialogue.yarn", "node": "Cutscene-Bridge-Demo" }
```

Пустой `allowed_actions` пропускает только `confirm`; `whitelist` фильтрует, с какими объектами можно взаимодействовать. Цель `wait_for_interact` обязана быть объектом, реально обрабатывающим взаимодействие (вызывает `scr_interaction`: наследники `par_interactable` вроде NPC/`obj_bench`, или `obj_save`): очередь `global.__interacted_targets` пишут только они. Голый `obj_actor` (`guard` из первого рецепта) интеракцию не регистрирует, поэтому ожидание сработает только по `timeout`. Механика режимов и софтлоки: [Частичный контроль](partial-control.md); поля `partial_control` и `wait_for_interact` описаны в [json-actions.md](json-actions.md).

## Переход комнаты внутри катсцены

`room_change` — блокирующий переход с фейдом через `obj_changingRoomsController`: `player_x`/`player_y` обязательны, `actors` задаёт позиции актёров в новой комнате (ключ → `{x,y}` или `[x,y]`); актёры со spec пересоздаются на Room Start менеджера.

```json title="fade + play_music(persist) + room_change"
{ "type": "parallel", "actions": [
    { "type": "fade_out", "seconds": 0.5 },
    { "type": "play_music", "sound": "music_SchoolRoutine", "fade": 0.5, "persist_room_change": true }
] },
{ "type": "room_change", "room": "rm_cutsceneTest", "player_x": 160, "player_y": 120,
  "actors": { "guard": { "x": 200, "y": 120 } } },
{ "type": "fade_in", "seconds": 0.5 }
```

`persist_room_change: true` (дефолт) помечает трек в `global.music_persist_track`: музыка комнаты его не затирает, пока идёт катсцена; на финише `finish_cutscene` пометку снимает. Поля `room_change` и `play_music` описаны в [json-actions.md](json-actions.md); про переходы см. [Смена комнат](../systems/room-transitions.md).

## Затемнение и музыка

`fade_out`/`fade_in` идут к альфе `1`/`0` и блокируют очередь на время фейда, а в `parallel` они отрабатывают фоном, пока соседняя ветка играет звук и ждёт.

```json title="fade_out → музыка → fade_in"
{ "type": "parallel", "actions": [
    { "type": "fade_out", "seconds": 0.6, "color": "black" },
    [
      { "type": "stop_music", "fade": 0.6 },
      { "type": "wait", "seconds": 0.6 },
      { "type": "play_music", "sound": "music_SchoolRoutine", "fade": 0.8, "volume": 0.8 },
      { "type": "play_sfx", "sound": "snd_wobble", "volume": 1, "pitch": 1 }
    ]
] },
{ "type": "fade_in", "seconds": 0.6 }
```

`color` принимает имена (`"black"`, `"white"`…) и hex-строки `"#RRGGBB"`. Поля `fade_in`, `fade_out`, `play_music`, `stop_music`, `play_sfx` описаны в [json-actions.md](json-actions.md).

## Привязка объекта к актёру

`attach_to_target` крепит проп к актёру: позиция (и по флагам `image_xscale`, `image_yscale`, depth) следует за родителем каждый кадр. `detach` отвязывает; `destroy_after_detach` убирает проп заодно.

```json title="эмоция-объект над головой"
{ "type": "spawn_entity", "object": "obj_dummy", "key": "prop", "x": 320, "y": 216, "depth": -216 },
{ "type": "attach_to_target", "target": "prop", "parent": "guard",
  "offset_x": 0, "offset_y": -24, "follow_facing": true, "follow_scale": true,
  "follow_depth": true, "duration_seconds": 0.3, "detach_on_cutscene_end": true },
{ "type": "move", "target": "guard", "x": 400, "y": 240, "speed_px_sec": 90 },
{ "type": "detach", "target": "prop", "destroy_after_detach": true }
```

Поле `depth` у `spawn_entity` для наследников `par_depth` (включая `obj_dummy` в примере) игнорируется: их Create перезаписывает глубину выражением `-y`; осмысленно оно только для объектов вне иерархии. Механика реестра `global.__cutscene_attachments` и follow-флагов: [Актёры и камера](actors-and-camera.md); поля `spawn_entity`, `attach_to_target`, `detach` описаны в [json-actions.md](json-actions.md).

## Troubleshooting

!!! warning "Экшен молча пропал"
    Фабрика отклоняет действие с записью `[CUTSCENE] FACTORY: action '…' rejected` и причиной: нет `target`, пропущены `x`/`y`, пустой `key`, `file` без `.yarn`, нераспознанный `direction`, отсутствующий `room`. Первый шаг отладки — консоль.

!!! warning "target не найден"
    `resolve_target` возвращает `noone`, и `start()` действия пишет `WARNING: … не найден ("…"), действие пропущено`. Порядок резолва строки: `"player"`/`"player_body"` (регистронезависимо, приоритет) → ключ `actor_map` (регистрозависимо: `Guard` и `guard` разные ключи) → имя object-ассета (берётся первый инстанс). `"target": null` в JSON становится `undefined` → `noone` и отклоняется как отсутствующий.

!!! note "Слой `Instances`"
    Слоя `"Instances"` в комнате может не быть: `scr_layer_ensure_instances()` создаёт его на depth `0`; им пользуются `cutscene_load_json` (менеджер) и `ActionDialogue` (текстбокс). Сами актёры спавнятся через `instance_create_depth` и слоя не требуют. Ручные `instance_create_layer` на `"Instances"` в комнатах без слоя делайте через тот же хелпер.

!!! warning "Камера не едет / стоит"
    Пока играет катсцена, follow-камера игрока выключена (`global.cutscene_camera_override`), поэтому без camera-действия вид застывает на стартовой позиции. У `camera_pan` поля `x`/`y`: абсолютная позиция **верхнего левого угла** вида; `camera_pan_obj` (`target`) и `camera_center` (`x`/`y`) центрируют вид на цели/точке. В `camera_pan_speed` `x`/`y`: скорости px/кадр, а `speed`/`speed_px_sec` игнорируются. `camera_track` без `seconds` завершается почти мгновенно (таймер ~1 кадр), поэтому для долгого слежения берите `camera_track_until_stop`.

!!! warning "Актёр не дошёл"
    `move` с `collision: true` у актёра на `obj_actor` при препятствии ставит `move_blocked` и warning `движение остановлено коллизией`, то есть действие завершается «не у цели». `follow_path` идёт другим драйвером: зависание снимает stall-таймаут (~60 кадров) с warning `move stalled by collision`, точка считается недостижимой, а `move_blocked` не пишется. Проверяйте маршрут или выключайте `collision` для сценовых перемещений.

!!! danger "Софтлок ожидания"
    `wait_for_interact` с `timeout: 0` под `partial_control` без `confirm`/`interact` в `allowed_actions` вешает очередь навсегда: ввод глушится, очередь взаимодействий не пополняется. Указывайте `timeout` или разрешайте `interact`. Подробно: [Частичный контроль](partial-control.md).

!!! warning "Секунды и кадры"
    В JSON время задаётся в секундах (`seconds`/`duration`/`time`); в кадрах только `frames`. В `c_*`-DSL и конструкторах `Action*` время задаётся в кадрах. Ключ `duration_frames` в `tween`/`tween_camera` исторически читается как секунды (так экспортирует Undefscene).

!!! warning "Не проверено"
    Поведение `auto_walk`-поля актёра заявлено в JSON (`auto_walk`), но никем не читается, визуального эффекта у него нет. Если в вашей сборке появится потребитель, перепроверьте по `obj_actor`.

## См. также

- [JSON-действия](json-actions.md): все типы и поля `actions[]`
- [Актёры и камера](actors-and-camera.md): `actor_map`, `actor_create`, camera-действия
- [Частичный контроль](partial-control.md): режимы `partial_control`, `wait_for_interact`
- [Архитектура менеджера](architecture.md): очередь, `room_change`, `finish_cutscene`
- [Обзор катсцен](overview.md): как запустить сцену
- [Ноды Undefscene](../undefscene/nodes.md): те же действия в редакторе

<!-- sources: scripts/cutscene_action_factory/cutscene_action_factory.gml:13-53, 157-215, 264-296, 335-366, 480-507, 906-1040, 1052-1131, 1200-1241; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:2109-2304, 2505-2632, 3210-3261, 3984-4056, 4526-4605, 4607-4678, 4712-4804; scripts/cutscene_load_json/cutscene_load_json.gml:455-477; scripts/scr_cutscene_music/scr_cutscene_music.gml:24-77; scripts/scr_global_on_room_change/scr_global_on_room_change.gml:25-55; objects/obj_cutsceneManager/Create_0.gml:426-497, 659-758; objects/obj_actor/Step_0.gml:3-133; scripts/scr_layer_ensure_instances/scr_layer_ensure_instances.gml; scripts/scr_inputApi/scr_inputApi.gml:112-137; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml:1-8; datafiles/cutscenes/test_actors.json; datafiles/cutscenes/cutscene.json; datafiles/cutscenes/tests/actor_create.json; datafiles/cutscenes/tests/attach_detach.json; datafiles/cutscenes/tests/branch_true.json; datafiles/cutscenes/tests/camera_track.json; datafiles/cutscenes/tests/emote.json; datafiles/cutscenes/tests/fade_in.json; datafiles/cutscenes/tests/fade_out.json; datafiles/cutscenes/tests/partial_control.json; datafiles/cutscenes/tests/play_music.json; datafiles/cutscenes/tests/room_change.json; datafiles/cutscenes/tests/wait_for_interact.json; datafiles/Dialogues/testDialogue.yarn -->
