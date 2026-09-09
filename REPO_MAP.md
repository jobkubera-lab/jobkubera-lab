# KUBERA repository map

Обновлено: 2026-09-09.

## Продукт

**KUBERA Local Desk / Agent OS** — человек описывает задачу, система выбирает ограниченную capability, находит и проверяет источник, готовит понятный результат, сохраняет доказательства и предлагает следующее действие; человек остаётся authority.

Это не live council service, не eligibility decision, не procurement authority, не банк и не автопостинг.

## Флагманы

1. **Lookup — Civic Evidence OS**  
   Репозиторий: `jobkubera-lab/kubera-improved-website`  
   Папка: `civic-evidence-os/`  
   Роль: детерминированный поиск по проверенному каталогу, официальный URL, fallback и safety.

2. **Place — Community Compass v0.2**  
   Репозиторий: `jobkubera-lab/jobkubera-lab`  
   Папка: `kubera-lab/dzambala-community-compass/`  
   Роль: карта, вручную проверенные события и provenance для London + Merton.

3. **Control — Agent Fabric / Trust Mesh + DZAMBALA**  
   Репозиторий: `jobkubera-lab/jobkubera-lab`  
   Папка: `kubera-lab/innovation-stack/reference-implementation/`  
   Стратегия: `kubera-lab/innovation-stack/DZAMBALA.md`  
   Роль: handoff, source/evidence/action gates, approval, idempotency, Evidence Ledger и контролируемое выполнение.

## Capability layer — KUBERA MCP LAB

Папка: `kubera-lab/mcp-lab/`

Роль: набор небольших MCP-серверов, которые делают существующие KUBERA-capabilities переиспользуемыми для разных каналов и AI-hosts.

```text
surface -> Agent OS -> MCP Gateway -> bounded MCP server -> official/data source
                                      -> evidence/result -> human-controlled action
```

Текущая foundation-версия включает:

- Hello MCP — учебный/smoke-test сервер;
- Evidence MCP — SHA-256 provenance envelopes;
- ONS MCP — read-only official statistics interface;
- Tender MCP — interface к существующему Tender Intelligence;
- TypeScript gateway reference с deny-by-default server/tool registry;
- security baseline;
- project-based learning track;
- Python/TypeScript CI.

MCP LAB **не является новым Agent OS**. Agent OS решает, когда использовать capability; MCP определяет ограниченный tool/resource contract; Control/Evidence слой обеспечивает границы и human authority.

## Операционные noses Agent OS

### KUBERA Tender Intelligence

Папка: `kubera-lab/tender-intelligence/`

Роль:

```text
official source -> normalize/provenance -> checkpoint -> deadline/CPV/requirements/buyer -> gaps -> BID/REVIEW/NO-BID -> DRAFT bid pack -> human
```

Включает read-only Find a Tender / Contracts Finder intake и v1.1 intelligence.

Ограничения:

- нет автономной подачи тендеров;
- нет подписания деклараций;
- нет принятия legal terms;
- нет заявлений о partnership с UK government.

### Future MCP-backed noses

Следующие направления развиваются как конфигурации общей системы, а не новые платформы:

- Local MCP / KUBERA Local Desk;
- Collector MCP / KUBERA Collector Intelligence;
- Document MCP / KUBERA Document Desk;
- Business/booking MCP для AI Receptionist — только после approval/idempotency/auth gates.

## Craft — отдельно от runtime

**KUBERA STONES**  
Папка: `kubera-lab/kubera-stones/`  
Роль: one-of-a-kind handmade stones, персональные символы и custom-order craft. Это отдельное творческое направление и не часть AI runtime.

## Витрина

Корневой профильный `README.md` — отдельная лицевая презентационная страница. Операционные статусы, runtime-изменения и служебные записи размещаются в `STATUS.md`, `REPO_MAP.md` и внутренних README проектов, а не добавляются автоматически на лицевую страницу.

## Склад / библиотека

Остальные репозитории и материалы не считаются отдельными флагманскими продуктами. Это библиотеки, заметки, старые эксперименты или черновики, пока они не нужны Lookup / Place / Control / Capability слоям.

Шаблоны виз и миграционные материалы остаются библиотекой, а не главным нарративом аккаунта.

## Заморожено

Innovation-stack модули 01–18 как отдельные продукты **не развивать и не расширять новыми модулями 19+**.

`reference-implementation/` и `DZAMBALA.md` — действующий Control-слой и продолжают развиваться через небольшие проверяемые компоненты и тесты.

Также не развивать как витринные направления: `ssh-check`, `kubera-local-ai2`, крипто-оплату, автокомменты и другие черновые эксперименты.

## Правило

**KUBERA prepares. MCP exposes bounded capabilities. The human remains the authority.**
