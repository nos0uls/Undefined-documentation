---
title: Инвентарь и статы
tags:
  - inventory
  - stats
  - menu
  - ui
  - save-system
---

# Инвентарь и статы

ООП-инвентарь на 8 слотов (`global.inventory`), классы предметов с методом `use()`, экипировка и статы персонажа (`global.stat_*`), сериализуемые в save-файл.

## Обзор

Инвентарь — массив `global.inventory` ровно на 8 слотов, где `undefined` означает пустую ячейку. Инвариант размера зашит в `inventory_deserialize` и читается UI напрямую через `array_length`. Инициализация — `scr_inventory_init()` из `obj_Init/Create_0`; тот же вызов выполняют `scr_defaultLoad` (новая игра) и `scr_saveLoad` (фолбэк при отсутствии секции инвентаря в сейве).

Предметы — экземпляры struct-классов из `scripts/constructorsForInventory/`. Тип предмета определяет поле `itemType` (enum `ITEMTYPE` из `scripts/currentENUMS/`).

## Конструкторы предметов

Все классы наследуют `Item` и переопределяют `use()` и `serialize()`:

| Конструктор | Параметры | `itemType` | Свои поля |
|---|---|---|---|
| `Item` | `_name`, `_description = "An Item"` | `ITEMTYPE.UNDEFINED` | `name`, `description` |
| `WeaponItem` | `_name`, `_damage = 20`, `_description` | `ITEMTYPE.WEAPON` | `damage` |
| `ArmorItem` | `_name`, `_defense = 9`, `_description` | `ITEMTYPE.DEFENSE` | `defense` |
| `FoodItem` | `_name`, `_amount = 1`, `_heal = 10`, `_description` | `ITEMTYPE.FOOD` | `heal`, `amount` |

Методы каждого предмета:

- `getDisplayName()` — имя для UI; `FoodItem` возвращает `"name xN"` со счётчиком стопки.
- `getStatBonus()` — строка бонуса (`string(damage)` у оружия, `string(defense)` у брони, `"+N HP"` у еды); у базового `Item` — `""`.
- `use()` — оркестрация без прямых мутаций состояния: у наследников вызывает `scr_item_apply_use(self)` и показывает нотификацию через `global.show_notification`. Возвращает consumed-bool: `true` — слот надо очистить. У базового `Item` `use()` лишь пишет debug-сообщение и возвращает `false`.
- `serialize()` — плоский struct для сейва с полем `__type` (`"item"`, `"weapon"`, `"armor"`, `"food"`) и специфичными полями (`damage`, `defense`, `heal`, `amount`).

### Enum `ITEMTYPE`

| Значение | Класс | Эффект при `use()` |
|---|---|---|
| `ITEMTYPE.WEAPON` | `WeaponItem` | Экипировка в `global.equipped_weapon` |
| `ITEMTYPE.DEFENSE` | `ArmorItem` | Экипировка в `global.equipped_armor` |
| `ITEMTYPE.FOOD` | `FoodItem` | Лечение `stat_hp`, декремент `amount` |
| `ITEMTYPE.SOMEPERK` | — | Зарезервировано, класса и обработчика нет |
| `ITEMTYPE.UNDEFINED` | `Item` | Эффекта нет |

## Фабрика и добавление предметов (`script_items`)

| Функция | Сигнатура | Назначение |
|---|---|---|
| `item_database_register` | `(_name, _factory)` | Регистрирует фабрику в runtime-реестре `global.__item_database_registry` |
| `item_database` | `(_name) -> struct|undefined` | Новый экземпляр предмета по имени: сначала реестр, затем hardcoded-фолбэк (`"Real Knife"`, `"Scarf"`, `"Chocolate"`); неизвестное имя — `undefined` + `[ITEM_DB] Unknown item` в лог |
| `inventory_add` | `(_item_or_name) -> real` | Кладёт предмет в первый свободный слот; принимает struct или строку (резолвится через `item_database`). Возвращает индекс слота или `-1` |

Особенности `inventory_add`:

- `FoodItem` одного имени стакается в существующую стопку (`amount` суммируется), свободный слот не занимается.
- При переполнении показывает `"Inventory is full"` и возвращает `-1`.
- До `scr_inventory_init` (нет `global.inventory`) вызов логирует WARN и возвращает `-1`.

!!! warning "Не проверено"
    `inventory_add` задекларирован как точка входа для катсцен, дропов и чит-кодов, но в ревизии `7ee444a` прод-вызывателей нет — `item_database` зовут только стресс-тесты (`scr_stress_tests`).

## Применение эффекта (`scr_item_apply_use`)

`scr_item_apply_use(_item)` — единственное место мутаций состояния при использовании предмета. Таблица эффектов по `itemType`:

| `itemType` | Мутации | Возврат |
|---|---|---|
| `ITEMTYPE.WEAPON` | `global.equipped_weapon = _item`, `scr_stats_recalc()` | `false` (предмет остаётся в слоте) |
| `ITEMTYPE.DEFENSE` | `global.equipped_armor = _item`, `scr_stats_recalc()` | `false` |
| `ITEMTYPE.FOOD` | `stat_hp = min(stat_hp + heal, stat_maxhp)`, `amount -= 1` | `true`, если `amount <= 0` |
| `UNDEFINED` / прочие | — | `false` |

Контракты:

- **consumed-bool**: `true` означает «удалить предмет из слота» — очистку выполняет вызывающий код (см. `obj_inGameMenu` ниже).
- **guard на не-struct**: аргумент не-struct → `[ITEM] WARN` в лог и `false`, мутации пропускаются.
- **guard полного HP** дублируется в `FoodItem.use()` (нотификация `"HP is already full"`) и в самой функции — прямой вызов в обход оркестрации не списывает порцию впустую.

## Статы персонажа

Глобалы объявляет `scr_inventory_init` (дефолты — placeholder-значения):

| Глобал | Дефолт | Назначение |
|---|---|---|
| `global.stat_hp` | `99` | Текущее HP |
| `global.stat_maxhp` | `99` | Максимум HP, потолок лечения |
| `global.stat_base_atk` | `0` | Базовый ATK без экипировки |
| `global.stat_base_def` | `0` | Базовая DEF без экипировки |
| `global.stat_atk` | вычисляется | Эффективный ATK (пишет только `scr_stats_recalc`) |
| `global.stat_def` | вычисляется | Эффективная DEF (пишет только `scr_stats_recalc`) |
| `global.stat_lv` | `20` | Уровень |
| `global.stat_gold` | `99` | Деньги |
| `global.player_name` | `"CHARA"` | Имя для экрана STAT |

### `scr_stats_recalc`

Живёт в том же файле `scr_inventory_init.gml`. Формула:

```gml title="scripts/scr_inventory_init/scr_inventory_init.gml"
global.stat_atk = global.stat_base_atk + _wpn_dmg; // _wpn_dmg = equipped_weapon.damage или 0
global.stat_def = global.stat_base_def + _arm_def; // _arm_def = equipped_armor.defense или 0
```

Прямая запись в `stat_atk`/`stat_def` бессмысленна — значение перезапишет первый же пересчёт. Вызывать после смены экипировки, загрузки сейва и изменения базовых статов.

## Экипировка, использование, выброс

Точки вызова `scr_stats_recalc` в проде:

- `scr_item_apply_use` — после записи `equipped_weapon`/`equipped_armor` (экипировка через `use()`).
- `obj_inGameMenu/Step_0` — после подтверждённого DROP: если выброшенный предмет был экипирован, ссылки `global.equipped_*` обнуляются до `undefined`; пересчёт выполняется после любого удаления.
- `scr_inventory_init` — после установки стартовой экипировки.
- `scr_saveLoad` — после применения статов из сейва.

Отдельного действия «снять экипировку» в меню нет: замена происходит экипировкой другого предмета, снятие — только выбросом надетого.

## UI инвентаря (`obj_inGameMenu`)

Меню открывает `scr_callMenuInit` по клавише `menu` (если нет UI-блокеров `scr_checkUIBlocking`); создаётся `obj_inGameMenu`, у `obj_player` сбрасывается `can_move`. Корневые пункты — `["ITEM","STAT","OPT"]`; `OPT` обязан оставаться на индексе `INGAME_MENU_OPT_INDEX` (`2`) — константу читает `obj_settingsManager`.

Вкладка ITEM (`current_option == 1`):

- Список рендерит все 8 слотов; пустые рисуются `"------"` серым. Навигация `up`/`down` пропускает пустые слоты, курсор `item_selOption` приводится к первому занятому.
- `confirm` на занятом слоте открывает ряд действий `["USE","INFO","DROP"]` (`item_use` 1–3, `left`/`right`):
  - **USE** — `_it_use.use()`; при `true` слот очищается и `global.item_count -= 1`.
  - **INFO** — показывает `description` предмета через `global.show_notification`.
  - **DROP** — вход в подтверждение YES/NO (`drop_confirming`); при YES предмет удаляется (с снятием экипировки, см. выше).
- `back`/`menu` возвращают на уровень выше; в корне закрывают меню и возвращают `can_move`.

Вкладка STAT (`current_option == 2`) рендерит `stat_text` — шесть строк `NAME/LV/HP/DAMAGE/DEFENSE/MONEY`, пересобираемых каждый кадр Draw_64, поэтому изменение HP едой видно сразу.

Ввод читается через `scr_ui_read_actions(true)` — см. [Система ввода](input.md).

## Сериализация в сейв

`scr_saveSave` (формат v3, append-only) пишет:

1. `inventory_serialize(global.inventory)` → `json_stringify` — массив из `serialize()` каждого слота, `undefined` для пустых/чужих записей.
2. Два индекса экипировки (`_eq_w`, `_eq_a`, `-1` = ничего не надето). Совпадение ищется по `name` + `itemType`, не по ссылке — после десериализации инстансы новые.
3. `stats_json`: `hp`, `maxhp`, `atk`, `def`, `base_atk`, `base_def`, `lv`, `gold`, `name` (с фолбэками `20/20/10/10/0/0/1/0/"HUMAN"`).

`scr_saveLoad` восстанавливает:

- `inventory_deserialize` — ровно 8 слотов; битые записи пропускаются с WARN, лишние хвосты отсекаются. `item_deserialize` проверяет `__type` и `name` до вызова конструктора, нечисловые поля подменяются безопасными значениями.
- Экипировка — по сохранённым индексам из свежего массива.
- Базовые статы: если `stats_json` есть (v3), но без `base_atk`/`base_def`, база выводится как `max(0, stat_atk - equipped_weapon.damage)` — обратная совместимость. Сейвы v1/v2 не хранят `stats_json` вообще: статы сбрасываются в дефолты `scr_inventory_init`.
- Финальный `scr_stats_recalc()` — сохранённые `atk`/`def` не доверяются, эффективные значения всегда пересчитываются.

## Troubleshooting

!!! warning "Предметы не добавляются до инициализации"
    `inventory_add` до `scr_inventory_init` возвращает `-1` — `global.inventory` ещё не существует. Точка инициализации — `obj_Init/Create_0`.

!!! warning "Стат изменился, но STAT показывает старое"
    Прямая запись в `stat_atk`/`stat_def` затирается пересчётом. Меняйте `stat_base_atk`/`stat_base_def` и зовите `scr_stats_recalc()`.

!!! note "Мёртвый код"
    `scr_checkItemSkip` (подсчёт пустых слотов) и конструктор `playableCharacterInfo` помечены `DELETE_CANDIDATE` — вызывателей в проекте нет, отдельной модели персонажа не существует.

## См. также

- [Система сохранений](save-system.md) — формат сейва, `scr_saveSave`/`scr_saveLoad`
- [UI и меню](ui-and-menus.md) — `obj_inGameMenu`, `obj_settingsManager`, нотификации
- [Система ввода](input.md) — `scr_ui_read_actions`, клавиша `menu`
- [Глобальное состояние](../architecture/global-state.md) — реестр `global.*`
- [Инициализация](../architecture/initialization.md) — `obj_Init`, `scr_inventory_init`

<!-- sources: scripts/constructorsForInventory/constructorsForInventory.gml:1-184; scripts/script_items/script_items.gml:1-87; scripts/scr_item_apply_use/scr_item_apply_use.gml:1-46; scripts/scr_inventory_init/scr_inventory_init.gml:1-74; scripts/currentENUMS/currentENUMS.gml:4-10; objects/obj_inGameMenu/Create_0.gml:1-68; objects/obj_inGameMenu/Step_0.gml:1-294; objects/obj_inGameMenu/Draw_64.gml:52-131; scripts/scr_saveSave/scr_saveSave.gml:65-142; scripts/scr_saveLoad/scr_saveLoad.gml:69-270; scripts/scr_callMenuInit/scr_callMenuInit.gml:1-25; objects/obj_Init/Create_0.gml:284-342; scripts/scr_defaultLoad/scr_defaultLoad.gml:26-41; scripts/scr_checkItemSkip/scr_checkItemSkip.gml:1-17; scripts/playableCharacterInfo/playableCharacterInfo.gml:1-19; docs_new/_meta/globals.txt:87-185 -->
