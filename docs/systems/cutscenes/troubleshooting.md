---
tags:
  - cutscenes
---

# Катсцены: Типовые проблемы

## Камера не двигается
**Причина**: Активирован `global.cutscene_camera_override`, блокирующий следование за игроком.
**Решение**: Добавьте экшен камеры `cutscene_camera_track` или `c_panobj`.

## Катсцена зависла
**Причина**: Один из экшенов не возвращает `true` в `update()`.
**Решение**: Проверьте Debug Overlay. Если счетчик `Wait` красный — этот шаг блокирует очередь. Часто это связано с ожиданием диалога, который не был запущен или завершен.

## Актёр не найден
**Причина**: Ошибка в строковом ключе `actor_map` или актёр еще не создан.
**Решение**: Используйте **instance id** вместо имен для критически важных действий. Проверьте логи на наличие предупреждений `resolve_target`.

## `cutscene_wait` работает слишком быстро/медленно
**Причина**: Путаница между секундами и кадрами.
**Решение**: Все GML-функции `wait` принимают время в **кадрах**. В JSON-файлах время указывается в **секундах**.

---

## См. также

- [Обзор катсцен](overview.md) — `obj_cutsceneManager`, `action_queue`, `global.cutscene_camera_override`
- [Архитектура](architecture.md) — `actor_map`, `resolve_target`, жизненный цикл
- [Актёры](actors.md) — `cutscene_actor_create`, `ActionActorCreate`
- [Камера](camera.md) — `cutscene_camera_pan`, `cutscene_camera_track`
- [API](api.md) — `cutscene_add`, Action-классы
- [Игрок в катсцене](player_in_cutscene.md) — блокировка движения, camera override