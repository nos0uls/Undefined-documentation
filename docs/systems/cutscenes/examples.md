# Катсцены: Примеры

## Пример 1: JSON-стиль (из `obj_cutsceneTest`)
Тестовая катсцена теперь загружается из JSON-файла через `cutscene_load_json()`:

```gml
var _mgr = cutscene_load_json("cutscenes/test_scene.json");
_mgr.start_cutscene();
```

JSON-файл содержит декларативное описание:
- `move`, `wait`, `dialogue`, `parallel`
- действия камеры (`camera_pan`, `camera_track`, `camera_shake`)
- `actor_create`, `set_facing`, `animate`
- `fade_in`, `fade_out`, `play_sfx`

Если в JSON-катсцене не добавить экшены камеры, камера останется на позиции старта катсцены.

### Legacy fallback
`obj_cutsceneTest.Step_0` всё ещё поддерживает legacy-функции (`fn`), но все 5 тестовых пунктов меню переписаны на JSON (`json`).

## Пример 2: Builder стиль (c_*)
Builder-стиль работает через «активного менеджера»:
- `c_begin(id)` создаёт менеджер и кладёт его в `global.__cutscene_build_mgr`.
- `c_play()` запускает.

Паттерн:
- `c_speaker("name")` — выбирает текущего актёра (строковый ключ).
- дальнейшие команды `c_setxy`, `c_depth`, `c_facing` используют этот ключ.

### Регистрация в Yarn (Chatterbox)
Все `c_*` команды зарегистрированы как Yarn-функции через `cutscene_register_chatterbox_functions()` (вызов в `obj_Init`):

```yarn
<<c_walk obj_player right 2 60>>
<<c_dialogue test.yarn Start>>
<<c_fadein 60>>
```

Примечание: строковые ключи актёров поддерживаются, но для самого надёжного поведения в экшенах предпочтительнее передавать instance id напрямую.

---

## См. также

- [Обзор катсцен](overview.md) — `obj_cutsceneManager`, `action_queue`
- [Архитектура](architecture.md) — JSON-загрузка, `cutscene_load_json()`
- [API](api.md) — `cutscene_add`, Action-классы
- [Игрок в катсцене](player_in_cutscene.md) — блокировка движения, camera override
- [Актёры](actors.md) — `cutscene_actor_create`, `ActionActorCreate`
