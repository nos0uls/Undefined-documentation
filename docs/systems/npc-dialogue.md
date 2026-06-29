---
tags:
  - dialogue
  - runtime
---

# NPC и диалоги (NPC Dialogue)

Система взаимодействия с NPC и объектами, запускающими Yarn-диалоги через единую точку входа `scr_interaction`.

## Обзор

Каждый интерактивный объект или NPC вызывает `scr_interaction` с именем Yarn-файла и стартовой ноды. `scr_interaction` проверяет нажатие `confirm`, существование `obj_pointMarker`, отсутствие UI-блокировки и условия `partial control` во время катсцены. Если все условия выполнены, вызывается `readDialogue`, который создаёт `textboxTest_scribble` и блокирует движение игрока.

Выбор конкретной ноды диалога задаётся в объекте-инициаторе (например, `obj_asher` использует ноду `Cutscene-Bridge-Demo` из `testDialogue.yarn`). `scr_npc_pick_dialogue` существует в проекте, но в текущей версии не содержит логики и не вызывается.

## Архитектура / API

### Скрипты

| Скрипт | Описание |
|--------|----------|
| `scr_interaction` | Единая проверка взаимодействия. Принимает `_scriptToReadFrom`, `_node`, `_use_mask_check`. Проверяет `obj_pointMarker`, `scr_checkUIBlocking`, `partial control` и вызывает `readDialogue`. |
| `interactionWithNPCsOrObjects` | Legacy-обёртка над `scr_interaction` с `_use_mask_check = false`. |
| `interactionWithMainCast` | Legacy-обёртка над `scr_interaction` с `_use_mask_check = true`. |
| `readDialogue` | Создаёт `textboxTest_scribble` в координатах камеры, передаёт `dialogue_filename` и `dialogue_node`, блокирует `obj_player.can_move`. |
| `scr_npc_pick_dialogue` | Заглушка. В текущей версии не используется. |
| `scr_parse_emote` | Парсит speaker-строку Yarn формата `DisplayName [code:emotion]: Text` и возвращает actor, emotion, display_name, ресурсы портрета. |

### Условия взаимодействия

1. Игрок нажал `confirm`.
2. Существует `obj_pointMarker` (маркер перед игроком).
3. `scr_checkUIBlocking(false, false)` возвращает `false`.
4. Если активна катсцена:
   - `partial_control_type == 0` — взаимодействие заблокировано.
   - `partial_control_type == 1` — только объекты из `partial_control_whitelist`.
   - `partial_control_type == 2` — полная свобода.
5. Маркер попадает в bbox (`point_in_rectangle`) или маску (`place_meeting`) цели.

### Примеры объектов-инициаторов

| Объект | Yarn-файл | Нода |
|--------|-----------|------|
| `obj_asher` | `testDialogue.yarn` | `Cutscene-Bridge-Demo` |
| `obj_bench` | `testDialogueBlue.yarn` | `Blue` |
| `obj_sheepFountain` | `fountain.yarn` | `RM_002: FOUNTAIN` |
| `obj_dialoguetest` | `testChoices.yarn` | `testChoices` |

## Примеры

### Запуск диалога из NPC

```gml title="obj_asher/Step_0"
scr_interaction("testDialogue.yarn", "Cutscene-Bridge-Demo");
```

### Проверка через маску (Main Cast)

```gml title="interactionWithMainCast"
interactionWithMainCast("main_cast.yarn", "intro");
// внутри вызывает scr_interaction(..., true)
```

### Парсинг строки Yarn

```gml title="scr_parse_emote"
var _parsed = scr_parse_emote("asher:happy", "Asher", _prev_actor, _prev_emotion, _prev_display);
// _parsed.actor = "asher", _parsed.emotion = "happy", _parsed.display_name = "Asher"
```

## Troubleshooting

!!! warning "Диалог не запускается"
    Убедитесь, что `obj_pointMarker` существует. Он создаётся в `obj_player/Create_0` и используется всеми интерактивными объектами. Если игрок был создан без вызова `scr_global_handle_dev_spawn`, маркер может отсутствовать.

!!! warning "Взаимодействие заблокировано во время катсцены"
    Проверьте `partial_control_type` активного менеджера катсцены. `0` полностью блокирует взаимодействие, `1` требует whitelist.

!!! note "NPC выбирает ноду в объекте, а не в скрипте"
    В текущей версии нода диалога задаётся непосредственно в `Step_0` объекта. Для динамического выбора ноды нужна собственная логика в объекте или расширение `scr_npc_pick_dialogue`.

## См. также

- [Система ввода](input.md) — `scr_input_pressed`, `scr_checkUIBlocking`
- [Система эмоций](emote.md) — `scr_parse_emote`, эмоции над персонажами
- [Диалоговые портреты](dialogue-portraits.md) — `textboxTest_scribble`, портреты
- [Катсцены: Partial Control](cutscenes/partial-control.md) — настройки partial control
- [GML-скрипты](../code-reference/gml-scripts.md) — полный список скриптов
