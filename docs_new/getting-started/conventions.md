---
title: Конвенции кода
tags:
  - getting-started
  - conventions
  - gml
---

# Конвенции кода

Правила именования и оформления кода в `Undefinedtale888/`. Формальный стандарт зафиксирован в `guide.md` в корне проекта; ниже — то, что реально соблюдено в коде, с расхождениями.

## Именование ресурсов { #naming-assets }

| Префикс | Ресурс | Примеры из проекта |
|---|---|---|
| `obj_` | Объекты | `obj_player`, `obj_Init`, `obj_cutsceneManager`, `obj_inGameMenu` |
| `par_` | Родительские объекты | `par_depth`, `par_actor`, `par_decor`, `par_entity`, `par_interactable` |
| `scr_` | Скрипты-модули | `scr_inputApi`, `scr_player_movement`, `scr_saveLoad`, `scr_settingsManager` |
| `c_*` | Команды GML-билдера катсцен | `c_begin`, `c_play`, `c_wait`, `c_pan`, `c_speaker` |
| `cutscene_*` | JSON-API движка катсцен | `cutscene_load_json`, `cutscene_actor_create`, `cutscene_camera_pan` |
| `rm_` | Комнаты | `rm_init`, `rm_roomMenu`, `rm_playground`, `rm_settings` |
| `spr_` | Спрайты | `spr_Chara_walking_D`, `spr_p3r_cursor`, `spr_rmChanger` |
| `snd_` | Звуковые эффекты | `snd_text_ch1`, `snd_wobble` |
| `mus_` / `music_` | Музыка | `mus_intro`, `mus_end`, `music_menu`, `music_SchoolRoutine` |
| `ft_` | Шрифты | `ft_menuFont`, `ft_dialogueTest`, `ft_p3r_title` |
| `shd_` | Шейдеры | `shd_grayscale`, `shd_p3r_glow`, `shd_Chara_Eyes` |

!!! note "Фактические исключения"
    Часть ресурсов именуется без префикса или по-своему: объекты `bush`, `npc1`, `npc2`, `pinkBench`, `sand`, `screenshot`, `textboxTest_scribble`, `spr_pinkBench` (объект с именем в спрайтовом префиксе), `objRoomChanger` (camelCase без подчёркивания); комнаты `DevRoom1`, `SCREENSHOTS`, `roomForDialogueTesting`; музыка встречается и как `mus_`, и как `music_`; спрайты `bush2`, `npc`, `kachela` без `spr_`. `guide.md` предписывает `fnt_`/`snd_`/`shd_`/`tls_`, но шрифты фактически идут как `ft_*`, а тайлсеты — `grassTile`, `ts_main`.

## Именование в коде { #naming-code }

| Конвенция | Где | Пример |
|---|---|---|
| `_param` / `_tmp` | Аргументы функций и локальные временные | `cutscene_load_json(_path)`, `var _buf`, `var _normalized_path` |
| `camelCase`/`snake_case` | Локальные и инстанс-переменные — в коде встречаются оба стиля | `menu_cursor_target_y`, `can_move`, `move_active`, `itemType` |
| `global.*` | Глобальное состояние | `global.game_state`, `global.input_map`, `global.player_settings` |
| `global.__*` | Внутренние глобалы подсистем | `global.__cutscene_build_mgr`, `global.__music_volume`, `global.__init_done` |
| `__name` | Приватные функции и макросы внутри подсистемы | `__cutscene_resolve_target`, `#macro __CUTSCENE_EPSILON`, `__shd_scribble*` (Scribble), `__Chatterbox*` (Chatterbox) |
| `UPPER_SNAKE_CASE` | `#macro` и элементы enum | `#macro SAVE_FORMAT_VERSION 3`, `#macro MANAGER_DEPTH -10000`, `ITEMTYPE.WEAPON` |
| `PascalCase` | Имена enum | `ITEMTYPE`, `PLAYER_AXIS_FSM` |

!!! note "Смысл двойного подчёркивания"
    `__` — маркер «не для внешнего использования»: у библиотек это весь внутренний слой (`__ChatterboxClassInstruction`, `__scribble_class_typist`), у своего кода — хелперы внутри файла (`__cutscene_get_resolver` в `scr_cutscene_classes.gml`) и служебные глобалы (`global.__cutscene_checkpoints`).

## JSDoc-комментарии { #jsdoc }

В коде сосуществуют два стиля заголовков.

Основной (Feather-стиль, ~83 проектных файла):

```gml title="scripts/readDialogue/readDialogue.gml"
/// @function readDialogue(_filename, _nodename)
/// @description Открывает диалоговое окно: создаёт textboxTest_scribble и передаёт ему
///              yarn-файл и стартовую ноду. Окно рисуется через Draw GUI, поэтому
///              мировые координаты инстанса нигде не читаются — создаём на (0, 0).
/// @param {string} _filename Имя yarn-файла из datafiles/Dialogues.
/// @param {string} _nodename Имя стартовой ноды внутри yarn-файла.
/// @return {instance} id созданного textboxTest_scribble или noone, если окно уже открыто.
function readDialogue(_filename, _nodename) {
```

Второй стиль (`@summary`/`@returns`/`@since`, 9 файлов, совпадает с шаблоном из `guide.md`):

```gml title="scripts/cutscene_load_json/cutscene_load_json.gml"
/// @summary Загружает катсцену из JSON и создаёт менеджер
/// @param {string} _path Путь к JSON относительно рабочей директории
///        (префиксы "./" и "datafiles/" в начале пути срезаются — в рантайме
///        каталога datafiles/ нет, IncludedFiles лежат в корне).
/// @returns {instance|noone} Менеджер катсцены или noone при ошибке
/// @since 0.1.0
function cutscene_load_json(_path) {
```

`guide.md` предписывает минимальный набор `@summary`, `@param`, `@returns`, `@since` для экспортируемых функций; старый код чаще использует `@function`/`@desc`/`@return`.

## Регионы и структура файлов { #regions }

`#region`/`#endregion` используются в 52 файлах — и в библиотеках, и в своих скриптах. Крупные модули делят на именованные блоки:

- `scr_cutscene_classes.gml` — по региону на класс действия: `#region ActionSetAnimationFrame`, `#region ActionMoveRelative — движение актёра относительно текущей позиции (dx/dy)`.
- `scr_music_init.gml` — фазы инициализации: `#region Защита повторной инициализации`, `#region Room-to-Track mapping`.
- `cutscene_action_factory.gml`, `scr_settings_step_root.gml`, `scr_saveLoad.gml` — аналогично.

## Правила проекта { #project-rules }

Файлов правил для агентов (`AGENTS.md`, `.windsurf/`, `.devin/rules/`) в репозитории игры нет. Действующий стандарт — `Undefinedtale888/guide.md`; из него и из фактического кода:

- **Заголовки `///` обязательны** для экспортируемых функций; их отсутствие — «блокирующая ошибка» на ревью.
- **Инициализация в `Create`, освобождение в `Clean Up`** — `ds_*`-структуры уничтожаются явно, утечки запрещены.
- **Guard clauses вместо исключений** — проверка входных данных в начале функции, ранний возврат с `show_debug_message` (`cutscene_load_json` возвращает `noone`; в `cutscene_add` отброшенный action логируется только при `global.debug`).
- **Глобалы объявляются в `obj_Init`** — `obj_Init/Create_0.gml` — «единое место инициализации» (`scr_settingsManager.gml` прямо фиксирует это в комментарии); единственное задокументированное исключение — `global.default_settings`, присваиваемый телом скрипта при загрузке программы.
- **Тексты не хардкодить** — строки выносятся в данные (Yarn/JSON).
- **Магические числа — в `#macro`/константы** (`__CUTSCENE_*`, `SAVE_FORMAT_VERSION`, `MANAGER_DEPTH`).
- **Префиксы ресурсов** — таблица выше; статический аудит по `guide.md` проверяет соответствие `obj_`/`spr_`/`snd_`/`rm_`/`scr_`/`shd_`/`fnt_`/`tls_`.

!!! info "Метки аудита в комментариях"
    Комментарии местами ссылаются на идентификаторы находок аудита — `(F-535)`, `(E-V03)`, `(F-055)`. Это ссылки на `audit_2026-09/`, а не часть стандарта именования.

## Кодировка и концы строк { #encoding }

- `.gitattributes` проекта принудительно ставит **LF** для `*.gml`, `*.yy`, `*.yyp`, `*.json` (`text eol=lf`); корневой `.gitattributes` репозитория добавляет `* text=auto`. CRLF в коммитах не ожидаются.
- Исходники — **UTF-8**: комментарии и строки на русском.
- **BOM** допустим во входных JSON: `cutscene_load_json` срезает сигнатуру UTF-8 BOM `EF BB BF` по байтам буфера до `buffer_read` — `buffer_text` иначе декодировал бы BOM в символ `U+FEFF` в начале текста.

## См. также

- [Структура проекта](project-structure.md) — каталоги и библиотеки
- [Установка и настройка](setup.md) — запуск проекта
- [Глобальное состояние](../architecture/global-state.md) — `global.*` и `obj_Init`
- [Справочник GML-скриптов](../reference/gml-scripts.md) — функции по модулям

<!-- sources: Undefinedtale888/guide.md; Undefinedtale888/README.md; Undefinedtale888/.gitattributes; _meta/objects.txt; _meta/scripts.txt; _meta/globals.txt; _meta/rooms.txt; scripts/readDialogue/readDialogue.gml:1-8; scripts/cutscene_load_json/cutscene_load_json.gml:1-6,51-59; scripts/scr_inputApi/scr_inputApi.gml:8-10; scripts/scr_player_movement/scr_player_movement.gml:1-6; scripts/scr_cutscene_classes/scr_cutscene_classes.gml:12-40,2464,2960; scripts/scr_music_init/scr_music_init.gml:6-151; scripts/scr_settingsManager/scr_settingsManager.gml:1-20,50; scripts/scr_saveSave/scr_saveSave.gml:7; scripts/scr_player_process_mutually_exclusive_inputs/scr_player_process_mutually_exclusive_inputs.gml:4; scripts/currentENUMS/currentENUMS.gml:4 -->
