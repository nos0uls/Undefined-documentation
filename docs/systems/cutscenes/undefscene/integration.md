# Undefscene: Интеграция с проектом

## Открытие проекта

В правой панели в блоке `Project Integration` нажмите **Open Project** и выберите файл `.yyp` проекта Undefinedtale-888.

После успешной загрузки редактор просканирует ресурсы игры, Yarn-файлы и настройки движка.
Если тот же `.yyp` уже открывался раньше, редактор может восстановить ресурсы из cache между сессиями и автоматически вернуть последний проект при старте приложения.

## Что даёт интеграция

- **Автокомплит** для объектов, спрайтов, звуков, комнат и других ресурсов.
- **Чтение настроек движка** из `datafiles/cutscene_engine_settings.json`.
- **Поддержка Yarn** через сканирование `.yarn` файлов в `datafiles`.
- **Yarn Preview** для dialogue-нод.

## Оптимизация загрузки проекта

Для ускорения открытия крупных GameMaker-проектов основная часть чтения ресурсов оптимизирована.

Сейчас параллельно выполняются:

- чтение `.yy` ресурсов из `.yyp`
- рекурсивный поиск `.yarn` файлов
- чтение и разбор содержимого `.yarn`

Дополнительно редактор хранит persistent cache в `userData`:

- сериализованный список ресурсов из `.yyp`
- метаданные последнего открытого проекта
- отдельную папку `room-screenshots` для `Visual Editing` и stitched room preview сценариев

Это снижает время ожидания при открытии больших проектов по сравнению с последовательным чтением.

Когда открывается `Visual Editing`, editor ищет room screenshots сначала в этой cache-папке проекта, а затем в fallback-папке `<projectDir>/screenshots`.

Это позволяет использовать как project-specific cache workflow, так и внешний screenshot runner, который пишет output рядом с самим GameMaker project.

Дополнительно editor умеет искать screenshots в `%LOCALAPPDATA%/<project>/screenshots`, что удобно для GameMaker runner flow, завязанного на `working_directory`.

Если и этого недостаточно, пользователь может явно выбрать custom screenshot folder через `Help > Advanced` или `Preferences`.

## Что важно помнить

- Раннее чтение некоторых настроек приложения остаётся синхронным там, где это нужно для старта Electron-процесса.
- Не все панели нужны в обычной работе: часть технических инструментов вынесена в `Help > Advanced`.
- Cache используется как ускорение и foundation для preview workflow, но при изменении самого `.yyp` редактор делает cold refresh и пересобирает данные.
- Текущий путь cache-папки для screenshots и фактические `Search Dirs` можно увидеть в `Project` panel и в окне `Visual Editing`.

---

## См. также

- [Обзор Undefscene](overview.md) — поддерживаемые ноды, запуск
- [Базовый workflow](workflow.md) — пошаговый процесс работы
- [Интерфейс и Preferences](ui.md) — `Project` panel, `Visual Editing`, `Help > Advanced`
- [Room Screenshot Pipeline](room-screenshot-pipeline.md) — `room-screenshots`, `Search Dirs`
- [Форматы, импорт и экспорт](formats.md) — engine `.json`, `datafiles`
