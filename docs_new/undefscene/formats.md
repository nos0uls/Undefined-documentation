---
title: "Undefscene: Сохранение и экспорт"
tags:
  - undefscene
  - editor
  - data-formats
---

# Undefscene: Сохранение и экспорт

## Два формата файлов

Редактор работает с двумя форматами:

| Формат | Для чего | Что хранит |
|--------|----------|-----------|
| `.usc.json` | Продолжение работы в редакторе | Граф, позиции нод, связи и заметки (раскладка панелей в файл сцены не пишется — она хранится отдельно) |
| `.json` (engine) | Использование в игре | Только действия и параметры — минимум лишнего |

## Сохранение проекта

| Команда | Что делает |
|---------|-----------|
| **Save** | Сохраняет текущую сцену в уже известный `.usc.json` |
| **Save As...** | Сохраняет в новый `.usc.json` файл |
| **Open Scene** | Открывает `.usc.json` или engine `.json` обратно в редактор |
| **New Scene** | Создаёт пустую сцену |
| **Create Example** | Загружает демонстрационную сцену |

!!! warning "Open Scene заменяет текущую"
    При открытии другой сцены текущая несохранённая работа будет потеряна. Редактор предупредит об этом.

## Экспорт для игры

File → **Export to Game...** (или Ctrl+E) создаёт чистый `.json`, который игра читает через `cutscene_load_json()`.

Сохраните экспортированный файл в папку `datafiles/cutscenes/` проекта GameMaker.

### Структура engine `.json`

Корень файла — объект:

| Поле | Тип | Описание |
|------|-----|----------|
| `schema_version` | number | Версия схемы экспорта (сейчас `1`) |
| `cutscene_id` | string | Идентификатор катсцены — slug из названия сцены |
| `settings` | object | Настройки воспроизведения |
| `settings.fps` | number | Частота кадров для конвертации секунд в кадры. Экспортёр всегда пишет `30`; движок при чтении принимает значения 1–240, при значении вне диапазона берёт `default_fps` из настроек движка |
| `actions` | array | Список действий катсцены |

Экспортёр записывает только перечисленные поля. Движок дополнительно понимает два «скрытых» поля, которые можно задать ручной правкой файла: `settings.skippable` — `false` запрещает пропуск катсцены кнопкой `back` (по умолчанию `true`), и `debug: true` на первом действии `start` — выводит в консоль лог выполнения действий.

```json title="Пример engine .json (реальный вывод экспортёра)"
{
  "schema_version": 1,
  "cutscene_id": "intro_scene",
  "settings": { "fps": 30 },
  "actions": [
    { "type": "mark_node", "name": "Start" },
    { "type": "start" },
    { "type": "mark_node", "name": "MOVE_1" },
    { "type": "move", "target": "asher", "x": 320, "y": 240, "speed_px_sec": 60 }
  ]
}
```

- Каждый элемент `actions` — объект с полем `type` и параметрами действия. Полный список типов и полей — в разделе [JSON-экшены катсцен](../cutscenes/json-actions.md).
- `{"type": "start"}` идёт первым действием; флаг `debug` движок читает только если `start` — самый первый элемент `actions`. Действие `{"type": "end"}` завершает список и понимается движком (действия после него не выполняются), но экспортёр его **не записывает** — обход массива просто заканчивается. Узел End в графе нужен для структуры и валидации.
- `{"type": "mark_node", "name": "…"}` — служебные метки, которые экспортёр ставит перед каждой именованной нодой, включая `start` (у него имя `Start` по умолчанию). На них ссылается действие `goto`.
- Часть legacy-имён движок нормализует автоматически: `waittalk`/`wait_talk` → `wait_for_dialogue`, `instant_mode` → `set_instant`, `shakeobj` → `shake_object`, `visible` → `set_visible`, `depth` → `set_depth`, `facing` → `set_facing`, `autofacing` → `auto_facing`, `autowalk` → `auto_walk`, `destroy_entity`/`destroy` → `actor_destroy`, `emote` → `show_emote`. Редактор при экспорте пишет актуальные имена; обратный импорт распознаёт и легаси-алиасы.

## Обратный импорт

Редактор открывает engine `.json` обратно: **Open Scene** → выберите файл. Граф восстановится из массива действий.

Если файл повреждён или не соответствует формату — импорт будет отклонён.

!!! note "Формат checkpoint полей"
    Поля `include_globals` и `include_instances` ноды `checkpoint_state` в Inspector ожидаются как JSON-строки (например, `"[\"var1\"]"`). При обратном импорте engine `.json` редактор корректно разбирает их и в виде строк, и в виде нативных JSON-массивов — массивы конвертируются в текстовое представление в параметрах ноды.

---

## См. также

- [Создание катсцены](workflow.md) — пошаговый процесс
- [Справочник нод](nodes.md) — все ноды с параметрами
- [Проверки и ошибки](validation.md) — что означают предупреждения
- [Катсцены: обзор](../cutscenes/overview.md) — как катсцены работают в игре

<!-- sources: editor-app/src/renderer/src/editor/compiler/exporters.ts:3-17; editor-app/src/renderer/src/editor/compiler/core.ts:218-232,374-379; editor-app/src/renderer/src/editor/reverseCompile.ts:66-82,620-628; editor-app/src/renderer/src/editor/useSceneIO.ts:84-239; editor-app/src/renderer/src/editor/runtimeTypes.ts:225-430; editor-app/src/renderer/src/editor/TopMenuBar.tsx:246-289; Undefinedtale888/scripts/cutscene_load_json/cutscene_load_json.gml:93-149,151-157,170-175,223-235; my-docs-repo/docs_new/_meta/json_actions.txt -->
