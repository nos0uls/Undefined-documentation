```markdown
# GML Скрипты

Справочник основных скриптов и функций, используемых в игре.

## 🎮 Скрипты игрока

### scr_player_movement

Управляет движением игрока с учетом коллизий.

```gml
/// @function scr_player_movement()
/// @description Обработка движения игрока

function scr_player_movement() {
    // Получение ввода
    var _left = keyboard_check(vk_left) || keyboard_check(ord("A"));
    var _right = keyboard_check(vk_right) || keyboard_check(ord("D"));
    var _jump = keyboard_check_pressed(vk_space);
    
    // Горизонтальное движение
    var _move = _right - _left;
    hspd = _move * move_speed;
    
    // Прыжок
    if (_jump && on_ground) {
        vspd = -jump_speed;
        on_ground = false;
    }
    
    // Применение гравитации
    if (!on_ground) {
        vspd += gravity_force;
    }
    
    // Ограничение скорости падения
    vspd = clamp(vspd, -max_fall_speed, max_fall_speed);
}
Переменные:

hspd — горизонтальная скорость

vspd — вертикальная скорость

move_speed — скорость движения (обычно 4-6)

jump_speed — сила прыжка (обычно 12-15)

gravity_force — сила гравитации (обычно 0.5-1)

scr_player_collision
Проверяет коллизии игрока с окружением.

text
/// @function scr_player_collision()
/// @description Обработка коллизий игрока

function scr_player_collision() {
    // Горизонтальная коллизия
    if (place_meeting(x + hspd, y, obj_wall)) {
        while (!place_meeting(x + sign(hspd), y, obj_wall)) {
            x += sign(hspd);
        }
        hspd = 0;
    }
    x += hspd;
    
    // Вертикальная коллизия
    if (place_meeting(x, y + vspd, obj_wall)) {
        while (!place_meeting(x, y + sign(vspd), obj_wall)) {
            y += sign(vspd);
        }
        
        // Проверка приземления
        if (vspd > 0) {
            on_ground = true;
        }
        
        vspd = 0;
    }
    y += vspd;
}
🎯 Скрипты врагов
scr_enemy_ai_basic
Базовый ИИ для простых врагов.

text
/// @function scr_enemy_ai_basic()
/// @description Простой ИИ врага - движение туда-сюда

function scr_enemy_ai_basic() {
    // Проверка стены или края платформы
    var _wall_ahead = place_meeting(x + (enemy_speed * facing), y, obj_wall);
    var _edge_ahead = !place_meeting(x + (enemy_speed * facing), y + 1, obj_wall);
    
    // Поворот при препятствии
    if (_wall_ahead || _edge_ahead) {
        facing *= -1;
        image_xscale = facing;
    }
    
    // Движение
    x += enemy_speed * facing;
    
    // Проверка столкновения с игроком
    if (place_meeting(x, y, obj_player)) {
        with (obj_player) {
            scr_player_take_damage(other.damage);
        }
    }
}
🔧 Утилиты
scr_camera_follow
Следование камеры за игроком с плавностью.

text
/// @function scr_camera_follow(_target)
/// @description Плавное следование камеры за целью
/// @param {instance} _target Объект, за которым следует камера

function scr_camera_follow(_target) {
    if (!instance_exists(_target)) return;
    
    // Получение размеров камеры
    var _cam_width = camera_get_view_width(view_camera);
    var _cam_height = camera_get_view_height(view_camera);
    
    // Целевая позиция камеры
    var _target_x = _target.x - _cam_width / 2;
    var _target_y = _target.y - _cam_height / 2;
    
    // Текущая позиция камеры
    var _current_x = camera_get_view_x(view_camera);
    var _current_y = camera_get_view_y(view_camera);
    
    // Плавное движение камеры
    var _new_x = lerp(_current_x, _target_x, camera_smooth);
    var _new_y = lerp(_current_y, _target_y, camera_smooth);
    
    // Ограничения камеры границами комнаты
    _new_x = clamp(_new_x, 0, room_width - _cam_width);
    _new_y = clamp(_new_y, 0, room_height - _cam_height);
    
    // Применение позиции
    camera_set_view_pos(view_camera, _new_x, _new_y);
}
🔊 Аудио скрипты
scr_audio_manager
Управление звуками и музыкой.

text
/// @function scr_play_sound(_sound, _pitch, _gain)
/// @description Проигрывание звука с настройками
/// @param {sound} _sound Звуковой ресурс
/// @param {real} _pitch Высота звука (1.0 = нормально)
/// @param {real} _gain Громкость (0.0-1.0)

function scr_play_sound(_sound, _pitch = 1.0, _gain = 1.0) {
    if (!audio_exists(_sound)) return -1;
    
    var _sound_id = audio_play_sound(_sound, 1, false);
    audio_sound_pitch(_sound_id, _pitch);
    audio_sound_gain(_sound_id, _gain * global.sound_volume, 0);
    
    return _sound_id;
}

/// @function scr_play_music(_music, _loop)
/// @description Проигрывание фоновой музыки
/// @param {sound} _music Музыкальный трек
/// @param {bool} _loop Зациклить ли музыку

function scr_play_music(_music, _loop = true) {
    // Остановка текущей музыки
    if (global.current_music != -1) {
        audio_stop_sound(global.current_music);
    }
    
    // Запуск новой музыки
    global.current_music = audio_play_sound(_music, 2, _loop);
    audio_sound_gain(global.current_music, global.music_volume, 0);
}
💾 Скрипты сохранения
scr_save_game
Сохранение игрового прогресса.

text
/// @function scr_save_game()
/// @description Сохранение текущего состояния игры

function scr_save_game() {
    var _save_data = {
        level: global.current_level,
        score: global.score,
        lives: global.lives,
        items_collected: global.items_collected,
        unlocked_levels: global.unlocked_levels,
        settings: {
            music_volume: global.music_volume,
            sound_volume: global.sound_volume,
            fullscreen: global.fullscreen
        }
    };
    
    var _json_string = json_stringify(_save_data);
    
    try {
        var _file = file_text_open_write("savegame.save");
        file_text_write_string(_file, _json_string);
        file_text_close(_file);
        
        show_debug_message("Игра сохранена успешно");
        return true;
    } catch(_error) {
        show_debug_message("Ошибка сохранения: " + string(_error));
        return false;
    }
}
📖 Соглашения по коду
Именование
Скрипты: scr_название_функции

Объекты: obj_название_объекта

Спрайты: spr_название_спрайта

Звуки: snd_название_звука

Переменные: snake_case для обычных, UPPER_CASE для констант

Комментарии
text
/// @function имя_функции(параметры)
/// @description Описание функции
/// @param {тип} имя_параметра Описание параметра
/// @return {тип} Описание возвращаемого значения
Константы
text
#macro PLAYER_SPEED 4
#macro JUMP_HEIGHT 15
#macro GRAVITY 0.8
#macro MAX_HEALTH 100
!!! tip "💡 Лучшие практики GML"
- Используйте functions вместо scripts для лучшей производительности
- Группируйте связанные функции в одном скрипте
- Документируйте сложные алгоритмы
- Используйте осмысленные имена переменных

!!! warning "⚠️ Частые ошибки"
- Забывание объявления локальных переменных (var)
- Неправильное использование with конструкций
- Отсутствие проверки существования объектов перед обращением

🔗 Дополнительные ресурсы
Объекты и события — справочник событий GameMaker

Архитектура — структура проекта

GameMaker Manual — официальная документация