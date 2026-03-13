# Система Ввода (Input System)

Игра использует единый API ввода (`scr_inputApi`), который абстрагирует физические клавиши от игровых действий.

## Архитектура Ввода

```mermaid
graph LR
    Keyboard[Клавиатура] --> InputMap[Input Map]
    InputMap --> Actions[Actions]
    Actions --> |Block?| Cutscene[Cutscene Guard]
    Cutscene --> GameLogic[Игровая Логика]
    
    subgraph "Mapping"
    InputMap
    end
    
    subgraph "Virtualization"
    Cutscene
    end
```

## Основные Понятия

*   **Action (Действие)**: Строковый ID действия (например, `"confirm"`, `"jump"`, `"menu"`).
*   **Input Map**: Глобальная структура `global.input_map`, связывающая Action с физическими клавишами (поддерживается до 2 клавиш на действие).
*   **Input Repeater**: Система для повторения нажатий (как при печати текста) для навигации в меню.

## API Справочник

### Проверка ввода

#### `scr_input_pressed(action)`
Возвращает `true`, если действие было активировано в *этом* кадре.
```gml
if (scr_input_pressed("jump")) {
    player_jump();
}
```

#### `scr_input_down(action)`
Возвращает `true`, пока кнопка действия удерживается.
```gml
if (scr_input_down("run")) {
    move_speed = run_speed;
}
```

#### `scr_input_repeater(action, [delay, interval])`
Возвращает `true` периодически, если кнопка удерживается. Идеально для списков меню.
*   `delay`: Задержка перед началом повтора (мс).
*   `interval`: Частота повторов (мс).

### Блокировка Катсценами
Функция `scr_input__is_cutscene_blocked_here()` проверяет, идет ли катсцена.
*   Если **Да**: Ввод перехватывается. Игрок не получает `true` от `scr_input_pressed`, если только катсцена не "нажимает" кнопки виртуально.
*   **Исключения**: UI объекты (`obj_menu`, `obj_textbox`) игнорируют блокировку катсцен, чтобы меню паузы работало.

### Переназначение (Rebinding)

#### `scr_input_rebind_slot(action, slotIndex, new_key, [target_settings])`
Переназначает конкретный слот клавиши. Используется для primary/secondary binding и защищает дефолтные клавиши от конфликтной перезаписи.

*   `slotIndex = 1` — основной слот
*   `slotIndex = 2` — альтернативный слот

```gml
// Назначить Пробел на primary-slot действия "confirm"
scr_input_rebind_slot("confirm", 1, vk_space);
```