from flask import Flask, request, render_template_string
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# Показатели: (название, единица, мин, макс, [врачи при отклонении], примечание)
PARAMS = [
    {
        "key": "hemoglobin",
        "name": "Гемоглобин",
        "unit": "г/л",
        "low": 120,
        "high": 160,
        "doctors": ["терапевт", "гематолог"],
        "hint": "Частая усталость, бледность — возможная анемия.",
    },
    {
        "key": "leukocytes",
        "name": "Лейкоциты",
        "unit": "×10⁹/л",
        "low": 4.0,
        "high": 9.0,
        "doctors": ["терапевт", "гематолог", "инфекционист"],
        "hint": "Может указывать на воспаление или снижение иммунитета.",
    },
    {
        "key": "platelets",
        "name": "Тромбоциты",
        "unit": "×10⁹/л",
        "low": 180,
        "high": 320,
        "doctors": ["терапевт", "гематолог"],
        "hint": "Отклонения требуют внимания: риск кровотечений или тромбозов.",
    },
    {
        "key": "glucose",
        "name": "Глюкоза (натощак)",
        "unit": "ммоль/л",
        "low": 3.3,
        "high": 5.5,
        "doctors": ["эндокринолог", "терапевт"],
        "hint": "Повышенный уровень — повод проверить углеводный обмен.",
    },
    {
        "key": "cholesterol",
        "name": "Холестерин общий",
        "unit": "ммоль/л",
        "low": None,
        "high": 5.2,
        "doctors": ["кардиолог", "терапевт"],
        "hint": "Повышенный уровень связан с риском для сосудов и сердца.",
    },
    {
        "key": "tsh",
        "name": "ТТГ",
        "unit": "мМЕ/л",
        "low": 0.4,
        "high": 4.0,
        "doctors": ["эндокринолог"],
        "hint": "Отклонения могут говорить о работе щитовидной железы.",
    },
    {
        "key": "alt",
        "name": "АЛТ",
        "unit": "Ед/л",
        "low": None,
        "high": 41,
        "doctors": ["гастроэнтеролог", "терапевт"],
        "hint": "Повышение может указывать на нагрузку на печень.",
    },
    {
        "key": "creatinine",
        "name": "Креатинин",
        "unit": "мкмоль/л",
        "low": 62,
        "high": 115,
        "doctors": ["нефролог", "терапевт"],
        "hint": "Показатель работы почек.",
    },
]

IDX = """
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Трек физического здоровья</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
  .wrap { max-width: 900px; margin: 0 auto; padding: 28px 20px 60px; }
  h1 { font-size: 26px; margin-bottom: 6px; }
  .sub { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
  .note { background: #1e293b; border: 1px dashed #334155; border-radius: 12px; padding: 12px 16px;
    color: #94a3b8; font-size: 13px; margin-bottom: 22px; }
  form { background: #1e293b; border-radius: 16px; padding: 20px; }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
  label { display: block; font-size: 13px; color: #94a3b8; margin-bottom: 4px; }
  input { width: 100%; padding: 9px 12px; border-radius: 9px; border: 1px solid #334155;
    background: #0f172a; color: #e2e8f0; font-size: 15px; }
  input::placeholder { color: #475569; }
  button { margin-top: 10px; padding: 12px 24px; border-radius: 12px; border: none; cursor: pointer;
    background: linear-gradient(135deg,#2563eb,#0ea5e9); color: #fff; font-weight: 700; font-size: 15px; }
  .result { margin-top: 22px; }
  .card { background: #1e293b; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px;
    border-left: 5px solid #4ade80; }
  .card.warn { border-left-color: #f87171; }
  .card h3 { font-size: 16px; margin-bottom: 4px; }
  .card p { color: #94a3b8; font-size: 14px; }
  .doctor { display: inline-block; margin-top: 8px; margin-right: 6px; padding: 4px 12px; border-radius: 999px;
    background: rgba(56,189,248,.12); color: #38bdf8; font-size: 13px; }
  h2 { font-size: 19px; margin-bottom: 10px; }
  .empty { color: #64748b; text-align: center; padding: 30px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Трек физического здоровья</h1>
  <div class="sub">По данным анализов — первое представление, к какому врачу обратиться.</div>
  <div class="note">⚠️ Приложение учебное и НЕ ставит диагноз. Референсные диапазоны усреднены
    и зависят от возраста, пола и лаборатории. При отклонениях или жалобах — обязательно к врачу.</div>

  <form method="post">
    <div class="row">
      {% for p in params %}
        <div>
          <label>{{ p.name }} ({{ p.unit }})</label>
          <input type="text" name="{{ p.key }}" placeholder="норма: {{ p.low if p.low is not none else '—' }}–{{ p.high }}" value="{{ entered[p.key] if p.key in entered else '' }}">
        </div>
      {% endfor %}
    </div>
    <button type="submit">Показать, к какому врачу идти</button>
  </form>

  {% if result is not none %}
  <div class="result">
    {% if result.warnings %}
      <h2>Рекомендации по отклонениям</h2>
      {% for w in result.warnings %}
      <div class="card warn">
        <h3>{{ w.name }}: {{ w.value }} {{ w.unit }}</h3>
        <p>{{ w.hint }}</p>
        {% for d in w.doctors %}<span class="doctor">{{ d }}</span>{% endfor %}
      </div>
      {% endfor %}
      <div class="card">
        <h3>Итоговая рекомендация</h3>
        <p>{{ result.summary }}</p>
      </div>
    {% elif result.invalid %}
      <div class="card warn">
        <h3>Часть значений не удалось прочитать</h3>
        <p>Проверьте, что числа введены через точку или запятую, без букв: {{ result.invalid_name }}</p>
      </div>
    {% else %}
      <div class="card">
        <h3>Все показатели в пределах нормы</h3>
        <p>Для профилактики достаточно посещения терапевта раз в год.</p>
      </div>
    {% endif %}
    <div class="note">Напоминаем: результат не является медицинским заключением.</div>
  </div>
  {% endif %}
</div>
</body>
</html>
"""


def parse_value(v):
    if v is None or str(v).strip() == "":
        return None
    t = str(v).replace(",", ".").strip()
    try:
        return float(t)
    except ValueError:
        return "invalid"


@app.route("/", methods=["GET", "POST"])
def index():
    entered = {}
    result = None
    if request.method == "POST":
        warnings = []
        invalid = None
        for p in PARAMS:
            entered[p["key"]] = request.form.get(p["key"], "")
            val = parse_value(request.form.get(p["key"]))
            if val == "invalid":
                invalid = p
                break
            if val is None:
                continue
            bad_high = p["high"] is not None and val > p["high"]
            bad_low = p["low"] is not None and val < p["low"]
            if bad_high or bad_low:
                warn = dict(p)
                warn["value"] = val
                warnings.append(warn)
        if invalid:
            result = {"warnings": [], "invalid": True, "invalid_name": invalid["name"]}
        else:
            doctors = []
            for w in warnings:
                for d in w["doctors"]:
                    if d not in doctors:
                        doctors.append(d)
            if warnings:
                if len(doctors) == 1:
                    summary = f"Стоит начать с врача: {doctors[0]}."
                else:
                    summary = "Стоит посетить: " + ", ".join(doctors) + "."
            else:
                summary = ""
            result = {"warnings": warnings, "invalid": False, "summary": summary}
    return render_template_string(
        IDX, params=PARAMS, entered=entered, result=result, today=datetime.now().strftime("%Y-%m-%d")
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)