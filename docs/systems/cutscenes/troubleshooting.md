# Катсцены: Типовые проблемы

## Камера «застыла» на месте запуска катсцены
Причина:
- `obj_cutsceneManager.start_cutscene()` выставляет `global.cutscene_camera_override = true`.
- `obj_player/Step_2.gml` при этом делает `exit` и перестаёт обновлять камеру.

Что делать:
- Добавлять экшены камеры (например `cutscene_camera_track(player, frames)`), либо использовать `c_pan/c_panobj`.

## `cutscene_wait` на самом деле ждёт кадры
`ActionWait` работает в кадрах.
Обёртка `cutscene_wait(_seconds)` по имени вводит в заблуждение: параметр — **кадры**.

## Строковые ключи актёров работают, но instance id надёжнее
`ActionActorCreate` сохраняет актёра в `manager.actor_map[$ key] = instance`.
Строковые ключи актёров поддерживаются, но самый предсказуемый вариант для сложных экшенов и ветвлений — передавать instance id напрямую.

Если строковая цель не находится:
- проверьте, что актёр уже создан и зарегистрирован в `actor_map`
- проверьте точный `key`, с которым он создавался
- если нужен максимально стабильный таргетинг, используйте instance id

## `cutscene_actor_create` по умолчанию создаёт `obj_actor`
Если не передать объект/спрайт, `ActionActorCreate` использует `obj_actor` как объект по умолчанию.
Если нужен другой объект, лучше передавать его явно.

---

## См. также

- [Обзор катсцен](overview.md) — `obj_cutsceneManager`, `action_queue`, `global.cutscene_camera_override`
- [Архитектура](architecture.md) — `actor_map`, `resolve_target`, жизненный цикл
- [Актёры](actors.md) — `cutscene_actor_create`, `ActionActorCreate`
- [Камера](camera.md) — `cutscene_camera_pan`, `cutscene_camera_track`
- [API](api.md) — `cutscene_add`, Action-классы
- [Игрок в катсцене](player_in_cutscene.md) — блокировка движения, camera override