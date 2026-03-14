# Undefscene: Room Screenshot Pipeline

## Цель

Эта страница фиксирует foundation-план для mini GameMaker screenshot-builder, который должен генерировать реальные room screenshots для Undefscene editor.

Идея нужна для случаев, когда editor-side preview уже недостаточно и нужен визуальный контекст настоящей комнаты.

## Почему это отдельный pipeline

Текущий editor-app умеет:

- читать `.yyp` ресурсы и комнаты
- хранить persistent cache папку `room-screenshots`
- показывать editor-side preview для `follow_path`

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
6. Builder сохраняет файл в `room-screenshots/<room-name>.png`.
7. Editor подхватывает PNG из cache folder без повторного parse шага.

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
4. проверить, что editor cache folder может принять и переиспользовать PNG между сессиями

## Связь с editor-side preview

Editor-side preview и screenshot-builder не конкурируют друг с другом.

Они закрывают разные уровни задачи:

- `follow_path` preview — быстрый structural preview ноды
- room screenshot pipeline — настоящий visual context комнаты

Обе системы могут жить параллельно.
