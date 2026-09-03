# KUBERA OPERATOR

**KUBERA prepares. The human remains the authority.**

Этот документ фиксирует рабочий способ запуска задач в DZAMBALA Control layer. Он не создаёт новую агентную систему и не заменяет существующие `HandoffArtifact`, gates, grants или Evidence Ledger.

## Workspace

Контекст работы должен жить в артефактах и файлах, а не только в истории чата. Для durable runtime используется соглашение:

```text
/workspace/tasks/
/workspace/handoffs/
/workspace/evidence/
/workspace/reviews/
/workspace/approved/
/workspace/archive/
```

Это соглашение каталогов, а не отдельная облачная файловая система.

## HandoffArtifact

Передача задачи между специалистами идёт через существующий `HandoffArtifact`: task/status/output/sources/evidence/next action/next owner. `to_handoff_md()` только рендерит этот же объект в `HANDOFF.md`; второго handoff-формата нет.

## WorkContract

Каждый исполнитель получает короткий `WorkContract` из пяти полей:

- **Job** — что именно делает исполнитель;
- **Sources** — какие классы источников допустимы;
- **Judgment** — какие решения он вправе принимать;
- **Output** — какой результат обязан вернуть;
- **Forbidden** — что делать нельзя.

Для необратимого действия пустой `Forbidden` считается недостаточной границей полномочий и выполнение блокируется.

## Three gates

Перед внешним действием обязательна цепочка:

`Source Gate → Evidence Gate → Action Gate`

Source/Evidence references должны реально разрешаться в canonical `EvidenceLedger`. Переданный вызывающим кодом boolean не является доказательством. Unknown/missing reference блокирует tool.

`Action Gate` применяет policy, reversibility и signed approval. Для необратимого действия **approval сильнее общего ALLOW**.

## Reversibility line

**Reversible preparation:** research, draft, summarize, prepare, compare, verify, queue.

**Irreversible/consequential:** send, publish, pay, buy, delete, sign, accept terms, Launch или эквивалентный внешний side effect.

Необратимое действие требует точного signed grant на финальный sanitized request.

## SovereignToolExecutor — единственная дверь к tool

`DeterministicAgentPipeline` готовит и проверяет работу, но не вызывает external adapters. Единственный reference execution path:

```text
HandoffArtifact
→ WorkContract
→ PrivacyGate
→ ToolValidator
→ ledger-backed Source/Evidence resolution
→ Source/Evidence/Action Gate
→ signed approval when required
→ IdempotencyStore.reserve
→ ToolAdapter.execute
→ idempotency complete
→ ActionLogger
→ EvidenceLedger
```

Приложение должно держать реальные provider credentials и raw clients вне доступа агентов/plugins, иначе Python-объект сам по себе не может физически запретить обход.

## Idempotent retry

- new key + request → reserve PENDING;
- COMPLETE + same request → REPLAY без второго side effect;
- PENDING + same request → `UNKNOWN_EXTERNAL_STATE`, не повторять execute;
- same key + different request → CONFLICT;
- если adapter мог выполнить действие, но локальная система не доказала результат, требуется reconciliation.

## Notify by exception

Обычный успешный подготовительный поток не должен перегружать человека уведомлениями. Эскалация нужна при approval, failure, unknown external state, значимом изменении состояния или превышении порога.

Где upstream поддерживает events/webhooks, они предпочтительнее бессмысленного частого polling.
