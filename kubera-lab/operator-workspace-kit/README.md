# KUBERA Operator Workspace Kit

**KUBERA prepares. The human remains the authority.**

Практический файловый набор для аккуратной работы над проектами KUBERA LAB: задачи, черновики, доказательства, review, approvals и архив не теряются в переписке и остаются проверяемыми.

Это **не новый agent framework** и не замена DZAMBALA. Runtime, `WorkContract`, `HandoffArtifact`, gates, grants, `SovereignToolExecutor`, `ActionLogger` и `EvidenceLedger` остаются canonical механизмами в `innovation-stack/reference-implementation`.

## Workspace

```text
workspace/
├── tasks/       # входящие задачи, найденные указатели и рабочий scope
├── handoffs/    # черновики и письменные передачи результата
├── evidence/    # проверенные факты и correction-сигналы
├── reviews/     # то, что ждёт проверки, включая improvement proposals
├── approved/    # результат, одобренный человеком
└── archive/     # устаревшее и завершённое
```

Простая логика: **нашёл → подготовил → доказал → отдал на review → получил approval → сохранил/архивировал**.

## Что входит

- `templates/WORK_CONTRACT.md` — пяти-полевой контракт `Job / Sources / Judgment / Output / Forbidden`;
- `templates/HANDOFF.md` — человекочитаемый шаблон существующего `HandoffArtifact`;
- `APPROVAL_RULES.md` — что можно готовить самостоятельно и что требует точного человеческого одобрения;
- `ACTION_LOG.md` — человекочитаемый журнал/экспорт действий; **не заменяет Evidence Ledger**;
- `skills/verify-before-claim.md` — сначала проверить факт, потом утверждать;
- `skills/recheck-before-write.md` — перечитать текущее состояние перед сохранением/commit;
- `examples/merton-civic-evidence-work-contract.md` — реальный пример контракта для Civic Evidence OS;
- `improvement-loop/README.md` — правила превращения повторяющихся corrections в проверяемые улучшения;
- `control-desk/` — статический интерактивный demo интерфейса Agents / Setup / Improve.

## Рабочий цикл

1. Создать файл задачи в `workspace/tasks/`.
2. Заполнить `WorkContract` до серьёзной работы.
3. Собирать проверяемые источники в `workspace/evidence/`.
4. Черновик/передачу хранить в `workspace/handoffs/`.
5. Всё, что требует человека, переносить в `workspace/reviews/`.
6. После явного approval сохранить итог в `workspace/approved/`.
7. Неактуальные версии переносить в `workspace/archive/`, а не выдавать за текущее состояние.

## Improvement loop

Повторяющаяся ошибка агента не должна каждый раз исправляться только в чате.

Reference runtime теперь содержит `ImprovementRegistry`:

```text
compact CorrectionSignal
→ deterministic cluster
→ promotion threshold
→ exact rule / skill / gate / doc proposal
→ evidence + exact diff
→ human approve / dismiss
→ approved payload
→ normal Git / PR workflow
```

По умолчанию хранятся **минимальные сигналы**, а не полный текст разговора: fingerprint, короткое summary, conversation id и pain score. Это уменьшает privacy-риск и не превращает историю чатов во вторую базу знаний.

Default promotion threshold: минимум **3 сигнала**, минимум **2 разных разговора**, суммарный pain минимум **3**. Порог детерминированный и может быть изменён явно через `PromotionThreshold`.

Proposal сам **не пишет файлы**. Даже после достижения порога он только готовит предложение и diff. `approved_change()` остаётся заблокированным до явного человеческого review конкретного proposal.

## Agent overview

`ImprovementRegistry` также содержит минимальный локальный реестр agent sessions со статусами:

`running · waiting_approval · finished · failed · idle · unknown`

Он не заявляет live-интеграцию с Codex/Claude/Cursor. Это provider-neutral data model, к которому реальные adapters могут быть подключены позже через отдельный проверяемый scope.

## Control Desk demo

`control-desk/index.html` показывает нашу собственную UX-модель:

- **Agents** — текущие состояния исполнителей;
- **Setup** — какие правила, skills и security boundaries ими управляют;
- **Improve** — повторяющиеся correction-сигналы, evidence, diff и human decision.

Демо работает только на фиктивных данных и не выполняет внешних действий.

## Правило истины

- Chat помогает координировать работу.
- Файл/commit фиксирует результат.
- Memory хранит устойчивый контекст, но **не заменяет свежий источник**.
- Изменяемое внешнее состояние перечитывается перед consequential action.
- В DZAMBALA canonical audit trail — `EvidenceLedger`; этот kit только делает процесс удобным для человека.

## Approval boundary

Без дополнительного разрешения допустимы чтение, поиск, анализ, сравнение, подготовка черновиков и локальные обратимые изменения в рабочем пространстве.

Точное человеческое одобрение требуется перед удалением значимого контента, публичной публикацией, отправкой наружу, оплатой/покупкой, подписью, принятием условий, использованием приватных данных вне разрешённого scope и другими consequential external actions.

Manual сам по себе не является security boundary. Реальное выполнение инструментов в KUBERA должно идти через `SovereignToolExecutor` и существующие gates.
