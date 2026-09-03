# KUBERA repository map

Обновлено: 2026-09-03.

## Продукт

**KUBERA Local Desk** — человек описывает задачу, система находит и проверяет официальный источник, готовит понятный результат и сохраняет доказательства; человек остаётся authority.

Это не live council service, не eligibility decision, не банк и не автопостинг.

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

## Витрина

Профильный `README.md`, `STATUS.md`, `KUBERA_LOCAL_DESK.md` и эта карта объясняют одну систему: **KUBERA Local Desk + DZAMBALA Control layer**.

## Склад / библиотека

Остальные репозитории и материалы не считаются отдельными флагманскими продуктами. Это библиотеки, заметки, старые эксперименты или черновики, пока они не нужны одному из трёх флагманских кусков: Lookup / Place / Control.

## Заморожено

Innovation-stack модули 01–18 как отдельные продукты **не развивать и не расширять новыми модулями 19+**.

`reference-implementation/` и `DZAMBALA.md` — действующий Control-слой и продолжают развиваться через небольшие проверяемые компоненты и тесты.

Остальной innovation-stack считается замороженным архитектурным материалом, если он не нужен действующему reference runtime.

Также не развивать как витринные направления: `ssh-check`, `kubera-local-ai2`, голос, крипто-оплату, автокомменты и другие черновые эксперименты.

## Правило

**KUBERA prepares. The human remains the authority.**
