# Megaplan Findings (Phase 10A Baseline)

Snapshot состояния документации на момент начала megaplan'а (30 апреля 2026). Этот файл — входные данные для последующих фаз 10B–10F.

## Baseline `mkdocs build --strict`

После Phase 10A фиксов (см. ниже) `mkdocs build --strict` завершается успешно — 0 mkdocs-warnings. Остаются 3 `WARNING:root:` от плагина `git-revision-date-localized` для untracked файлов (`404.md`, `tags.md`, `glossary.md`) — это нормально и пропадёт после коммита.

### Baseline фиксы, применённые в Phase 10A

- `mkdocs.yml:1` — случайно вставленный префикс `/me` в `site_name`. Удалено.
- `mkdocs.yml plugins` — `search.highlight: true` невалидная опция плагина, `tags.tags_file` deprecated. Оба убраны.
- `mkdocs.yml nav` — пропал `- Теги: tags.md`, возвращён.
- `docs/getting-started/first-run.md:35` — битая ссылка `../../architecture/initialization.md` → `../architecture/...`
- `docs/getting-started/project-structure.md:50-52` — три битые ссылки с лишним `../`.
- `docs/glossary.md:115` — ссылка на `.windsurf/plans/docs-style-guide.md` вне корня docs → текстовое упоминание.
- `docs/index.md:68` — `t.me/n0souls` без схемы → `https://t.me/n0souls`.

## Категории проблем для последующих фаз

### A. Временные маркеры / changelog-стиль (Phase 10C)

| Файл | Строки | Текст |
|------|-------|-------|
| `code-reference/gml-scripts.md` | 3 | `UndefinedTale#888` — нестандартное написание (см. категорию E) |
| `systems/cutscenes/undefscene/faq.md` | 48-61 | Целая секция `## Что было улучшено в последних правках?` — классический changelog в reference |
| `systems/cutscenes/undefscene/ui.md` | 21 | `Inspector теперь показывает отдельный Path Preview` |
| `systems/cutscenes/undefscene/ui.md` | 23 | `Visual Editing теперь открывается в отдельном native окне` |
| `systems/cutscenes/undefscene/ui.md` | 90 | `Нижний dock больше не должен сам раздуваться` |
| `systems/cutscenes/undefscene/ui.md` | 93 | `Runtime JSON при resize панели теперь растягивается` |
| `systems/cutscenes/undefscene/ui.md` | 105 | `Runtime JSON теперь занимает доступную высоту панели целиком` |
| `systems/cutscenes/undefscene/formats.md` | 46 | `Экспорт больше не показывает...Этот риск теперь обрабатывается` |
| `systems/cutscenes/undefscene/integration.md` | 8 | `Если тот же .yyp уже открывался раньше` |
| `systems/cutscenes/undefscene/integration.md` | 19 | `основная часть чтения ресурсов была оптимизирована` |
| `systems/cutscenes/api.md` | 37 | `ActionCameraShake теперь корректно... (Phase 1 fix)` |
| `systems/cutscenes/api.md` | 153 | `Все ChatterboxAddFunction-обёртки теперь stateless` |
| `systems/cutscenes/examples.md` | 4 | `Тестовая катсцена теперь загружается из JSON-файла` |
| `systems/dialogue-portraits.md` | 86 | `теперь построено вокруг одного anchor` |
| `systems/dialogue-portraits.md` | 96 | `portrait больше не управляет...Теперь и portrait...` |
| `systems/dialogue-portraits.md` | 110 | `Анимация разговора теперь привязана` |
| `systems/dialogue-portraits.md` | 119-121 | `Для этой схемы была внесена маленькая правка в __scribble_class_typist.gml` — **RESOLVED: удалить упоминание** (scribble — внешняя либа, не модифицируем) |
| `systems/ui-tuning-map.md` | 62 | `Старой автосвязки portrait margin → text column больше нет` |

Не считаются проблемами (пассивный залог в описании факта):

- `input.md:44` — `если действие было активировано в этом кадре` (описание semantics, не changelog).
- `camera.md:16` — `чтобы центр был в (x, y)` (описание semantics).
- `actors.md:25` — `Если передан строковый ключ и он был в actor_map` (условие, не changelog).
- `room-screenshot-pipeline.md:139` — `Source — папка, из которой реально был загружен` (описание semantics).
- `initialization.md:50` — `Если инициализация уже была — выходим` (условие).
- `404.md:3` — `была перемещена` (факт про страницу, не changelog).

### B. AI-вводные / голые "Важно:" без admonition (Phase 10C)

| Файл | Строки | Замечание |
|------|-------|-----------|
| `systems/cutscenes/examples.md` | 40 | Голое `Примечание:` — обернуть в `!!! note` |
| `systems/cutscenes/actors.md` | 19 | Голое `Важно:` — обернуть в `!!! warning` или `!!! tip` |

### C. Placeholder-ы / TODO (Phase 10C)

Не найдено. `rg -i "TODO|FIXME|XXX|TBD|Lorem"` → 0 matches.

### D. Структурные пробелы (Phase 10D)

- Ни одна страница не имеет `tags:` в frontmatter → `tags.md` рендерится пустым.
- `getting-started/syntax.md` не имеет H1 — файл начинается с `## Основа...`.
- `index.md:13,21,29,40,49` использует emoji-шорткоды без префикса `:fontawesome-` / `:material-` для `:rocket:`, `:arrow_right:`. Работает через `pymdownx.emoji`, но по стайл-гайду лучше `material/fontawesome` иконки.
- `getting-started/project-structure.md:53-55` — секция `### obj_pointMarker` оказалась **после** `## См. также` (неправильный порядок).
- Длинные таблицы без `???` collapsible:
  - `systems/music.md:38-62` — 25 строк globals.
  - `architecture/global-state.md` — длинные таблицы inventory/face/DEV-LOAD (проверить).
- Отсутствует abbr-секция (для `GML`, `NPC`, `UI`, `SFX`, `BPM`, `OGG`, `RF`, `IPC`).
- Content tabs применяются только в `systems/music.md:70` (play_music vs immediate). Можно расширить на:
  - `cutscenes/examples.md` — JSON vs GML style
  - `cutscenes/api.md` — Yarn vs ActionClass
- Grid cards — только в `index.md` и `404.md`. Overview-страницы без grid cards:
  - `systems/cutscenes/overview.md`
  - `systems/cutscenes/undefscene/overview.md`
  - `architecture/overview.md`
  - `gameplay/overview.md`

### E. Именование проекта (Phase 10C)

Разные написания в прозе (папка `Undefinedtale888/` и файл `Undefinedtale888.yyp` — корректные, их не трогаем):

| Файл | Строка | Вариант |
|------|--------|---------|
| `code-reference/gml-scripts.md` | 3 | `UndefinedTale#888` — **ошибка** |
| `systems/dialogue-portraits.md` | 3 | `в Undefinedtale888` (в прозе) — унифицировать до `Undefinedtale-888` |

Корректные случаи (оставляем):

- `Undefinedtale888/` как директория
- `Undefinedtale888.yyp` как имя файла GameMaker-проекта
- `Undefinedtale-888` в прозе везде

### F. Fact-check чеклист (Phase 10B, выполняется отдельной итерацией)

Каждая страница требует сверки с кодом в `c:\Users\n0souls\Documents\GitHub\Undefinedtale-888\`.

**Выполнено (выборочно по критическим страницам):**

- [x] `architecture/initialization.md` — сверен против `obj_Init/Create_0.gml`, `obj_globalManager/Create_0.gml`, `scr_constants`. Порядок инициализации и константы совпадают.
- [x] `systems/music.md` — сверен против `scr_music_init`. Все API-функции подтверждены.
- [x] `systems/input.md` / `code-reference/gml-scripts.md` — `scr_buildInputMap` возвращает 8 действий (up/down/left/right/confirm/back/menu/**delete**), в docs указано 7 — **нужно поправить**.
- [x] `systems/cutscenes/api.md` — `c_facing`/`c_autofacing`/`c_autowalk` описаны верно (`ActionRunFunction` / `ActionSetProperty`). JSON action types совпадают.
- [x] `cutscene_load_json` — существует, возвращает менеджер.

**Критические расхождения (фантомные функции / неверные имена):**

| Функция (docs) | Реальное имя в коде | Файл | Статус |
|----------------|---------------------|------|--------|
| `scr_facing_to_sprite` | `scr_sprite_for_facing` | `scr_player_facing.gml` | **Исправлено в 10C** |
| `scr_sprite_to_facing` | `scr_facing_for_sprite` | `scr_player_facing.gml` | **Исправлено в 10C** |
| `interactionWithNPCsOrObjects` | `interactionWithNPCsOrObjects` | `interactionWithNPCsOrObjects.gml` | Существует, docs корректны |
| `interactionWithMainCast` | `interactionWithMainCast` | `interactionWithMainCast.gml` | Существует, docs корректны |
| `scr_interaction` | `scr_interaction` | `interactionWithNPCsOrObjects.gml` | Существует, docs корректны |
| `scr_buildInputMap` actions | 8 действий (up/down/left/right/confirm/back/menu/**delete**) | `scr_settingsManager.gml` | **Исправлено в 10C** (docs говорили 7)

## Снижение риска

- Выполнять фазы 10B–10F последовательно, коммитить каждую отдельно.
- После каждой фазы запускать `mkdocs build --strict`.
- Grep-acceptance запускать после Phase 10C и финально в 10F.
