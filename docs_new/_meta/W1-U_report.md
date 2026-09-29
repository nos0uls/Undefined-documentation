# W1-U — перенос раздела Undefscene в docs_new/ + синхронизация с редактором

Дата: проход W1-U. Источник страниц: `docs/systems/cutscenes/undefscene/` → `docs_new/undefscene/` (11 файлов, те же имена).

## Реестр нод (для патча скилла)

- Файл: `$E/src/renderer/src/editor/nodes/nodeRegistry.ts` — **путь из скилла верный**, менять не нужно.
- Экспорт: `NODE_REGISTRY` (строка 1988) — собирается из четырёх карт: `baseNodes` (64–390), `cameraNodes` (393–559), `conditionalNodes` (562–669), `otherNodes` (672–1986).
- `NODE_TYPES` (строка 1997) — производный список ключей.
- Всего в реестре **84 типа**; `start` в реестр **не входит** — создаётся кодом (`reverseCompile.ts:102`, `runtimeTypes.ts:137`). Итого для пользователя: **85 нод**.
- Палитра группирует по `category` (`ActionsPanel.tsx`, `CATEGORY_ORDER`); русские имена категорий — `i18n/ru.ts:177-188` (`flow` → «Сценарий», `wait` → «Ожидание», `meta` → «Мета»).
- Цвета категорий: `NODE_COLORS` (строки 5–15): flow — синий, movement/actor/visual — фиолетовый, dialogue — розовый, camera — зелёный, logic — оранжевый, audio — бирюзовый, wait — серо-синий.

## Что изменено по файлам

### overview.md (уже существовал — доработан)
- Исправлен сломанный таб `=== "Готовый билд"`: контент не был отступом внутри таба → добавлены отступы, текст переписан без «Просто».
- Количество нод «85» подтверждено реестром (84 + `start`), оставлено.
- Убрано расширение `.tsx` из sources-комментария (проверка на внутренние детали требует 0 совпадений).

### tutorial.md
- Фронтматтер: добавлен `title`; tags: `undefscene`, `editor`.
- Исправлен фактический баг: средняя кнопка мыши создаёт ноду `Dialogue` (`useNodeOperations.ts:336-342` — `createDefaultPaneNode` → `'dialogue'`), а не `Start`; `Start` появляется вместе со сценой.
- `Parallel Start` → `Parallel` (label в реестре).
- Добавлены `## См. также` (был) и `<!-- sources: -->`.

### workflow.md
- Фронтматтер: `title` + tags. Sources добавлен. Контент без изменений по смыслу.

### how-to.md
- Фронтматтер: `title`; tags: `undefscene`, `editor`, `how-to`.
- Добавлен рецепт «Переход к метке» (`Mark Node` + `GoTo Node`).
- «Условия перехода»: добавлена `Branch Flag`.
- Исправлены названия категорий палитры под `i18n/ru.ts`: `Attach To Target` → «Актёр», `Emote` → «Визуал», `Fade In/Out` → «Камера» (в реестре категория `camera`), `Halt` → «Движение».
- Убрано упоминание `Show Emote` как отдельной ноды (в палитре только `Emote`; `show_emote` — тип экшена движка).
- Sources добавлен.

### ui.md
- Фронтматтер: `title` + tags.
- Убрана внутренняя деталь `event.code` из tip про раскладку (запрещено скиллом).
- `Zen Mode F12 (production)` → `F12` (без деталей сборки).
- Дедупликация `Saved` / `Saved` в списке toast-уведомлений.
- Sources добавлен (без `.tsx`).

### nodes.md — основная синхронизация с `NODE_REGISTRY`
- Таблица категорий переписана по фактическим `category`/цветам/именам палитры: Сценарий 4, Движение 9, Актёр 6, Визуал 11, Камера 12, Диалог 9, Логика 19, Звук 15 (+ сноска: `Start` не в палитре). Итог = 85.
- Перемещены между разделами по реестру: `Room Change` → Сценарий; `Halt` → Движение; `Fade In`/`Fade Out`, `Tween`, `Set Property`, `Tween Camera` → Камера; `Instant Mode` → Логика; `Wait Talk` → Диалог.
- **Новые секции**: `GoTo Node` (`target` — метка/имя ноды; валидатор: пустой target = Warn, несуществующая цель = Error), `Branch Flag` (`key`, `operator`: `==/!=/>/</>=/<=/exists/!exists`, `value`; два выхода True/False — `compiler/core.ts:441-453`), `Wait Talk` (алиас-нода, экспорт нормализуется движком в `wait_for_dialogue`).
- `Dialogue`: добавлено поле `auto_advance`.
- `Play Music`: добавлено поле `persist_room_change`; уточнено, что ключ `sound` отображается как `Track`.
- `Camera Pan (Speed)`: поля исправлены под реестр — `x`/`y` это скорость в px/frame + `seconds`; удалены несуществующие `speed`/`smooth` и неверное описание «перемещение к координатам».
- `Set Emotion`: удалено несуществующее поле `blend`.
- `Partial Control`: добавлено поле `allowed_actions`.
- `Halt`: добавлена таблица параметров (`target`).
- `Actor Destroy`: добавлена таблица параметров (`target`).
- `Mark Node`: описание исправлено — цель для `GoTo Node`, а не для `Jump` (в валидаторе `nodeChecks.ts:622-625` прямо зафиксировано, что `jump.target` — актёр).
- `Instant Mode`: заметка про нормализацию типа `instant_mode` → `set_instant` в движке.
- `Parallel Start` → `Parallel` (label в палитре).
- Sources добавлен.

### room-visual-editor.md
- Фронтматтер: `title` + tags. «Позволяет включить сетку» → «включает сетку». Sources добавлен (без `.tsx`).

### formats.md
- Фронтматтер: `title` + tags (`+ data-formats`).
- Добавлен раздел «Структура engine .json» по `cutscene_load_json.gml` и `compiler/exporters.ts`: `schema_version` (=1), `cutscene_id` (slug из названия сцены), `settings.fps` (1–240), `settings.skippable` (default `true`), `actions[]`; семантика маркеров `start`/`end` и `mark_node`; таблица legacy-алиасов типов (`waittalk`→`wait_for_dialogue`, `instant_mode`→`set_instant` и др.).
- Добавлены ссылки на `../cutscenes/json-actions.md` и `../cutscenes/overview.md`.
- Sources добавлен.

### validation.md
- Фронтматтер: `title` + tags (`+ troubleshooting`).
- Удалена неверная строка «`wait_until` `timeout_seconds == 0` → Warn»: код предупреждает только при `< 0` (`nodeChecks.ts:187-196`).
- Добавлен блок «Структурные ошибки (Error)»: нет/много `Start`, нет/недостижим `End`, `goto` на несуществующую метку, дубль `checkpoint_id` — по `graphChecks.ts`, `core.ts:119-131`, `nodeChecks.ts:641-668`.
- Добавлены строки проверок: `goto` (Warn/Error), `follow_path` (пустой/1 точка), `halt` (исходящие связи), `jump` (`seconds<=0`), `emote` (нет sprite — Tip), `crossfade_music` (intensity 0–1), `camera_shake` (`seconds<=0`).
- Sources добавлен.

### faq.md
- Фронтматтер: `title` + tags (`+ faq`, `+ troubleshooting`).
- Убраны временные маркеры: «исправлена в последних версиях» → описание текущего поведения; «В актуальной версии» → прямое описание.
- Добавлен пункт про `GoTo Node` как причину зависания (бесконечный цикл).
- `Zen Mode (F12)` без «production».
- Sources добавлен.

### glossary.md
- Фронтматтер: `title` + tags.
- Добавлены термины: `Branch Flag`, `GoTo Node`, `Wait Talk`; `Branch` переформулирован (по функции). `Mark Node` — «цель перехода для GoTo Node». `Wait for Interact` → `Wait Interact` (label в реестре).
- «позволяющий» → переписано.
- Sources добавлен.

## Проверки
- `grep '\.tsx|requestAnimationFrame|userData'` по `docs_new/undefscene/` → **0 совпадений**.
- Запрещённые паттерны (AI-water, временные маркеры, TODO/XXX) → 0 (совпадение `todo` в ui.md/how-to.md — это имя категории заметок в UI, не placeholder).
- Каждый файл: `title` + разрешённые tags, `## См. также`, `<!-- sources: -->`, ровно один H1.
- Относительные ссылки: все `../` указывают в `../cutscenes/` (sibling-раздел по `nav_plan.md`); остальные ссылки — внутри `undefscene/`.

## Оставшиеся расхождения / на заметку
- **`../cutscenes/json-actions.md` ещё не существует** в `docs_new/cutscenes/` (есть в `nav_plan.md`, создание — отдельный проход). Ссылка из `formats.md` останется мёртвой до его появления.
- **`partial_control` — баг редактора**: в `validators/nodeChecks.ts:47` REQUIRED_PARAMS требует ключ `type`, но поле ноды называется `control_type` → нода всегда получает Warn «field empty» для несуществующего поля. В доках не описано (ждёт исправления в редакторе).
- **Engine-типы без нод в редакторе** (есть в `cutscene_action_factory.gml`, не экспонируются в палитре): алиасы `destroy`/`destroy_entity`→`actor_destroy`, `emote`→`show_emote`, а также `branch` true/false-структура формируется рёбрами, `parallel` собирается из `parallel_start`/`parallel_join`. Это уровень engine-формата, не UI — покрывается в `cutscenes/json-actions.md`.
- **`spawn_entity`**: поле `actor_sprite` читает движок (`json_actions.txt`), но в инспекторе редактора его нет — в `nodes.md` описаны только поля редактора.
- **`schedule_action.action_type`** — закрытый список из 8 типов в селекте редактора; движок принимает любой известный тип в `action`.
