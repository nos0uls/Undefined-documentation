# Катсцены: Актёры

## Реестр актёров у менеджера
- `actor_map` хранит сопоставление `key -> instance`.
- `actor_names` хранит список ключей (нужен для дебага/итерации).

## Создание (`cutscene_actor_create` / `ActionActorCreate`)

Сигнатура обёртки:
- `cutscene_actor_create(key, x, y, sprite_or_object, copy_from_object=undefined)`

Поведение `ActionActorCreate`:
- Если передан `copy_from_object` (и это instance), то базовые параметры берутся от него:
  - `x/y`, `object_index`, `sprite_index`, `image_index`, `image_xscale/yscale`.
- Если `sprite_or_object` — asset объекта, будет создан этот объект.
- Если `sprite_or_object` — строка, движок пытается найти asset по имени и трактует его как объект или спрайт.
- Если `sprite_or_object` — sprite asset, он будет назначен в `sprite_index` созданного инстанса.

Важно:
- Если объект для создания не определён, по умолчанию используется **`obj_actor`**.
- После создания инстанс регистрируется как `manager.actor_map[$ key] = instance`.

## Уничтожение (`cutscene_actor_destroy` / `ActionActorDestroy`)
- `cutscene_actor_destroy(target_ref)` принимает instance id или некоторые legacy ссылки.
- Если передан строковый ключ и он был в `actor_map`, запись удаляется.

## Практические рекомендации
- Для надёжности передавай в экшены **instance id**, а не строковые ключи.
- Если нужно создавать не игрока, а актёра катсцены, передавай объект явно (например `obj_actor`).