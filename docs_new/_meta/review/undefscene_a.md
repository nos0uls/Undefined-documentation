# Фактчек `undefscene/overview.md` + `tutorial.md` + `how-to.md` + `workflow.md` — ревизия кода 7ee444a

Источник истины: `$E` = `Undefscene/editor-app` (только чтение). Cross-check JSON-экшенов и GML-сниппета: `$P` (только чтение). Ссылки между страницами проверены по `_meta/nav_plan.md` — все целевые файлы существуют.

Ключевые факты из $E:
- Реестр нод: `src/renderer/src/editor/nodes/nodeRegistry.ts` — **84 типа в палитре** + `start` (создаётся с новой сценой, в палитре отсутствует) = 85 типов суммарно.
- MMB по пустому месту холста создаёт `dialogue`-ноду: `useNodeOperations.ts:337-342` (`createDefaultPaneNode`), обработчик `FlowCanvas.tsx:968-999` (`event.button !== 1` → выход; только `.react-flow__pane`).
- Хоткеи (`useEditorShortcuts.ts`): Ctrl+A, Ctrl+Z/Y/Shift+Z, Ctrl+S (save), Ctrl+N (new scene), Ctrl+O (open **scene**, не project), Ctrl+E (export), Ctrl+P (preferences), Delete, Ctrl+C/X/V. Canvas: Space / Ctrl+0 → fitView (`FlowCanvasKeyboardShortcuts.tsx:29-47`). В RVE: B — Карандаш, G — Ластик, Ctrl+E — Импорт пути, Shift — прямая линия (`en.ts:164`, `ru.ts:164`).
- Меню (`TopMenuBar.tsx:243-353` + i18n): File → New Scene, Create Example, Open Scene..., **Open Project (.yyp)...**, Save, Save As..., **Export to Game...** (ru «Экспорт в игру...», `ru.ts:39` / `en.ts:39`), Preferences..., Exit. View → Reset Layout, **Visual Editing**. Панели: меню **Panels**.
- Имена панелей (`useEditorCallbacks.ts:112-119`, `en.ts:839-845`, `ru.ts:831-837`): Actions, Bookmarks, Text, Inspector, **«Логи / Ошибки» (ru) / «Logs / Warnings» (en)**, JSON, **«Шаблоны» (ru) / «Templates» (en)**, Notes.
- Layout по умолчанию (`useLayoutState.ts:16-101`): left = Actions+Bookmarks, right = Text+Inspector, bottom = Logs; Notes и Templates скрыты, открываются через меню Panels.
- Поля в Inspector рендерятся через `t('nodes.fields.'+key, label)` (`NodeInspector.tsx:147,151`) — ru-лейблы: `actor_name`→`Actor Name`, `actor_sprite`→`Actor Sprite` (`ru.ts:419-420`).
- Новая сцена: подтверждение → `createEmptyRuntimeState()` → на холсте `start`-нода `Start` (`useSceneIO.ts:250-260`, `runtimeTypes.ts:216`).
- Экспорт: валидация (ошибки блокируют) → `compileGraph` → диалог сохранения `.json` (`useSceneIO.ts:84-126`, `ipc.ts:1387-1397`). Save → `.usc.json` (`ipc.ts:1404-1405`).
- Welcome-модалка: язык+тема+акцентный цвет, только при первом запуске (`hasCompletedInitialSetup`), Esc закрывает (`WelcomeSetupModal.tsx:43-53`, `useEditorState.ts:154-161`).
- RVE: отдельное native-окно (View → Visual Editing). Импорт пути: при выбранной ноде — заменяет её на `follow_path` с точками, иначе — создаёт новую (`useVisualEditing.ts:202-286`). Импорт актёров пишет `x`/`y` в `actor_create` (`useVisualEditing.ts:289-346`).
- Bookmarks-панель — это список всех нод (заголовок «Nodes»), **нет** кнопки «Add Bookmark»; одиночный клик выбирает ноду и центрирует холст (`BookmarksPanel.tsx`, `useEditorCallbacks.ts:481-492`, `FlowCanvas.tsx:683-692` `setCenter`).
- Templates-панель: кнопка **«Save Selection»** (не «Save as Template»), **«Insert»**, хранение в localStorage — доступно во всех сценах (`TemplateLibraryPanel.tsx:159-183`, `templateStorage.ts`).
- Notes: кнопка «+», категории acting/camera/sound/todo/warning, pin → наверх списка, привязка — иконка 🔗 (title «Link to selected node»); клик по заметке центрирует холст на привязанной ноде/координатах (`NotesPanel.tsx`).
- Двойной клик по ребру → фокус на поле «Wait on edge (seconds)» в Inspector (`useNodeOperations.ts:301-304`, `EdgeInspector.tsx:21-47`). Условие на ребре — отдельный чекбокс «Condition» в Inspector при выбранном ребре (`EdgeInspector.tsx:48-114`).

## overview.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 10 | Граф нод: движение, диалоги, камера без правки JSON | OK (`nodeRegistry` категории movement/dialogue/camera) |
| 13 | React Flow | OK (`@xyflow/react`, `AGENTS.md`, `BaseNode.tsx:1`) |
| 14 | Инспектор параметров | OK (`InspectorPanel`, правый док `useLayoutState.ts:18`) |
| 15 | Автопроверка ошибок перед экспортом | OK (`useSceneIO.ts:84-101` — `hasErrors` блокирует экспорт) |
| 16 | Экспорт в `datafiles/cutscenes/` | OK (конвенция; рантайм срезает `datafiles/` — `cutscene_load_json.gml:29-31`) |
| 17 | Room Visual Editor — актёры и пути поверх скриншота комнаты | OK (`RoomVisualEditorModal`, `useVisualEditing.ts`) |
| 18 | «Template Library» | **WRONG** — панель называется «Шаблоны»/`Templates` (`ru.ts:837`, `en.ts:845`, `useEditorCallbacks.ts:119`); «Template Library» в UI нет. Исправлено |
| 19 | Bookmarks/Notes — навигация и заметки | OK частично: панель Bookmarks = список нод с центрированием по клику; заметки режиссёра — `notesTitle` `ru.ts:190` |
| 22 | Ссылка GitHub Releases | UNVERIFIABLE (внешний URL, офлайн не проверить) |
| 23 | «Подключите проект (.yyp) в настройках» | **WRONG** — проект открывается через File → Open Project (.yyp)..., в Preferences этого пункта нет (`TopMenuBar.tsx:261-266`, `ru.ts:36`) |
| 26 | «Export for Engine» | **WRONG** — пункт меню «Export to Game...»/«Экспорт в игру...» (`en.ts:39`, `ru.ts:39`). Исправлено |
| 31-32 | `pnpm install` / `pnpm dev` в `editor-app` | OK (`AGENTS.md`) |
| 35 | `.exe`: установщик или portable | OK (`AGENTS.md` — `pnpm build:win` = NSIS + portable) |
| 45 | «Все 85 нод» | OK с оговоркой: в палитре/NODE_REGISTRY — 84 типа, +`start` = 85 (nodeRegistry.ts keys; `nodes/index.ts:110`) |
| 47,55,63,71,79,87,95,103 | Ссылки на nodes/how-to/ui/workflow/formats/validation/faq/glossary | OK — все файлы есть в `nav_plan.md` и на диске |
| 111-112 | Ссылки `../cutscenes/overview.md`, `../cutscenes/architecture.md` | OK — есть в `nav_plan.md` |

## tutorial.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 15 | Экран приветствия: язык и акцентный цвет | OK (ещё есть тема; показывается только при первом запуске — `useEditorState.ts:154-161`). Уточнено «при первом запуске» |
| 16 | File → Open Project (.yyp) | OK (`TopMenuBar.tsx:261-266`, `en.ts:36`) |
| 17 | File → New Scene → нода Start | OK (`useSceneIO.ts:250-260`, `runtimeTypes.ts:216`) |
| 20 | Esc пропускает приветствие | OK (`WelcomeSetupModal.tsx:43-53`) |
| 24 | СКМ по пустому месту → Dialogue; drag из палитры слева | OK (`useNodeOperations.ts:337-342`, `FlowCanvas.tsx:968-999`; палитра в левом доке `useLayoutState.ts:17`, drag — `ActionsPanel.tsx:79-83`) |
| 26 | Поля `File`/`Node`, `testDialogue.yarn`, `Cutscene-Bridge-Demo` | OK (`nodeRegistry.ts:353-354`; `$P` `datafiles/Dialogues/testDialogue.yarn:30` — title `Cutscene-Bridge-Demo` существует) |
| 31 | Actor Create между Start и Dialogue | OK (тип `actor_create`, `nodeRegistry.ts:121`) |
| 32 | `Actor Name` | OK — ru-лейбл поля `actor_name` = «Actor Name» (`ru.ts:419`, `NodeInspector.tsx:147`) |
| 33 | `Sprite` | **WRONG (неточно)** — ru-лейбл = «Actor Sprite» (ключ `actor_sprite`, `ru.ts:420`; en fallback «Sprite / Object» `nodeRegistry.ts:135`). Исправлено |
| 34-35 | RVE: разместить актёра → Импорт актёров → x/y | OK (`useVisualEditing.ts:289-346` пишет `x`/`y` в `actor_create`; кнопки `ru.ts:172,175`) |
| 39-41 | Follow Path + Карандаш + Импорт пути | OK (`nodeRegistry.ts:1723`; `useVisualEditing.ts:202-286`; `ru.ts:160,163`) |
| 42 | `Target` = asher, `Speed` | OK частично — поле `speed_px_sec`, лейбл «Speed (px/sec)» (`nodeRegistry.ts:1736-1740`, `ru.ts:417`). Уточнено |
| 46 | File → Export for Engine | **WRONG** — «Export to Game...»/«Экспорт в игру...» (`en.ts:39`, `ru.ts:39`). Исправлено |
| 47 | Сохранить в `datafiles/cutscenes/` | OK (диалог выбора пути `ipc.ts:1387-1397`; конвенция `cutscenes/`) |
| 48 | «Если в логах нет ошибок» | OK (экспорт блокируется при ошибках `useSceneIO.ts:86-101`) |
| 52-53 | Camera Pan / Camera Track / Parallel / Parallel Join | OK (`nodeRegistry.ts:394,436,1863,1870`) |
| 54 | «Template Library» | **WRONG** — панель «Шаблоны»/`Templates`. Исправлено |

## how-to.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 14-18 | New Scene → Start → Dialogue → End → Export `.json` | OK |
| 21-23 | Dialogue, Yarn Preview в панели Text, Wait for Dialogue | OK (`nodeRegistry.ts:348,360`; `panels.text` `en.ts:841`; TextPanel показывает превью yarn) |
| 26-29 | Actor Create ключ, Follow Path `Target`, Visual Editing, Import Path | OK |
| 32-34 | Camera Pan / Camera Track / Camera Shake (секунды) | OK (`nodeRegistry.ts:394,436,501` — поле `seconds` «Duration (seconds)») |
| 37 | Parallel + Parallel Join | OK (`nodeRegistry.ts:1863-1876`, пара создаётся вместе `useNodeOperations.ts:44-101`) |
| 40 | Branch — по результату функции | OK (`compiler/core.ts:419-463` — `condition` строкой; `$P` `cutscene_branch.gml:1-8` — callable/имя скрипта) |
| 41 | Branch Flag: `key`, `operator`, `value` | OK (`nodeRegistry.ts:1263-1291`) |
| 42 | Edge Condition «двойной клик по ребру» | **WRONG** — двойной клик фокусирует поле задержки (`useNodeOperations.ts:301-304`); условие включается чекбоксом «Condition» в Inspector у выбранного ребра (`EdgeInspector.tsx:48-114`). Исправлено |
| 45-46 | Set Facing / Auto Facing | OK (`nodeRegistry.ts:689,711`) |
| 49 | Play SFX: `Volume`, `Pitch` | OK (`nodeRegistry.ts:773-789`) |
| 53-58 | Play Music `sound`/`volume`, Music Duck `multiplier`/`fade`, Music Unduck, Stop Music `fade`; категория «Звук» | OK (`nodeRegistry.ts:791-854`; `ru.ts:186` audio=«Звук») |
| 60-62 | Duck = множитель, Volume = абсолют | OK (`$P` `scr_cutscene_music.gml:180-204` — «относительное приглушение», `duck_music(mult,fade)`) |
| 66-70 | Move Relative `target`/`dx`/`dy`, Set Position Relative; «Движение» | OK (`nodeRegistry.ts:1675-1722`, category movement) |
| 74-78 | Wait Until `condition_var`/`condition_equals`/`timeout_seconds`, 0=бесконечно; «Логика» | OK (`nodeRegistry.ts:1384-1412`; компилируется в `guard_global` — глобальная переменная, `compiler/compilers/logic.ts:5-26`) |
| 82-84 | Mark Node `name`, GoTo Node `Target Mark`; «Логика» | OK (`nodeRegistry.ts:1216-1247`) |
| 88-93 | Attach To Target `target`/`parent_ref`/`offset_*`/`follow_*`, Detach; «Актёр» | OK (`nodeRegistry.ts:161-246`, category actor=`Актёр` `ru.ts:180`) |
| 97-100 | Checkpoint State `checkpoint_id` + include_* (актёры/игрок/камера/музыка/globals), Restore State | OK (`nodeRegistry.ts:1800-1862`) |
| 104-108 | Schedule Action `delay_seconds`/`action_type`/`action_params`/`blocking` | OK (`nodeRegistry.ts:1614-1669`; options включая `play_sfx`,`emote`,`flip`) |
| 112-116 | Set Dialogue Speed, Dialogue Control (`prevent_skip`/`auto_advance`/`stay_open`), Set Portrait Next/Now, Clear Dialogue, Wait Typing | OK (`nodeRegistry.ts:1878-1953`) |
| 120-124 | Emote: «Визуал», `target`/`sprite`/`seconds`/`offset_*`/`wait`; пример `spr_emote_exclamation` | OK по полям (`nodeRegistry.ts:1015-1048`), **WRONG** по примеру спрайта — `spr_emote_*` в $P нет; реальный пример `spr_StatHeart` (`$P` `datafiles/cutscenes/tests/emote.json:5`). Исправлено |
| 128-131 | Jump: «Движение», `target`/`x`/`y`/`seconds`/`height`=16, `easing`=`linear` | OK (`nodeRegistry.ts:1049-1074`) |
| 135-137 | Halt: «Движение», мгновенный сброс скорости/флагов | OK (`nodeRegistry.ts:1075-1088`; `$P` `cutscene_runtime_halt` `scr_cutscene_classes.gml:1289-1299`) |
| 141-144 | Fade In/Out: «Камера», `seconds`, `color` (чёрный) | OK (`nodeRegistry.ts:753-772`, `color` default `'black'`) |
| 148-152 | View → Visual Editing; список комнат; Разместить актёра → Импорт актёров; Карандаш → Импорт пути; Ластик (G) | OK (`TopMenuBar.tsx:316-321`; `ru.ts:135,160-175`; хоткей G `ru.ts:164`) |
| 155 | Shift — прямая линия | OK (`ru.ts:164` / `en.ts:164`) |
| 159-162 | Панель «Template Library», «Save as Template», «Insert», локальное хранение | **WRONG** — панель «Шаблоны»/«Templates» (скрыта по умолчанию, `useLayoutState.ts:92-101`, открывается через Panels), кнопка «Save Selection» (`TemplateLibraryPanel.tsx:177`); «Insert» OK; localStorage OK (`templateStorage.ts:25,66-72`). Исправлено |
| 165-168 | Bookmarks: «Add Bookmark», двойной клик центрирует | **WRONG** — панель «Закладки» это список всех нод, кнопки добавления нет; одиночный клик выбирает ноду и центрирует холст (`BookmarksPanel.tsx`, `useEditorCallbacks.ts:481-492`). Исправлено |
| 171-175 | Notes: «+», категории, pin, кнопка «Link» → подсветка при выборе ноды | OK частично: «+»/категории/pin — OK (`NotesPanel.tsx:30,372-379,348-350`); **неточно**: привязка — иконка 🔗, клик по связанной заметке центрирует холст на ноде (`NotesPanel.tsx:135-141,262-282`). Панель скрыта по умолчанию. Исправлено |

## workflow.md

| Строка | Утверждение | Вердикт |
|--------|-------------|---------|
| 14 | Open Project → `.yyp`, автозаполнение ресурсов | OK (`TopMenuBar.tsx:261-266`; autocomplete через `useProjectResources`) |
| 17 | New Scene → нода Start | OK (`useSceneIO.ts:250-260`, `runtimeTypes.ts:216`) |
| 20-21 | Перетаскивание из левой палитры; выходы справа, входы слева | OK (`ActionsPanel.tsx:79-83,162`; `BaseNode.tsx:86-91` target=Left, source=Right) |
| 22 | Цепочка Start → Actor Create → Move → Dialogue → End | OK — все типы существуют (`nodeRegistry.ts`) |
| 25 | Inspector — правая панель | OK (`useLayoutState.ts:18`) |
| 28 | Двойной клик по ребру вместо ноды Wait | OK (двойной клик → фокус «Wait on edge (seconds)», `useNodeOperations.ts:301-304`, `EdgeInspector.tsx:21-47`) |
| 31,48 | Панель «Логи / Предупреждения» | **WRONG (неточно)** — ru «Логи / Ошибки», en «Logs / Warnings» (`ru.ts:265,835`; `en.ts:843`). Исправлено на «Логи / Ошибки» |
| 32 | Save → `.usc.json` | OK (`ipc.ts:1404-1405` `defaultPath: scene.usc.json`, фильтр `usc.json`) |
| 33 | «Export for Engine» (`.json`) | **WRONG** — «Export to Game...»/«Экспорт в игру...», `.json` верно (`en.ts:39`, `ipc.ts:1391`). Исправлено |
| 37-38 | `cutscene_load_json("cutscenes/my_scene.json")` + `_mgr.start_cutscene()` | OK (`$P` `cutscene_load_json.gml:7` возвращает менеджер; `obj_cutsceneManager/Create_0.gml:586` `start_cutscene`) |
| 45 | Сначала `.yyp`, потом автокомплит | OK |
| 46 | Visual Editing — рисование пути на фоне комнаты | OK (`useVisualEditing.ts`, `ru.ts:160-164`) |
| 47 | Yarn Preview в панели Text | OK (`TextPanel.tsx`, `en.ts:127,841`) |
| 54-58 | Ссылки «См. также» | OK — все файлы есть в `nav_plan.md` |

## Итог

- **WRONG/неточности (исправлено):** имя пункта экспорта «Export for Engine» → «Export to Game»/«Экспорт в игру» (3 страницы); «в настройках» → File → Open Project; панель «Template Library» → «Шаблоны»/«Templates» + кнопка «Save Selection»; Bookmarks-раздел переписан под реальное поведение; Notes — иконка привязки и поведение клика; Edge Condition — убран двойной клик; `Sprite` → `Actor Sprite`; `Speed` → `Speed (px/sec)`; `spr_emote_exclamation` → `spr_StatHeart`; «Логи / Предупреждения» → «Логи / Ошибки» (2 места).
- **UNVERIFIABLE:** URL GitHub Releases (overview.md:22).
- Внутренних деталей в страницах не найдено (`.tsx`, `requestAnimationFrame`, `userData`, имена компонентов — grep 0).
