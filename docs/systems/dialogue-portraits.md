# Портреты диалога (Dialogue Portraits)

Этот документ описывает текущую runtime-схему портретов для Yarn + Chatterbox в `Undefinedtale888`.

## Формат строки

Рекомендуемый формат `.yarn` строки:

```text
actor[emotion]: Текст реплики
```

Где:
- `speaker` используется как `actor id`
- `speaker data` используется как `emotion`
- пустой `speaker` означает narrator
- пустая `emotion` у того же actor сохраняет предыдущую emotion

## Основная цепочка данных

1. `textboxTest_scribble/Step_0.gml` получает текущую content-строку через Chatterbox helper-функции.
2. `scr_parse_emote(...)` нормализует `actor/emotion` и применяет fallback-правила.
3. `map_emotions(...)` делает lookup по схеме `actor -> emotion -> resources`.
4. `textboxTest_scribble` сохраняет итог в runtime-state:
   - `actor_prev`
   - `emotion_prev`
   - `mouth_open_prev`
   - `mouth_closed_prev`
   - `sound_prev`
   - `talk_hold_timer`
   - `talk_open_now`
5. `obj_face` читает уже готовый runtime-state и только рисует portrait.

## Где живёт runtime-state

Runtime-state хранится в `textboxTest_scribble`, потому что именно этот объект управляет текущей репликой и переходами `ChatterboxContinue()` / `ChatterboxSelect()`.

Это важно по двум причинам:
- предыдущее состояние не теряется между строками
- `obj_face` остаётся простым renderer-объектом без парсинга текста

## Правила fallback

## Talk Animation

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

### Narrator

Если `speaker == ""`, строка считается narrator:
- портрет скрыт
- используется narrator fallback sound

### Отсутствие portrait sprite

Если `mouth_closed == noone` или closed sprite невалиден:
- портрет не рисуется
- звук реплики всё равно остаётся доступным
- `obj_face` просто пропускает Draw для этой строки

### Повтор того же actor без emotion

Если:
- actor тот же, что и `actor_prev`
- `speaker data == ""`

тогда система использует `emotion_prev`.

### Новый actor без emotion

Если actor новый и emotion пустая, система использует `default` для этого actor.

### Неизвестный actor или emotion

`map_emotions(...)` сначала ищет:
1. actor
2. emotion внутри actor
3. `default` внутри actor
4. narrator fallback

## Ответственность файлов

### `scripts/scr_parse_emote/scr_parse_emote.gml`
- нормализует входные строки
- применяет правила narrator / previous emotion / default
- возвращает единый struct результата

### `scripts/map_emotions/map_emotions.gml`
- хранит nested struct lookup
- возвращает `mouth_closed`, `mouth_open`, `sound`
- использует `static`, чтобы таблица создавалась один раз

### `objects/textboxTest_scribble/Create_0.gml`
- инициализирует portrait runtime-state
- задаёт стартовый typist sound
- при старте диалога создаёт `obj_face`, если renderer ещё не существует
- регистрирует `Scribble` per-character callback для reveal-driven talk animation

### `objects/textboxTest_scribble/Step_0.gml`
- пересчитывает portrait runtime после загрузки диалога
- пересчитывает portrait runtime после `ChatterboxSelect()`
- пересчитывает portrait runtime после `ChatterboxContinue()`
- обновляет `talk_hold_timer` и `talk_open_now`

### `objects/obj_face/Step_0.gml`
- читает текущий portrait-state
- считает, что портрет существует только если валиден `mouth_closed` sprite
- не считает reveal сам, а только читает готовый `talk_open_now`

### `objects/obj_face/Draw_64.gml`
- только рисует already resolved portrait sprite

## Почему выбрана nested struct схема

Схема `actor -> emotion -> resources` была выбрана вместо плоского ключа `actor:emotion`, потому что она:
- легче читается
- проще расширяется
- даёт удобный fallback на `default`
- лучше подходит для runtime-логики narrator / actor / previous emotion
