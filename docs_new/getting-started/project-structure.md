---
title: Структура проекта
tags:
  - getting-started
  - architecture
---

# Структура проекта

Карта каталогов GameMaker-проекта `Undefinedtale888/` и роли файлов в корне. Состав указан по фактическому содержимому репозитория (ветка `audit-fixes-2026-09`).

## Корень проекта { #root }

| Файл / каталог | Назначение |
|---|---|
| `Undefinedtale888.yyp` | Файл проекта GameMaker: список ресурсов, `RoomOrderNodes` (первой идёт `rm_init`), `IncludedFiles` |
| `Undefinedtale888.resource_order` | Порядок ресурсов в IDE (в `.gitignore`) |
| `.gitattributes`, `.gitignore` | Правила Git: LF для `*.gml`/`*.yy`/`*.yyp`/`*.json`, `*.resource_order` и прочее в ignore |
| `guide.md` | Внутренние стандарты разработки: именование, JSDoc, диалоги, локализация, чек-листы |
| `README.md` | Руководство для участника: установка, запуск, Yarn, локализация, деплой |
| `УПРАВЛЕНИЕ.txt` | Таблица игровых и debug-клавиш |
| `cutscene_system_research.md` | Исследование движка катсцен |
| `audit/`, `audit_2026-09/` | Рабочие материалы аудитов кода; к ресурсам игры отношения не имеют |

## Каталоги ресурсов { #resource-dirs }

| Каталог | Содержимое | Примечания |
|---|---|---|
| `objects/` | 53 объекта | Системные `obj_Init`, `obj_globalManager`, `obj_music_ctrl`, `obj_cutsceneManager`; родители `par_depth`, `par_actor`, `par_decor`, `par_entity`, `par_interactable`; библиотечный `o_SharedTweener`. Есть объекты без префикса (`bush`, `npc1`, `pinkBench`, `textboxTest_scribble`) |
| `scripts/` | 359 скриптов, один ресурс = один `.gml` | Свои: `scr_*` (модули), `c_*` (GML-билдер катсцен), `cutscene_*` (JSON-движок). Библиотеки: `Chatterbox*`/`__Chatterbox*` (103), `scribble*`/`__scribble_*` (110), `TGMX_*` (12) |
| `rooms/` | 16 комнат | Служебные: `rm_init`, `rm_roomMenu`, `rm_savesSelect`, `rm_settings`, `rm_devLoad`. Игровые и тестовые: `rm_playground`, `rm_uphill_school`, `DevRoom1`, `rm_cutsceneTest`, `SCREENSHOTS` и др. `RoomCreationCode.gml` есть у части комнат |
| `datafiles/` | Included Files | См. раздел ниже |
| `sounds/` | 8 аудио-ресурсов | Музыка `mus_*`/`music_*` (`mus_intro`, `music_menu`, `music_SchoolRoutine`), звуки `snd_*` (`snd_text_ch1`, `snd_wobble`) |
| `sprites/` | 79 спрайтов | Префикс `spr_` соблюдён не везде: рядом с `spr_Chara_walking_*` лежат `bush2`, `npc`, `kachela` |
| `fonts/` | 11 шрифтов | `ft_*` (`ft_menuFont`, `ft_p3r_title`), `Montserrat`, `scribble_fallback_font` |
| `shaders/` | Шейдеры | Свои `shd_*` (`shd_grayscale`, `shd_p3r_*`) и служебные `__shd_scribble*` библиотеки Scribble |
| `animcurves/` | 3 кривые | `EaseFastToSlow`, `EaseHeartbeat`, `EaseMidSlow` |
| `tilesets/` | 5 тайлсетов | `grassTile`, `pathTile`, `treesTile`, `ts_inside`, `ts_main` |
| `notes/` | Заметки GMS | Только документация библиотеки: `TGMX_Documentation`, `TGMX_Terms_of_Use`, `TGMX_Update_Log` |
| `options/` | Настройки платформ | `main`, `windows`, `linux`, `mac`, `html5`, `android`, `ios`, `tvos`, `operagx`, `reddit`, `extensions` |

## Ключевые объекты { #key-objects }

Полную иерархию родителей и событий см. в [Объектах](../architecture/object-hierarchy.md); здесь приведён ориентир по главным.

- Boot: `obj_Init` (persistent, единственный инстанс в `rm_init`, первой комнате `RoomOrder`) объявляет `global.*` и создаёт `obj_globalManager` и `obj_music_ctrl`.
- Runtime-оркестратор: `obj_globalManager` (persistent, создаётся из `obj_Init` на слое `scr_layer_ensure_instances()`) отвечает за смену комнат, debug-хоткеи, уведомления, покадровый шаг катсцен и эмоутов.
- Игрок и сцена: `obj_player` (наследник `par_actor` → `par_depth`), интерактивные объекты под `par_interactable`, декор под `par_decor`, коллайдеры `obj_collider`/`obj_slopeCollider` под `par_entity`.
- Катсцены: `obj_cutsceneManager`: очередь действий; `obj_actor`: управляемый персонаж; тестовый UI: `obj_cutsceneTest`.
- UI: `obj_menu`, `obj_inGameMenu`, `obj_settingsManager`, `obj_saveManager`, `obj_devLoader`, `obj_face`, `textboxTest_scribble`; P3R-мокапы: `obj_p3r_*`.

## Библиотеки в проекте { #libraries }

- **Chatterbox**: рантайм диалогов Yarn Spinner. Скрипты `Chatterbox*` и приватные `__Chatterbox*`. `obj_Init` загружает `.yarn` через `ChatterboxLoadFromFile`; `readDialogue` создаёт окно `textboxTest_scribble` и передаёт ему файл и стартовую ноду, а само окно ведёт диалог по нодам через `ChatterboxCreate`/`ChatterboxContinue`/`ChatterboxSelect`.
- **Scribble**: рендер текста с разметкой и эффектами. Скрипты `scribble*`/`__scribble_*`, шейдеры `__shd_scribble*`, шрифт `scribble_fallback_font`, лицензия `datafiles/scribble_license.txt`. Обёртки проекта: `draw_text_scribble`, `string_width_scribble` и др. Используется в текстбоксе и меню `obj_p3r_*`.
- **TGMX (TweenGMX 1.0.8)**: твины. Скрипты `TGMX_*`, заметки в `notes/`, persistent-объект `o_SharedTweener` (создаётся лениво функцией `SharedTweener()` при первом твине). По факту твины вызывают только мокапы меню `obj_p3r_title`, `obj_p3r_pause`, `obj_p3r_settings`, `obj_p3r_transition` через `TweenFire`; библиотека сохранена в проекте до решения по P3R-мокапам.

## datafiles/ { #datafiles }

| Путь | Содержимое |
|---|---|
| `Dialogues/` | 4 Yarn-файла: `fountain.yarn`, `testDialogue.yarn`, `testDialogueBlue.yarn`, `testChoices.yarn` |
| `cutscenes/` | Сценарии катсцен: `cutscene.json`, `cutscene1.json`, `cutscene_demo_888.yarn`, тестовые `test_*.json` и `cutscene_engine_settings.json` |
| `cutscenes/tests/` | ~90 JSON-тестов движка катсцен по одному действию (`move_basic`, `camera_pan`, `dialogue` и т.д.) + подкаталог `stress/` |
| `scribble_license.txt` | Лицензия Scribble |

`cutscene_engine_settings.json` содержит настройки движка катсцен: `schema_version`, `default_fps`, `strict_mode_default`, `default_actor_object`, `default_emote_sprite`, вайтлисты `run_functions`/`branch_conditions`, флаги `debug`. Читается один раз за сессию `cutscene_load_engine_settings`.

!!! warning "Регистрация Included Files"
    Файл из `datafiles/` попадает в сборку только если он зарегистрирован как Included File в `Undefinedtale888.yyp`. Простого копирования в каталог недостаточно.

!!! note "Пути в рантайме"
    Included Files копируются в рабочую директорию без префикса `datafiles/`: `cutscene_load_json` срезает префиксы `./` и `datafiles/` перед `file_exists`. В коде пути пишут относительно рабочей директории (`"cutscenes/test_movement.json"`).

## См. также

- [Установка и настройка](setup.md) — запуск проекта в GameMaker
- [Сборка](build.md) — конфигурации и экспорт
- [Конвенции кода](conventions.md) — именование и стиль
- [Архитектура: инициализация](../architecture/initialization.md) — `obj_Init`, порядок старта
- [Форматы данных](../architecture/data-formats.md) — JSON катсцен, сейвы, Yarn

<!-- sources: Undefinedtale888/ (ls каталогов); _meta/objects.txt; _meta/scripts.txt; _meta/datafiles.txt; _meta/rooms.txt; objects/o_SharedTweener/Create_0.gml; scripts/TGMX_System/TGMX_System.gml:477-493; objects/obj_Init/Create_0.gml:275; scripts/cutscene_load_json/cutscene_load_json.gml:13-32; scripts/cutscene_load_engine_settings/cutscene_load_engine_settings.gml; datafiles/cutscenes/cutscene_engine_settings.json; audit_2026-09/fix/DESIGN_DECISIONS.md (F-223) -->
