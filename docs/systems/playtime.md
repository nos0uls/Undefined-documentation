---
tags:
  - gameplay
  - code-reference
  - init
---

# Playtime

Подсчёт времени, проведённого в игре — для каждого сейва отдельно и суммарно за все сессии.

## Обзор

Два показателя:

- **Время сейва** (`global.__save_playtime_seconds`) — накапливается в `obj_globalManager.Step_0` через `delta_time`, сохраняется внутри каждого слота.
- **Общее время** (`global.__no_shower_seconds`) — сумма за все сессии и сейвы, хранится в `game_state.dat`.

## Отображение

- **Меню сейвов** (`obj_saveManager.Draw_0`) — строка `H:MM:SS` под каждым существующим слотом (только если время > 0).
- **Настройки → Разное** — readonly-пункт *"show me how many hours have passed since i showered"* показывает общее время при нажатии (`obj_settingsManager`).

## Настройки отрисовки

Переменные в `obj_saveManager.Create_0`:

| Переменная | Значение по умолчанию | Описание |
|------------|-----------------------|----------|
| `playtime_font` | `ft_menuFont_1` | Шрифт текста |
| `playtime_scale` | `1.0` | Масштаб |
| `playtime_x_offset` | `0` | Смещение по X от центра рамки |
| `playtime_y_offset` | `55` | Смещение по Y от центра рамки |
| `playtime_color` | `#FF9F9F` | Цвет текста (hex) |
| `playtime_show` | `true` | Показать/скрыть строку |

## Форматирование

`scr_format_playtime(seconds)` → строка `H:MM:SS`.

```gml title="Пример использования" linenums="1"
var _text = scr_format_playtime(global.__save_playtime_seconds);
// _text = "2:15:30"
```

## Файлы

| Файл | Роль |
|------|------|
| `scripts/scr_format_playtime/scr_format_playtime.gml` | Форматирование секунд в строку |
| `objects/obj_globalManager/Step_0.gml` | Накопление `delta_time` |
| `objects/obj_Init/Create_0.gml` | Инициализация переменных + кэш метаданных |
| `scripts/scr_saveSave/scr_saveSave.gml` | Запись `playtime_seconds` в сейв |
| `scripts/scr_saveLoad/scr_saveLoad.gml` | Чтение `playtime_seconds` из сейва |
| `scripts/scr_game_state/scr_game_state.gml` | `total_playtime_seconds` в `game_state` |
| `objects/obj_saveManager/Draw_0.gml` | Отрисовка времени в меню сейвов |
| `objects/obj_settingsManager/Draw_64.gml` | Отрисовка общего времени в настройках |

## См. также

- [Инициализация и Runtime](../development/undefinedtale888-init-and-runtime.md) — `obj_Init`, `obj_globalManager`
- [Сейвы](save-load.md) — `scr_saveSave`, `scr_saveLoad`
