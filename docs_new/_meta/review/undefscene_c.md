# Фактчек: undefscene/validation.md, faq.md, glossary.md (сверка с $E, cross-check $P)

Источники: `src/renderer/src/editor/validators/nodeChecks.ts`, `graphChecks.ts`, `core.ts`, `edgeChecks.ts`, `parallelChecks.ts`, `continuity.ts`, `resourceChecks.ts`, `types.ts`, `validationRuleOverrides.ts`, `useEditorValidation.ts`, `useSceneIO.ts`, `compiler/core.ts`, `compiler/utils.ts`, `compiler/exporters.ts`, `compiler/compilers/*`, `nodes/nodeRegistry.ts`, `inspector/NodeInspector.tsx`, `LogsPanel.tsx`, `TopMenuBar.tsx`, `DockPanel.tsx`, `UpdateNotification.tsx`, `RuntimeJsonPanel.tsx`, `TextPanel.tsx`, `yarnPreview.ts`, `FollowPathPreview.tsx`, `usePreferences.ts`, `useEditorState.ts`, `useEditorCallbacks.ts`, `useDockDropPreview.ts`, `useEditorShortcuts.ts`, `App.tsx`, `main/ipc.ts`, `main/updater.ts`, `main/appState.ts`, `main/windowManager.ts`, `i18n/ru.ts`, `i18n/en.ts`, `reverseCompile.ts` в $E; `scripts/cutscene_action_factory`, `scripts/cutscene_load_json`, `scripts/scr_cutscene_classes`, `scripts/__ChatterboxConfigMacros`, `scripts/interactionWithNPCsOrObjects`, `scripts/readDialogue` в $P; `_meta/nav_plan.md` в $D.

Примечание: уровни серьёзности в валидаторе — это `defaultSeverity`; пользователь может переопределить уровень или скрыть правило через контекстное меню лога (`validationRuleOverrides.ts:44-66`, `LogsPanel.tsx:483`). Вердикты ниже сверены с дефолтными уровнями.

## undefscene/validation.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| 11 | Автовалидация графа перед экспортом, результаты в «Логи / Предупреждения» | OK — `validateGraph` прогоняется на каждое изменение runtime (`useEditorValidation.ts:50-90`), вывод в `LogsPanel` |
| 15–19 | Уровни Error/Warn/Tip; Error блокирует экспорт, Warn/Tip — нет | OK — `ValidationSeverity = 'error'|'warn'|'tip'` (types.ts:13); экспорт прерывается при `hasErrors` с тостом «Export blocked» (useSceneIO.ts:86-101). Не сказано, что уровни — дефолтные и переопределяемы (см. примечание выше) |
| 23 | Нет Start / больше одной Start — Error | OK — `missingStartNode`, `tooManyStartNodes` = error (graphChecks.ts:52-67) |
| 24 | Нет End / ни один End недостижим — Error | OK — `missingEndNode` (graphChecks.ts:68-75), `noEndNodeReachable` (113-121) = error |
| 25 | GoTo в несуществующую точку — Error | OK — `gotoTargetNotFound` = error, цель сверяется с именами mark_node и имён нод (nodeChecks.ts:656-667) |
| 26 | Дублирующийся `checkpoint_id` — Error | OK — `duplicateCheckpointId` = error (core.ts:119-131) |
| 21–26 | Список Error-проверок | **MISSING** — не перечислены error-правила: `actorUsedBeforeCreate`/`actorUsedAfterDestroy` (continuity.ts:370-392), битые пары parallel_start/join (`parallelStartMissingJoin`, `parallelStartJoinMissing`, `parallelStartJoinNotJoin`, `parallelJoinPairMissing`, `parallelJoinPairNotStart` — parallelChecks.ts:19-45,184-202), рёбра на несуществующие ноды (`edgeMissingSource`/`edgeMissingTarget` — edgeChecks.ts:13-30) |
| 30 | Пустое обязательное поле (Target/Sprite/File) — Warn | OK — `missingRequiredParam` = warn по таблице `REQUIRED_PARAMS` (nodeChecks.ts:5-74,123-142) |
| 31 | Изолированная нода — Warn | OK — `unreachableNodes` = warn для нод, недостижимых из start (graphChecks.ts:103-111) |
| 32 | >1 исходящей связи у обычной ноды — Warn; совет «Branch, Branch Flag или Parallel» | OK по уровню (nodeChecks.ts:106-121), но известная особенность: `branch_flag` НЕ исключён из проверки — корректная branch_flag с out_true/out_false получает ложный warn `nodeMultipleOutputs`; компилятор branch_flag с двумя выходами разрешает (compiler/core.ts:254,295) |
| 33 | Задержка/тряска с ≤0 длительностью — Warn | OK — `edgeNegativeWait` (edgeChecks.ts:32-40), `waitUntilNegativeTimeout` (nodeChecks.ts:187-196), `cameraShakeSecondsInvalid` (499-518) = warn |
| 34 | Actor Create без `actor_sprite` и `copy_target` — Warn | OK — `missingSpriteOrCopyFrom` = warn (nodeChecks.ts:145-158) |
| 35 | Branch без false-ветки | **WRONG** — лежит в разделе Warn, но дефолтная серьёзность `tip` (`branchMissingFalse`, nodeChecks.ts:162-172). В таблице ниже указано верно |
| 36 | Tween без target при kind=instance — Warn | OK — warn при `kind !== 'camera' && !target` (nodeChecks.ts:207-215); варианты kind — `instance`/`camera` (nodeRegistry.ts:569-573) |
| 37 | Set Property без `value` — Warn | OK — `setPropertyMissingValue` = warn (nodeChecks.ts:262-270) |
| 38 | Run Function без имени / битый JSON в args — Warn | OK — `runFunctionMissingName`, `runFunctionInvalidArgs` = warn (nodeChecks.ts:386-415) |
| 39 | Schedule Action: битый JSON в `action_params` или отрицательная задержка | Частично **WRONG** — задержка <0 = warn (`scheduleActionInvalidDelay`, nodeChecks.ts:443-452), но битый/не-объектный JSON в `action_params` = tip (`scheduleActionInvalidParams`/`scheduleActionParamsNotObject`, 419-441), не warn |
| 40 | Music Pitch вне 0.5–2.0 | **WRONG** — лежит в разделе Warn, но дефолтная серьёзность `tip` (`musicPitchExtreme`, nodeChecks.ts:374-382). В таблице ниже указано верно |
| 42–46 | При подключенном `.yyp`: проверка ассетов, yarn-файлов/нод, имён GML-функций | OK, неполно — `checkResources` также проверяет звуки (`sounds`) и whitelist условий `branch` (`branchConditionNotWhitelisted`, resourceChecks.ts:89-104,134-228) |
| 48–49 | Клик по сообщению в логе фокусирует проблемную ноду | OK — клик/Enter по записи с nodeId вызывает `onSelectNode` (LogsPanel.tsx:83-91,128-129,237-238) |
| 55–56 | `play_music`/`play_sfx` sound — Warn | OK — nodeChecks.ts:274-299 (+`play_music` также в REQUIRED_PARAMS:53) |
| 57 | `wait_until` `condition_var` — Error | OK — `waitUntilMissingCondition` = error (nodeChecks.ts:177-186); дополнительно срабатывает warn `missingRequiredParam` (REQUIRED_PARAMS:49) — дубль, не ошибка доки |
| 58 | `wait_until` `timeout_seconds < 0` — Warn | OK — nodeChecks.ts:187-196 |
| 59–60 | `goto`: пустой target — Warn; цель не найдена — Error | OK — nodeChecks.ts:642-667 |
| 61 | `tween` target при kind=instance — Warn | OK — nodeChecks.ts:207-215 |
| 62 | `tween` `prop`/`end_value` — Warn | OK — `tweenMissingProperty`, `tweenMissingToValue` = warn (216-233); читаются и алиасы property/field, to/value |
| 63–64 | `set_property` target/property/value — Warn | OK — nodeChecks.ts:244-270 |
| 65 | `run_function` имя — Warn | OK — nodeChecks.ts:386-400 |
| 66 | `run_function` `args` — валидный JSON-массив | Частично **WRONG** — проверяется только `JSON.parse(args)`: любой валидный JSON (объект, число, строка) проходит; «массив» не требуется (nodeChecks.ts:402-415) |
| 67 | `schedule_action` `delay_seconds >= 0` — Warn | OK — nodeChecks.ts:443-452 |
| 68 | `schedule_action` `action_params` — валидный JSON-объект — Tip | OK — tip и при битом JSON, и при валидном не-объекте/массиве (nodeChecks.ts:419-441) |
| 69–70 | `checkpoint_state` `include_globals`/`include_instances` — JSON-строка массива — Warn | OK — warn при битом JSON и при валидном не-массиве (nodeChecks.ts:469-496) |
| 71 | `music_pitch` pitch >0 и конечен — Warn | OK — `musicPitchInvalid` = warn при `!isFinite \|\| <=0` (nodeChecks.ts:364-373) |
| 72 | `music_pitch` вне 0.5–2.0 — Tip | OK — `musicPitchExtreme` = tip (374-382) |
| 73 | `actor_create` `actor_sprite` или `copy_target` — Warn | OK — nodeChecks.ts:145-158 |
| 74 | `branch` нет false-ветки — Tip | OK — `branchMissingFalse` = tip (162-172) |
| 75 | `mark_node` дубликаты имён — Warn | OK — `duplicateMarkerName` = warn (core.ts:59-71); пустое имя — тоже warn (nodeChecks.ts:587-597, REQUIRED_PARAMS:45) |
| 76 | `follow_path` пустой `points` — Warn | OK — `followPathEmptyPoints` = warn (nodeChecks.ts:552-561); дополнительно `emptyPath` warn из continuity (continuity.ts:394-407) |
| 77 | `follow_path` <2 точек — Tip | OK — `followPathTooFewPoints` = tip при 1 точке (562-570); параллельно срабатывает `emptyPath` warn (continuity.ts:394-407) — в доке не отражено, не ошибка |
| 78 | `halt` есть исходящие связи — Warn | OK — `haltHasOutgoingEdges` = warn (nodeChecks.ts:573-584) |
| 79 | `jump` `seconds <= 0` — Warn | OK — `jumpInvalidSeconds` = warn (626-637) |
| 80 | `emote` пустой `sprite` — Tip | OK — `emoteMissingSprite` = tip (713-724) |
| 81 | `crossfade_music` `intensity` вне 0–1 — Warn | OK — warn также при нечисловом значении (nodeChecks.ts:349-360) |
| 82 | `camera_shake` `seconds <= 0` — Warn | OK — nodeChecks.ts:499-518; те же правила частоты/амплитуды (`shakeFrequencyTooLow`, `shakeMagnitudeX/Y`) в таблице не перечислены |
| 53–82 | Таблица проверок — полнота | **MISSING** — вне таблицы остались: `partial_control` (баг ключа, см. ниже), `dialogue.file` (warn, nodeChecks.ts:456-467), `mark_node` пустое имя, `set_facing` невалидное направление (600-620), `spawn_entity` без object (699-711), `restore_state` пустой/неизвестный checkpoint_id (672-683; core.ts:134-147), `detach` без target (685-697), `camera_shake`/`shake_object` frequency/magnitude (519-548), `play_boss_music` calm/battle (302-323), `play_music_intro` intro/loop (326-347), `actorTargetNotFound` (728-773), `actorCreatedTwice`/`actorDestroyedNotCreated`/`musicNotStopped` (core.ts:149-208), проверки рёбер (edgeChecks.ts:32-143), `unsafeWait`/`cameraOverrideNotReset`/`musicActionWithoutMusic`/`cameraTrackMissingTarget` (continuity.ts:409-464), `nodeNoName`/`duplicateName` (graphChecks.ts:11-39), resource-проверки (resourceChecks.ts) |
| — | `partial_control` | Баг подтверждён: `REQUIRED_PARAMS.partial_control = ['type']` (nodeChecks.ts:47), реальное поле инспектора — `control_type` (nodeRegistry.ts:1320-1325). `node.params.type` всегда пуст → на каждую ноду Partial Control постоянный warn `«поле "type" не заполнено»` (ru.ts:685). Оформить как известную особенность |
| 86–90 | «См. также»: nodes.md, workflow.md, faq.md | OK — все файлы есть в nav_plan.md §undefscene |

## undefscene/faq.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| 16 | Target у Move/Follow Path = ключ из Actor Create | OK — ключ берётся из `actor_name` (core.ts:25-28, nodeRegistry.ts:127-131); неизвестная цель → warn `actorTargetNotFound` (nodeChecks.ts:749-759). Допустимы также `player`, `player_body`, имена объектов проекта (nodeChecks.ts:90-96) |
| 17 | Speed = 0 → актёр стоит | OK — `speed_px_sec`→`_speed_pf = speed/fps`; при 0 движения нет (cutscene_action_factory.gml:22-26 $P) |
| 18 | `collision` можно выключить (`false`) | OK — поле move `collision`, дефолт `'false'` (nodeRegistry.ts:95-100) |
| 22 | Без ноды камеры камера остаётся на месте | OK — переопределение камеры не сбрасывается само; есть tip `cameraOverrideNotReset` (continuity.ts:432-438) |
| 23 | «Camera Track Until Stop нужно остановить другой нодой камеры, иначе камера будет следить вечно» | **WRONG** — действие завершается само, когда у актёра `move_active`→false (или сразу, если флага нет) (scr_cutscene_classes.gml:4513-4524 $P). Камера после этого держит последнюю позицию — вернуть дефолт можно `camera_center` или `tween_camera` с `return_to_default` (совет из `cameraOverrideNotReset`) |
| 27–29 | Dialogue: выбрать File и Node; `.yarn` в `datafiles/Dialogues/`; Yarn Preview в панели Text | OK — поля `file`/`node` (nodeRegistry.ts:353-354); игра грузит из `CHATTERBOX_INCLUDED_FILES_SUBDIRECTORY "Dialogues"` (__ChatterboxConfigMacros.gml:10 $P; редактор сканирует весь `datafiles/` рекурсивно — ipc.ts:273-279 $E); превью — TextPanel + yarnPreview.ts |
| 33–36 | Ветки должны заканчиваться End; Halt блокирует выполнение; GoTo может создать цикл; незавершённый диалог стопорит сцену | OK — `noEndNodeReachable` error (graphChecks.ts:113-121); сообщение валидатора «нода halt блокирует выполнение» (ru.ts:723); `goto` — рантайм-прыжок к mark_node, цикл возможен; у dialogue есть `block_queue` (nodeRegistry.ts:355) |
| 40–44 | Warn не блокирует экспорт | OK — блокирует только `hasErrors` (useSceneIO.ts:86) |
| 48–49 | Save → `.usc.json`; «Export for Engine» → `.json` в `datafiles/` | Частично **WRONG** — пункт меню называется «Export to Game...»/«Экспорт в игру...» (en.ts:39, ru.ts:39), «Export for Engine» в UI не существует. `.usc.json` и сохранение engine-JSON — верно (ipc.ts:1404-1405,1458) |
| 53 | Open Scene открывает engine `.json`, граф восстановится из actions | OK — фильтр диалога `usc.json`/`json` (ipc.ts:1502); при нераспознанном runtime-формате вызывается `reverseCompileCutscene` (useSceneIO.ts:219-240) |
| 57 | gridSize — только визуальная сетка, не шаг расстановки нод | OK — `gridSize` идёт только в `gap` сетки (FlowCanvas.tsx:143); подсказка в настройках: «Меняет только визуальный шаг сетки» (ru.ts:70) |
| 61 | Help → Copy Log to Clipboard; файл `undefscene.log` в папке данных | OK — пункт меню (TopMenuBar.tsx:331-332), IPC `app.copyLogToClipboard` (ipc.ts:1536), `LOG_FILE_NAME = 'undefscene.log'` (appState.ts:51) |
| 65 | Сочетания работают независимо от раскладки; привязка в «Edit → Preferences → Keyboard Shortcuts» | Частично **WRONG** — раскладка не влияет (используется `e.code`: useEditorShortcuts.ts:115-120, App.tsx:68-69), но Preferences находится в меню **File**, не Edit (TopMenuBar.tsx:282-286; в Edit только Undo/Redo). Раздел Keyboard Shortcuts внутри Preferences есть (PreferencesKeyboardSection.tsx:30) |
| 69 | Автообновление: toast с кнопкой установки; portable — ссылка на релиз; Help → Check for Updates | Частично **WRONG** — уведомление это полоса вверху редактора (`UpdateNotification`), toast показывается при ручной проверке (useEditorCallbacks.ts:320-326); кнопка «Restart & Update» появляется после скачивания (UpdateNotification.tsx:104-120); в portable `autoDownload=false` — показывается только текст «Update available: v…», ссылки на релиз нет (updater.ts:4,98-100, UpdateNotification.tsx:4,88-92). Help → Check for Updates — OK (TopMenuBar.tsx:343) |
| 73–76 | Докинг: перетаскивание с превью зоны; стрелка сворачивания; View → Reset Layout; Zen Mode (`F12`) | OK — `useDockDropPreview.ts`; кнопка ▸/▾ в заголовке панели (DockPanel.tsx:64-72); Reset Layout в View (TopMenuBar.tsx:311-315); `zen_mode` по умолчанию F12 в packaged (usePreferences.ts:68; в dev-сборке F11) |
| 80 | Help → Tutorial; Welcome Setup заново через Help → Advanced → Cleanup Dev Data | OK — Tutorial в Help (TopMenuBar.tsx:350); Cleanup Dev Data удаляет `preferences.json`, где лежат `hasCompletedInitialSetup`/`hasCompletedTutorial` (ipc.ts:1549-1585; useEditorState.ts:154-160,184-195); шаги тура — меню/палитра/холст/инспектор/логи (ru.ts:551-578) |
| 84 | Настройки (язык, тема, акцент) синхронизируются между окнами | OK — `preferences.write` рассылает `preferences.onChanged` всем окнам (ipc.ts:1213-1217); visual-editor — отдельное окно (windowManager.ts:34-105) |
| 88 | Автоподстановка File/Node из папки Dialogues | OK — `file` → список yarn-файлов проекта, `node` → ноды выбранного файла (NodeInspector.tsx:222-227) |
| 94–97 | «См. также»: nodes.md, how-to.md, validation.md, ui.md | OK — все файлы есть в nav_plan.md §undefscene |

## undefscene/glossary.md

| Строка | Утверждение | Вердикт |
|---|---|---|
| 15–17 | Нода / Ребро / Inspector | OK — термины соответствуют runtime-модели (nodes/edges) и панели инспектора |
| 18 | Target — ключ актёра или `player` | OK, можно уточнить — резолвер принимает `player`, `player_body`, ключи actor_create/spawn_entity и имена object-ассетов (nodeChecks.ts:90-96) |
| 19–22 | Key / Actor / Yarn / `.yyp` | OK — `actor_name` с label `Key` (nodeRegistry.ts:127-131); Chatterbox-макрос `Dialogues` ($P); открытие `.yyp` даёт resources/yarnFiles/whitelist для автокомплита и resourceChecks |
| 23 | `.usc.json` хранит «граф, позиции нод, состояние панелей» | Частично **WRONG** — `.usc.json` = RuntimeState (title, nodes+позиции, edges, notes; serializeSceneState, useSceneIO.ts:66-77; runtimeTypes.ts:99-124). Состояние панелей хранится отдельно в `layout.json` (ipc.ts:1555-1556) и в файл сцены не попадает |
| 24–25 | «Export for Engine» — команда экспорта | **WRONG** — пункт меню называется «Export to Game...»/«Экспорт в игру...» (en.ts:39, ru.ts:39); формат export — `stripExport` (exporters.ts:4-16) |
| 26 | Visual Editing — отдельное окно | OK — отдельное BrowserWindow `visual-editor` (windowManager.ts:66-105) |
| 27–28 | Yarn Preview / Path Preview | OK — TextPanel + yarnPreview.ts; FollowPathPreview.tsx (i18n `followPathPreview` = 'Path Preview', en.ts:249) |
| 29–30 | Edge Condition / Wait on Edge | OK — `conditionEnabled`/`conditionVar`/`conditionEquals` и `waitSeconds` на ребре (edgeChecks.ts:32-143; compiler/core.ts:133-190) |
| 31–33 | Parallel / Branch / Branch Flag | OK — `parallel_start`/`parallel_join`→`parallel` action (compiler/core.ts:300-337); `branch` по имени функции-условия (whitelist `branchConditions`); `branch_flag` по `key`/`operator`/`value` (compiler/core.ts:441-454) |
| 34–36 | Mark Node / GoTo Node / Easing | OK — `mark_node`/`goto`; easing options `linear`/`ease_in`/`ease_out`/`ease_in_out` (nodeRegistry.ts:613,1069,1783) |
| 37–41 | Sprite / Depth / Facing / Emote / Tween | OK — стандартная семантика GM; `set_facing` валидирует left/right/up/down (nodeChecks.ts:600-620); `emote`, `tween` — ноды реестра |
| 42–45 | SFX / Fade In-Out / Instant Mode / Halt | OK — `play_sfx`; `fade_in`/`fade_out` (category camera, seconds+color, nodeRegistry.ts:753-768); `instant_mode`→`set_instant` в игре (factory:984-989 $P); `halt`→`cutscene_runtime_halt` (scr_cutscene_classes.gml:3037-3049 $P), валидатор прямо говорит «блокирует выполнение» |
| 46 | Autosave | OK — `autoSaveEnabled` + `autoSaveIntervalMinutes`, отдельный autosave-файл (useSceneIO.ts:166-190) |
| 47–51 | Attach To Target / Detach / Checkpoint / Restore State / Schedule Action | OK — типы `attach_to_target`, `detach`, `checkpoint_state`, `restore_state`, `schedule_action` в реестре и валидаторе |
| 52 | Partial Control: игрок может двигаться/взаимодействовать | OK — `control_type` 0/1/2: 0 — полный контроль катсцены, 1 — взаимодействие только по whitelist, 2 — полная свобода (scr_cutscene_classes.gml:4808-4812 $P; nodeRegistry.ts:1314-1342) |
| 53 | Wait Interact | OK — `wait_for_interact` → `ActionWaitForInteract` ($P) |
| 54 | Wait Talk — вариант Wait for Dialogue; «в экспорте нормализуется в `wait_for_dialogue`» | **WRONG** — нода `waittalk` (label Wait Talk, nodeRegistry.ts:375-388) компилируется pass-through и экспортируется как `type: "waittalk"` (compiler/utils.ts:29, core.ts:68-74). Нормализация `waittalk`/`wait_talk`→`wait_for_dialogue` происходит при загрузке JSON в игре (cutscene_load_json.gml:229 $P) и при обратном импорте в редактор (reverseCompile.ts:484) — не «в экспорте» |
| 55–59 | Set Portrait / Dialogue Control / Set Dialogue Speed / Wait Typing / Clear Dialogue | OK — `set_portrait_next`/`set_portrait_now` (target+emotion); `dialogue_control` (prevent_skip/stay_open/auto_advance, compilers/dialogue.ts:14-24); `set_dialogue_speed`; `wait_typing`; `clear_dialogue` |
| 60–61 | Template Library / Bookmarks | OK — TemplateLibraryPanel.tsx + templateStorage.ts (localStorage); BookmarksPanel.tsx |
| 62 | Notes — заметки режиссёра, editor-only | OK — `notes` в RuntimeState помечены «редактор-only, не экспортируются» (runtimeTypes.ts:112-113); `stripExport` их не включает (exporters.ts:4-16) |
| 63 | Runtime JSON — «просмотр JSON-экспорта катсцены в реальном времени» | **WRONG** — панель показывает сырое состояние сцены редактора (schemaVersion, title, nodes, edges, lastSavedAtMs), а не engine-экспорт; подсказка панели: «Raw editor scene state with node positions, selection, and editor-only fields» (RuntimeJsonPanel.tsx:14-30) |
| 69–70 | «См. также»: overview.md, nodes.md | OK — оба файла есть в nav_plan.md §undefscene |

## Сводка правок

- **validation.md**: пометить tip-проверки в разделе Warn (строки 35, 39, 40); уточнить строку 66 («валидный JSON» без «-массив»); расширить список Error (actor before create/after destroy, parallel-пары, битые рёбра); дополнить «Интеграцию с проектом» звуками и условиями branch; адмонишен «Известные особенности»: `partial_control` проверяет несуществующее поле `type` вместо `control_type` (вечный warn), `branch_flag` с двумя выходами получает ложный warn о множественных выходах; упомянуть переопределение уровней через контекстное меню лога.
- **faq.md**: исправить семантику Camera Track Until Stop (строка 23); «Export for Engine»→«Export to Game» (49); «Edit → Preferences»→«File → Preferences» (65); переписать блок автообновления (69): полоса уведомления + Restart & Update после скачивания, portable — только номер версии.
- **glossary.md**: `.usc.json` — убрать «состояние панелей» (23); «Export for Engine»→«Export to Game» (24–25); Wait Talk — нормализация на загрузке в игре, не в экспорте (54); Runtime JSON — состояние сцены, не экспорт (63).
