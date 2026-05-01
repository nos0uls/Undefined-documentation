---
tags:
  - undefscene
  - editor
---

# Undefscene: Room Screenshot Pipeline

## Цель

Эта страница фиксирует foundation-план для mini GameMaker screenshot-builder, который должен генерировать реальные room screenshots для Undefscene editor.

Идея нужна для случаев, когда editor-side preview уже недостаточно и нужен визуальный контекст настоящей комнаты.

## Почему это отдельный pipeline

Текущий editor-app умеет:

- читать `.yyp` ресурсы и комнаты
- хранить persistent cache папку `room-screenshots`
- показывать editor-side preview для `follow_path`
- открывать `Visual Editing` в отдельном native окне и stitch'ить room screenshot tiles в единый фон
- искать room screenshots сначала в project cache, а затем в fallback-папке `<projectDir>/screenshots`
- искать output и в `%LOCALAPPDATA%/<project>/screenshots`, если runner использует GameMaker `working_directory`
- позволять user override для screenshot output folder через `Advanced` / `Preferences`
- автоматически перечитывать screenshot bundle после возврата фокуса в окно visual editor

Но сам Electron editor не знает реальную геометрию room, tile layers, camera setup и стартовое состояние объектов GameMaker.

Поэтому полноценный room preview должен собираться не в React Flow canvas, а через отдельный GameMaker runtime/tooling шаг.

## Что уже есть в проекте

В `Undefinedtale-888` уже есть полезные foundation-точки:

- безопасный `room_goto(...)` workflow
- debug room navigation helpers
- room change controller
- editor cache папка `userData/project-cache/<project>/room-screenshots`

На текущий момент готового screenshot export pipeline в game repo нет.

## Предлагаемый minimal architecture

### 1. Отдельный mini runner room

Нужна отдельная техническая room, например `rm_screenshot_builder`, которая не используется в обычной игре.

Её задача:

- принять имя целевой комнаты
- перейти в неё или загрузить её controlled way
- дождаться стабилизации room/camera
- снять кадр
- сохранить PNG во внешний folder
- перейти к следующей комнате

### 2. Отдельный controller object

Нужен технический объект вроде `obj_roomScreenshotBuilder`, который:

- читает queue комнат из JSON или command file
- знает output folder
- управляет phase machine (`boot -> load room -> wait -> capture -> save -> next`)
- пишет status/log обратно во внешний файл

### 3. Внешний manifest

Самый безопасный формат — отдельный JSON manifest на диске.

Например:

```json
{
  "output_dir": "C:/.../room-screenshots",
  "rooms": ["rm_roomMenu", "rm_init", "rm_forest_1"]
}
```

Это хорошо стыкуется с уже обсуждённым ограничением: packaged `datafiles` не стоит считать hot-swappable by default.

## Рекомендуемый runtime flow

1. Editor или отдельный script пишет manifest во внешний folder.
2. Mini screenshot-builder build запускается отдельно от основной игры.
3. Builder читает manifest.
4. Builder открывает каждую комнату по очереди.
5. После короткой стабилизации делает screenshot.
6. Builder сохраняет PNG tiles и `meta JSON` в предсказуемую директорию.
7. Editor ищет bundle сначала в `userData/project-cache/<project>/room-screenshots`, затем в `<projectDir>/screenshots`, затем в `%LOCALAPPDATA%/<project>/screenshots`.
8. При необходимости пользователь может задать явный custom output folder через `Help > Advanced` или `Preferences`.
9. При возврате пользователя в окно `Visual Editing` editor пытается автоматически перечитать bundle и обновить stitched room preview.

## Почему не стоит полагаться на packaged `datafiles`

Для fast iteration packaged `datafiles` неудобны:

- они относятся к build output
- их hot-swap без rebuild ненадёжен
- editor не должен зависеть от неявной runtime-магии

Если нужен быстрый цикл без полной пересборки, builder должен читать manifest как внешний файл с диска.

## Что считать готовым первым milestone

Первый milestone для screenshot pipeline должен уметь только это:

- принять список комнат
- создать PNG на диск
- сохранить predictable имена файлов
- не ломать основной runtime проекта

Без этого не стоит добавлять более сложные features вроде:

- camera variants
- multiple spawn anchors
- actor overlays
- animated previews

## Следующий implementation step

Практический следующий шаг:

1. создать technical room и controller object в `Undefinedtale-888`
2. выбрать безопасный внешний manifest path
3. реализовать capture-only proof of concept для 1 комнаты
4. проверить, что editor cache folder может принять и переиспользовать PNG/meta между сессиями
5. убедиться, что visual editor корректно показывает `Source` и `Search Dirs`, если runner пишет output не в первую ожидаемую папку

## Связь с editor-side preview

Editor-side preview и screenshot-builder не конкурируют друг с другом.

Они закрывают разные уровни задачи:

- `follow_path` preview — быстрый structural preview ноды
- room screenshot pipeline — настоящий visual context комнаты

Обе системы могут жить параллельно.

## Текущее editor-side поведение

Сейчас `Visual Editing` показывает диагностическую информацию, полезную для screenshot workflow:

- `Source` — папка, из которой реально был загружен найденный bundle
- `Search Dirs` — все директории, которые editor проверил при поиске screenshots
- `Missing Tiles` — количество отсутствующих PNG tiles относительно `meta JSON`

Если bundle ещё не найден, пользователь может:

1. запустить внешний screenshot runner
2. вернуться в окно `Visual Editing`
3. дождаться автоматического refresh после `focus`/`visibilitychange` или нажать `Refresh`

---

## См. также

- [Интерфейс Undefscene](ui.md) — `Visual Editing`, `Search Dirs`, `Source`
- [Интеграция с проектом](integration.md) — загрузка `.yyp`, screenshot cache paths
- [Workflow](workflow.md) — шаг 10: Visual Editing + screenshot runner
