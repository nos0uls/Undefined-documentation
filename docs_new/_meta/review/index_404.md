# Фактчек: `index.md` и `404.md`

- Дата проверки: ревизия кода `7ee444a` (ветка `audit-fixes-2026-09`, `git rev-parse HEAD` → `7ee444acb780d895901eeef0e786d6cd2229514b`).
- Страницы: `docs_new/index.md`, `docs_new/404.md`.
- Источники: `$P/README.md`, `$P/Undefinedtale888.yyp`, `$P/scripts/**`, `$P/objects/**`, `$P/audit_2026-09/`, `docs_new/_meta/nav_plan.md`, реальное дерево `docs_new/`, `mkdocs.yml`, `Undefscene/editor-app`.

## index.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 2–5 | frontmatter `title` + `hide: [navigation, toc]` для лендинга | OK — SKILL.md «Page structure»: лендинги используют `hide` вместо тегов |
| 8 | единственный H1 | OK |
| 10 | «сюжетно-ориентированная RPG с пазлами на GameMaker» | OK — `$P/README.md:3`: «сюжетно‑ориентированную RPG с пазлами на GameMaker Studio 2» |
| 10 | «GML 2.3+» | OK — код использует синтаксис GML 2.3+ (`function`, `constructor`, struct): `scripts/scr_cutscene_classes/scr_cutscene_classes.gml`, `scripts/constructorsForInventory/constructorsForInventory.gml`; runtime `2026.100.0.1106` |
| 10 | документация описывает архитектуру, системы, движок катсцен, Undefscene | OK — разделы `nav_plan.md` (architecture/, systems/, cutscenes/, undefscene/); движок катсцен: `scripts/cutscene_*/`, `objects/obj_cutsceneManager/`; редактор: `Undefscene/editor-app` |
| 16–17 | карточка «Начало работы» → `getting-started/setup.md`; «установка, клонирование, первый запуск, сборка» | OK — файл есть; раздел содержит `setup.md` («Требования», «Клонирование», «Открытие и первый запуск») и `build.md` |
| 21–22 | карточка «Архитектура» → `architecture/overview.md`; «persistent-объекты, иерархия `par_*`, глобальное состояние, комнаты, форматы данных» | OK — файл есть; `par_*` = 5 объектов (`par_actor`, `par_decor`, `par_depth`, `par_entity`, `par_interactable`); persistent — 9 объектов (`"persistent":true` в `.yy`); страницы `initialization.md`, `object-hierarchy.md`, `global-state.md`, `rooms.md`, `data-formats.md` существуют |
| 26–27 | карточка «Системы» → `systems/input.md`; перечень систем | OK — файл есть; все темы соответствуют файлам `nav_plan.md` (input, player, room-transitions, dialogue, interaction, inventory-and-stats, save-system, music, ui-and-menus); геймпад подтверждён `scr_inputApi.gml:139-165` (`scr_input_gamepad_update`, `gamepad_*`); debug-and-testing в перечень не входит, но ссылка есть в «См. также» (резюме карточки, не ошибка) |
| 31–32 | карточка «Катсцены» → `cutscenes/overview.md`; «JSON-действия, Action-классы, акторы, камера, `partial_control`» | OK — `cutscene_load_json`, `cutscene_action_factory` (~80 типов), `scr_cutscene_classes` (конструкторы `Action*`), `cutscene_actor_create/destroy`, `cutscene_camera_*`, `partial_control` (`cutscene_action_factory.gml`, `scr_cutscene_classes.gml`) |
| 36–37 | карточка «Undefscene» → `undefscene/overview.md`; «ноды, инспектор, экспорт в JSON» | OK — файл есть; `editor-app/src/.../nodes/nodeRegistry.ts`, компоненты инспектора (`EditorShell*.tsx`, `DockingLayout.tsx`), `compiler/exporters.ts`; `overview.md` — «Визуальный редактор катсцен» |
| 41–42 | карточка «Справочник» → `reference/gml-scripts.md`; «таблицы всех GML-скриптов, объектов и событий; глоссарий» | OK — `gml-scripts.md`, `objects-and-events.md`, `glossary.md` существуют; страницы генерируются `_meta/gen_reference.py` из инвентарей (351 файл с объявлениями, 53 объекта); вне справочника только внешние библиотеки (Chatterbox/Scribble/TweenGMX), тест-фреймворк и enum-only `currentENUMS` — исключения санкционированы SKILL.md |
| 50 | `getting-started/setup.md` — «IDE, runtime, первый запуск» | OK — `setup.md` «Требования»: IDE `2026.100.0.1161`, Runtime `2026.100.0.1106`, «Открытие и первый запуск» |
| 51 | `getting-started/project-structure.md` — «что где лежит» | OK — файл есть, заголовки «Корень проекта», «Каталоги ресурсов», «datafiles/» |
| 52 | `architecture/overview.md` — «как связаны подсистемы» | OK — файл есть |
| 56 | `cutscenes/overview.md` — «способы задать сцену: JSON, GML, `c_*`-функции» | OK — `overview.md` «Три способа задать катсцену»: JSON-файл, GML напрямую, `c_*`-DSL; `c_*`-функции существуют (`c_begin`, `c_end`, `c_cmd`, `c_walk`…) |
| 57 | `undefscene/overview.md` — «визуальный редактор сценариев» | OK |
| 58 | `cutscenes/json-actions.md` — «все типы действий и их поля» | OK — справочник типов действий (move, follow_path, …) |
| 62 | цепочка `architecture/overview.md` → `initialization.md` → `global-state.md` | OK — все файлы есть |
| 63 | `systems/input.md` — «ввод, игрок, сохранения, музыка» | OK — раздел содержит все названные страницы |
| 64 | `reference/gml-scripts.md` — «сигнатуры функций» | OK — таблицы «Функция / Сигнатура / Назначение» |
| 66–67 | `!!! info`: «код на ветке `audit-fixes-2026-09` (ревизия `7ee444a`)» | OK — `git branch --show-current` → `audit-fixes-2026-09`, `HEAD` = `7ee444a`; `docs_new/_meta/CODE_REV.txt` = `7ee444a` |
| 71 | `reference/glossary.md` — термины `persistent`, `entity_state`, `mark_node` | OK — `glossary.md`: «Persistent-объект» (L14), «`global.entity_state`» (L84), «`mark_node` / `goto`» (L228) |
| 72 | `getting-started/conventions.md` — именование `obj_`/`par_`/`scr_` | OK — `conventions.md:17-19` таблица префиксов |
| 73 | `systems/debug-and-testing.md` — «debug-флаг, хоткеи, тест-фреймворк» | OK — заголовки «Активация `global.debug`», «Горячие клавиши», «Тест-фреймворк катсцен» |
| 74 | `undefscene/faq.md` — FAQ по редактору | OK — файл есть, «Частые вопросы и проблемы» |
| 76 | sources-комментарий: `audit_2026-09/08_DOCS_REWRITE_SWARM.md`, `CODE_REV.txt`, `README.md`, `.yyp` | OK — `$P/audit_2026-09/08_DOCS_REWRITE_SWARM.md`, `docs_new/_meta/CODE_REV.txt`, `$P/README.md`, `$P/Undefinedtale888.yyp` — все существуют |
| — | все 15 внутренних ссылок | OK — каждая ведёт на существующий файл в `docs_new/` |

## 404.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 1 | H1 «404 — Страница не найдена», без frontmatter | OK — SKILL.md: `404.md` освобождён от frontmatter; файл в `not_in_nav` (`mkdocs.yml:11`) |
| 10 | ссылка `index.md` | OK — `docs_new/index.md` существует |
| 15 | ссылка `tags.md` | OK — `docs_new/tags.md` существует и содержит маркер `<!-- material/tags -->` |

## Замечания (не блокеры)

- `404.md`: относительные ссылки на deep-404 URL (GitHub Pages отдаёт `404.html` по запрошенному пути) разрешаются относительно запрошенного пути — известное ограничение платформы, затрагивает и CSS/JS; стандартная практика MkDocs — оставить как есть.
- `mkdocs.yml` в корне пока указывает на старый `docs/` (W4-реврайт не приземлился, см. предупреждение «Transition state» в SKILL.md); проверка `not_in_nav`/`nav` для `docs_new/` делалась по `nav_plan.md`.

## Итог

WRONG: 0 · UNVERIFIABLE: 0 · MISSING: 0. Правки страниц не требуются.
