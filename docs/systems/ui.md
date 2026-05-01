---
tags:
  - ui
  - ui-blocking
---

# Система Интерфейса (UI System)

Система UI (User Interface) управляет окнами, меню и блокировкой ввода.

## UI Blocking (`scr_checkUIBlocking`)

В отличие от полноценного UI Stack, блокировка ввода реализована через `scr_checkUIBlocking()`. Это функция, которая проверяет существование ключевых UI-объектов и возвращает `true`, если ввод должен быть заблокирован.

### Принцип работы

Блокировка срабатывает, если выполнено хотя бы одно из условий:

| Условие | Описание |
|---------|----------|
| `global.settings_closing` | Меню настроек закрывается (временная блокировка) |
| `global.active_cutscene_id != ""` | Идёт катсцена |
| `global.cutscene_camera_override == true` | Камера захвачена катсценой |
| `instance_exists(textboxTest_scribble)` | Открыт диалог |
| `instance_exists(obj_settingsManager)` | Открыты настройки |
| `instance_exists(obj_menu)` | Открыто главное меню |
| `instance_exists(obj_saveManager)` | Открыт экран сейвов |
| `instance_exists(obj_inGameMenu)` | Открыто in-game меню |

### Функция

#### `scr_checkUIBlocking(exclude_self = false, include_cutscene = true)`
Проверяет, заблокирован ли ввод из-за открытых UI элементов.
*   `exclude_self`: если `true`, исключает текущий объект из проверки (полезно для самого меню, чтобы оно работало).
*   `include_cutscene`: если `true`, катсцены и `cutscene_camera_override` тоже блокируют ввод.

```gml
// В коде игрока
if (!scr_checkUIBlocking()) {
    // Можно двигаться
}
```

### Как это работает в объектах

Объекты меню (`obj_menu`, `obj_settingsManager`, `obj_saveManager`) не регистрируются явно — их существование проверяется напрямую в `scr_checkUIBlocking`. Игрок и NPC вызывают эту функцию перед обработкой движения и взаимодействия.



## Диалоговые окна (Textbox)
Диалоговая система использует `Scribble` для отрисовки текста и `Chatterbox` для логики.

### Отрисовка опций выбора
Логика отрисовки опций в `obj_textbox` (и его наследниках, например `textboxTest_scribble`) зависит от количества вариантов ответа.

!!! note "Логика расположения (Layout)"
    Разные количества опций требуют разного выравнивания (`wrap` width) и позиционирования.

#### Конфигурация ширины (`__col_wrap`)
Ширина текста ограничивается в зависимости от количества колонок:
- **1 опция**: 80% ширины (`inner_width * 0.8`)
- **2 опции**: 36% ширины (`inner_width * 0.36`)
- **3 опции**: 28% ширины (`inner_width * 0.28`)
- **4 опции**: 18% ширины для каждой (`inner_width * 0.18`), используются индивидуальные параметры `__col_wrap_4`.

#### Позиционирование
- **2 опции**: Разделены на левую и правую колонки (центры на 25% и 75% ширины).
- **3 опции**: Равномерно распределены (17%, 50%, 83%).
- **4 опции**: Расположены "ромбом" (или крестом):
    - Левый: 25% ширины, центр по Y.
    - Правый: 75% ширины, центр по Y.
    - Нижний: 50% ширины, смещен вниз (`+60px`).
    - Верхний: 50% ширины, смещен вверх (`-60px`).

```gml
// Пример логики 4-х опций
var option_spacing_4_x = [0, 0]; 
var option_spacing_4_y = [0, 0]; 
if (option_count == 4) {
    option_spacing_4_x[0] = inner_width * 0.25; // левая
    option_spacing_4_x[1] = inner_width * 0.75; // правая
    option_spacing_4_y[0] = 60; // вниз
    option_spacing_4_y[1] = 60; // вверх
}
```

---

## См. также

- [Карта тонкой настройки UI](ui-tuning-map.md) — layout-переменные textbox, portrait, marker
- [Диалоговые портреты](dialogue-portraits.md) — `textboxTest_scribble`, `obj_face`
- [Система ввода](input.md) — `scr_checkUIBlocking()`
- [Глобальное состояние](../architecture/global-state.md) — UI blocking флаги
