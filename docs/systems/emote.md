---
tags:
  - emote
  - runtime
  - dialogue
---

# Система эмоций (Emote System)

Всплывающие спрайты-эмоции над персонажами и объектами, обновляемые центральным менеджером и привязанные к world-координатам цели.

## Обзор

Система хранит список активных эмоций в `global.global_emote_system.active_emotes`. Каждая эмоция — структура с целевым объектом, спрайтом, таймером жизни и оффсетом. Инициализация `global.global_emote_system` происходит в `obj_Init`. Обновление и отрисовка вызываются из `obj_globalManager` (`emote_step` и `emote_draw_gui`).

Эмоции можно показать из любого места кода: катсцен, диалогов, скриптов взаимодействия. `scr_parse_emote` использует те же actor/emotion-коды при разборе speaker-строк Yarn, чтобы синхронизировать портрет и эмоцию персонажа.

## Архитектура / API

### Публичные функции

| Функция | Параметры | Описание |
|---------|-----------|----------|
| `emote_show` | `_target`, `_sprite`, `_duration`, `_offset_x`, `_offset_y`, `_scale` | Создаёт эмоцию над объектом. `_sprite` принимает индекс или строку. Возвращает структуру или `noone`. |
| `emote_hide_all_for` | `_target` | Скрывает все эмоции для указанного объекта. |
| `emote_hide_all` | — | Скрывает все активные эмоции. |
| `scr_emote_show` | `_target`, `_sprite`, `_duration`, `_offset_x`, `_offset_y`, `_scale` | Тонкая обёртка над `emote_show`. |
| `scr_emote_hide_for` | `_target` | Обёртка над `emote_hide_all_for`. |
| `scr_emote_hide_all` | — | Обёртка над `emote_hide_all`. |

### Структура эмоции

| Поле | Тип | Описание |
|------|-----|----------|
| `active` | `bool` | Флаг активности. |
| `target` | `instance` | Объект, к которому привязана эмоция. |
| `sprite` | `asset` | Индекс спрайта. |
| `image_index` | `real` | Текущий кадр анимации. |
| `image_speed` | `real` | Скорость анимации относительно `game_get_speed`. |
| `frames_left` | `real` | Оставшееся время жизни. |
| `offset_x` | `real` | Смещение по X от центра объекта. |
| `offset_y` | `real` | Смещение по Y от верха `bbox_top`. |
| `scale` | `real` | Масштаб эмоции. |

### Разрешение спрайта

`emote_resolve_sprite` принимает строку или индекс:

- Если передан индекс и спрайт существует — возвращает его.
- Если передана строка — ищет `asset_get_index(_sprite)`.
- Если точное имя не найдено — добавляет префикс `spr_` и повторяет поиск.
- При неудаче возвращает `noone`, и эмоция не создаётся.

## Примеры

### Показать эмоцию над игроком

```gml title="scr_emote_show"
scr_emote_show(obj_player, "spr_exclamation", 60, 0, -32, 1);
```

### Скрыть все эмоции NPC

```gml title="scr_emote_hide"
scr_emote_hide_for(obj_asher);
```

### Эмоция из катсцены

```gml title="Пример внутри cutscene action"
emote_show(actor, "spr_heart", 90, 0, -24, 1);
```

### Интеграция с диалогом

```gml title="Yarn-строка и парсинг"
// Yarn: Asher [asher:happy]: Привет!
var _parsed = scr_parse_emote("asher:happy", "Asher", _prev_actor, _prev_emotion, _prev_display);
// _parsed.emotion содержит "happy" — можно использовать для выбора портрета
// или запустить эмоцию над объектом актёра.
```

## Troubleshooting

!!! warning "Эмоция не появляется"
    Проверьте, что `_sprite` существует. `emote_resolve_sprite` возвращает `noone`, если не найден ни точный индекс, ни вариант с префиксом `spr_`.

!!! note "Эмоция пропадает при смерти цели"
    `emote_step` удаляет эмоцию, если `instance_exists(_target)` возвращает `false`. Если цель уничтожается раньше таймера, эмоция исчезнет.

## См. также

- [NPC и диалоги](npc-dialogue.md) — `scr_parse_emote`, `readDialogue`
- [Диалоговые портреты](dialogue-portraits.md) — портреты, привязанные к actor/emotion
- [GML-скрипты](../code-reference/gml-scripts.md) — полный список скриптов
- [Архитектура: объекты](../architecture/objects.md) — `obj_globalManager`, `obj_Init`
