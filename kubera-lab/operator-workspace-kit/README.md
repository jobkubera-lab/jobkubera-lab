# KUBERA Operator Workspace Kit

**KUBERA prepares. The human remains the authority.**

Практический файловый набор для аккуратной работы над проектами KUBERA LAB: задачи, черновики, доказательства, review, approvals и архив не теряются в переписке и остаются проверяемыми.

Это **не новый agent framework** и не замена DZAMBALA. Runtime, `WorkContract`, `HandoffArtifact`, gates, grants, `SovereignToolExecutor`, `ActionLogger` и `EvidenceLedger` остаются canonical механизмами в `innovation-stack/reference-implementation`.

## Workspace

```text
workspace/
├── tasks/       # входящие задачи, найденные указатели и рабочий scope
├── handoffs/    # черновики и письменные передачи результата
├── evidence/    # проверенные факты и ссылки на источники
├── reviews/     # то, что ждёт проверки
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
- `examples/merton-civic-evidence-work-contract.md` — реальный пример контракта для Civic Evidence OS.

## Рабочий цикл

1. Создать файл задачи в `workspace/tasks/`.
2. Заполнить `WorkContract` до серьёзной работы.
3. Собирать проверяемые источники в `workspace/evidence/`.
4. Черновик/передачу хранить в `workspace/handoffs/`.
5. Всё, что требует человека, переносить в `workspace/reviews/`.
6. После явного approval сохранить итог в `workspace/approved/`.
7. Неактуальные версии переносить в `workspace/archive/`, а не выдавать за текущее состояние.

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
