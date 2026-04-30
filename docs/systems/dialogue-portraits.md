# Портреты диалога (Dialogue Portraits)

Этот документ описывает текущую runtime-схему портретов для Yarn + Chatterbox в `Undefinedtale888`.

## Формат строки

Актуальный формат `.yarn` строки:

```text
DisplayName [code:emotion]: Текст реплики
```

Где:
- `DisplayName` — человекочитаемое имя для nameplate (может содержать пробелы, может быть пустым).
- `code` — внутренний идентификатор актёра (lookup-ключ для `map_emotions` и `actor_display_name`).
- `emotion` — эмоция/настроение строки. Можно опустить (`[code]: ...`), тогда применится previous/default.
- Полностью без `[]` и `:` → narrator (без портрета и без nameplate).

Примеры:

```text
Mysterious Boy [chara:question]: А вот и я!
[chara]: Та же реплика, эмоция берётся из предыдущей.
Это текст рассказчика без говорящего.
```

## Speaker nameplate

Nameplate (подложка с именем) рисуется в `textboxTest_scribble/Draw_64.gml` поверх textbox.

| Свойство | Описание |
|----------|----------|
| Источник имени | `display_name_prev` (из parser). Если пусто — nameplate не рисуется |
| Скрытие при options | Скрывается при выборе опций (`ChatterboxGetOptionCount > 0`) |
| Экранирование | `[` → `[lsb]`, `]` → `[rsb]` перед `scribble(...)`, чтобы скобки в имени не ломали разметку |
| Настройки | `Create_0.gml`, `#region Speaker nameplate settings` |

**Настройки nameplate** (в `Create_0.gml`):

| Переменная | Назначение |
|------------|------------|
| `nameplate_visible`, `nameplate_sprite` | Видимость и спрайт подложки |
| `nameplate_offset_x/y` | Смещение от центра textbox |
| `nameplate_anchor_x/y` | Anchor point |
| `nameplate_padding_x/y` | Padding внутри nameplate |
| `nameplate_auto_fit_width`, `nameplate_min_width` | Автоширина и минимум |
| `nameplate_text_font`, `nameplate_text_scale`, `nameplate_text_color` | Параметры текста |
| `nameplate_text_offset_x/y` | Смещение текста внутри nameplate |

### Источник DisplayName (приоритет)

| Приоритет | Источник | Условие |
|-----------|----------|---------|
| 1 | Текст из yarn перед `[` | Явно задано в строке |
| 2 | `actor_display_name(code)` | Таблица fallback по code |
| 3 | `display_name_prev` | Actor тот же, явного имени нет |
| 4 | ` "" ` | Nameplate скрыт |

## Основная цепочка данных

1. `textboxTest_scribble/Step_0.gml` получает текущую content-строку через Chatterbox helper-функции.
2. `scr_parse_emote(...)` нормализует `actor/emotion` и применяет fallback-правила.
3. `map_emotions(...)` делает lookup по схеме `actor -> emotion -> resources`.
4. `textboxTest_scribble` сохраняет итог в runtime-state:
   - `actor_prev`
   - `emotion_prev`
   - `display_name_prev`
   - `mouth_open_prev`
   - `mouth_closed_prev`
   - `sound_prev`
   - `talk_hold_timer`
   - `talk_open_now`
5. `obj_face` читает уже готовый runtime-state и только рисует portrait.
6. `textboxTest_scribble/Draw_64.gml` читает `display_name_prev` и рисует nameplate (sprite + scribble).

## Где живёт runtime-state

Runtime-state хранится в `textboxTest_scribble`, потому что именно этот объект управляет текущей репликой и переходами `ChatterboxContinue()` / `ChatterboxSelect()`.

Это важно по двум причинам:
- предыдущее состояние не теряется между строками
- `obj_face` остаётся простым renderer-объектом без парсинга текста

## Layout внутри textbox

Позиционирование portrait, текста и continue marker теперь построено вокруг одного anchor:

- `box_x`, `box_y` — это центр textbox
- `textboxTest_scribble/Create_0.gml` хранит два preset-набора layout-переменных:
  - `with_portrait`
  - `without_portrait`
- текст использует `text_offset_x_*`, `text_offset_y_*`, `text_wrap_width_*`, `text_wrap_height_*`
- continue marker использует `marker_visible_*`, `marker_offset_x_*`, `marker_offset_y_*`, `marker_scale_*`
- portrait использует `portrait_offset_x_*`, `portrait_offset_y_*`, `portrait_scale_*`

Это означает, что portrait больше не управляет текстовой колонкой через margins/gap. Теперь и portrait, и текст, и marker настраиваются как независимые зоны внутри одного textbox.

### Правило для continue marker

Continue marker `>` внутри textbox — это отдельная часть layout preset, а не часть portrait renderer.

В текущей схеме:
- если активен preset с portrait, `>` marker скрыт
- если portrait нет, marker можно настраивать отдельно от текста

## Правила fallback

### Talk Animation

Анимация разговора теперь привязана к **реальному reveal символов** через `Scribble typist.function_per_char(...)`.

Схема работает так:
- `textboxTest_scribble/Create_0.gml` регистрирует per-character callback в typist
- callback вызывается только когда Scribble действительно открывает новый символ
- callback поднимает короткий `talk_hold_timer`
- `textboxTest_scribble/Step_0.gml` уменьшает hold на паузах и готовит `talk_open_now`
- `obj_face/Step_0.gml` просто выбирает `mouth_open` или `mouth_closed` по `talk_open_now`

Для этой схемы была внесена маленькая правка в `__scribble_class_typist.gml`:
- `function_per_char` теперь получает вычисленный `execution_scope`, а не только target text element
- это позволяет callback безопасно обновлять runtime-state самого `textboxTest_scribble`

Это проще и точнее, чем polling по таймеру в `obj_face`, потому что рот двигается только от реального продвижения текста.

| Сценарий | Поведение |
|----------|-----------|
| **Narrator** (`speaker == ""`) | Портрет скрыт, narrator fallback sound |
| **Нет portrait sprite** (`mouth_closed == noone`) | Портрет не рисуется, звук реплики доступен, `obj_face` пропускает Draw |
| **Повтор actor без emotion** | Используется `emotion_prev` |
| **Новый actor без emotion** | Используется `default` для actor |
| **Неизвестный actor/emotion** | `map_emotions` fallback: actor → emotion → `default` → narrator fallback |

## Ответственность файлов

| Файл | Роль | Ключевые функции |
|------|------|------------------|
| [`scr_parse_emote.gml`](#) | Парсинг строки | Сплит `code:emotion`, fallback-логика, возвращает `{ actor, emotion, display_name, mouth_closed, mouth_open, sound }` |
| [`actor_display_name.gml`](#) | Fallback имен | Статическая таблица display name по `code` |
| [`map_emotions.gml`](#) | Mapping ресурсов | Nested struct lookup `actor → emotion → sprite/sound`, создаётся один раз через `static` |
| [`textboxTest_scribble/Create_0.gml`](#) | Инициализация | Создание `obj_face`, typist sound, per-character callback, layout presets |
| [`textboxTest_scribble/Step_0.gml`](#) | Runtime | Пересчёт portrait state после `ChatterboxContinue/Select`, `talk_hold_timer` |
| [`obj_face/Step_0.gml`](#) | Выбор sprite | Чтение `talk_open_now`, валидация `mouth_closed` |
| [`obj_face/Draw_64.gml`](#) | Отрисовка | `draw_sprite_ext` с `portrait_offset_*` и `portrait_scale_*` |

!!! warning "Не менять Scribble вне проекта"
    Правка в `__scribble_class_typist.gml` (`function_per_char` получает `execution_scope`) сделана локально. При обновлении библиотеки эта правка может быть перезаписана.

## Почему nested struct

Схема `actor -> emotion -> resources` вместо плоского `actor:emotion`:

| Критерий | Nested struct | Плоский ключ |
|----------|--------------|--------------|
| Читаемость | Высокая | Средняя |
| Расширяемость | Добавить emotion — вложенный struct | Добавить ключ — править парсер |
| Fallback | `default` внутри actor | Отдельная логика |
| Narrator | Естественно через отсутствие actor | Специальный ключ |

---

## См. также

- [Карта тонкой настройки UI](ui-tuning-map.md) — все layout-переменные textbox, portrait, marker
- [Система взаимодействия](interaction.md) — как запускается диалог
- [Катсцены: API](cutscenes/api.md) — dialogue actions в катсценах
