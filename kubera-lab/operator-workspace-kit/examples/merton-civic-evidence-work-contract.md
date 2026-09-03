# Example WorkContract — Merton Civic Evidence OS

Реальный тип задачи: расширение controlled service catalogue и сохранение parity между Python lookup и browser demo.

## Job

Добавить новые Merton service routes в существующий controlled catalogue, покрыть их тестами и убедиться, что browser finder возвращает те же conservative decisions, что Python logic.

## Sources

- текущий код `civic-evidence-os`;
- только проверяемые официальные страницы `merton.gov.uk` для service URLs;
- существующие unit/parity tests как regression source.

Перед утверждением URL или статуса источник перечитывается заново.

## Judgment

Можно самостоятельно решать структуру catalogue entry и тест-кейсов при сохранении текущей deterministic matching model. Любая неоднозначность должна давать fallback, а не выдуманную eligibility decision.

`Done` = catalogue обновлён, tests проходят, Python/JS parity сохранена, README описывает только фактически реализованный scope.

## Output

- изменённый controlled catalogue;
- regression tests;
- browser parity check;
- краткий diff/report с источниками.

## Forbidden

- не имитировать Merton Council;
- не принимать решения о праве/eligibility;
- не отправлять формы и не выполнять действия от имени жителя;
- не придумывать official URLs;
- не хранить raw sensitive resident query без необходимости;
- не менять проекты вне согласованного Civic Evidence scope.

## Example handoff status

`complete` только после прохождения tests/parity. Если официальный source не подтверждён — `partial` или `blocked`, но не «готово».
