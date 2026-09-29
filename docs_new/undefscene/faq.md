---
title: "Undefscene: Частые вопросы и проблемы"
tags:
  - undefscene
  - editor
  - faq
  - troubleshooting
---

# Undefscene: Частые вопросы и проблемы

## Актёр не двигается

Проверьте:

- У Move / Follow Path ноды заполнен **Target**? Он должен совпадать с ключом из Actor Create
- Скорость > 0? Speed = 0 означает «стоять на месте»
- Актёр не застрял в стене? Попробуйте выключить `collision` (установить `false`)

## Камера застряла на месте

- Добавьте ноду камеры (Camera Pan, Camera Track и т.д.) — без неё камера остаётся там, где была до катсцены
- Camera Track Until Stop завершается сам, когда отслеживаемый актёр останавливается. Камера при этом держит последнюю позицию — вернуть её можно нодой Camera Center или Tween Camera с возвратом к дефолту

## Диалог не запускается

- Проверьте, что в Dialogue ноде выбран **File** и **Node**
- Файл `.yarn` должен быть в папке `datafiles/Dialogues/` проекта
- Проверьте текст диалога через **Yarn Preview** в панели Text

## Катсцена зависла

- Проверьте, что все ветки графа заканчиваются нодой **End**
- Нода **Halt** блокирует выполнение — не ставьте после неё другие ноды
- Нода **GoTo Node** может создать бесконечный цикл — проверьте, что у цикла есть условие выхода
- Если после Dialogue катсцена не идёт дальше — возможно, диалог не завершился корректно

## Предупреждения в логах, но экспорт работает

Предупреждения (warn) не блокируют экспорт, но лучше их исправить:

- Пустые поля → заполните обязательные параметры
- Имена ресурсов → проверьте, что объект/спрайт существует в проекте
- Изолированные ноды → соедините с графом или удалите

## Чем Save отличается от Export?

- **Save** — сохраняет рабочую сцену (`.usc.json`) для продолжения работы в редакторе
- **Export to Game** (меню File) — создаёт файл для игры (`.json`), который кладётся в `datafiles/`

## Можно ли открыть экспортированный `.json` обратно?

Да. Редактор поддерживает обратный импорт: **Open Scene** → выберите engine `.json`. Граф восстановится из массива действий.

## Почему gridSize не меняет расстояние между нодами?

GridSize влияет только на **визуальную сетку** фона. Расстояние между новыми нодами от него не зависит.

## Где найти логи для баг-репорта?

**Help → Copy Log to Clipboard** — лог копируется в буфер обмена. Или найдите файл `undefscene.log` в папке данных приложения.

## Горячие клавиши не работают на русской раскладке

Сочетания клавиш работают независимо от текущего языка ввода. Если сочетание не срабатывает, проверьте привязку в **File → Preferences → Keyboard Shortcuts** и обновите редактор до последней версии. Если проблема остаётся — напишите баг-репорт.

## Как включить автообновление?

Автопроверка обновлений работает сама в packaged-версии редактора. При появлении новой версии вверху окна показывается полоса уведомления: после автоматического скачивания в ней появляется кнопка **Restart & Update**. Для portable-версии уведомление показывает только номер новой версии — обновление скачивается и ставится вручную. Ручная проверка — **Help → Check for Updates**, результат приходит toast-уведомлением.

## Как вернуть панели на место?

- Перетащите панель за заголовок к нужному краю — появится превью зоны докинга.
- Чтобы свернуть панель, кликните стрелку на её заголовке.
- Вернуть стандартное расположение можно через **View → Reset Layout**.
- Полностью скрыть все панели — **Zen Mode** (`F12`).

## Как пройти обучение заново?

Интерактивный тур запускается через **Help → Tutorial**. Он включает шаги по меню, палитре нод, холсту, инспектору и логам. Welcome Setup можно повторить, если сбросить данные приложения (**Help → Advanced → Cleanup Dev Data**), но это удалит и другие локальные настройки.

## Почему изменения настроек не применились ко всем окнам?

Настройки (язык, тема, акцентный цвет) синхронизируются автоматически между всеми окнами (Main Editor, Visual Editor). Если синхронизация не сработала, попробуйте переоткрыть окно Visual Editor.

## Как быстро найти нужный Yarn файл в инспекторе?

Используйте автоподстановку: начните печатать название файла в поле **File**, и редактор предложит подходящие варианты из папки `Dialogues`. То же самое работает для нод внутри файла.

---

## См. также

- [Справочник нод](nodes.md) — все ноды с параметрами
- [How-to карточки](how-to.md) — короткие рецепты
- [Проверки и ошибки](validation.md) — что означают предупреждения
- [Интерфейс](ui.md) — как работать с редактором

<!-- sources: editor-app/src/renderer/src/editor/validators/nodeChecks.ts; editor-app/src/renderer/src/editor/validators/continuity.ts; editor-app/src/renderer/src/editor/nodes/nodeRegistry.ts; editor-app/src/renderer/src/editor/TopMenuBar; editor-app/src/renderer/src/editor/UpdateNotification; editor-app/src/renderer/src/editor/useEditorCallbacks.ts; editor-app/src/renderer/src/editor/useSceneIO.ts; editor-app/src/renderer/src/editor/inspector/NodeInspector; editor-app/src/renderer/src/editor/DockPanel; editor-app/src/renderer/src/editor/useEditorShortcuts.ts; editor-app/src/renderer/src/editor/usePreferences.ts; editor-app/src/main/ipc.ts; editor-app/src/main/updater.ts; editor-app/src/main/appState.ts; editor-app/src/main/windowManager.ts; Undefinedtale888/scripts/scr_cutscene_classes/scr_cutscene_classes.gml; Undefinedtale888/scripts/cutscene_action_factory/cutscene_action_factory.gml; Undefinedtale888/scripts/__ChatterboxConfigMacros/__ChatterboxConfigMacros.gml; editor-app/src/renderer/src/i18n/ru.ts -->
