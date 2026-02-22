# Катсцены: Примеры

## Пример 1: cutscene_* стиль (из `scr_cutscene.gml`)
Тестовая катсцена создаёт менеджер, добавляет экшены и запускает:
- движения (`cutscene_move`)
- анимации (`cutscene_animate`)
- поворот (`cutscene_set_facing`)
- диалог (`cutscene_dialogue`)
- действия камеры (`cutscene_camera_center`, `cutscene_camera_pan`, `cutscene_camera_track`)
- параллель (`cutscene_parallel`)
- выполнение функции (`cutscene_run_function`)

Важно: если в катсцене не добавить экшены камеры, камера может остаться на позиции старта катсцены.

## Пример 2: Builder стиль (c_*)
Builder-стиль работает через «активного менеджера»:
- `c_begin(id)` создаёт менеджер и кладёт его в `global.__cutscene_build_mgr`.
- `c_play()` запускает.

Паттерн:
- `c_speaker("name")` — выбирает текущего актёра (строковый ключ).
- дальнейшие команды `c_setxy`, `c_depth`, `c_facing` используют этот ключ.

Примечание: в текущей реализации строковый ключ **не всегда резолвится** экшенами через `resolve_target` (см. `troubleshooting.md`).
