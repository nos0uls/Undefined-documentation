# Система Музыки (Music Engine)

Централизованная система управления музыкой с time-based фейдами, поддержкой intro+loop, pitch control, cutscene-командами и debug overlay.

---

## Архитектура

```
obj_Init.Create_0
  ├─ scr_music_init()              ← глобалы + все API функции
  ├─ instance_create(obj_music_ctrl) ← persistent контроллер
  └─ instance_create(obj_globalManager)

obj_music_ctrl.Step_0 (каждый кадр)
  ├─ scr_global_music_update_current()  ← time-based fade + intro→loop
  └─ scr_global_music_fade_previous()   ← fade-out предыдущего трека

obj_music_ctrl.Draw_64
  └─ debug overlay (только при global.debug)
```

### Ключевые файлы

| Файл | Назначение | Папка в Asset Browser |
|------|------------|----------------------|
| `scr_music_init` | Глобалы и все API функции | Системы / Sounds \| Music |
| `scr_global_music_update_current` | Fade-in текущего + intro→loop | Системы / Sounds \| Music |
| `scr_global_music_fade_previous` | Fade-out предыдущего трека | Системы / Sounds \| Music |
| `scr_cutscene_music` | Cutscene action классы и обёртки | Системы / Sounds \| Music |
| `scr_SFXPlay` | Воспроизведение SFX | Системы / Sounds \| Music |
| `scr_menu_volume_guard` | Auto-duck громкости в меню | Системы / Sounds \| Music |
| `obj_music_ctrl` | Persistent контроллер (Step + Draw GUI) | N0souls_music |

---

## Глобальные переменные

| Переменная | Тип | Описание |
|-----------|-----|---------|
| `global.music_current` | sound/noone | Asset текущего трека |
| `global.music_instance` | real | Playing instance |
| `global.music_volume` | real (0..1) | Текущая громкость |
| `global.music_volume_target` | real (0..1) | Целевая громкость |
| `global.music_pitch` | real | Текущий pitch (1.0 = норма) |
| `global.music_fade_duration` | real | Длительность фейда (сек) |
| `global.music_fade_timer` | real | Оставшееся время фейда |
| `global.music_fade_from` | real | Начальная громкость фейда |
| `global.music_prev_instance` | real | Instance предыдущего трека |
| `global.music_intro_instance` | real | Instance intro-трека |
| `global.music_loop_asset` | sound/noone | Asset loop-трека |
| `global.music_paused` | bool | Пауза |
| `global.music_default_fade` | real | Дефолтный фейд (0.5 сек) |
| `global.music_default_game_track` | sound | Трек по умолчанию для игровых комнат |
| `global.room_music_override` | ds_map | room_id → sound для комнат с особой музыкой |
| `global.music_duck_multiplier` | real (0..1) | Текущий множитель приглушения (1.0 = без duck) |
| `global.music_duck_target` | real (0..1) | Целевой множитель duck |
| `global.music_layered_mode` | bool | true = играют два трека (Layer 2) |
| `global.music_layer2_instance` | real | Instance второго слоя (battle) |
| `global.music_layer2_asset` | sound/noone | Asset второго слоя |
| `global.music_layer_intensity` | real (0..1) | Текущая интенсивность (0=calm, 1=battle) |
| `global.music_layer_intensity_target` | real (0..1) | Целевая интенсивность |

---

## API Reference

### Основные функции

#### `global.play_music(snd_asset)`
Плавная смена трека с дефолтным фейдом (`global.music_default_fade`).
Если уже играет этот трек — ничего не делает.

```gml
global.play_music(music_SchoolRoutine);
```

#### `global.play_music_fade(snd_asset, fade_sec)`
Плавная смена трека с явным временем кроссфейда.

```gml
global.play_music_fade(music_boss, 2.0); // 2 секунды кроссфейд
```

#### `global.play_music_immediate(snd_asset)`
Мгновенная смена без фейда. Старый трек останавливается сразу.

```gml
global.play_music_immediate(music_battle);
```

#### `global.stop_music(fade_sec)`
Остановка с опциональным затуханием. `0` = мгновенно.

```gml
global.stop_music(1.0); // затухает 1 секунду, потом останавливается
```

#### `global.set_music_pitch(pitch)`
Установка pitch текущего трека. `1.0` = нормальный.

```gml
global.set_music_pitch(0.8); // замедление
```

#### `global.set_music_volume_fade(vol, fade_sec)`
Плавное изменение громкости (не меняет трек).

```gml
global.set_music_volume_fade(0.3, 0.5); // тише за 0.5 секунды
```

#### `global.play_music_intro_loop(intro_asset, loop_asset, fade_sec)`
Играет intro один раз, затем автоматически переключается на loop.

```gml
global.play_music_intro_loop(music_boss_intro, music_boss_loop, 0.5);
```

#### `global.duck_music(multiplier, fade_sec)`
Относительное приглушение: финальная громкость = `settings_vol * multiplier`.
Не ставит абсолютное значение — всегда умножает на громкость из настроек.

```gml
global.duck_music(0.3, 0.5); // приглушить до 30% от текущей за 0.5 сек
```

#### `global.unduck_music(fade_sec)`
Снять приглушение (duck → 1.0).

```gml
global.unduck_music(0.3); // вернуть полную громкость за 0.3 сек
```

!!! tip "Когда использовать duck vs set_music_volume_fade"
    - **`duck_music`** — относительное приглушение (уважает настройки игрока). Идеально для катсцен, диалогов, меню.
    - **`set_music_volume_fade`** — абсолютная громкость. Использовать только когда нужно именно конкретное значение.

#### `global.pause_music()` / `global.resume_music()`
Пауза и снятие с паузы. Также ставит на паузу prev_instance при кроссфейде и layer2_instance.

---

### Layer 2 API — два трека одновременно

#### `global.play_music_layered(calm_asset, battle_asset, fade_sec)`
Запускает два трека синхронно: calm (спокойная версия) + battle (боевая версия).
По умолчанию интенсивность = 0 (слышно только calm).

```gml
global.play_music_layered(music_explore_calm, music_explore_battle, 1.0);
```

#### `global.set_music_layer_intensity(intensity, fade_sec)`
Меняет соотношение calm/battle слоёв.
- `intensity = 0` → только calm (battle на громкости 0)
- `intensity = 1` → только battle (calm на громкости 0)
- `intensity = 0.5` → оба на 50%

```gml
global.set_music_layer_intensity(1.0, 2.0); // переход к battle за 2 сек
global.set_music_layer_intensity(0, 1.5);   // возврат к calm за 1.5 сек
```

Формула громкости:
- `calm_volume = base_volume × (1 - intensity)`
- `battle_volume = base_volume × intensity`

#### `global.stop_layered_music(fade_sec)`
Останавливает оба слоя с фейдом.

```gml
global.stop_layered_music(2.0);
```

!!! tip "Когда использовать Layer 2"
    - **Исследование vs Бой**: один трек, две версии (спокойная + напряжённая)
    - **Динамический саундтрек**: плавный переход между настроениями без перебивания
    - **НЕ для**: разных треков (используйте обычный `play_music` с кроссфейдом)

---

## Room-to-Track Mapping

### Как работает

1. **Меню-комнаты** (из `global.__service_menu_rooms`) → всегда `music_menu`
2. **Override** (из `global.room_music_override`) → если комната есть в таблице, используется её трек
3. **По умолчанию** → `global.music_default_game_track` (сейчас `music_SchoolRoutine`)

### Как добавить музыку в комнату

В `scr_music_init()` найдите секцию `Room-to-Track mapping` и добавьте:

```gml
ds_map_add(global.room_music_override, rm_boss_room, music_boss_theme);
```

Чтобы сменить дефолтный трек для всех игровых комнат:

```gml
global.music_default_game_track = music_new_default;
```

---

## Cutscene-команды

Для управления музыкой из катсцен доступны wrapper-функции, возвращающие `CutsceneAction`:

| Функция | Описание |
|---------|---------|
| `cutscene_music_play(snd, fade)` | Смена трека с фейдом (default 0.5) |
| `cutscene_music_stop(fade)` | Остановка (default 1.0) |
| `cutscene_music_volume(vol, fade)` | Изменение громкости |
| `cutscene_music_pitch(pitch)` | Изменение pitch |
| `cutscene_music_pause()` | Пауза |
| `cutscene_music_resume()` | Снять паузу |
| `cutscene_music_intro_loop(intro, loop, fade)` | Intro + Loop |
| `cutscene_music_duck(multiplier, fade)` | Относительное приглушение (default 0.3) |
| `cutscene_music_unduck(fade)` | Снять приглушение (default 0.3) |
| `cutscene_music_layered(calm, battle, fade)` | Запустить Layer 2 (два трека) (default 0.5) |
| `cutscene_music_intensity(intensity, fade)` | Изменить интенсивность слоёв (default 1.0) |

### Пример использования в катсцене

```gml
cutscene_add(manager, cutscene_music_play(music_dramatic, 1.0));
cutscene_add(manager, cutscene_dialogue("story.yarn", "dramatic_scene"));
cutscene_add(manager, cutscene_music_stop(2.0));
```

---

## Debug Overlay

При включённом `global.debug` (активация: F12 × 5) в левом нижнем углу отображается панель:

- **Track** — имя текущего звукового ресурса
- **Vol** — текущая → целевая громкость + прогресс фейда
- **Pitch** — текущий pitch (жёлтый если ≠ 1.0)
- **Instance** — ID instance и статус [playing/stopped]
- **Intro→Loop** — статус intro+loop перехода
- **Duck** — текущий и целевой множитель приглушения (голубой если < 1.0)
- **Layer 2** — статус режима двух треков (зелёный если активен)
- **Battle** — имя второго трека (только в Layer 2 режиме)
- **Intensity** — текущая интенсивность слоёв (цвет: зелёный=calm, красный=battle)
- **Prev** — instance предыдущего трека (оранжевый при кроссфейде)
- **PAUSED** — красный индикатор паузы

**Клавиши отладки:**
- F12 × 5 — включить/выключить debug mode
- F9 — toggle music overlay (требуется debug mode)

---

## Гайд для композитора

### Форматы
- **OGG Vorbis** — рекомендуемый формат для GameMaker (streaming)

### Нейминг
- `music_<location>` — напр. `music_school`, `music_menu`
- `music_<name>_intro` + `music_<name>_loop` — для intro+loop

### Требования к loop-файлам
- Loop-файл должен быть **шовным** (seamless): начало = конец по фазе
- Intro и loop должны быть **на одном BPM и в одной тональности**

### Добавление нового трека
1. Импортировать OGG в GameMaker (Sound asset)
2. Добавить override в `scr_music_init()` если нужна привязка к комнате
3. Или использовать `global.play_music()` / cutscene-команду напрямую
