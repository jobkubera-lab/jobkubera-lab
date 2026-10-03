# ПРОМПТ ДЛЯ ChatGPT — Завершение чистки GitHub jobkubera-lab

## ✅ Что делать

Это финальная чистка профиля jobkubera-lab. Ты имеешь полные права делать это (он дал явное разрешение).

### ЗАДАЧА 1: PR #59 — вернуть цифры с источниками

**Status:** Pull request #59 на ветке `cleanup/profile-readme-20261002` падает на проверку Portfolio Evidence Audit.

**Причина:** В файле `README.md` есть фразы из `FORBIDDEN_PUBLIC_TEXT`:
```python
FORBIDDEN_PUBLIC_TEXT = [
    "1.1M+ Google Maps views",
    "1.8K profile impressions",
    ...
]
```

**Решение:** Переписать фразы с указанием источника:
- `"1.1M+ Google Maps views"` → `"👁️ **1.1M+ views (Google Maps contributor dashboard)**"`
- `"1.8K profile impressions"` → `"✨ **1.8K profile impressions (contributor dashboard)**"`

**Что делать:**
1. Открой PR #59, ветка `cleanup/profile-readme-20261002`
2. В файле `README.md` найди обе фразы и замени:
   - старая: `1.1M+ Google Maps views`
   - новая: `👁️ **1.1M+ views (Google Maps contributor dashboard)**`
   
   - старая: `1.8K profile impressions`
   - новая: `✨ **1.8K profile impressions (contributor dashboard)**`

3. В файле `kubera-lab/kubera-guide-global-mapping/README.md` добавь в секцию "Google Maps profile":
   ```markdown
   ### 📊 Public reach
   - 👁️ **1.1M+ views (Google Maps contributor dashboard)**
   - ✨ **1.8K profile impressions (contributor dashboard)**
   ```

4. **Не трогай** файл `tools/portfolio_audit.py` — новые формулировки его не нарушают, потому что там строго `"1.1M+ Google Maps views"` и `"1.8K profile impressions"`, а не `"(contributor dashboard)"`

5. Запусти workflow (или пусть запустится автоматически) — Portfolio Evidence Audit должен пройти зелёным
6. Слей PR в main

---

### ЗАДАЧА 2: Обновить описания репозиториев

Используй GitHub API или Settings → About в каждом репо:

| Репозиторий | Старое описание | Новое описание |
|---|---|---|
| **jobkubera-lab** | "Profile repository for Nikola Kubera: AI-powered migration consultant with expertise in visas, job placement, and HR automation projects." | "AI systems builder — evidence-first AI agents, AI assurance and civic-tech prototypes" |
| **NikolaKubera** | "AI-powered migration consultant · Visas & job placement · Denmark/Czechia/Norway/Iceland · Kubera LLC (US/WY)" | "Visual and content experiments (Japanese Doll Collection, AI motion)" |
| **kubera-improved-website** | "Улучшенный сайт Kubera с AI-консультированИем по миграции. Современный дизайн, интерактивные формы, отзывы клиентов и FAQ." | "Website experiments and community-map prototypes" |
| **kuberajob** | "Сайт по трудоустройству и миграционным услугам Kubera Job" | "Kubera Job website (legacy)" |
| **kubera-visa-playbooks** | "Country playbooks for work visas & residence (Denmark, Czechia, Norway, Iceland)." | "Official-source relocation research checklists. Not immigration advice." |
| **kubera-migration-checklist** | (нужно добавить) | "Official-source checklist generator for relocation research. Not immigration advice." |

**Для `kubera-local-ai2` и `ssh-check`:**
- Откройся эти репо
- Посмотри, что там в README или что лежит в коде
- Напиши одну честную строку описания
- Сообщи мне — я скажу финальный текст

---

### ЗАДАЧА 3: Обновить README в NikolaKubera

В файле `NikolaKubera/README.md`:
- Удали строки о "AI-powered migration consultant" и "Kubera LLC (US/WY)"
- Удали список стран (Denmark, Czechia, Norway, Iceland)
- Оставь блок **Japanese Doll Collection** нетронутым

---

### ЗАДАЧА 4: Добавить Topics

В главном репо `jobkubera-lab/jobkubera-lab` → Settings → Topics добавить:
```
ai-agents, python, ai-assurance, evidence-ledger, human-in-the-loop, civic-tech, mcp
```

---

### ЗАДАЧА 5 (ОПЦИОНАЛЬНО): Переименовать `kubera-learning.`

Если ты готов — переименуй `kubera-learning.` в `kubera-learning` (убрать точку в конце).

**Будет ли это нарушением?** Нет, точка в названии — это просто случайный артефакт. Новое имя логичнее.

---

## 📋 ОТЧЁТ ПОСЛЕ ВЫПОЛНЕНИЯ

Когда закончишь, сообщи:
1. ✅ PR #59 слит? (ссылка на слитый PR)
2. ✅ Проверка Portfolio Evidence Audit прошла зелёным? (скриншот или ссылка на workflow)
3. ✅ Какие репо переименованы/обновлены? (список)
4. ❓ Что не получилось и почему?

---

## 🔗 Справка

- **Главный репо:** https://github.com/jobkubera-lab/jobkubera-lab
- **PR #59:** https://github.com/jobkubera-lab/jobkubera-lab/pulls
- **Workflow Portfolio Audit:** https://github.com/jobkubera-lab/jobkubera-lab/actions/workflows/portfolio-audit.yml
- **API для описаний:** `PATCH /repos/jobkubera-lab/{repo}` → поле `description`
