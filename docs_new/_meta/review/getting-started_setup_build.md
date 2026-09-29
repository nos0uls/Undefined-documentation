# Фактчек: getting-started/setup.md + getting-started/build.md (ревизия кода 7ee444a)

Источники: `Undefinedtale888.yyp`, `options/*/*.yy`, `audit_2026-09/07_STUDY_PROMPT.md`, `audit_2026-09/07_study/S04.md`, `S04_compile.log`, `S04_compile_given_rt2024.log`, `git remote -v` обоих репозиториев, `ls` $P и `Cache/runtimes/`, `$E/PRODUCT.md`, `_meta/nav_plan.md`, `docs_new/` (существование целей ссылок).

## setup.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| 15 | GameMaker IDE (ветка Beta) `2026.100.0.1161`, поле `MetaData.IDEVersion` в `.yyp` | OK — Undefinedtale888.yyp:212 `"IDEVersion":"2026.100.0.1161"`; Beta-канал подтверждён каталогом `~/.local/share/GameMakerStudio2-Beta/` |
| 16 | Runtime `2026.100.0.1106` — все прогоны компиляции | OK — S04.md:10-11 (`compile_final.log`, `R16/compile_2.log`), S04.md:30 (собственный прогон), S04.md:97 |
| 17 | Платформа Linux, цель `Linux Compile` | OK — 07_STUDY_PROMPT.md:28 (`-- Linux Compile`); S04_compile.log:4 `MACHINE TYPE = LINUX` |
| 20 | Beta-каталоги `~/.local/share/GameMakerStudio2-Beta/`; установлены `runtime-2026.100.0.1098` и `runtime-2026.100.0.1106`; сборка на `1106` | OK — `ls Cache/runtimes/` = ровно эти два; S04.md:24 |
| 24 | `option_game_speed` = `60`, `option_author` = `Sp0ildy` | OK — options/main/options_main.yy:13,7 |
| 25 | `option_linux_display_name` = `Undefinedtale888`, текстурная страница `2048x2048` | OK — options/linux/options_linux.yy:8,22 |
| 26 | `option_windows_display_name` = `UNDEFINEDtale-888`, exe `${undefinedtale-888}.exe`, NSIS-инсталлятор, `2048x2048` | OK — options/windows/options_windows.yy:14,16,22 (`option_windows_nsis_file`),31 |
| 27 | Прочие платформенные каталоги `options/`: `android`, `html5`, `ios`, `mac`, `operagx`, `tvos`, `reddit` | OK — `ls options/` даёт ровно этот список (+ `extensions`, не платформа) |
| 32 | `git clone https://github.com/Sp0ildy/Undefinedtale-888.git` | OK — `git remote -v` корня репозитория: `origin https://github.com/Sp0ildy/Undefinedtale-888.git` |
| 35 | Проект в подкаталоге `Undefinedtale888/`, файл `Undefinedtale888/Undefinedtale888.yyp` | OK — `ls` корня репо: `Undefinedtale888/` рядом с README.md и пр. |
| 40 | Библиотеки уже в проекте: Scribble и Chatterbox (папка `доп_расширения`), TweenGMX (папка `TweenGMX`) | OK с уточнением — это `GMFolder` дерева ресурсов в `.yyp` (:27-44), а не каталоги на диске; сами скрипты на месте (`scripts/`: scribble×117, Chatterbox×104, TGMX×12) |
| 41 | `F5` компилирует и запускает | OK — стандартное поведение IDE; согласуется с F5/F6-навигацией в initialization.md |
| 43 | Стартовая комната `rm_init` — первая в `RoomOrderNodes`, за ней `rm_roomMenu` | OK — Undefinedtale888.yyp:769-771 |
| 47 | Перечень «стандартных каталогов ресурсов» | MISSING — пропущены присутствующие `shaders/` и `animcurves/` (ls $P; project-structure.md перечисляет оба) |
| 49 | `guide.md`, `УПРАВЛЕНИЕ.txt`, `notes/` — «заметки разработчиков по управлению и дизайну» | **WRONG** для `notes/` — каталог содержит только вендорские файлы `TGMX_Documentation`, `TGMX_Terms_of_Use`, `TGMX_Update_Log` (ls notes/; project-structure.md:«Только документация библиотеки»). Для `guide.md`/`УПРАВЛЕНИЕ.txt` описание верно |
| 49–51 | Полнота списка «что ещё лежит в каталоге проекта» | MISSING — не упомянуты `README.md` и `cutscene_system_research.md` в корне проекта (ls $P) |
| 55 | Undefscene = `nos0uls/Undefscene`, Electron-приложение `editor-app/`, node-редактор → JSON для движка катсцен | OK — `git remote -v` репо Undefscene; `editor-app/` с `electron-builder.yml`, `package.json`; PRODUCT.md:15 |
| 60 | IDE `2026.100.0.1161`, рантайм `2026.100.0.1106` | OK — см. строки 15–16 |
| 60 | «`MetaData.IDEVersion` перезаписывается при каждом сохранении проекта» | UNVERIFIABLE — поведение IDE, из кода/логов не следует |
| 63 | `ls ~/.local/share/GameMakerStudio2-Beta/Cache/runtimes/`; для сборки нужен `1106` | OK — каталог и версия проверены |
| 68–71 | Ссылки: `build.md`, `project-structure.md`, `conventions.md`, `../undefscene/overview.md`, `../architecture/initialization.md` | OK — все файлы есть в docs_new/ и в `_meta/nav_plan.md` |

## build.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| 10 | Igor — консольный движок сборки GameMaker; собирает IFF-пакет `.zip` без IDE и запуска игры | OK — S04_compile.log:31 `Saving IFF file... *.zip`; S04.md:102 («Igor-прогон лишь собирает IFF»); бинарник `bin/igor/linux/x64/Igor` существует в runtime-1106 |
| 15–26 | Команда Igor (флаги, `-- Linux Compile`, `tee`, `EXIT=${PIPESTATUS[0]}`) | OK — совпадает с 07_STUDY_PROMPT.md:27-28 с задокументированной подменой `RT` на `runtime-2026.100.0.1106` и обобщением путей `/tmp/ut888*` и `--project`; `--user` каталог `unknownUser_unknownUserID` существует (`ls ~/.config/GameMakerStudio2-Beta/`) |
| 30 | `-j=8` — число потоков компиляции | OK — стандартная семантика флага Igor; значение 8 — из задания |
| 35 | `--user` — профиль IDE, оттуда читается `local_settings.json` | OK — S04_compile.log:2 `Options: .../unknownUser_unknownUserID/local_settings.json` |
| 41–46 | `Saving IFF... /tmp/ut888_s04/Undefinedtale888.zip`, `Final Compile finished.`, `Igor complete.` — последняя строка, `EXIT=0` | OK — log:31, :29, :87; S04.md:34,38 |
| 43 | Zip назван по имени проекта, лежит в каталоге выхода (родитель `--cache`/`--temp`) | OK — log:31; для задокументированной формы команды совместимо (родитель cache/temp = каталог `--of`) |
| 48–49 | Старый `runtime-2024.1400.5.1031` отсутствует; `EXIT=127`, «Нет такого файла или каталога»; все сборки аудита на `1106` | OK — 07_STUDY_PROMPT.md:27 (старый RT), S04.md:24-25, S04_compile_given_rt2024.log:1, S04.md:97 |
| 51–52 | Компилирует рабочее дерево включая незакоммиченные правки; игра не запускается | OK — S04.md:55-56 (37 записей `git status`), S04.md:102 |
| 58 | `MACHINE TYPE = LINUX`, `Found Project Format 2` | OK — log:4-5 |
| 59 | `Release build` | OK — log:10 |
| 60 | `Compile Scripts/Rooms/Objects...finished.`, `47 empty events`, `2 CC empty` — не ошибки | OK — log:20-23 |
| 61 | `Converting music_* to Wav 16bit ...` | OK — log:38-45 |
| 62 | Чанки IFF `GEN8`, `OPTN`, `SOND`, `SPRT`, `VARI`, `FUNC`, `TXTR`, `AUDO` и др. | OK — все присутствуют в log:32-84 |
| 63 | `TextureGroup missing for Font - ft_menuFont_2` — INFO во всех прогонах | OK — log:6; S04.md:51 («в обоих прогонах») |
| 68–74 | Строка Stats, `Elapsed` в мс, расшифровка счётчиков; `ma`/`fm` — «не проверен» | OK — log:85-86 дословно; `ma`/`fm` самооговорены страницей |
| 78 | `grep -icE error` → `0` в успешном логе | OK — S04.md:37 |
| 80–82 | Диагностика сбоев; `EXIT=127` = неверный путь/нет runtime | OK — S04.md:25, given_rt2024.log:1 |
| 86–88 | Ссылки: `setup.md`, `project-structure.md`, `../architecture/overview.md` | OK — все файлы есть в docs_new/ и в `_meta/nav_plan.md` |

## Итог

- **WRONG: 1** — setup.md:49 (`notes/` описан как «заметки разработчиков», на деле — вендорская документация TweenGMX).
- **UNVERIFIABLE: 1** — setup.md:60 (механика перезаписи `MetaData.IDEVersion` — поведение IDE, не из кода).
- **MISSING: 2** — setup.md:47 (`shaders/`, `animcurves/` в перечне ресурсных каталогов), setup.md:49–51 (`README.md`, `cutscene_system_research.md` в списке файлов корня).
- **Уточнение: 1** — setup.md:40 (`доп_расширения`/`TweenGMX` — папки дерева ресурсов `.yyp`, не диска).
- Остальное подтверждено.
