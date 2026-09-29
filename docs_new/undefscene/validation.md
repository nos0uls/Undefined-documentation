---
title: "Undefscene: Проверки и ошибки"
tags:
  - undefscene
  - editor
  - troubleshooting
---

# Undefscene: Проверки и Ошибки

Автоматическая валидация графа перед экспортом для предотвращения сбоев в игре. Результаты отображаются в панели **Логи / Предупреждения**.

## Уровни критичности

| Уровень | Описание | Блокировка экспорта |
|---------|----------|-------------------|
| :octicons-x-circle-16:{ style="color: red" } **Error** | Критическая ошибка (битые связи). | **Да** |
| :octicons-alert-16:{ style="color: orange" } **Warn** | Пропущено поле или логическая ошибка. | Нет |
| :octicons-light-bulb-16:{ style="color: green" } **Tip** | Рекомендация по оптимизации. | Нет |

Уровни в таблицах ниже — значения по умолчанию. Любое правило можно повысить, понизить или скрыть через контекстное меню записи в логе (правый клик по сообщению).

## Структурные ошибки (Error)

- **Нет ноды Start** или **больше одной ноды Start** — у графа должна быть ровно одна точка входа.
- **Нет ноды End** или **ни один End недостижим** из Start — сцене некуда завершиться.
- **GoTo Node в несуществующую точку** — `Target Mark` не совпадает ни с одной меткой `Mark Node` и ни с одним именем ноды.
- **Дублирующийся `checkpoint_id`** — две ноды `Checkpoint State` с одинаковым ID.
- **Актёр используется до создания или после уничтожения** — действие обращается к ключу, который не создаёт ни одна нода `Actor Create` / `Spawn Entity` на этом пути, либо актёр уже удалён `Actor Destroy`.
- **Битая пара Parallel** — у `Parallel Start` нет связанного `Parallel Join` (или наоборот), либо связанная нода имеет другой тип.
- **Связь указывает на несуществующую ноду** — ребро ссылается на удалённый блок.

## Типовые предупреждения (Warn)

- **Пустое поле**: не указан `Target`, `Sprite` или `File`.
- **Изолированная нода**: блок не соединен с общей цепочкой.
- **Множественные выходы**: обычная нода имеет >1 исходящей связи (используйте `Branch`, `Branch Flag` или `Parallel`).
- **Таймаут**: задержка или тряска с нулевой/отрицательной длительностью.
- **Actor Create без спрайта**: не указан `actor_sprite` и `copy_target`.
- **Branch без false-ветки**: только true-ветка, false может быть забыта (уровень Tip).
- **Tween без target**: для `kind=instance` обязателен `target`.
- **Set Property без значения**: поле `value` пустое.
- **Run Function без имени**: поле `function` пустое или битый JSON в `args`.
- **Schedule Action**: отрицательная задержка; битый JSON в `action_params` — уровень Tip.
- **Music Pitch**: значение вне диапазона 0.5–2.0 (уровень Tip).

## Интеграция с проектом
При подключенном `.yyp` редактор дополнительно проверяет:
- Существование указанных ассетов (объектов, спрайтов, звуков).
- Наличие `.yarn` файлов и нод диалогов.
- Валидность имен GML-функций (`run_function`) и условий `branch` по белому списку движка.

!!! tip "Как исправить"
    Кликните по сообщению в логе — редактор сфокусируется на проблемной ноде для быстрого исправления.

## Проверки конкретных нод

| Нода | Проверка | Уровень | Блокировка экспорта |
|------|----------|---------|---------------------|
| `play_music` | Поле `sound` заполнено | Warn | Нет |
| `play_sfx` | Поле `sound` заполнено | Warn | Нет |
| `wait_until` | Поле `condition_var` заполнено | Error | Да |
| `wait_until` | `timeout_seconds < 0` | Warn | Нет |
| `goto` | Поле `target` (Target Mark) заполнено | Warn | Нет |
| `goto` | Цель не найдена среди меток и имён нод | Error | Да |
| `tween` | `target` заполнен (для `kind=instance`) | Warn | Нет |
| `tween` | `prop` / `end_value` заполнены | Warn | Нет |
| `set_property` | `target` заполнен (для `kind=instance`) | Warn | Нет |
| `set_property` | `property` / `value` заполнены | Warn | Нет |
| `run_function` | Имя функции не пустое | Warn | Нет |
| `run_function` | `args` — валидный JSON | Warn | Нет |
| `schedule_action` | `delay_seconds >= 0` | Warn | Нет |
| `schedule_action` | `action_params` — валидный JSON-объект | Tip | Нет |
| `checkpoint_state` | `include_globals` — валидная JSON-строка массива | Warn | Нет |
| `checkpoint_state` | `include_instances` — валидная JSON-строка массива | Warn | Нет |
| `music_pitch` | Значение `pitch` > 0 и конечно | Warn | Нет |
| `music_pitch` | Значение `pitch` вне 0.5–2.0 | Tip | Нет |
| `actor_create` | Указан `actor_sprite` или `copy_target` | Warn | Нет |
| `branch` | Нет false-ветки | Tip | Нет |
| `mark_node` | Дубликаты имён меток | Warn | Нет |
| `follow_path` | Пустой список `points` | Warn | Нет |
| `follow_path` | Меньше двух точек в `points` | Tip | Нет |
| `halt` | Есть исходящие связи (ноды после Halt не выполнятся) | Warn | Нет |
| `jump` | `seconds <= 0` | Warn | Нет |
| `emote` | Поле `sprite` пустое | Tip | Нет |
| `crossfade_music` | `intensity` вне диапазона 0–1 | Warn | Нет |
| `camera_shake` | `seconds <= 0` | Warn | Нет |

!!! warning "Известные особенности валидатора"
    - **Partial Control**: проверка обязательных полей смотрит на ключ `type`, которого нет в инспекторе (реальное поле ноды — `control_type`). На каждой ноде Partial Control постоянно висит предупреждение «поле "type" не заполнено» — его можно игнорировать или скрыть через контекстное меню записи в логе.
    - **Branch Flag**: корректная нода с двумя выходами (true/false) получает предупреждение о множественных выходах. Это ложное срабатывание — два выхода у `Branch Flag` разрешены так же, как у `Branch`.

---

## См. также

- [Справочник нод](nodes.md) — обязательные параметры каждой ноды
- [Создание катсцены](workflow.md) — пошаговый процесс
- [FAQ](faq.md) — частые вопросы и проблемы

<!-- sources: editor-app/src/renderer/src/editor/validators/nodeChecks.ts; editor-app/src/renderer/src/editor/validators/graphChecks.ts; editor-app/src/renderer/src/editor/validators/core.ts; editor-app/src/renderer/src/editor/validators/edgeChecks.ts; editor-app/src/renderer/src/editor/validators/parallelChecks.ts; editor-app/src/renderer/src/editor/validators/continuity.ts; editor-app/src/renderer/src/editor/validators/resourceChecks.ts; editor-app/src/renderer/src/editor/validators/types.ts; editor-app/src/renderer/src/editor/validationRuleOverrides.ts; editor-app/src/renderer/src/editor/useSceneIO.ts; editor-app/src/renderer/src/editor/LogsPanel; editor-app/src/renderer/src/editor/nodes/nodeRegistry.ts -->
