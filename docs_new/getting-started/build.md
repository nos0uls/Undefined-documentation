---
title: Сборка из командной строки
tags:
  - getting-started
  - build
---

# Сборка из командной строки

Headless-компиляция проекта через Igor — консольный движок сборки GameMaker. Собирает IFF-пакет (`.zip`) без запуска IDE и самой игры.

## Команда

```bash
RT=/home/n0souls/.local/share/GameMakerStudio2-Beta/Cache/runtimes/runtime-2026.100.0.1106
"$RT/bin/igor/linux/x64/Igor" -j=8 \
    --project="/path/to/Undefinedtale888/Undefinedtale888.yyp" \
    --runtime=VM \
    --runtimePath="$RT" \
    --cache=/tmp/ut888/cache \
    --temp=/tmp/ut888/temp \
    --user=$HOME/.config/GameMakerStudio2-Beta/unknownUser_unknownUserID \
    --of=/tmp/ut888/out.zip --tf=out.zip \
    -- Linux Compile 2>&1 | tee compile.log
echo "EXIT=${PIPESTATUS[0]}"
```

| Флаг | Значение |
|------|----------|
| `-j=8` | число потоков компиляции |
| `--project` | путь к `.yyp` проекта |
| `--runtime=VM` | сборка под VM (не YYC) |
| `--runtimePath` | каталог рантайма |
| `--cache`, `--temp` | рабочие каталоги сборки |
| `--user` | профиль пользователя IDE — оттуда Igor читает `local_settings.json` |
| `--of`, `--tf` | параметры выходного файла |
| `-- Linux Compile` | целевая платформа и конфигурация |

## Результат

По логу прогона (`audit_2026-09/07_study/S04_compile.log`):

- пакет IFF: строка `Saving IFF file... /tmp/ut888_s04/Undefinedtale888.zip` — zip назван по имени проекта и лежит в каталоге выхода (родитель `--cache`/`--temp`);
- `Final Compile finished.` — конец компиляции кода и ресурсов;
- `Igor complete.` — последняя строка, сборка завершена;
- `EXIT=0` — код возврата.

!!! warning "Runtime `2024.1400.5.1031` отсутствует"
    В старых инструкциях в `RT` указан `runtime-2024.1400.5.1031` — его нет в `Cache/runtimes/` (установлены `runtime-2026.100.0.1098` и `runtime-2026.100.0.1106`). Запуск с ним падает сразу: `Igor: Нет такого файла или каталога`, `EXIT=127`. Все сборки аудита используют `runtime-2026.100.0.1106` — подставляйте его в `RT`.

!!! note "Что компилируется"
    Igor собирает рабочее дерево — включая незакоммиченные изменения. Компиляция только упаковывает ресурсы: сама игра при этом не запускается.

## Чтение лога

Ключевые строки успешного прогона:

- `MACHINE TYPE = LINUX`, `Found Project Format 2` — окружение и формат проекта;
- `Release build` — режим сборки;
- `Compile Scripts...finished.`, `Compile Rooms...finished.`, `Compile Objects...finished.... 47 empty events` — этапы; `empty events` и `2 CC empty` — информационные счётчики, не ошибки;
- `Converting music_* to Wav 16bit ...` — конвертация звуков под платформу;
- `Writing Chunk... <NAME> size ...` — запись чанков IFF (`GEN8`, `OPTN`, `SOND`, `SPRT`, `VARI`, `FUNC`, `TXTR`, `AUDO` и др.);
- `Core Resources : Info - TextureGroup missing for Font - ft_menuFont_2` — INFO-строка, присутствует во всех прогонах, не ошибка.

### Строка Stats

```text
Stats : GMA : Elapsed=14061.1029
Stats : GMA : sp=78,au=8,bk=5,pt=0,sc=2400,sh=14,fo=11,tl=0,ob=53,ro=16,da=103,ex=0,ma=6,fm=0x…
```

- `Elapsed` — время работы asset-компилятора в миллисекундах;
- счётчики ресурсов: `sp` — спрайты, `au` — звуки, `bk` — фоны, `pt` — пути, `sc` — скрипты, `sh` — шейдеры, `fo` — шрифты, `tl` — таймлайны, `ob` — объекты, `ro` — комнаты, `da` — включённые файлы, `ex` — расширения;
- `ma`, `fm` — служебные поля (точный смысл не проверен).

## Ошибки

В успешном логе нет строк `Error`/`error` — проверка `grep -icE error compile.log` даёт `0`. При сбое:

1. Смотрите `EXIT` — ненулевой код означает падение Igor.
2. `grep -inE "error" compile.log` — строки компилятора с причиной.
3. `EXIT=127` с `Нет такого файла или каталога` — неверный путь к Igor или отсутствующий runtime (см. предупреждение выше).

## См. также

- [Установка и настройка](setup.md) — версии IDE, runtime, клонирование
- [Структура проекта](project-structure.md) — что собирается в пакет
- [Обзор архитектуры](../architecture/overview.md) — подсистемы собранного проекта

<!-- sources: audit_2026-09/07_STUDY_PROMPT.md:27-28 (команда Igor); audit_2026-09/07_study/S04.md:22-56 (подстановка runtime, EXIT=0, оговорка о дереве); audit_2026-09/07_study/S04_compile.log:1-87 (Final Compile finished:29, Saving IFF:31, Stats:85-86, Igor complete:87, TextureGroup INFO:6, empty events:23, option_game_speed:33); audit_2026-09/07_study/S04_compile_given_rt2024.log:1 (EXIT=127, нет runtime-2024.1400.5.1031) -->
