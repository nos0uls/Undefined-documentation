---
tags:
  - gameplay
---

# Система Взаимодействия (Interaction System)

Унифицированная система общения с NPC и взаимодействия с игровыми объектами.

## Принцип работы

Взаимодействие инициируется при нажатии `confirm` при соблюдении условий:
1.  Игрок находится в радиусе действия объекта.
2.  Вектор взгляда игрока направлен на объект (проверка через `obj_pointMarker`).
3.  Отсутствует блокировка интерфейса (`scr_checkUIBlocking`).

## API Справочник

### `scr_interaction(_scriptToReadFrom, _node, [_use_mask_check])`
Основная функция для запуска взаимодействия.

*   `_scriptToReadFrom`: Имя файла Yarn диалога (строка).
*   `_node`: Имя стартового узла в Yarn (строка).
*   `_use_mask_check` (опционально):
    *   `false` (по умолчанию): Использует проверку попадания точки маркера в прямоугольник (`bbox`) объекта. Точнее для мелких объектов.
    *   `true`: Использует физическое пересечение масок (`place_meeting`) маркера и объекта.

!!! warning "Путь к Yarn-файлу"
    Yarn-файлы хранятся в `Included Files/datafiles/Dialogues`.
    Для `scr_interaction(...)` передавайте только имя файла (например, `"fountain.yarn"`), без префикса `Dialogues/`.

```gml title="Step-событие NPC" linenums="1"
// Запустит диалог, если игрок нажмёт Confirm рядом
scr_interaction("npc_dialogue.yarn", "StartNode");
```

### Совместимость
Старые функции-обёртки вызывают `scr_interaction` внутри:

| Функция | Что делает | Проверка |
|---------|-----------|----------|
| `interactionWithNPCsOrObjects(script, node)` | `scr_interaction(script, node, false)` | `bbox` (точнее для мелких объектов) |
| `interactionWithMainCast(script, node)` | `scr_interaction(script, node, true)` | `place_meeting` (маска, для персонажей) |

!!! tip "Когда что использовать"
    *   **NPC и объекты** (`interactionWithNPCsOrObjects`) — `bbox` подходит для стен, знаков, предметов.
    *   **MainCast / персонажи** (`interactionWithMainCast`) — `place_meeting` нужен для точной проверки маски персонажа.

## Маркер Игрока (`obj_pointMarker`)
Это невидимый объект, который всегда висит перед лицом игрока на небольшом расстоянии. Именно он определяет, с чем мы взаимодействуем.
*   Если игрок поворачивается, маркер перемещается.
*   Это позволяет взаимодействовать только с тем, что находится *перед* игроком, а не спиной.

---

## См. также

- [Карта тонкой настройки UI](ui-tuning-map.md) — `obj_pointMarker`, debug draw (F3)
- [Система ввода](input.md) — `scr_input_pressed("confirm")`, UI blocking
- [Диалоговые портреты](dialogue-portraits.md) — `textboxTest_scribble`, Yarn формат
