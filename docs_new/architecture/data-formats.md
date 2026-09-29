---
title: Форматы данных на диске
tags:
  - architecture
  - data-formats
  - persistence
  - save-system
  - settings
  - cutscene-json
  - dialogue
---

# Форматы данных на диске

Справочник файлов, которые Undefinedtale-888 читает и пишет: сейвы слотов, `game_state.dat`, реестр `entity_state`, `player_settings.dat`, JSON катсцен и yarn-диалоги.

## Карта файлов { #file-map }

| Файл | Путь в рантайме | Формат | Писатель / читатель |
|------|-----------------|--------|---------------------|
| `save1.txt` … `save3.txt` | `working_directory` | Позиционный текст + JSON-строки | `scr_saveSave` / `scr_saveLoad` |
| `game_state.dat` | `working_directory` | `key=value` | `scr_game_state_save` / `scr_game_state_load` |
| `player_settings.dat` | `working_directory` | `key=value` | `scr_saveSettings` / `scr_loadSettings` |
| `entity_state` | Не файл — секция внутри сейва | JSON-struct | `scr_entity_state_*` |
| `cutscenes/*.json` | `working_directory` (Included Files) | JSON | `cutscene_load_json` |
| `cutscenes/cutscene_engine_settings.json` | `working_directory` (Included Files) | JSON | `cutscene_load_engine_settings` |
| `Dialogues/*.yarn` | `working_directory` (Included Files) | Yarn (Chatterbox) | `ChatterboxLoadFromFile` |

Сейвы слотов и `game_state.dat` пишутся атомарно: данные идут в `<file>.tmp`, затем `file_rename` переносит его поверх целевого (fallback — `file_copy` + `file_delete`). `player_settings.dat` атомарности не имеет — `scr_saveSettings` пишет напрямую в целевой файл.

## Сейв `<slot>.txt` { #save-slot }

Слоты — `"save1"`, `"save2"`, `"save3"` (единый список в `scr_save_slot_names`). Путь: `working_directory + global.current_save_slot + ".txt"`. Формат позиционный, строго append-only: новые поля добавляются только перед строкой версии — «шапку» (строки 1–5) позиционно читают `obj_Init` и `scr_save_read_metadata`.

Текущая версия схемы — `#macro SAVE_FORMAT_VERSION 3` в `scr_saveSave`. Номер версии всегда пишется последней строкой файла.

### Раскладка строк (v3)

| № | Содержимое | Тип | Источник |
|---|------------|-----|----------|
| 1 | `x` игрока | real | `obj_player.x` |
| 2 | `y` игрока | real | `obj_player.y` |
| 3 | `facing_direction` | real | `obj_player.facing_direction` (индекс `global.DIR`) |
| 4 | Имя комнаты | string | `room_get_name(room)` |
| 5 | Время в сейве, секунды | real | `global.__save_playtime_seconds` |
| 6 | Инвентарь | JSON array | `inventory_serialize(global.inventory)` |
| 7 | Индекс экипированного оружия | real −1..7 | поиск по `name`+`itemType` в `global.inventory` |
| 8 | Индекс экипированной брони | real −1..7 | то же для `global.equipped_armor` |
| 9 | Флаги сюжета | JSON object | `global.flag` (`"{}"` при отсутствии) |
| 10 | Прогресс сюжета | real | `global.plot` (дефолт `0`) |
| 11 | Реестр сущностей | JSON object | `global.entity_state` (`"{}"` при отсутствии) |
| 12 | Статы игрока | JSON object | `global.stat_*` + `global.player_name` |
| 13 | Переменные диалогов | JSON object / `""` | `ChatterboxVariablesExport()` |
| 14 | Версия схемы | real | `SAVE_FORMAT_VERSION` = `3` |

Инвентарь (строка 6) — массив из 8 записей: пустой слот — `null`, предмет — `{ "__type": …, "name": …, "description": … }`. `__type` определяет конструктор при загрузке (`item_deserialize`):

| `__type` | Дополнительные поля | Конструктор |
|----------|---------------------|-------------|
| `item` | — | `Item` |
| `weapon` | `damage` | `WeaponItem` |
| `armor` | `defense` | `ArmorItem` |
| `food` | `heal`, `amount` | `FoodItem` |

Статы (строка 12) — структура:

```json
{"hp":20,"maxhp":20,"atk":10,"def":10,"base_atk":0,"base_def":0,"lv":1,"gold":0,"name":"HUMAN"}
```

При записи отсутствующие `global.stat_*` подменяются дефолтами: `hp`/`maxhp` `20`, `atk`/`def` `10`, `base_atk`/`base_def` `0`, `lv` `1`, `gold` `0`, `name` `"HUMAN"`. Сохранённые `atk`/`def` — write-only: при загрузке эффективные значения пересчитывает `scr_stats_recalc` из `base_*` и экипировки.

Строка 13 — `json_encode` карты переменных Chatterbox (константы исключены); при исключении в `ChatterboxVariablesExport` пишется пустая строка.

!!! warning "Ручная правка сейва"
    Формат позиционный: вставка или удаление строки в середине файла сдвигает раскладку и ломает детект версии (строка версии распознаётся только по позиции после `entity_state`). Единственные безопасные правки — значения на своих строках и добавление полей внутрь JSON-объектов.

### Детект версии в `scr_saveLoad`

Все строки после 4-й читаются под guard `file_text_eof` — усечённый или старый файл не обрывает разбор. После строки 11 логика такая:

1. **EOF** → версия `1`.
2. Следующая строка непустая и начинается с `{` → раскладка v3: stats JSON, затем строка Chatterbox, затем номер версии.
3. Иная непустая строка → номер версии (`real(...)`), формат v2.
4. `_save_version > SAVE_FORMAT_VERSION` → отказ: сейв записан более новой сборкой, раскладка неизвестна.

### Миграция v1/v2 → v3

Отсутствующие секции получают дефолты: playtime `0`, инвентарь — `scr_inventory_init()` (стартовый набор), экипировка — `undefined`, `flag` — `{}`, `plot` — `0`, `entity_state` — `{}`.

Статы в v1/v2 не хранились — применяются дефолты сессии (совпадают с `scr_inventory_init`): `stat_hp`/`stat_maxhp` `99`, `stat_base_atk`/`stat_base_def` `0`, `stat_lv` `20`, `stat_gold` `99`, `player_name` `"CHARA"`.

Для сейвов v3 без `base_atk`/`base_def` база выводится из эффективных значений: `max(0, atk − equipped_weapon.damage)` и `max(0, def − equipped_armor.defense)`. Пустая или не-JSON строка Chatterbox → `ChatterboxVariablesResetAll()` + `ChatterboxVariablesClearVisitedAll()`; JSON-строка → `ChatterboxVariablesImport`.

## `game_state.dat` { #game-state }

Мета-состояние между запусками. Путь: `working_directory + global.game_state_file` — имя `"game_state.dat"` задаёт `obj_Init`; при отсутствии файла по этому пути загрузчик проверяет голый относительный `global.game_state_file` (файл от старой версии).

Формат — строки `key=value`. Читатель разбивает по первому `=`, триммит ключ и значение; применяются только ключи, существующие в дефолтной структуре, неизвестные пропускаются. Значение `"true"`/`"false"` → bool, иначе попытка `real()`, при неудаче — строка как есть.

| Ключ | Тип | Дефолт | Назначение |
|------|-----|--------|------------|
| `last_played_save_slot` | string | `"save1"` | Слот для кнопки «Продолжить»/фокуса меню |
| `total_playtime_seconds` | real | `0` | Суммарное время игры за все запуски |

Записи пишутся в том порядке, в каком их отдаёт `variable_struct_get_names` по переданной структуре.

**Кто пишет:** `obj_saveManager` после сохранения/загрузки слота и при удалении слота (fallback на другой слот), `scr_global_quick_save` — обновляют `last_played_save_slot`. При выходе `obj_globalManager` (Game End, `Other_3`) копирует `global.__total_playtime_seconds` в `total_playtime_seconds` и вызывает `scr_game_state_save`.

`scr_resetGameToDefault` удаляет `game_state.dat` и все слоты, затем ставит `global.clean_state = true`. Game End проверяет этот guard и не пишет файл после полного сброса — иначе wipe отменялся бы на выходе.

## Реестр `entity_state` { #entity-state }

`global.entity_state` — struct (создаётся в `obj_Init`), отдельным файлом не существует: целиком сериализуется в строку 11 сейва и восстанавливается оттуда `scr_saveLoad`.

**Ключ записи:** `"<room_name>:<entity_id>"`. `entity_id` — инстанс-поле `par_interactable`; если не задан в редакторе/коде, fallback детерминированный: `"<object_name>:<xstart>:<ystart>"` (стабилен между сессиями, в отличие от instance `id`).

**Структура record** (пишет `__entity_state_save` в `par_interactable`):

| Поле | Тип | Описание |
|------|-----|----------|
| `interaction_count` | real | Число взаимодействий с сущностью |
| `seen_dialogues` | array | Узлы диалогов вида `"file.yarn:Node"` |
| `x`, `y` | real | Позиция на момент записи |
| *custom* | any | Поля из `_custom_fields` сливаются поверх |

**Зарезервированная сущность `"_room"`:** `scr_world_flag_set/get` хранит персистентные комнатные флаги в записи `"<room_name>:_room"` под полем `flags` — `{"flags": {"flag_name": value}}`. Сессионный `global.room_flags` в сейв не входит и сбрасывается при загрузке.

**Жизненный цикл:** восстановление — `__entity_state_restore` в `Create_0` и `Other_4` (Room Start) `par_interactable`; запись — `__entity_state_save` в `Other_5` (Room End) и после каждого взаимодействия в `scr_interaction` (инкремент `interaction_count`, добавление `"file:node"` в `seen_dialogues`).

## `player_settings.dat` { #settings-file }

Имя файла — `"player_settings.dat"` (`global.settings_file` в `obj_Init`), относительный путь — `working_directory`. Формат — строки `key=value`; порядок записи — порядок ключей `global.default_settings`.

Разбор: первый `=`, trim ключа и значения; неизвестные ключи игнорируются и выпадают при перезаписи. Тип значения выводится из типа дефолта: для bool-ключей `"true"`/`"false"` или число `!= 0`; для real-ключей число либо `"true"`/`"false"` → `1`/`0`; для string — строка как есть.

После разбора — валидация: bool-ключ должен остаться bool; real-ключ — real без NaN; значения `input_*` сверяются с `scr_input_normalize_key` (допустимы `-1` — слот пуст — и целые `2..255`; `vk_lshift`/`vk_rshift` сводятся к `vk_shift`; `vk_nokey`, `vk_anykey`, дробные и вне диапазона не проходят) — при расхождении ключ откатывается к дефолту; прочие real-поля клампятся в `0..1`. `need_resave` ставят отсутствие файла, пропущенный ключ и любое исправленное валидацией значение — файл перезаписывается объединёнными настройками.

| Ключ | Тип | Дефолт | Описание |
|------|-----|--------|----------|
| `debug_enabled` | bool | `false` | Отладочный режим (F-клавиши, оверлеи) |
| `master_volume` | real | `1.0` | Общая громкость (`audio_master_gain`) |
| `music_volume` | real | `1.0` | Громкость музыки |
| `sfx_volume` | real | `1.0` | Громкость звуков |
| `fullscreen` | bool | `false` | Не используется: режим окна задаёт `fullscreen_borderless` |
| `fullscreen_borderless` | bool | `false` | Безрамочное окно на весь экран |
| `devload_focus` | bool | `false` | Фокус меню на кнопке загрузки (dev) |
| `input_<action>1`, `input_<action>2` | real | см. ниже | Код клавиши vk_* / `ord()`; `-1` — слот пуст |

Действия (единый список `scr_input_actions_list`): `up`, `down`, `left`, `right`, `run`, `confirm`, `back`, `menu`, `delete` — у каждого два слота. Дефолтные бинды: `up/down/left/right` — стрелки `vk_up`/`vk_down`/`vk_left`/`vk_right`; `confirm` — `Z` + `vk_enter`; `run` — `vk_shift`; `back` — `X` + `vk_shift`; `menu` — `C` + `vk_escape`; `delete` — `B`. Вторые слоты у `up/down/left/right`, `run` и `delete` пусты (`-1`). В файле коды пишутся десятичными числами (`input_up1=38`, `input_confirm1=90`).

!!! note "Авто-ресейв файла"
    `scr_loadSettings` перезаписывает `player_settings.dat`, когда файл отсутствует, ключа нет или значение исправлено валидацией: отсутствующие ключи дописываются, невалидные значения откатываются к дефолту. Неизвестные ключи сами по себе ресейв не вызывают, но при перезаписи стираются; то же со строками без `=` — комментариев в файле быть не должно.

## Cutscene JSON { #cutscene-json }

Загрузчик — `cutscene_load_json(path)`. Префиксы `./` и `datafiles/` в начале пути срезаются в любом порядке: в рантайме Included Files лежат без каталога `datafiles/`, рабочий путь — `cutscenes/<имя>.json`. UTF-8 BOM срезается по сигнатуре `EF BB BF`; файл парсится `json_parse`, корень обязан быть объектом.

### Верхний уровень

| Поле | Тип | Дефолт | Назначение |
|------|-----|--------|------------|
| `cutscene_id` | string | `""` | Идентификатор катсцены (идёт в `obj_cutsceneManager.cutscene_id`) |
| `schema_version` | real | — | Версия схемы экспортёра; загрузчиком не читается |
| `settings` | object | `{}` | Параметры сцены (ниже) |
| `actions` | array | — | Обязательный массив действий; отсутствует или не массив → `noone` |

Поля `settings`:

| Поле | Тип | Дефолт | Назначение |
|------|-----|--------|------------|
| `fps` | real | `default_fps` движка | FPS сцены для конвертаций `seconds` → кадры; принимается только диапазон `1..240` |
| `skippable` | bool | `true` | `false` запрещает пропуск сцены клавишей back |

### Массив `actions`

Каждый элемент — объект `{ "type": <имя>, ... }`; остальные поля зависят от типа и разбираются фабрикой `cutscene_action_factory` — полный список в [JSON-действиях](../cutscenes/json-actions.md).

Служебные элементы схемы экспортёра: `{"type": "start"}` — не действие; у первого элемента из него читается `debug` (bool, включает лог менеджера); `{"type": "end"}` — конец списка, действия после него не выполняются.

Имя `type` нормализуется: lowercase + trim, затем алиасы приводятся к canonical-именам:

| Алиас в JSON | Canonical `type` |
|--------------|------------------|
| `shakeobj` | `shake_object` |
| `visible` | `set_visible` |
| `instant_mode` | `set_instant` |
| `waittalk`, `wait_talk` | `wait_for_dialogue` |
| `depth` | `set_depth` |
| `facing` | `set_facing` |
| `autofacing` | `auto_facing` |
| `autowalk` | `auto_walk` |

Неизвестный тип → warning в лог, элемент пропускается. Длительности читаются как `frames` (приоритет) или `seconds` (конвертация через `fps` сцены). Направления принимаются строками `"right"/"r"`, `"left"/"l"`, `"up"/"u"`, `"down"/"d"` или числом; нераспознанное значение отклоняет действие. Цвета — имена (`black`, `white`, `red`, …) или hex `#RRGGBB`/`RRGGBB`.

## `cutscene_engine_settings.json` { #engine-settings }

Глобальные настройки движка катсцен. В проекте — `datafiles/cutscenes/cutscene_engine_settings.json`, в рантайме ищется `cutscenes/cutscene_engine_settings.json`. Читает `cutscene_load_engine_settings(_force_reload)`: результат кэшируется в `static` до конца сессии, структура общая для всех потребителей и read-only по контракту. При отсутствии или битом JSON возвращаются дефолты.

| Поле | Тип | Дефолт | Назначение |
|------|-----|--------|------------|
| `schema_version` | real | `1` | Больше поддерживаемой — warning, файл читается как есть |
| `engine_version` | string | `"1.0.0"` | Зарезервировано, потребителей нет |
| `default_fps` | real | `60` | FPS по умолчанию; вне `1..240` → `60` |
| `strict_mode_default` | bool | `false` | Зарезервировано (strict-валидация не реализована) |
| `default_actor_object` | string | `"obj_actor"` | Объект-актёр по умолчанию |
| `default_emote_sprite` | string | `"chara_question_o"` | Спрайт эмоции по умолчанию |
| `whitelist.run_functions` | string[] | `[]` | Advisory-список допустимых функций для `run_function` |
| `whitelist.branch_conditions` | string[] | `[]` | Advisory-список условий для `branch` |
| `debug.enable_extended_log` | bool | `false` | Расширенный консольный лог (watchdog) |
| `debug.show_overlay` | bool | `false` | Визуальный debug-оверлей |

## Yarn-диалоги { #yarn }

Файлы лежат в `datafiles/Dialogues/*.yarn`; `CHATTERBOX_INCLUDED_FILES_SUBDIRECTORY` = `"Dialogues"` — загрузка идёт по имени файла через `ChatterboxLoadFromFile("testDialogue.yarn")`. `obj_Init` грузит `testDialogue.yarn` при старте; остальные файлы подгружает `textboxTest_scribble` по запросу (`dialogue_filename`), если файл ещё не в системе (`ChatterboxIsLoaded`). Точка входа в диалог — `readDialogue(filename, node)`.

### Структура узла

```text title="Узел yarn — пример по мотивам Dialogues/testDialogue.yarn и testChoices.yarn"
#__PrivCrochet_version:1
__PrivCrochet_colorID: 0
__PrivCrochet_position: 644,133
__PrivCrochet_tags:
title: Intro-dialogue-CUT
---
Chara [chara:question]: Текст реплики с [wave]разметкой[/wave].
<<c_begin("dialogue_bridge_demo")>>
[]
-> Вариант ответа
    Реплика после выбора
    <<jump OtherNode>>
===
```

- **Заголовки** — строки `key: value` до разделителя `---`. Обязателен `title:` (имя узла для `<<jump>>`/`readDialogue`); `__PrivCrochet_*` — служебные поля редактора Crochet (позиция, цвет, теги), Chatterbox читает их как обычные заголовки.
- **`---`** — конец заголовков, дальше тело узла.
- **`===`** — конец узла; следующий блок заголовков открывает новый узел.
- **`#`** — начало метаданных до конца строки (`\#` экранирует; файловый тег `#__PrivCrochet_version:1` — такой же маркер), **`//`** — комментарий до конца строки (внутри `<< >>` не действует). Оба маркера срабатывают в любом месте строки, не только в её начале.
- **`->`** — вариант выбора; его тело — строки с большим отступом.
- **`<< >>`** — команда: `<<jump Node>>`, `<<wait>>`, `<<set>>` и произвольные вызовы. `CHATTERBOX_ACTION_MODE` = `1` — содержимое исполняется как выражение; функции должны быть зарегистрированы `ChatterboxAddFunction`. `cutscene_register_chatterbox_functions` (вызывается в `obj_Init`) регистрирует мост катсцен: `c_begin`, `c_play`, `c_end`, `c_wait`, `c_walk`, `c_waittalk`, `c_speaker`, `c_facing`, `c_emote`, `c_sfx`, `c_soundplay`, `c_var`, `c_var_lerp_to`, `c_tween`, `c_fadein`, `c_fadeout`, `cutscene_play_json` и др.
- **Реплика** — `Спикер [code:emotion]: текст`. Текстбокс разбирает строку через `ChatterboxGetContentSpeaker` (имя) и `ChatterboxGetContentSpeakerData` (содержимое `[...]` → `scr_parse_emote` выбирает портрет); `[тег]`-вставки внутри реплики (`[wave]`, `[delay, 400]`, `[c_red]`) — разметка Scribble, литеральная скобка экранируется `[[`.
- Переменные узлов и visited-метки попадают в сейв строкой 13 (`ChatterboxVariablesExport`/`ChatterboxVariablesImport`).

## См. также

- [Система сохранений](../systems/save-system.md) — жизненный цикл сейва, `obj_saveManager`, слоты
- [Глобальное состояние](global-state.md) — `global.flag`, `global.plot`, `global.entity_state`, playtime-глобалы
- [Инициализация](initialization.md) — порядок загрузки файлов в `obj_Init`
- [JSON-действия катсцен](../cutscenes/json-actions.md) — все типы `actions` с параметрами
- [GML-DSL катсцен](../cutscenes/gml-dsl.md) — `c_*`-функции, доступные в yarn
- [Диалоги](../systems/dialogue.md) — `textboxTest_scribble`, `scr_parse_emote`, воспроизведение узлов
- [Инвентарь и статы](../systems/inventory-and-stats.md) — конструкторы предметов, `scr_stats_recalc`
- [Ввод](../systems/input.md) — карта `input_map`, ребинд клавиш

<!-- sources: scripts/scr_saveSave/scr_saveSave.gml; scripts/scr_saveLoad/scr_saveLoad.gml:139-287,353-430; scripts/scr_game_state/scr_game_state.gml; scripts/scr_entity_state/scr_entity_state.gml; scripts/scr_settingsManager/scr_settingsManager.gml; scripts/cutscene_load_json/cutscene_load_json.gml; scripts/cutscene_load_engine_settings/cutscene_load_engine_settings.gml; scripts/constructorsForInventory/constructorsForInventory.gml; scripts/c_cmd/c_cmd.gml:141-209; scripts/__ChatterboxConfigMacros/__ChatterboxConfigMacros.gml; scripts/ChatterboxLoadFromFile/ChatterboxLoadFromFile.gml; scripts/ChatterboxVariablesExport/ChatterboxVariablesExport.gml; scripts/__ChatterboxSplitBody/__ChatterboxSplitBody.gml:160-198; scripts/scr_inputApi/scr_inputApi.gml:21-47; scripts/scr_resetGameToDefault/scr_resetGameToDefault.gml; scripts/scr_inventory_init/scr_inventory_init.gml; scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml:90-115; scripts/readDialogue/readDialogue.gml; objects/obj_Init/Create_0.gml:35-36,69-94,214-225,270-275,337-339; objects/obj_globalManager/Other_3.gml; objects/par_interactable/Create_0.gml:17-74; objects/par_interactable/Other_4.gml; objects/par_interactable/Other_5.gml; objects/obj_saveManager/Step_0.gml:77-81,140-144,213-217; objects/textboxTest_scribble/Step_0.gml:33-41,156-170; datafiles/cutscenes/cutscene_engine_settings.json; datafiles/cutscenes/cutscene1.json; datafiles/Dialogues/testDialogue.yarn; datafiles/Dialogues/testChoices.yarn; datafiles/Dialogues/fountain.yarn; datafiles/Dialogues/testDialogueBlue.yarn; docs_new/_meta/datafiles.txt -->
