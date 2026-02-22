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

## Строковые ключи актёров не резолвятся через `resolve_target`
`ActionActorCreate` сохраняет актёра в `manager.actor_map[$ key] = instance`.
Но `resolve_target` менеджера поддерживает только:
- instance id
- asset объекта
- строку `"player"`

Поэтому экшены, которым передать строку-ключ (`"chara"`, `"npc"`), могут не найти цель.

Решение на уровне использования:
- передавать instance id напрямую,
- либо расширять `resolve_target` (это уже правка кода).

## `cutscene_actor_create` по умолчанию создаёт `obj_player`
Если не передать объект/спрайт, `ActionActorCreate` берёт `obj_player` как объект по умолчанию.
Если нужно создавать катсцен-актора, лучше явно передавать `obj_actor`.
