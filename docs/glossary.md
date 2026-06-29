---
tags:
  - glossary
---

# Глоссарий (Glossary)

Основные термины и понятия проекта.

## Actor
Персонаж, управляемый катсценой: игрок, NPC или временный инстанс. Используют объект `obj_actor`.
[Подробнее](systems/cutscenes/actors.md)

## Action Queue
Очередь действий катсцены: массив структур `{ action, params, blocking, actor }`, выполняемых по порядку.
[Подробнее](systems/cutscenes/architecture.md)

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
Переназначение клавиши действия.
См. также: [Система ввода](systems/input.md)

## UI Blocking

Блокировка игрового ввода при открытых UI-элементах: меню, диалог, настройки, сейвы, катсцены. Проверяется через `scr_checkUIBlocking()`.

См. также: [Глобальное состояние](architecture/global-state.md), [Система UI](systems/ui.md)

---

## Inventory
Инвентарь игрока. 8 слотов, экипировка оружия и брони. Хранится в `global.inventory`.
[Подробнее](systems/inventory.md)

---

## Emote
Визуальная эмоция (иконка/анимация) над объектом или персонажем. Управляется `global.global_emote_system`.
[Подробнее](systems/emote.md)

---

## Save Slot
Слот сохранения (`save1`, `save2`, `save3`). Метаданные кэшируются в `global.__save_slot_metadata_cache`.
[Подробнее](systems/save-system.md)

---

## Room Transition
Смена игровой комнаты с fade-эффектом. Управляется `obj_changingRoomsController` и `scr_room_fade_update`.
[Подробнее](systems/room-transitions.md)

---

## NPC Dialogue
Диалог с неигровым персонажем или объектом. Запускается через `scr_interaction` / `readDialogue` и Yarn.
[Подробнее](systems/npc-dialogue.md)

---

## Debug Mode
Режим отладки, включаемый через `F12 × 5`. Предоставляет оверлеи, ghost mode и быстрые команды.
[Подробнее](systems/debug-tools.md)

---

## Dev Spawn
Быстрый спавн игрока в выбранной комнате через экран `obj_devLoader`. Координаты задаются в `global.__dev_spawn_*`.

---

## Room Fade
Fade-эффект (затемнение/осветление) при переходе между комнатами. Управляется `scr_room_fade_update`.

---

## Entity State
Состояние сущностей мира (интерактивных объектов, дверей и т.д.), сохраняемое и восстанавливаемое через `global.entity_state`.

---

## Point Marker
`obj_pointMarker` — невидимый объект перед игроком, определяющий цель взаимодействия.

---

## Undefscene
Визуальный редактор катсцен. Экспортирует катсцены как JSON. 
[Подробнее](systems/cutscenes/undefscene/overview.md)

---

## Yarn
Язык разметки диалогов.
[Подробнее](systems/dialogue-portraits.md)
