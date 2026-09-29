---
title: Объекты и события
tags:
  - reference
  - objects
  - events
---

# Объекты и события

Все объекты проекта Undefinedtale-888 из `objects/`: родитель, persistent-флаг, спрайт и реализованные события GameMaker.

!!! info "Генерируемая страница"
    Таблицы собираются скриптом `_meta/gen_reference.py` из `_meta/objects.txt`. После изменения кода страницу пересобирают, а не правят вручную.

!!! note "Наследование событий"
    В колонке «События» перечислены только события с кодом в самом объекте; события родителя наследуются по стандартным правилам GameMaker (`event_inherited()`).

## Родители `par_*`

| Объект | Родитель | Persistent | Спрайт | События | Док-страница |
| --- | --- | --- | --- | --- | --- |
| `par_actor` | `par_depth` | нет | — | Step, Create | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `par_decor` | `par_depth` | нет | — | Create | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `par_depth` | — | нет | `spr_rmChanger` | Create, Step | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `par_entity` | — | нет | — | Create | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `par_interactable` | `par_depth` | нет | — | Create, Other Room Start, Other Room End | [Иерархия объектов](../architecture/object-hierarchy.md) |

## Системные менеджеры

| Объект | Родитель | Persistent | Спрайт | События | Док-страница |
| --- | --- | --- | --- | --- | --- |
| `o_SharedTweener` | — | да | — | Create, End Step, Begin Step, Other Room End, Other Room Start, Other Game End, Destroy | — |
| `obj_changingRoomsController` | — | да | — | Create, Draw, Step | [Переходы комнат](../systems/room-transitions.md) |
| `obj_globalManager` | — | да | — | Create, Step, End Step, Draw GUI, Other Game End | [Глобальное состояние](../architecture/global-state.md) |
| `obj_Init` | — | да | — | Create | [Инициализация](../architecture/initialization.md) |
| `obj_music_ctrl` | — | да | — | Create, Step, Draw GUI | [Музыка и звук](../systems/music.md) |
| `obj_saveManager` | — | нет | — | Create, Step, Draw GUI | [Сохранения](../systems/save-system.md) |
| `obj_settingsManager` | — | нет | — | Create, Destroy, Step, Draw GUI | [UI и меню](../systems/ui-and-menus.md) |

`o_SharedTweener`: служебный объект библиотеки TweenGMS, не игровой код.

## Игрок и мир

| Объект | Родитель | Persistent | Спрайт | События | Док-страница |
| --- | --- | --- | --- | --- | --- |
| `bush` | `par_decor` | нет | `bush2` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `npc1` | `par_interactable` | нет | `npc` | Create, Step | [Взаимодействие](../systems/interaction.md) |
| `npc2` | `npc1` | нет | `npc247` | — | [Взаимодействие](../systems/interaction.md) |
| `obj_anim` | — | нет | — | Create, Step, Other User 0 | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `obj_asher` | `par_interactable` | нет | `spr_asher_default` | Step, Create | [Взаимодействие](../systems/interaction.md) |
| `obj_bench` | `par_interactable` | нет | `bench1` | Step, Create | [Взаимодействие](../systems/interaction.md) |
| `obj_collider` | `par_entity` | нет | `spr_collider` | Create, Step | [Игрок](../systems/player.md) |
| `obj_dialoguetest` | `par_interactable` | нет | `spr_interact` | Create, Step | [Взаимодействие](../systems/interaction.md) |
| `obj_kachela` | `par_decor` | нет | `kachela` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `obj_lantern` | `par_decor` | нет | `lantern` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `obj_player` | `par_actor` | да | `spr_Chara_walking_D` | Create, Step, Begin Step, End Step, CleanUp | [Игрок](../systems/player.md) |
| `obj_pointMarker` | — | да | `spr_interact` | Create | [Взаимодействие](../systems/interaction.md) |
| `obj_save` | `par_interactable` | нет | `spr_save` | Step, Key Press 13, Create, Alarm 0, Draw GUI | [Сохранения](../systems/save-system.md) |
| `obj_sheepFountain` | `par_interactable` | нет | `fountain` | Create, Step | [Взаимодействие](../systems/interaction.md) |
| `obj_sign` | `par_decor` | нет | `sign1` | Step | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `obj_slopeCollider` | `par_entity` | нет | `spr_slopeCollider` | Step, Create, Collision obj_player | [Игрок](../systems/player.md) |
| `obj_tree1` | `par_decor` | нет | `tree1` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `obj_tree2` | `par_decor` | нет | `tree2` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `obj_visualObject` | `par_depth` | нет | `Sprite8` | Create | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `objRoomChanger` | — | нет | `spr_rmChanger` | Create, Step, Collision obj_player | [Переходы комнат](../systems/room-transitions.md) |
| `pinkBench` | `par_decor` | нет | `bench` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `sand` | `par_decor` | нет | `pesochnica` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |
| `spr_pinkBench` | `par_decor` | нет | `bench` | — | [Иерархия объектов](../architecture/object-hierarchy.md) |

## UI и меню

| Объект | Родитель | Persistent | Спрайт | События | Док-страница |
| --- | --- | --- | --- | --- | --- |
| `obj_face` | — | нет | — | Create, End Step, Draw GUI | [Диалоги](../systems/dialogue.md) |
| `obj_inGameMenu` | — | нет | — | Create, Destroy, Draw GUI, Step | [UI и меню](../systems/ui-and-menus.md) |
| `obj_menu` | — | нет | — | Create, Draw GUI, Step | [UI и меню](../systems/ui-and-menus.md) |
| `obj_menuBGSpriteChanger` | — | нет | `_1` | Create, Step, Draw | [UI и меню](../systems/ui-and-menus.md) |
| `obj_p3r_background` | — | нет | `spr_black` | Create, Step, Begin Step, End Step, Draw, Draw GUI, Draw GUI Begin, Draw GUI End, Pre Draw, Post Draw, Destroy | [UI и меню](../systems/ui-and-menus.md) |
| `obj_p3r_pause` | — | нет | `spr_black` | Create, Step, Begin Step, End Step, Draw, Draw GUI, Draw GUI Begin, Draw GUI End, Pre Draw, Post Draw, Destroy | [UI и меню](../systems/ui-and-menus.md) |
| `obj_p3r_settings` | — | нет | `spr_black` | Create, Step, Begin Step, End Step, Draw, Draw GUI, Draw GUI Begin, Draw GUI End, Pre Draw, Post Draw, Destroy | [UI и меню](../systems/ui-and-menus.md) |
| `obj_p3r_title` | — | нет | `spr_black` | Create, Step, Begin Step, End Step, Draw, Draw GUI, Draw GUI Begin, Draw GUI End, Pre Draw, Post Draw, Destroy | [UI и меню](../systems/ui-and-menus.md) |
| `obj_p3r_transition` | — | нет | `spr_black` | Create, Step, Begin Step, End Step, Draw, Draw GUI, Draw GUI Begin, Draw GUI End, Pre Draw, Post Draw, Destroy | [UI и меню](../systems/ui-and-menus.md) |
| `textboxTest_scribble` | — | нет | — | Create, Begin Step, Step, Draw GUI, CleanUp | [Диалоги](../systems/dialogue.md) |

## Катсцены

| Объект | Родитель | Persistent | Спрайт | События | Док-страница |
| --- | --- | --- | --- | --- | --- |
| `obj_actor` | `par_actor` | нет | — | Create, Step | [Актёры и камера](../cutscenes/actors-and-camera.md) |
| `obj_cutsceneManager` | — | да | — | Create, Step, Draw, Draw GUI, Other Room Start, Other Room End, CleanUp | [Архитектура катсцен](../cutscenes/architecture.md) |
| `obj_dummy` | `obj_actor` | нет | `spr_Dummy` | — | [Актёры и камера](../cutscenes/actors-and-camera.md) |

## Debug и прочее

| Объект | Родитель | Persistent | Спрайт | События | Док-страница |
| --- | --- | --- | --- | --- | --- |
| `obj_cutsceneTest` | — | нет | `spr_save` | Create, Step, Draw, Draw GUI | [Отладка и тесты](../systems/debug-and-testing.md) |
| `obj_devLoader` | — | нет | — | Create, Step, Draw GUI | [Отладка и тесты](../systems/debug-and-testing.md) |
| `obj_menuTest` | — | нет | `spr_black` | Create, Step, Begin Step, End Step, Draw, Draw GUI, Draw GUI Begin, Draw GUI End, Pre Draw, Post Draw | [Отладка и тесты](../systems/debug-and-testing.md) |
| `obj_sound_test` | — | нет | `spr_save` | Create, Draw GUI, Step | [Отладка и тесты](../systems/debug-and-testing.md) |
| `screenshot` | — | да | — | Create, Step, Draw GUI, CleanUp | [Отладка и тесты](../systems/debug-and-testing.md) |

## См. также

- [Справочник GML-скриптов](gml-scripts.md): функции проекта
- [Иерархия объектов](../architecture/object-hierarchy.md): роль `par_*` родителей
- [Инициализация](../architecture/initialization.md): `obj_Init` и стартовая последовательность

<!-- sources: _meta/objects.txt; objects/*/*.yy; docs_new/_meta/nav_plan.md -->
