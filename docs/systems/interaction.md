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
Старые функции-обёртки **мёртвы**: тела зачищены до заглушек (`DELETE_CANDIDATE`, 0 вызовов). Рабочий путь — только `scr_interaction` (она определена в файле `scripts/interactionWithNPCsOrObjects/interactionWithNPCsOrObjects.gml`).

| Функция | Статус | Былое поведение |
|---------|--------|------------------|
| `interactionWithNPCsOrObjects(script, node)` | Заглушка (не вызывать) | `scr_interaction(script, node, false)` |
| `interactionWithMainCast(script, node)` | Заглушка (не вызывать) | `scr_interaction(script, node, true)` |

!!! tip "Когда что использовать"
    *   **NPC и объекты** — `scr_interaction(script, node)` или `scr_interaction(script, node, false)`: `point_in_rectangle` по `bbox` маркера (подходит для стен, знаков, предметов).
    *   **MainCast / персонажи** — `scr_interaction(script, node, true)`: `position_meeting` по маске для точной проверки.

## Маркер Игрока (`obj_pointMarker`)
Это невидимый объект, который всегда висит перед лицом игрока на небольшом расстоянии. Именно он определяет, с чем мы взаимодействуем.

## Коллизия
Движение игрока разрешает коллизию через `scr_collision_resolve()` с тремя группами объектов:
- `obj_collider` — базовые коллайдеры
- `par_decor` — декорации (`is_static = true`)
- `par_interactable` — интерактивные объекты

При спавне игрока выполняется проверка на застревание во всех трёх группах с поиском свободного места по спирали.
*   Если игрок поворачивается, маркер перемещается.
*   Это позволяет взаимодействовать только с тем, что находится *перед* игроком, а не спиной.

---

## См. также

- [Карта тонкой настройки UI](ui-tuning-map.md) — `obj_pointMarker`, debug draw (F3)
- [Система ввода](input.md) — `scr_input_pressed("confirm")`, UI blocking
- [NPC и диалоги](npc-dialogue.md) — `readDialogue`, Yarn-интеграция
- [Диалоговые портреты](dialogue-portraits.md) — `textboxTest_scribble`, Yarn формат
