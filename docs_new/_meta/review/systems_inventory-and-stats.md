# Review: systems/inventory-and-stats.md (код @ 7ee444a)

| Строка | Утверждение | Вердикт |
|---|---|---|
| 13 | Инвентарь `global.inventory` на 8 слотов, классы с `use()`, `global.stat_*`, сериализация в сейв | OK (scr_inventory_init.gml:5, constructorsForInventory.gml:5-103) |
| 17 | `undefined` = пустой слот; инвариант 8 слотов в `inventory_deserialize`; UI читает `array_length`; init из `obj_Init/Create_0`, `scr_defaultLoad`, `scr_saveLoad` (фолбэк) | OK (constructorsForInventory.gml:159-160; obj_inGameMenu/Step_0.gml:97, Draw_64.gml:66; obj_Init/Create_0.gml:342; scr_defaultLoad.gml:34; scr_saveLoad.gml:226) |
| 19 | Классы из `constructorsForInventory`, тип = `itemType` (enum `ITEMTYPE` из `currentENUMS`) | OK (currentENUMS.gml:4-10) |
| 27 | `Item(_name, _description = "An Item")`, `ITEMTYPE.UNDEFINED`, поля `name`, `description` | OK (constructorsForInventory.gml:5-8) |
| 28 | `WeaponItem(_name, _damage = 20, _description)`, `ITEMTYPE.WEAPON`, поле `damage` | OK (constructorsForInventory.gml:26-28; `_description = "A Weapon"` — дефолт в доке опущен, допустимо) |
| 29 | `ArmorItem(_name, _defense = 9, _description)`, `ITEMTYPE.DEFENSE`, поле `defense` | OK (constructorsForInventory.gml:49-51; `_description = "Armor"`) |
| 30 | `FoodItem(_name, _amount = 1, _heal = 10, _description)`, `ITEMTYPE.FOOD`, поля `heal`, `amount` | OK (constructorsForInventory.gml:73-76) |
| 34 | `getDisplayName()` — имя для UI; `FoodItem` → `"name xN"` | OK (constructorsForInventory.gml:10, 77) |
| 35 | `getStatBonus()` — `"99"` для оружия, `"+40 HP"` для еды, `""` у `Item` | WRONG → imprecise (constructorsForInventory.gml:29, 52, 78): возвращаются `string(damage)`, `string(defense)`, `"+"+string(heal)+" HP"`; `"99"`/`"+40 HP"` — лишь значения Real Knife/Chocolate. Исправлено на общие формы |
| 36 | `use()` вызывает `scr_item_apply_use(self)` + `global.show_notification`, возвращает consumed-bool | WRONG → imprecise: верно только для наследников; у базового `Item` `use()` лишь пишет debug-сообщение и возвращает `false`, без `scr_item_apply_use` и без нотификации (constructorsForInventory.gml:12-15). Уточнено |
| 37 | `serialize()` → `__type` `"item"/"weapon"/"armor"/"food"` + специфичные поля | OK (constructorsForInventory.gml:16-18, 39-41, 62-64, 100-102) |
| 43-47 | Таблица `ITEMTYPE`: WEAPON→equip weapon, DEFENSE→equip armor, FOOD→heal+amount-1, SOMEPERK зарезервирован, UNDEFINED без эффекта | OK (scr_item_apply_use.gml:16-44; SOMEPERK попадает в default → `false`) |
| 53 | `item_database_register(_name, _factory)` → `global.__item_database_registry` | OK (script_items.gml:10-15) |
| 54 | `item_database(_name)`: реестр → hardcoded-фолбэк (Real Knife/Scarf/Chocolate); неизвестное → `undefined` + WARN | WRONG → imprecise (script_items.gml:22-39): сообщение `"[ITEM_DB] Unknown item:"` без тега WARN. Исправлено |
| 55 | `inventory_add(_item_or_name) -> real`: struct или строка через `item_database`; индекс слота или `-1` | OK (script_items.gml:50-86) |
| 59 | `FoodItem` одного имени стакается (`amount` суммируется), слот не занимается | OK (script_items.gml:64-72) |
| 60 | Переполнение → `"Inventory is full"` + `-1` | OK (script_items.gml:82-86) |
| 61 | До `scr_inventory_init` → WARN + `-1` | OK (script_items.gml:51-54) |
| 63-64 | Прод-вызывателей нет; `item_database` зовут только `scr_stress_tests` | OK (grep: вызовы только в scr_stress_tests.gml:952,959; `inventory_add` — 0 вызывателей вообще) |
| 68-75 | Таблица эффектов `scr_item_apply_use` | OK (scr_item_apply_use.gml:15-44) |
| 79 | consumed-bool: `true` → слот очищает вызывающий код | OK (obj_inGameMenu/Step_0.gml:216-220) |
| 80 | Не-struct → `[ITEM] WARN` + `false` | OK (scr_item_apply_use.gml:11-14) |
| 81 | Guard полного HP в `FoodItem.use()` и в самой функции | OK (constructorsForInventory.gml:84-89; scr_item_apply_use.gml:33-35) |
| 87-97 | Таблица `stat_*` дефолтов: hp=99, maxhp=99, base_atk=0, base_def=0, lv=20, gold=99, player_name="CHARA" | OK (scr_inventory_init.gml:23-32) |
| 101-106 | `scr_stats_recalc` в том же файле `scr_inventory_init.gml`; формула база + `damage`/`defense` экипировки | OK (scr_inventory_init.gml:61-74) |
| 114-117 | Вызыватели `scr_stats_recalc`: `scr_item_apply_use`, `obj_inGameMenu/Step_0` (DROP), `scr_inventory_init`, `scr_saveLoad` | OK по списку (apply_use:20,25; Step_0:182; init:29; saveLoad:270); см. уточнение DROP ниже |
| 115 | При DROP «если выброшенный был экипирован: ссылки обнуляются, затем пересчёт» | WRONG → imprecise (Step_0.gml:174-182): обнуление `equipped_*` условное, а `scr_stats_recalc()` выполняется безусловно после YES. Исправлено |
| 119 | Нет действия «снять экипировку»; снятие — только выбросом надетого | OK (obj_inGameMenu/Step_0.gml:213-246 — действий только USE/INFO/DROP) |
| 123 | `scr_callMenuInit` по `menu`, gate `scr_checkUIBlocking`; создаёт `obj_inGameMenu`, `can_move = false`; `OPT` на индексе `INGAME_MENU_OPT_INDEX` (2), читает `obj_settingsManager` | OK (scr_callMenuInit.gml:7-19; Create_0.gml:5,17; obj_settingsManager/Create_0.gml:242). Доп. gate `!global.is_menu_room(room)` не упомянут — допустимо |
| 127-131 | Вкладка ITEM: 8 слотов, `"------"` серым, навигация пропускает пустые, `item_selOption` к первому занятому; `["USE","INFO","DROP"]` item_use 1–3; USE очищает слот и `item_count -= 1`; INFO → `description` через `show_notification`; DROP → `drop_confirming` YES/NO | OK (Step_0.gml:92-256; Draw_64.gml:66-108) |
| 132 | `back`/`menu` — уровень выше; в корне закрытие + `can_move` | OK (Step_0.gml:50-59; `can_move` — под `!global.cutscene_active`, деталь опущена) |
| 134 | STAT (`current_option == 2`): `stat_text`, 6 строк NAME/LV/HP/DAMAGE/DEFENSE/MONEY, пересборка каждый Draw_64 | OK (Draw_64.gml:119-129) |
| 136 | Ввод через `scr_ui_read_actions(true)` | OK (Step_0.gml:4; scr_ui_read_actions.gml:4) |
| 142 | `inventory_serialize` → `json_stringify`; `undefined` для пустых/чужих | OK (scr_saveSave.gml:66; constructorsForInventory.gml:139-149) |
| 143 | Индексы `_eq_w`/`_eq_a`, `-1` = ничего; совпадение по `name`+`itemType` | OK (scr_saveSave.gml:73-84) |
| 144 | `stats_json`: hp/maxhp/atk/def/base_atk/base_def/lv/gold/name, фолбэки 20/20/10/10/0/0/1/0/"HUMAN" | OK (scr_saveSave.gml:110-123) |
| 148 | `inventory_deserialize` — ровно 8 слотов, WARN на битых, хвосты отсекаются; `item_deserialize` проверяет `__type`+`name` до конструктора | OK (constructorsForInventory.gml:109-133, 155-184) |
| 149 | Экипировка восстанавливается по индексам из свежего массива | OK (scr_saveLoad.gml:228-231) |
| 150 | Если в сейве нет `base_atk`/`base_def` («v1/v2»), база = `max(0, stat_atk − equipped_weapon.damage)` | WRONG (scr_saveLoad.gml:239-267): у сейвов v1/v2 нет `stats_json` вообще → срабатывает else-ветка с дефолтами (99/99/0/0/20/99/"CHARA"). Фолбэк `max(0, atk − dmg)` применяется, когда `stats_json` есть (v3), но полей `base_*` нет. Исправлено |
| 151 | Финальный `scr_stats_recalc()` — сохранённым atk/def не доверяют | OK (scr_saveLoad.gml:270) |
| 155-156 | `inventory_add` до init → `-1`; точка init — `obj_Init/Create_0` | OK |
| 158-159 | Прямая запись в `stat_atk`/`stat_def` затирается пересчётом | OK (scr_inventory_init.gml:21-22, 72-73) |
| 161-162 | `scr_checkItemSkip` и `playableCharacterInfo` — `DELETE_CANDIDATE`, вызывателей нет | OK (оба файла с маркером; grep: 0 вызовов, только .yy/.yyp-регистрации) |
| 166-170 | Ссылки «См. также» | OK (все страницы существуют в nav_plan.md и на диске) |
| 172 | sources-комментарий | OK (все файлы и диапазоны проверены) |

## Исправления, внесённые в страницу

1. `getStatBonus`: примеры `"99"`/`"+40 HP"` → общие формы `string(damage)`/`string(defense)`/`"+N HP"`.
2. `use()`: уточнено, что `scr_item_apply_use` + нотификация — у наследников; базовый `Item.use()` только логирует и возвращает `false`.
3. `item_database`: «WARN в лог» → сообщение `[ITEM_DB] Unknown item` (без тега WARN).
4. Список вызовов `scr_stats_recalc`: пересчёт после DROP — безусловный (не «только если экипирован»).
5. Загрузка статов: фолбэк `max(0, atk − бонус)` — для v3-сейвов без `base_*`; сейвы v1/v2 (нет `stats_json`) получают дефолты `scr_inventory_init`.
