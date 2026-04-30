# Глоссарий (Glossary)

## Actor

Персонаж, управляемый катсценой: игрок, NPC или временный созданный экземпляр. Все акторы используют один и тот же объект `obj_actor` с разными `chara_sprites`.

См. также: [Актёры катсцен](systems/cutscenes/actors.md)

---

## Action Queue

Очередь действий катсцены: массив объектов `{ action, params, blocking, actor }`, который `obj_cutsceneManager` выполняет по порядку.

См. также: [Архитектура катсцен](systems/cutscenes/architecture.md)

---

## Blocking

Свойство действия катсцены: если `blocking == true`, менеджер ждёт завершения действия перед переходом к следующему. См. также **UI Blocking**.

---

## Chatterbox

Библиотека-обёртка для парсинга Yarn-файлов (`.yarn`) в runtime GameMaker. Используется для диалогов и катсцен.

---

## Edge

Ребро графа катсцены: соединение между двумя нодами с направлением. Может иметь условие `condition`.

См. также: [Undefscene: валидация](systems/cutscenes/undefscene/validation.md)

---

## Face System

Система эмоций лиц персонажей: каждый актёр имеет таблицу `face_sprites` — mapping `emotion → sprite`.

См. также: [Диалоги и портреты](systems/dialogue-portraits.md)

---

## Global State

Глобальное состояние игры, хранящееся между комнатами и сессиями: настройки, инвентарь, состояние квестов, позиция игрока.

См. также: [Глобальное состояние](architecture/global-state.md)

---

## Init Room (`rm_init`)

Первая комната при запуске. Пустая, содержит только `obj_Init` для инициализации систем. После загрузки сразу переходит в главное меню.

См. также: [Инициализация](architecture/initialization.md)

---

## Input Map

Структура, собранная `scr_buildInputMap()`: mapping `действие → [клавиша1, клавиша2]`. Хранится в `global.input_map`.

См. также: [Система ввода](systems/input.md)

---

## Node

Нода графа катсцены: точка с типом (`start`, `move`, `dialogue`, `camera_pan`, `end`, и др.). Содержит параметры действия.

См. также: [Катсцены: обзор](systems/cutscenes/overview.md)

---

## Rebind

Переназначение клавиши действия. Защищает дефолтные клавиши (`Z`, `Enter`, `Esc`) от перезаписи.

См. также: [Система ввода](systems/input.md)

---

## UI Blocking

Блокировка игрового ввода при открытых UI-элементах: меню, диалог, настройки, сейвы, катсцены. Проверяется через `scr_checkUIBlocking()`.

См. также: [Глобальное состояние](architecture/global-state.md), [Система UI](systems/ui.md)

---

## Undefscene

Визуальный редактор катсцен для проекта Undefinedtale-888. Работает поверх React Flow, экспортирует граф в JSON для движка.

См. также: [Обзор Undefscene](systems/cutscenes/undefscene/overview.md)

---

## Yarn

Формат файлов диалогов, используемый в проекте. Файлы имеют расширение `.yarn` и парсятся через Chatterbox.

См. также: [Система диалогов и портретов](systems/dialogue-portraits.md)

---

## `???` Collapsible Block

Сворачиваемый блок MkDocs Material. Используется для скрытия дополнительной информации: подробных таблиц переменных, примеров, деталей реализации.

См. также: стайл-гайд документации в `.windsurf/plans/docs-style-guide.md` (вне корня docs).
