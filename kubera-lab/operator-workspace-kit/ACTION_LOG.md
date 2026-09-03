# ACTION LOG

Человекочитаемый журнал для быстрого обзора работы.

> **Не canonical source of truth.** В DZAMBALA canonical audit trail остаётся `EvidenceLedger` + `ActionLogger`. Этот файл может заполняться вручную или генерироваться как export.

| Timestamp | Actor | Task | Action | Sources / refs | Outcome | Approval | Files / artifacts |
|---|---|---|---|---|---|---|---|
| `<ISO-8601>` | `<agent/human>` | `<task-id>` | `<what happened>` | `<refs>` | `<success/blocked/unknown>` | `<not-needed/requested/granted>` | `<paths>` |

Правила:

1. Писать фактический outcome, а не намерение.
2. Не записывать секреты, токены, пароли или лишние персональные данные.
3. При `UNKNOWN_EXTERNAL_STATE` писать именно это и не выдавать действие за успешно завершённое.
4. При наличии ledger entry указывать его reference вместо дублирования доказательств.
