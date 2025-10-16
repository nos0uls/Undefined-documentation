# Архитектура проекта

## Структура объектов

obj_parent
├── obj_player
├── obj_enemy_parent
│ ├── obj_enemy_basic
│ └── obj_enemy_boss
└── obj_collectible


## Основные скрипты

- `scr_player_movement` — движение игрока
- `scr_camera_follow` — камера
- `scr_enemy_ai` — ИИ врагов
```markdown
# Архитектура проекта

Обзор структуры и организации проекта игры в GameMaker Studio 2.

## 📁 Структура проекта

### Общая организация

MyGame.yyp
├── 📂 Sprites/
│ ├── 🎨 Player/
│ │ ├── spr_player_idle
│ │ ├── spr_player_walk
│ │ └── spr_player_jump
│ ├── 🎨 Enemies/
│ │ ├── spr_enemy_basic
│ │ └── spr_enemy_boss
│ └── 🎨 Environment/
│ ├── spr_wall
│ ├── spr_platform
│ └── spr_background
├── 📂 Objects/
│ ├── 🎮 Player/
│ │ └── obj_player
│ ├── 👾 Enemies/
│ │ ├── obj_enemy_parent
│ │ ├── obj_enemy_basic
│ │ └── obj_enemy_boss
│ ├── 🌍 Environment/
│ │ ├── obj_wall
│ │ ├── obj_platform
│ │ └── obj_collectible
│ └── 🎯 System/
│ ├── obj_game_manager
│ ├── obj_camera
│ └── obj_ui_manager
├── 📂 Scripts/
│ ├── 🎮 Player/
│ │ ├── scr_player_movement
│ │ ├── scr_player_collision
│ │ └── scr_player_animations
│ ├── 🧠 AI/
│ │ ├── scr_enemy_ai_basic
│ │ └── scr_pathfinding
│ ├── 🔧 Utilities/
│ │ ├── scr_camera_follow
│ │ ├── scr_audio_manager
│ │ └── scr_save_load
│ └── 📊 Game Logic/
│ ├── scr_level_manager
│ ├── scr_score_system
│ └── scr_collision_manager
├── 📂 Rooms/
│ ├── rm_menu
│ ├── rm_level_01
│ ├── rm_level_02
│ └── rm_game_over
├── 📂 Sounds/
│ ├── 🎵 Music/
│ │ ├── mus_menu
│ │ ├── mus_level
│ │ └── mus_boss
│ └── 🔊 SFX/
│ ├── snd_jump
│ ├── snd_collect
│ └── snd_enemy_hit
└── 📂 Fonts/
├── fnt_ui_large
└── fnt_ui_small

text

## 🏗️ Системная архитектура

### Иерархия объектов

```mermaid
graph TD
    A[obj_parent] --> B[obj_living_entity]
    B --> C[obj_player]
    B --> D[obj_enemy_parent]
    D --> E[obj_enemy_basic]
    D --> F[obj_enemy_boss]
    
    A --> G[obj_static_entity]
    G --> H[obj_wall]
    G --> I[obj_platform]
    G --> J[obj_collectible]
    
    A --> K[obj_system]
    K --> L[obj_game_manager]
    K --> M[obj_camera]
    K --> N[obj_ui_manager]
Менеджер игры
obj_game_manager — центральный объект, контролирующий:

text
// Создание (Create Event)
global.score = 0;
global.lives = 3;
global.current_level = 1;
global.game_state = "playing"; // "playing", "paused", "game_over"

// Пошаговое выполнение (Step Event)
switch(global.game_state) {
    case "playing":
        scr_update_game_logic();
        break;
        
    case "paused":
        // Обновление только UI
        scr_update_pause_menu();
        break;
        
    case "game_over":
        scr_update_game_over_screen();
        break;
}

// Функция управления состоянием
function scr_set_game_state(_new_state) {
    global.game_state = _new_state;
    
    switch(_new_state) {
        case "paused":
            instance_deactivate_all(true);
            instance_activate_object(obj_ui_manager);
            break;
            
        case "playing":
            instance_activate_all();
            break;
    }
}
🎮 Система игрока
obj_player — основной объект игрока
Переменные инициализации:

text
// Create Event
hspd = 0;           // Горизонтальная скорость
vspd = 0;           // Вертикальная скорость
move_speed = 4;     // Скорость движения
jump_speed = 12;    // Сила прыжка
gravity_force = 0.8;// Гравитация
on_ground = false;  // На земле ли игрок

max_health = 100;
current_health = max_health;
invincible = false;
invincible_timer = 0;

// Анимации
current_animation = "idle";
animation_speed = 0.2;
Основной цикл (Step Event):

text
// Обработка ввода и движения
scr_player_input();
scr_player_movement();
scr_player_collision();
scr_player_animations();

// Обработка неуязвимости
if (invincible) {
    invincible_timer--;
    if (invincible_timer <= 0) {
        invincible = false;
        image_alpha = 1;
    } else {
        image_alpha = 0.5;
    }
}
👾 Система ИИ врагов
obj_enemy_parent — базовый класс врагов
text
// Create Event
enemy_health = 50;
enemy_speed = 2;
damage = 10;
facing = choose(-1, 1);
patrol_distance = 128;
start_x = x;

// Состояния ИИ
ai_state = "patrol"; // "patrol", "chase", "attack", "stunned"
detection_range = 200;
attack_range = 32;

// Таймеры
attack_cooldown = 0;
stun_timer = 0;
Машина состояний:

text
// Step Event
switch(ai_state) {
    case "patrol":
        scr_enemy_patrol();
        scr_check_player_detection();
        break;
        
    case "chase":
        scr_enemy_chase_player();
        scr_check_attack_range();
        break;
        
    case "attack":
        scr_enemy_attack();
        break;
        
    case "stunned":
        scr_enemy_stunned();
        break;
}

scr_enemy_update_timers();
📺 Система камеры
obj_camera — управление видом
text
// Create Event
follow_target = obj_player;
camera_smooth = 0.1;
camera_offset_x = 0;
camera_offset_y = -32;

// Границы камеры
camera_min_x = 0;
camera_min_y = 0;
camera_max_x = room_width - camera_get_view_width(view_camera);
camera_max_y = room_height - camera_get_view_height(view_camera);

// Step Event
if (instance_exists(follow_target)) {
    scr_camera_follow(follow_target);
    scr_camera_shake(); // Если включен эффект тряски
}
🎵 Аудио система
Структура звуков
text
// В obj_game_manager Create Event
global.music_volume = 0.7;
global.sound_volume = 0.8;
global.current_music = -1;

// Массивы звуков по категориям
global.ui_sounds = [snd_button_click, snd_menu_select];
global.player_sounds = [snd_jump, snd_land, snd_hurt];
global.enemy_sounds = [snd_enemy_hurt, snd_enemy_death];
global.environment_sounds = [snd_collect_item, snd_door_open];
💾 Система сохранений
Структура данных
text
// Глобальные переменные для сохранения
global.save_data = {
    // Прогресс игры
    current_level: 1,
    unlocked_levels: ,
    total_score: 0,
    best_times: array_create(10, -1),
    
    // Настройки
    music_volume: 0.7,
    sound_volume: 0.8,
    fullscreen: false,
    controls: {
        left: vk_left,
        right: vk_right,
        jump: vk_space,
        action: ord("Z")
    },
    
    // Достижения
    achievements: {},
    
    // Статистика
    total_playtime: 0,
    deaths_count: 0,
    items_collected: 0
};
🔄 Система событий
Менеджер событий
text
// В obj_game_manager
global.event_listeners = ds_map_create();

/// @function scr_register_event_listener(_event_name, _object_id, _callback)
function scr_register_event_listener(_event_name, _object_id, _callback) {
    if (!ds_map_exists(global.event_listeners, _event_name)) {
        ds_map_add(global.event_listeners, _event_name, ds_list_create());
    }
    
    var _listeners = global.event_listeners[? _event_name];
    ds_list_add(_listeners, {object_id: _object_id, callback: _callback});
}

/// @function scr_trigger_event(_event_name, _data)
function scr_trigger_event(_event_name, _data = undefined) {
    if (ds_map_exists(global.event_listeners, _event_name)) {
        var _listeners = global.event_listeners[? _event_name];
        
        for (var i = 0; i < ds_list_size(_listeners); i++) {
            var _listener = _listeners[| i];
            if (instance_exists(_listener.object_id)) {
                script_execute(_listener.callback, _data);
            }
        }
    }
}
Примеры событий
text
// Регистрация событий
scr_register_event_listener("player_died", obj_ui_manager, scr_ui_show_death_screen);
scr_register_event_listener("level_complete", obj_game_manager, scr_load_next_level);
scr_register_event_listener("item_collected", obj_score_manager, scr_add_score);

// Вызов события
scr_trigger_event("player_died", {cause: "fall", position: {x: x, y: y}});
🏠 Система комнат
Соглашения по именованию
rm_menu — главное меню

rm_level_XX — игровые уровни (01, 02, 03...)

rm_boss_XX — боссы

rm_cutscene_XX — кат-сцены

rm_shop — магазин/улучшения

Переходы между комнатами
text
/// @function scr_change_room(_room, _transition_type)
function scr_change_room(_room, _transition_type = "fade") {
    global.next_room = _room;
    global.transition_type = _transition_type;
    
    with (obj_transition_manager) {
        scr_start_transition();
    }
}
🧪 Система отладки
Отладочная информация
text
// В obj_debug_manager (только в Debug режиме)
#macro DEBUG true

if (DEBUG) {
    draw_set_color(c_white);
    draw_text(10, 10, "FPS: " + string(fps));
    draw_text(10, 30, "Player: (" + string(obj_player.x) + ", " + string(obj_player.y) + ")");
    draw_text(10, 50, "State: " + global.game_state);
    draw_text(10, 70, "Instances: " + string(instance_count));
}
📈 Оптимизация
Принципы оптимизации
Управление объектами

Используйте object pooling для часто создаваемых объектов

Деактивируйте объекты вне экрана

Удаляйте ненужные объекты

Графическая оптимизация

Используйте texture pages эффективно

Минимизируйте draw calls

Используйте поверхности для сложных эффектов

Алгоритмическая оптимизация

Кэшируйте дорогие вычисления

Используйте пространственное разбиение для коллизий

Оптимизируйте циклы

!!! tip "💡 Лучшие практики архитектуры"
- Используйте наследование объектов для общей функциональности
- Разделяйте логику на небольшие, переиспользуемые скрипты
- Документируйте все публичные функции
- Используйте константы для магических чисел
- Планируйте архитектуру заранее, особенно для больших проектов

!!! warning "⚠️ Частые проблемы"
- Циклические зависимости между объектами
- Слишком много логики в событиях Step
- Отсутствие проверок существования объектов
- Глобальные переменные везде вместо инкапсуляции
