# Валидация графа (Graph Validation)

Перед экспортом катсцены редактор проверяет граф на ошибки, предупреждения и советы. Результаты отображаются в панели **Logs**.

## Уровни серьёзности

| Уровень | Значение | Блокирует экспорт |
|---------|----------|-------------------|
| `error` | Критическая ошибка | Да |
| `warn`  | Важное предупреждение | Нет |
| `tip`   | Рекомендация / best practice | Нет |

## Структурные проверки

### Ноды

- **start / end**: граф должен содержать ровно одну `start` и хотя бы одну `end`. `start` не должна иметь входящих связей, `end` — исходящих.
- **Изолированные ноды**: ноды без входящих и исходящих связей (кроме `start`/`end`) вызывают `warn`.
- **Недостижимые ноды**: ноды, до которых нельзя добраться от `start`, вызывают `warn`.
- **Множественные выходы**: обычные ноды (не `branch`/`parallel_start`) с более чем одним исходящим ребром вызывают `warn`.

### Рёбра

- **Потерянные ссылки**: рёбра, ссылающиеся на несуществующие `source`/`target`, — `error`.
- **Отрицательный wait**: `waitSeconds < 0` — `warn`.
- **Условия на рёбрах**: если включено `conditionEnabled`, поля `Variable` и `Equals` должны быть заполнены. Переменные не должны начинаться с `global.`.
- **wait_until_true**: для режимов `global_var`, `node_reached` и `timeout` проверяется корректность соответствующих полей.

### Пары parallel_start ↔ parallel_join

- Проверяется взаимная ссылка (`joinId` / `pairId`).
- Совпадение списка `branches` в обеих нодах.
- Корректность `sourceHandle` / `targetHandle` (формат `out_*` / `in_*`).
- Отсутствие дублирующихся веток и рёбер.

## Проверка обязательных параметров

Для каждого типа ноды задан список обязательных полей (`REQUIRED_PARAMS`). Если поле пустое — `warn`.

| Тип ноды | Обязательные поля |
|----------|-------------------|
| `move`, `set_position`, `animate`, `camera_track`, `camera_track_until_stop`, `set_depth`, `set_facing`, `follow_path`, `auto_facing`, `auto_walk`, `emote`, `jump`, `halt`, `flip`, `spin`, `shake_object`, `set_visible` | `target` |
| `actor_create` | `key` |
| `camera_pan` | `x`, `y` |
| `camera_pan_obj` | `target` |
| `branch` | `condition` |
| `mark_node` | `name` |

## Best-practice проверки (новые)

Дополнительные проверки, добавленные для улучшения качества катсцен:

- **dialogue**: если `.yarn` файл не выбран — `warn`.
- **camera_shake**: `duration <= 0` — `warn`.
- **follow_path**: пустой `path` — `warn`; только одна точка — `tip` (рекомендуется использовать `set_position`).
- **halt**: наличие исходящих связей у `halt` — `warn` (нода блокирует выполнение).
- **mark_node**: пустое имя маркера — `warn`.
- **set_facing**: значение `direction` отличное от `left`/`right` — `warn`.
- **jump**: пустой `target` — `warn`.

## Расширенная валидация (контекст ресурсов)

Если редактор загрузил `.yyp` проект, включаются дополнительные проверки:

- **actor_create.key**: проверка существования объекта/спрайта в проекте.
- **dialogue.file / .node**: проверка существования `.yarn` файла и ноды внутри него.
- **run_function.function**: проверка по whitelist из `cutscene_engine_settings.json`.
- **branch.condition**: проверка по whitelist условий.
- **animate.sprite / emote.sprite**: проверка существования спрайта в проекте.

## Формат результата

```typescript
type ValidationResult = {
  entries: ValidationEntry[]
  hasErrors: boolean
}

type ValidationEntry = {
  severity: 'error' | 'warn' | 'tip'
  nodeId?: string
  edgeId?: string
  message: string
}
```

Сообщения формулируются кратко, на английском, с actionable hint (указанием, что именно исправить).

---

## См. также

- [Форматы, импорт и экспорт](formats.md) — `.usc.json`, engine `.json`
- [Базовый workflow](workflow.md) — проверка warnings перед экспортом
- [Интерфейс и Preferences](ui.md) — панель `Логи / Предупреждения`
- [Интеграция с проектом](integration.md) — загрузка `.yyp`, проверка ресурсов
