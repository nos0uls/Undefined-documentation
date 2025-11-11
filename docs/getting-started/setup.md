Файл: objects/textboxTest_scribble/Draw_64.gml
1) Общие ширины wrap для 1/2/3 и массив для 4 опций:
Draw_64.gmlLines 118-138
        var __col_wrap = 0;        var __col_wrap_4 = [0, 0, 0, 0]; // Кастомные wrap для 4 опций: [левая, правая, нижняя, верхняя]        if (option_count == 1) {            __col_wrap = inner_width * 0.8;        } else if (option_count == 2) {            __col_wrap = inner_width * 0.36;        } else if (option_count == 3) {            __col_wrap = inner_width * 0.28;        } else if (option_count == 4) {            __col_wrap_4[0] = inner_width * 0.18;            __col_wrap_4[1] = inner_width * 0.18;            __col_wrap_4[2] = inner_width * 0.18;            __col_wrap_4[3] = inner_width * 0.18;        }
2) Центры для 2 опций (левая/правая колонки):
Draw_64.gmlLines 231-251
        } else if (option_count == 2) {            var __x2a = inner_left + inner_width * 0.25;            var __x2b = inner_left + inner_width * 0.75;            // левая            ...            // правая            ...
3) Центры для 3 опций:
Draw_64.gmlLines 254-266
        } else if (option_count == 3) {            for (var i = 0; i < option_count; i++) {                var pos = 0.0;                if (i == 0) { pos = 0.17; }                else if (i == 1) { pos = 0.50; }                else if (i == 2) { pos = 0.83; }                var __xi = inner_left + inner_width * pos;
4) Позиции для 4 опций (ромб) — смещения и отрисовка:
Draw_64.gmlLines 88-98
        var option_spacing_4_x = [0, 0]; // [левая, правая]        var option_spacing_4_y = [0, 0]; // [нижняя, верхняя]        if (option_count == 4) {            option_spacing_4_x[0] = inner_width * 0.25; // левая            option_spacing_4_x[1] = inner_width * 0.75; // правая            option_spacing_4_y[0] = 60; // вниз            option_spacing_4_y[1] = 60; // вверх        }
Draw_64.gmlLines 275-285
        } else if (option_count == 4) {            for (var i = 0; i < option_count; i++) {                var draw_x = 0;                var draw_y = option_base_y;                switch (i) {                    case 0: draw_x = inner_left + option_spacing_4_x[0]; draw_y = option_base_y; break; // левый                    case 1: draw_x = inner_left + option_spacing_4_x[1]; draw_y = option_base_y; break; // правый                    case 2: draw_x = inner_left + inner_width * 0.50; draw_y = option_base_y + option_spacing_4_y[0]; break; // низ                    case 3: draw_x = inner_left + inner_width * 0.50; draw_y = option_base_y - option_spacing_4_y[1]; break; // верх                }
Кратко:
2 опции: центры 0.25 и 0.75 ширины; wrap = inner_width0.36.
3 опции: центры 0.17, 0.50, 0.83; wrap = inner_width0.28.
4 опции: ромб через option_spacing_4_x/y; wrap по каждой через __col_wrap_4[i]
