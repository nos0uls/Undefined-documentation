---
title: Установка и настройка
tags:
  - getting-started
---

# Установка и настройка

Требования к окружению и первый запуск проекта Undefinedtale-888.

## Требования

| Компонент | Версия | Источник |
|-----------|--------|----------|
| GameMaker IDE (ветка Beta) | `2026.100.0.1161` | поле `MetaData.IDEVersion` в `Undefinedtale888.yyp` |
| Runtime | `2026.100.0.1106` | используется всеми прогонами компиляции (см. [Сборка](build.md)) |
| Платформа разработки | Linux | headless-сборка идёт целью `Linux Compile` |

!!! note "Каталоги Beta-канала"
    IDE и кэш рантаймов лежат под `~/.local/share/GameMakerStudio2-Beta/`: проект работает на Beta-канале GameMaker. В `Cache/runtimes/` установлены `runtime-2026.100.0.1098` и `runtime-2026.100.0.1106`; сборка использует `runtime-2026.100.0.1106`.

### Настройки проекта (`options/`)

- Общие (`options/main/options_main.yy`): `option_game_speed` = `60` (игра рассчитана на 60 FPS); `option_author` = `Sp0ildy`.
- Linux (`options/linux/options_linux.yy`): `option_linux_display_name` = `Undefinedtale888`, текстурная страница `2048x2048`.
- Windows (`options/windows/options_windows.yy`): `option_windows_display_name` = `UNDEFINEDtale-888`, имя исполняемого файла `${undefinedtale-888}.exe`, настроен NSIS-инсталлятор, текстурная страница `2048x2048`.
- Каталоги `options/` для других платформ (`android`, `html5`, `ios`, `mac`, `operagx`, `tvos`, `reddit`) присутствуют в репозитории; фактическая сборка нацелена на Linux (см. [Сборка](build.md)).

## Клонирование

```bash
git clone https://github.com/Sp0ildy/Undefinedtale-888.git
```

Проект GameMaker лежит в подкаталоге `Undefinedtale888/` внутри репозитория, файл проекта: `Undefinedtale888/Undefinedtale888.yyp`.

## Открытие и первый запуск

1. Запустите GameMaker IDE и откройте `Undefinedtale888/Undefinedtale888.yyp`.
2. Внешние библиотеки ставить не нужно: они уже внутри проекта. Scribble и Chatterbox лежат скриптами в `scripts/` под папкой дерева ресурсов `доп_расширения`, а TweenGMX лежит под папкой `TweenGMX` (это папки в дереве ресурсов `.yyp`, а не каталоги на диске).
3. Нажмите `F5`: IDE скомпилирует проект и запустит игру.

Стартовая комната: `rm_init`; она идёт первой в списке `RoomOrderNodes` в `Undefinedtale888.yyp`, за ней следует `rm_roomMenu`. Порядок инициализации описан в [Инициализации](../architecture/initialization.md).

### Что ещё лежит в каталоге проекта

Кроме стандартных каталогов ресурсов (`objects/`, `scripts/`, `rooms/`, `sprites/`, `sounds/`, `fonts/`, `tilesets/`, `shaders/`, `animcurves/`, `datafiles/`, `options/`):

- `README.md`: руководство для участника (установка, запуск, Yarn, локализация, деплой);
- `guide.md`, `УПРАВЛЕНИЕ.txt`: внутренние стандарты разработки и таблица игровых/debug-клавиш;
- `cutscene_system_research.md`: исследование движка катсцен;
- `notes/`: вендорская документация библиотеки TweenGMX (`TGMX_Documentation`, `TGMX_Terms_of_Use`, `TGMX_Update_Log`);
- `audit/`, `audit_2026-09/`: материалы аудитов кода, не часть сборки;
- `Undefinedtale888.resource_order`: порядок ресурсов в дереве IDE.

## Рядом с проектом: редактор Undefscene

Катсцены для игры собираются в **Undefscene**, отдельном репозитории [`nos0uls/Undefscene`](https://github.com/nos0uls/Undefscene). Это Electron-приложение (каталог `editor-app/`): визуальный node-based редактор, который компилирует граф нод в JSON, исполняемый движком катсцен игры. Установка и интерфейс описаны в разделе [Undefscene](../undefscene/overview.md).

## Проблемы при открытии

!!! warning "Проект не открывается или просит другой runtime"
    Проверьте версию IDE: в `MetaData.IDEVersion` записано `2026.100.0.1161`, фактический рантайм: `2026.100.0.1106`. Работайте на Beta-канале соответствующей версии.

!!! tip "Нет подходящего runtime"
    Список установленных рантаймов: `ls ~/.local/share/GameMakerStudio2-Beta/Cache/runtimes/`. Для сборки из консоли нужен `runtime-2026.100.0.1106` (подробности в [Сборке](build.md)).

## См. также

- [Сборка из командной строки](build.md) — headless-компиляция через Igor
- [Структура проекта](project-structure.md) — папки и ресурсы `Undefinedtale888/`
- [Конвенции кода](conventions.md) — именование и стиль GML
- [Обзор Undefscene](../undefscene/overview.md) — редактор катсцен
- [Инициализация](../architecture/initialization.md) — `rm_init`, `obj_Init`, глобалы

<!-- sources: Undefinedtale888.yyp:11,27-44,211-213,769-772 (MetaData.IDEVersion, GMFolder доп_расширения/TweenGMX, RoomOrderNodes rm_init→rm_roomMenu); options/main/options_main.yy:7,13; options/linux/options_linux.yy:8,22; options/windows/options_windows.yy:14,16,22,31; ls $P (README.md, guide.md, УПРАВЛЕНИЕ.txt, cutscene_system_research.md, notes/, audit/, audit_2026-09/, *.resource_order, shaders/, animcurves/); ls $P/notes (TGMX_*); audit_2026-09/07_study/S04.md:24-30; audit_2026-09/07_study/S04_compile.log:1,4,10; git remote -v (origin https://github.com/Sp0ildy/Undefinedtale-888.git, https://github.com/nos0uls/Undefscene.git); $E/PRODUCT.md; $E/editor-app/electron-builder.yml -->
