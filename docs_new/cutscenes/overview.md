---
title: Катсцены — обзор
tags:
  - cutscenes
  - cutscene-json
  - cutscene-api
  - undefscene
---

# Катсцены — обзор

Катсцена в Undefinedtale-888 — очередь action-структур с контрактом `start`/`update`/`cleanup`, которую покадрово исполняет persistent-объект `obj_cutsceneManager`. Сцена управляет актёрами, камерой, музыкой и диалогами, забирая у игрока частичный или полный контроль до конца очереди.

## Три способа задать катсцену

### JSON-файл: канонический

Сцена описывается JSON-файлом в `datafiles/cutscenes/` и загружается через `cutscene_load_json`:

- `cutscene_load_json(_path)`: читает файл (`buffer_load` + `json_parse`), создаёт менеджер и заполняет `action_queue` через фабрику `cutscene_init_action_factory`. Возвращает менеджер или `noone` при ошибке.
- `cutscene_play_json(_path)`: то же + немедленный `start_cutscene`.
- Путь задаётся относительно рабочей директории: Included Files в рантайме лежат в корне, префиксы `./` и `datafiles/` срезаются автоматически. Пример: `cutscene_play_json("cutscenes/cutscene1.json")`.
- `settings.fps` задаёт пер-файловый FPS для конвертации `seconds` в кадры, `settings.skippable`: можно ли пропустить сцену кнопкой `back` (см. [архитектуру](architecture.md)).

### GML напрямую

Процедурная сборка очереди из кода: менеджер создаётся `instance_create_layer(..., obj_cutsceneManager)`, действия: конструкторами `Action*` из `scr_cutscene_classes`, в очередь кладутся через `cutscene_add(_mgr, _action)`, запуск: `_mgr.start_cutscene()`. `cutscene_add` нормализует минимум контракта (флаг `started`) и отбрасывает не-struct с логом только при `global.debug`.

!!! warning "scr_cutscene_make: заглушка"
    `scr_cutscene_make()` помечена `DELETE_CANDIDATE`: тело зачищено, функция всегда возвращает `noone`, вызовов в проекте нет. Фабрикой менеджера для кода служит `c_begin()`.

### `c_*`-DSL: код и Yarn

Командный слой `c_*` (скрипты `c_begin`, `c_play`, `c_end`, `c_cmd` и одноимённые файлы команд) — тот же движок через сессию «билдера»:

- `c_begin(_id)` создаёт build-менеджер в `global.__cutscene_build_mgr`; каждая `c_*`-команда пушит action через `cutscene_add`; `c_play()` запускает сцену; `c_end()` закрывает сессию билдера или останавливает играющую катсцену.
- Все команды зарегистрированы в Chatterbox (`cutscene_register_chatterbox_functions` вызывается из `obj_Init`), поэтому из Yarn вызываются как `<<c_wait(60)>>`, `<<c_play_json("cutscenes/intro.json")>>`.
- Подходит для коротких сцен внутри диалогов и прототипирования без файлов.

## Когда что использовать

| Способ | Когда применять |
|--------|-----------------|
| JSON (`cutscene_play_json`) | Контентные сцены: сюжетные катсцены, экспорт из Undefscene, версионируемые файлы в `datafiles/cutscenes/` |
| `c_*`-DSL | Короткие вставки из кода или внутри Yarn-диалогов: команды разбросаны по репликам |
| `cutscene_add` + `Action*` | Динамические сцены, собираемые в рантайме: сгенерированные ветки, тестовая автоматика |

## Глобальное состояние

| Глобал | Назначение |
|--------|------------|
| `global.cutscene_active` | `true`, пока играет катсцена (инициализируется в `obj_Init`) |
| `global.active_cutscene_manager` | Инстанс `obj_cutsceneManager` текущей сцены |
| `global.active_cutscene_id` | Строковый `cutscene_id` активной сцены |
| `global.cutscene_camera_override` | `true`: сцена управляет камерой, follow-камера игрока отключена |
| `global.__cutscene_build_mgr` | Недозапущенный build-менеджер из `c_begin` |

## Связка с Undefscene

Визуальный редактор Undefscene экспортирует граф нод в JSON того же формата; каноничное расположение на диске: `datafiles/cutscenes/`, то есть ровно там, где его читает `cutscene_load_json`. Подробности: [обзор редактора](../undefscene/overview.md).

## Быстрый старт

Минимальная рабочая катсцена `datafiles/cutscenes/cutscene1.json` содержит метки `mark_node` (навигация `goto`, остановки `stop_when: "node_reached"`), `wait` в секундах и блокирующий `dialogue` на yarn-файле:

```json title="datafiles/cutscenes/cutscene1.json"
{
  "schema_version": 1,
  "cutscene_id": "untitled_cutscene",
  "settings": {
    "fps": 60
  },
  "actions": [
    {
      "type": "mark_node",
      "name": "Start"
    },
    {
      "type": "wait",
      "seconds": 1.5
    },
    {
      "type": "mark_node",
      "name": "Node"
    },
    {
      "type": "dialogue",
      "file": "intro.yarn",
      "node": "Greeting",
      "block_queue": true
    },
    {
      "type": "mark_node",
      "name": "End"
    }
  ]
}
```

Запуск из кода: `cutscene_play_json("cutscenes/cutscene1.json")`, из Yarn: `<<c_play_json("cutscenes/cutscene1.json")>>`. Менеджер сам ставит `global.cutscene_active`, фризит игрока (при `partial_control_type == 0`) и возвращает управление после конца очереди.

## См. также

- [Архитектура менеджера](architecture.md) — жизненный цикл, переходы комнат, watchdog
- [JSON-действия](json-actions.md) — все типы `actions[]`
- [GML и `c_*`-DSL](gml-dsl.md) — команды билдера и Yarn-интеграция
- [Частичный контроль](partial-control.md) — `partial_control`, `wait_for_interact`
- [Актёры и камера](actors-and-camera.md) — `actor_map`, движение, camera-действия
- [Рецепты](cookbook.md) — готовые примеры сцен
- [Обзор Undefscene](../undefscene/overview.md) — визуальный редактор катсцен
- [Форматы данных](../architecture/data-formats.md) — схема JSON и engine-настройки
- [Диалоги](../systems/dialogue.md) — Chatterbox и yarn-файлы

<!-- sources: objects/obj_cutsceneManager/Create_0.gml:4-34; objects/obj_cutsceneManager/Step_0.gml:1-26; scripts/cutscene_load_json/cutscene_load_json.gml:7-235; scripts/cutscene_action_factory/cutscene_action_factory.gml:6-10,144-163; scripts/cutscene_add/cutscene_add.gml:6-45; scripts/scr_cutscene_make/scr_cutscene_make.gml:1-10; scripts/c_begin/c_begin.gml:1-32; scripts/c_play/c_play.gml:1-22; scripts/c_end/c_end.gml:4-54; scripts/c_cmd/c_cmd.gml:114-213; objects/obj_Init/Create_0.gml:149-163,269-270; datafiles/cutscenes/cutscene1.json; undefscene-repo editor-app/src/main/ipc.ts:1293-1296,1387-1397 -->
