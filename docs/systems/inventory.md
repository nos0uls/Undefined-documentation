---
tags:
  - inventory
  - runtime
---

# Система инвентаря (Inventory System)

ООП-инвентарь из 8 слотов, конструкторы предметов и экипировка, сериализуемые в save-файл.

## Обзор

Инвентарь хранится в `global.inventory` — массиве на 8 ячеек, где `undefined` означает пустой слот. Инициализация происходит в [`obj_Init`](../architecture/objects.md) через `scr_inventory_init`. Предметы создаются через конструкторы из `constructorsForInventory`, а фабрика `item_database` позволяет получать новые экземпляры по имени.

Основные типы предметов:

- `WeaponItem` — оружие, влияет на стат `global.equipped_weapon`.
- `ArmorItem` — броня, влияет на `global.equipped_armor`.
- `FoodItem` — расходник, восстанавливает HP и уменьшает `amount` при использовании.
- Базовый `Item` — универсальный предмет без боевого эффекта.

## Архитектура / API

### Конструкторы предметов

| Конструктор | Параметры | Поля | Описание |
|-------------|-----------|------|----------|
| `Item` | `_name`, `_description` | `name`, `description`, `itemType` | Базовый предмет, `itemType = ITEMTYPE.UNDEFINED`. |
| `WeaponItem` | `_name`, `_damage`, `_description` | `damage` | `itemType = ITEMTYPE.WEAPON`, `use()` экипирует оружие. |
| `ArmorItem` | `_name`, `_defense`, `_description` | `defense` | `itemType = ITEMTYPE.DEFENSE`, `use()` экипирует броню. |
| `FoodItem` | `_name`, `_amount`, `_heal`, `_description` | `heal`, `amount` | `itemType = ITEMTYPE.FOOD`, `use()` восстанавливает HP и уменьшает `amount`. |

Методы каждого предмета:

- `getDisplayName()` — имя для UI (`FoodItem` добавляет `x<count>`).
- `getStatBonus()` — строка с бонусом (урон, защита, HP).
- `use()` — применяет эффект. Возвращает `true`, если предмет нужно удалить из инвентаря (например, `FoodItem` закончился).
- `serialize()` — структура для JSON-сейва.

### Типы предметов (`ITEMTYPE`)

| Значение | Описание |
|----------|----------|
| `ITEMTYPE.WEAPON` | Оружие |
| `ITEMTYPE.DEFENSE` | Броня |
| `ITEMTYPE.FOOD` | Расходник |
| `ITEMTYPE.SOMEPERK` | Зарезервированный тип |
| `ITEMTYPE.UNDEFINED` | Базовый/неизвестный тип |

### Фабрика и база данных предметов

```gml title="script_items.gml"
// Получить новый экземпляр предмета по имени
var _knife = item_database("Real Knife");

// Зарегистрировать собственную фабрику
item_database_register("My Potion", function() {
    return new FoodItem("My Potion", 1, 25, "Heals 25 HP.");
});
```

### Сериализация

```gml title="constructorsForInventory.gml"
// Преобразовать весь инвентарь в JSON-массив
var _json = json_stringify(inventory_serialize(global.inventory));

// Восстановить инвентарь из JSON
var _inv = inventory_deserialize(json_parse(_json));
```

Сериализация сохраняет `__type`, `name`, `description` и специфичные поля (`damage`, `defense`, `heal`, `amount`). Экипировка после загрузки восстанавливается по имени и типу, а не по ссылке, поэтому создаются новые инстансы предметов.

## Примеры

### Создание стартового инвентаря

```gml title="scr_inventory_init"
global.inventory = array_create(8, undefined);
global.inventory[0] = new WeaponItem("Real Knife", 99, "CUTSCENE DIALOGUE");
global.inventory[1] = new FoodItem("Chocolate", 1, 40, "CUTSCENE DIALOGUE");
global.inventory[2] = new ArmorItem("Scarf", 9, "CUTSCENE DIALOGUE");

global.equipped_weapon = global.inventory[0];
global.equipped_armor  = global.inventory[2];
```

### Использование предмета из инвентаря

```gml title="Пример использования еды"
var _item = global.inventory[3];
if (is_struct(_item) && variable_struct_exists(_item, "use")) {
    var _consume = _item.use();
    if (_consume) {
        global.inventory[3] = undefined; // Предмет израсходован
    }
}
```

### Регистрация кастомного предмета

```gml title="Расширение item_database"
item_database_register("Golden Apple", function() {
    return new FoodItem("Golden Apple", 1, 50, "Restores 50 HP.");
});

var _apple = item_database("Golden Apple");
```

## Troubleshooting

!!! warning "Экипировка не сохраняется"
    `scr_saveSave` записывает индексы экипировки, а не ссылки. После `scr_saveLoad` она восстанавливается по совпадению `name` и `itemType`. Если в инвентаре оказались два одинаковых предмета, выбирается первый подходящий слот.

!!! note "Старые сейвы без JSON-инвентаря"
    `scr_saveLoad` пропускает блоки инвентаря, флагов и `entity_state`, если их нет в файле. Игра продолжает работать с дефолтным инвентарем.

## См. также

- [Система сохранений](save-system.md) — `scr_saveSave`, `scr_saveLoad`
- [GML-скрипты](../code-reference/gml-scripts.md) — полный список скриптов
- [Архитектура: объекты](../architecture/objects.md) — `obj_Init`, `obj_saveManager`
