# KUBERA GitHub Portfolio — Исправления для ChatGPT

**Статус:** Проверено и подтверждено  
**Дата:** 2 октября 2026  
**Исполнитель:** ChatGPT / Claude  
**Автор плана:** Nikola Kubera + AI Review

---

## 📋 ОБЗОР РАБОТ

### Что уже сделано ✅
- 134 GitHub Actions запуска
- 8 workflows (MCP Lab Tests, Innovation Stack Tests, Profile README Lock)
- ~25 тестовых файлов, покрытие 89%
- pyproject.toml с зависимостями
- MIT лицензии на 5 проектов
- reference-implementation с demo.py

### Что нужно сделать
1. **Переименовать:** `kubera-learning.` → `kubera-learning`
2. **Добавить descriptions:** в 2 пустых репо
3. **Добавить topics:** во все 18 репо
4. **Унифицировать идентичность:** одна биография везде
5. **Убрать Monero:** из профиля
6. **Создать 4 стратегических репо:** Agent OS, Civic Evidence, Tender Intelligence, RESI
7. **Обновить README:** главный профиль (с обходом боте-защиты!)

---

## ⚠️ КРИТИЧЕСКОЕ: Боте-защита профиля README

### Проблема
На `jobkubera-lab/jobkubera-lab` включен workflow **"Profile README Lock"**, который:
- Защищает файл `README.md`
- Откатывает все изменения, сделанные вне специального процесса
- Проверяет коммиты в `main` ветку

### Решение: Обход боте-защиты

**Вариант 1 — Временно отключить защиту** (рекомендуется)
```bash
# 1. В Settings → Actions → General
#    - Отключить "Profile README Lock" workflow
# 2. Внести изменения в README.md
# 3. Включить workflow обратно
```

**Вариант 2 — Использовать защищённый процесс**
```bash
# Если боте-файл настроен на проверку коммит-сообщений:
# - Коммит должен содержать: [PROFILE_UPDATE]
# Например:
git commit -m "[PROFILE_UPDATE] Remove Monero, unify bio"
```

**Вариант 3 — Создать ветку и merge через bot-исключение**
```bash
# 1. Создать ветку: git checkout -b profile-cleanup
# 2. Внести все изменения
# 3. Push на GitHub: git push origin profile-cleanup
# 4. Создать Pull Request
# 5. В PR добавить label: [PROFILE_LOCK_OVERRIDE] или похожий
# 6. Merge PR
```

**Рекомендуемый вариант:** Вариант 1 (отключить → изменить → включить обратно)

---

## 🔧 ЗАДАЧИ ПО ПРИОРИТЕТАМ

### ЭТАП 1 — Немедленно (День 1)

#### 1.1 Переименовать репозиторий
```
Текущее имя: kubera-learning.
Новое имя: kubera-learning

Где: GitHub Settings (в репо) → Repository name
Результат: старая ссылка редиректится автоматически
```

**После переименования обновить в главном README:**
- Строка: `➡️ **[KUBERA AI Engineer Roadmap](docs/AI_ENGINEER_ROADMAP.md)`
- Проверить, что ссылка всё ещё работает

---

#### 1.2 Добавить descriptions в 2 пустых репо

| Репо | Текущее | Новое |
|------|---------|-------|
| `kubera-local-ai2` | (пусто) | "KUBERA Local AI — local model experiments (learning repository)" |
| `ssh-check` | (пусто) | "SSH connectivity check tool — infrastructure testing" |

**Где менять:** Settings → Description (каждый репо)

---

#### 1.3 Убрать Monero из профиля

**Файл:** `jobkubera-lab/README.md` (главный профиль)  
**Что удалить:** строки 3-10 (иконка Monero + ценовой бадж)

```markdown
// УДАЛИТЬ ЭТО (строки 3-10):
<p align="right">
  <a href="https://www.coingecko.com/en/coins/monero" title="Monero (XMR)">
    <img src="https://cdn.simpleicons.org/monero/FF6600" width="18" height="18" alt="XMR" />
  </a>
  <a href="https://www.coingecko.com/en/coins/monero" title="Live XMR/USD price">
    <img src="https://img.shields.io/badge/dynamic/json?url=..." />
  </a>
</p>
```

**Причина:** Госсектор UK (NHS, GOV.UK) не одобряет крипто в профилях разработчиков

---

### ЭТАП 2 — День 2-3 (добавление topics и унификация)

#### 2.1 Добавить GitHub Topics ко всем 18 репо

**Где:** Settings → Topics (в каждом репозитории)

| Репозиторий | Topics |
|-------------|--------|
| `jobkubera-lab` | `ai-agents` `python` `evidence-ledger` `ai-assurance` `mcp` `orchestration` |
| `kubera-improved-website` | `civic-tech` `javascript` `local-intelligence` `maps` `prototype` |
| `kubera-learning` | `ai-education` `python` `machine-learning` `agents` `learning-path` |
| `kubera-ai-prompts` | `prompts` `ai-workflows` `llm` `templates` `reusable` |
| `kubera-visa-playbooks` | `relocation` `visa-guides` `employment` `documentation` |
| `kubera-migration-templates` | `templates` `cv` `letters` `multilingual` `hr` |
| `kubera-migration-checklist` | `checklist` `relocation` `workflow` `python` |
| `NikolaKubera` | `portfolio` `html` `personal-brand` |
| `.devcontainer` | `devcontainers` `fork` `infrastructure` |
| `design-system` | `design-system` `nhs` `fork` `accessibility` |
| `fAIr` | `ai-mapping` `fork` `geospatial` |
| `govuk-infrastructure` | `govuk` `infrastructure` `fork` |
| `localgov_multilingual` | `localgov` `drupal` `multilingual` `fork` |
| `kubera-local-ai` | `local-ai` `llm` `privacy` `python` |
| `kubera-local-ai2` | `local-ai` `experiments` `learning` `python` |
| `kubera-real-estate-os` | `real-estate` `ai` `research` `evidence` `beta` |
| `llm-eval-monitor-framework` | `llm` `evaluation` `monitoring` `framework` |
| `mock-hsds-api` | `api` `flask` `mock` `hsds` |
| `ssh-check` | `infrastructure` `tools` `testing` |

---

#### 2.2 Унифицировать биографию везде

**ЕДИНАЯ ФОРМУЛИРОВКА:**
```
AI Systems Builder · Infrastructure & Assurance · 
Evidence-Driven Automation · Civic Tech · 
Relocation Intelligence · Agent Orchestration
```

**Где обновить:**

**A. Главный профиль (jobkubera-lab/README.md)**
- Строка 20 в текущем README:
```markdown
// ТЕКУЩЕЕ:
## AI Solutions Builder · AI Assurance & Infrastructure · KUBERA LAB · Agent Systems

// НОВОЕ:
## AI Systems Builder · Infrastructure & Assurance · Evidence-Driven Automation
```

**B. Описание репозитория (jobkubera-lab)**
- Settings → Description
```markdown
// ТЕКУЩЕЕ:
Profile repository for Nikola Kubera: AI-powered migration consultant with expertise in visas, job placement, and HR automation projects.

// НОВОЕ:
AI systems builder: agent orchestration, MCP, evidence ledger, civic tech, international relocation intelligence. GitHub portfolio & engineering records.
```

**C. Другие главные репо:**

`kubera-learning`:
```markdown
Learning path for AI engineers: Python, ML, LLMs, agents, local AI, evals, production systems. Public learning record for KUBERA AGENT OS development.
```

`kubera-improved-website`:
```markdown
Public prototypes: Civic Evidence OS, local intelligence, interactive mapping, community tools. Experimental public web projects.
```

`kubera-ai-prompts`:
```markdown
Reusable AI workflows: prompt systems, evidence chains, structured outputs, tool use patterns. Copy & adapt for your LLM.
```

---

### ЭТАП 3 — День 4-5 (новые стратегические репо)

#### 3.1 Создать 4 новых репо

**A. kubera-agent-os**
```
Описание: KUBERA AGENT OS — modular AI orchestration with model routing, 
skill DNA, permissions, evidence ledger and human control. 
Provider-neutral, locally-owned memory and policies.

Topics: ai-agents orchestration mcp python ai-assurance evidence-ledger

Базовый код:
- Скопировать: kubera-lab/agent-os-demo/ (файлы + структура)
- Скопировать: kubera-lab/innovation-stack/ (архитектура, визуализация)
- Скопировать: LICENSE (MIT, если нет — добавить)
- Скопировать: pyproject.toml (из innovation-stack/reference-implementation/)
- Скопировать: GitHub Actions workflow (из главного репо)

README должен содержать:
- Архитектуру из текущего README (Model Router, Skill DNA, Policy & Permissions и т.д.)
- Примеры кода (из agent-os-demo/)
- Статус: Beta
- Roadmap
```

**B. kubera-civic-evidence-os**
```
Описание: Evidence-first civic service navigator. 
Official sources, deterministic matching, privacy controls, verified results. 
Prototype for UK local authority service discovery.

Topics: civic-tech evidence local-services python javascript privacy

Базовый код:
- Скопировать: kubera-improved-website/civic-evidence-os/ (весь контент)
- Скопировать: LICENSE (MIT)
- Скопировать: .gitignore (Python + Node)
- Добавить: GitHub Actions для Python tests + JS parity.test.mjs

README должен содержать (уже есть там):
- Что это делает (детерминированное совпадение)
- Как устанавливать и запускать
- Trust rules и Safety principles
- Примеры (examples/01_basic_lookup.py и т.д.)
- Статус: Production-ready (v1.0)
```

**C. kubera-tender-intelligence**
```
Описание: UK procurement opportunity qualification with deterministic evidence, 
deadline intelligence, CPV matching, requirement verification and buyer history. 
Official read-only intake. Tender Intelligence v1.1+

Topics: procurement uk tenders evidence python automation

Базовый код:
- Скопировать: kubera-lab/tender-intelligence/ (весь контент)
- Скопировать: LICENSE (MIT)
- Скопировать: pyproject.toml
- Добавить: GitHub Actions для Python tests

README должен содержать:
- Что это делает (official UK procurement matching)
- Как использовать (примеры запросов)
- Источники данных
- Статус: Production (v1.1)
- Roadmap
```

**D. kubera-resi (из твоего ПК!)**
```
Описание: KUBERA RESI — AI-assisted real estate intelligence. 
Property research, due diligence, evidence gathering, structured comparison. 
v0.3 with model evaluation framework.

Topics: real-estate ai research evidence due-diligence python

Базовый код:
- Загрузить ВСЕ 38 файлов из C:\Users\user\KUBERA-TAO
- Использовать README, который уже написан в файле
- Скопировать LICENSE (MIT)
- Добавить: pyproject.toml (если нет)
- Добавить: .gitignore
- Добавить: GitHub Actions для tests

README должен содержать (уже есть!):
- Что это делает
- Статус: v0.3 Beta (готов к моделям оценки из SN46)
- Архитектура
- Примеры использования
- Roadmap
```

---

### ЭТАП 4 — День 5-6 (обновить главный профиль)

#### 4.1 Обновить главный README (с обходом боте-защиты!)

**ПРОЦЕДУРА ОБХОДА ЗАЩИТЫ:**

1. **Открыть Settings в главном репо**
2. **Перейти в Actions → Workflows**
3. **Найти "Profile README Lock"**
4. **Нажать на workflow → нажать "Disable workflow"**
5. **Выполнить все изменения README.md** (смотри ниже)
6. **После Commit & Push — включить workflow обратно**

**ИЗМЕНЕНИЯ В README.md:**

Строка 20:
```markdown
// ПЕРЕД:
## AI Solutions Builder · AI Assurance & Infrastructure · KUBERA LAB · Agent Systems

// ПОСЛЕ:
## AI Systems Builder · Infrastructure & Assurance · Evidence-Driven Automation
```

Строка 50 (усилить):
```markdown
// ДОБАВИТЬ:
**Currently strengthening:** Linux · networking · observability · incident analysis · 
AI infrastructure operations · AI governance and assurance · evidence systems · 
real-estate AI models.
```

Секция "✨ What I build" — ДОБАВИТЬ новые репо (строка ~109):
```markdown
- 🤖 **KUBERA AGENT OS** — modular orchestration, model routing, skill DNA, permissions, evidence ledger.
- 🏛️ **Civic Evidence OS** — official-source service navigation, deterministic matching, privacy controls.
- 📊 **Tender Intelligence** — UK procurement qualification, deadline intelligence, CPV matching, evidence tracking.
- 🏠 **KUBERA RESI** — property research, due diligence, structured comparison, AI evaluation.
```

Секция "🚀 Selected public projects" (строка ~171):
```markdown
- **[KUBERA AGENT OS](https://github.com/jobkubera-lab/kubera-agent-os)** — modular orchestration, model routing, skill DNA
- **[Civic Evidence OS](https://github.com/jobkubera-lab/kubera-civic-evidence-os)** — official-source service navigation
- **[Tender Intelligence](https://github.com/jobkubera-lab/kubera-tender-intelligence)** — UK procurement qualification
- **[KUBERA RESI](https://github.com/jobkubera-lab/kubera-resi)** — real estate intelligence & due diligence
```

---

## 🎯 ПРОВЕРОЧНЫЙ ЛИСТ

**После завершения всех работ:**

- [ ] `kubera-learning.` переименован в `kubera-learning`
- [ ] Descriptions добавлены в `kubera-local-ai2` и `ssh-check`
- [ ] Topics добавлены ко всем 18 репо
- [ ] Monero удален из главного профиля
- [ ] Биография унифицирована везде
- [ ] Созданы 4 новых репо:
  - [ ] `kubera-agent-os`
  - [ ] `kubera-civic-evidence-os`
  - [ ] `kubera-tender-intelligence`
  - [ ] `kubera-resi`
- [ ] Главный README обновлён (с обходом боте-защиты)
- [ ] Все ссылки в README проверены
- [ ] GitHub Actions включены обратно (если отключались)

---

## ⚠️ ЧТО НЕ ТРОГАТЬ

```
❌ НИКОГДА НЕ УДАЛЯТЬ:
- .devcontainer, design-system, fAIr, govuk-infrastructure, localgov_multilingual
- ПРИЧИНА: это форки, нужны для PR в NHS, GOV.UK, LocalGov

❌ НИКОГДА НЕ АРХИВИРОВАТЬ:
- kubera-real-estate-os (перейдёт в kubera-resi)
- kubera-learning (станет kubera-learning, отличный ресурс)

❌ НИКОГДА НЕ МЕНЯТЬ БЕЗ РАЗРЕШЕНИЯ:
- Tests и CI/CD workflows (они работают идеально)
- Лицензии MIT
- Криптографические подписи коммитов
```

---

## 📝 ИТОГО

**Время работы:** ~6-8 часов  
**Сложность:** Средняя  
**Главный риск:** Боте-защита профиля README (решается отключением/включением)  
**Результат:** Чистый, унифицированный портфолио с 4 стратегическими продуктами

---

**Готово для ChatGPT / Claude!** 🚀
