from flask import Flask, request, render_template_string
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# ╨Я╨╛╨║╨░╨╖╨░╤В╨╡╨╗╨╕: (╨╜╨░╨╖╨▓╨░╨╜╨╕╨╡, ╨╡╨┤╨╕╨╜╨╕╤Ж╨░, ╨╝╨╕╨╜, ╨╝╨░╨║╤Б, [╨▓╤А╨░╤З╨╕ ╨┐╤А╨╕ ╨╛╤В╨║╨╗╨╛╨╜╨╡╨╜╨╕╨╕], ╨┐╤А╨╕╨╝╨╡╤З╨░╨╜╨╕╨╡)
PARAMS = [
    {
        "key": "hemoglobin",
        "name": "╨У╨╡╨╝╨╛╨│╨╗╨╛╨▒╨╕╨╜",
        "unit": "╨│/╨╗",
        "low": 120,
        "high": 160,
        "doctors": ["╤В╨╡╤А╨░╨┐╨╡╨▓╤В", "╨│╨╡╨╝╨░╤В╨╛╨╗╨╛╨│"],
        "hint": "╨з╨░╤Б╤В╨░╤П ╤Г╤Б╤В╨░╨╗╨╛╤Б╤В╤М, ╨▒╨╗╨╡╨┤╨╜╨╛╤Б╤В╤М тАФ ╨▓╨╛╨╖╨╝╨╛╨╢╨╜╨░╤П ╨░╨╜╨╡╨╝╨╕╤П.",
    },
    {
        "key": "leukocytes",
        "name": "╨Ы╨╡╨╣╨║╨╛╤Ж╨╕╤В╤Л",
        "unit": "├Ч10тБ╣/╨╗",
        "low": 4.0,
        "high": 9.0,
        "doctors": ["╤В╨╡╤А╨░╨┐╨╡╨▓╤В", "╨│╨╡╨╝╨░╤В╨╛╨╗╨╛╨│", "╨╕╨╜╤Д╨╡╨║╤Ж╨╕╨╛╨╜╨╕╤Б╤В"],
        "hint": "╨Ь╨╛╨╢╨╡╤В ╤Г╨║╨░╨╖╤Л╨▓╨░╤В╤М ╨╜╨░ ╨▓╨╛╤Б╨┐╨░╨╗╨╡╨╜╨╕╨╡ ╨╕╨╗╨╕ ╤Б╨╜╨╕╨╢╨╡╨╜╨╕╨╡ ╨╕╨╝╨╝╤Г╨╜╨╕╤В╨╡╤В╨░.",
    },
    {
        "key": "platelets",
        "name": "╨в╤А╨╛╨╝╨▒╨╛╤Ж╨╕╤В╤Л",
        "unit": "├Ч10тБ╣/╨╗",
        "low": 180,
        "high": 320,
        "doctors": ["╤В╨╡╤А╨░╨┐╨╡╨▓╤В", "╨│╨╡╨╝╨░╤В╨╛╨╗╨╛╨│"],
        "hint": "╨Ю╤В╨║╨╗╨╛╨╜╨╡╨╜╨╕╤П ╤В╤А╨╡╨▒╤Г╤О╤В ╨▓╨╜╨╕╨╝╨░╨╜╨╕╤П: ╤А╨╕╤Б╨║ ╨║╤А╨╛╨▓╨╛╤В╨╡╤З╨╡╨╜╨╕╨╣ ╨╕╨╗╨╕ ╤В╤А╨╛╨╝╨▒╨╛╨╖╨╛╨▓.",
    },
    {
        "key": "glucose",
        "name": "╨У╨╗╤О╨║╨╛╨╖╨░ (╨╜╨░╤В╨╛╤Й╨░╨║)",
        "unit": "╨╝╨╝╨╛╨╗╤М/╨╗",
        "low": 3.3,
        "high": 5.5,
        "doctors": ["╤Н╨╜╨┤╨╛╨║╤А╨╕╨╜╨╛╨╗╨╛╨│", "╤В╨╡╤А╨░╨┐╨╡╨▓╤В"],
        "hint": "╨Я╨╛╨▓╤Л╤И╨╡╨╜╨╜╤Л╨╣ ╤Г╤А╨╛╨▓╨╡╨╜╤М тАФ ╨┐╨╛╨▓╨╛╨┤ ╨┐╤А╨╛╨▓╨╡╤А╨╕╤В╤М ╤Г╨│╨╗╨╡╨▓╨╛╨┤╨╜╤Л╨╣ ╨╛╨▒╨╝╨╡╨╜.",
    },
    {
        "key": "cholesterol",
        "name": "╨е╨╛╨╗╨╡╤Б╤В╨╡╤А╨╕╨╜ ╨╛╨▒╤Й╨╕╨╣",
        "unit": "╨╝╨╝╨╛╨╗╤М/╨╗",
        "low": None,
        "high": 5.2,
        "doctors": ["╨║╨░╤А╨┤╨╕╨╛╨╗╨╛╨│", "╤В╨╡╤А╨░╨┐╨╡╨▓╤В"],
        "hint": "╨Я╨╛╨▓╤Л╤И╨╡╨╜╨╜╤Л╨╣ ╤Г╤А╨╛╨▓╨╡╨╜╤М ╤Б╨▓╤П╨╖╨░╨╜ ╤Б ╤А╨╕╤Б╨║╨╛╨╝ ╨┤╨╗╤П ╤Б╨╛╤Б╤Г╨┤╨╛╨▓ ╨╕ ╤Б╨╡╤А╨┤╤Ж╨░.",
    },
    {
        "key": "tsh",
        "name": "╨в╨в╨У",
        "unit": "╨╝╨Ь╨Х/╨╗",
        "low": 0.4,
        "high": 4.0,
        "doctors": ["╤Н╨╜╨┤╨╛╨║╤А╨╕╨╜╨╛╨╗╨╛╨│"],
        "hint": "╨Ю╤В╨║╨╗╨╛╨╜╨╡╨╜╨╕╤П ╨╝╨╛╨│╤Г╤В ╨│╨╛╨▓╨╛╤А╨╕╤В╤М ╨╛ ╤А╨░╨▒╨╛╤В╨╡ ╤Й╨╕╤В╨╛╨▓╨╕╨┤╨╜╨╛╨╣ ╨╢╨╡╨╗╨╡╨╖╤Л.",
    },
    {
        "key": "alt",
        "name": "╨Р╨Ы╨в",
        "unit": "╨Х╨┤/╨╗",
        "low": None,
        "high": 41,
        "doctors": ["╨│╨░╤Б╤В╤А╨╛╤Н╨╜╤В╨╡╤А╨╛╨╗╨╛╨│", "╤В╨╡╤А╨░╨┐╨╡╨▓╤В"],
        "hint": "╨Я╨╛╨▓╤Л╤И╨╡╨╜╨╕╨╡ ╨╝╨╛╨╢╨╡╤В ╤Г╨║╨░╨╖╤Л╨▓╨░╤В╤М ╨╜╨░ ╨╜╨░╨│╤А╤Г╨╖╨║╤Г ╨╜╨░ ╨┐╨╡╤З╨╡╨╜╤М.",
    },
    {
        "key": "creatinine",
        "name": "╨Ъ╤А╨╡╨░╤В╨╕╨╜╨╕╨╜",
        "unit": "╨╝╨║╨╝╨╛╨╗╤М/╨╗",
        "low": 62,
        "high": 115,
        "doctors": ["╨╜╨╡╤Д╤А╨╛╨╗╨╛╨│", "╤В╨╡╤А╨░╨┐╨╡╨▓╤В"],
        "hint": "╨Я╨╛╨║╨░╨╖╨░╤В╨╡╨╗╤М ╤А╨░╨▒╨╛╤В╤Л ╨┐╨╛╤З╨╡╨║.",
    },
]

IDX = """
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>╨в╤А╨╡╨║ ╤Д╨╕╨╖╨╕╤З╨╡╤Б╨║╨╛╨│╨╛ ╨╖╨┤╨╛╤А╨╛╨▓╤М╤П</title>
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
  <h1>╨в╤А╨╡╨║ ╤Д╨╕╨╖╨╕╤З╨╡╤Б╨║╨╛╨│╨╛ ╨╖╨┤╨╛╤А╨╛╨▓╤М╤П</h1>
  <div class="sub">╨Я╨╛ ╨┤╨░╨╜╨╜╤Л╨╝ ╨░╨╜╨░╨╗╨╕╨╖╨╛╨▓ тАФ ╨┐╨╡╤А╨▓╨╛╨╡ ╨┐╤А╨╡╨┤╤Б╤В╨░╨▓╨╗╨╡╨╜╨╕╨╡, ╨║ ╨║╨░╨║╨╛╨╝╤Г ╨▓╤А╨░╤З╤Г ╨╛╨▒╤А╨░╤В╨╕╤В╤М╤Б╤П.</div>
  <div class="note">тЪая╕П ╨Я╤А╨╕╨╗╨╛╨╢╨╡╨╜╨╕╨╡ ╤Г╤З╨╡╨▒╨╜╨╛╨╡ ╨╕ ╨Э╨Х ╤Б╤В╨░╨▓╨╕╤В ╨┤╨╕╨░╨│╨╜╨╛╨╖. ╨а╨╡╤Д╨╡╤А╨╡╨╜╤Б╨╜╤Л╨╡ ╨┤╨╕╨░╨┐╨░╨╖╨╛╨╜╤Л ╤Г╤Б╤А╨╡╨┤╨╜╨╡╨╜╤Л
    ╨╕ ╨╖╨░╨▓╨╕╤Б╤П╤В ╨╛╤В ╨▓╨╛╨╖╤А╨░╤Б╤В╨░, ╨┐╨╛╨╗╨░ ╨╕ ╨╗╨░╨▒╨╛╤А╨░╤В╨╛╤А╨╕╨╕. ╨Я╤А╨╕ ╨╛╤В╨║╨╗╨╛╨╜╨╡╨╜╨╕╤П╤Е ╨╕╨╗╨╕ ╨╢╨░╨╗╨╛╨▒╨░╤Е тАФ ╨╛╨▒╤П╨╖╨░╤В╨╡╨╗╤М╨╜╨╛ ╨║ ╨▓╤А╨░╤З╤Г.</div>

  <form method="post">
    <div class="row">
      {% for p in params %}
        <div>
          <label>{{ p.name }} ({{ p.unit }})</label>
          <input type="text" name="{{ p.key }}" placeholder="╨╜╨╛╤А╨╝╨░: {{ p.low if p.low is not none else 'тАФ' }}тАУ{{ p.high }}" value="{{ entered[p.key] if p.key in entered else '' }}">
        </div>
      {% endfor %}
    </div>
    <button type="submit">╨Я╨╛╨║╨░╨╖╨░╤В╤М, ╨║ ╨║╨░╨║╨╛╨╝╤Г ╨▓╤А╨░╤З╤Г ╨╕╨┤╤В╨╕</button>
  </form>

  {% if result is not none %}
  <div class="result">
    {% if result.warnings %}
      <h2>╨а╨╡╨║╨╛╨╝╨╡╨╜╨┤╨░╤Ж╨╕╨╕ ╨┐╨╛ ╨╛╤В╨║╨╗╨╛╨╜╨╡╨╜╨╕╤П╨╝</h2>
      {% for w in result.warnings %}
      <div class="card warn">
        <h3>{{ w.name }}: {{ w.value }} {{ w.unit }}</h3>
        <p>{{ w.hint }}</p>
        {% for d in w.doctors %}<span class="doctor">{{ d }}</span>{% endfor %}
      </div>
      {% endfor %}
      <div class="card">
        <h3>╨Ш╤В╨╛╨│╨╛╨▓╨░╤П ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╨░╤Ж╨╕╤П</h3>
        <p>{{ result.summary }}</p>
      </div>
    {% elif result.invalid %}
      <div class="card warn">
        <h3>╨з╨░╤Б╤В╤М ╨╖╨╜╨░╤З╨╡╨╜╨╕╨╣ ╨╜╨╡ ╤Г╨┤╨░╨╗╨╛╤Б╤М ╨┐╤А╨╛╤З╨╕╤В╨░╤В╤М</h3>
        <p>╨Я╤А╨╛╨▓╨╡╤А╤М╤В╨╡, ╤З╤В╨╛ ╤З╨╕╤Б╨╗╨░ ╨▓╨▓╨╡╨┤╨╡╨╜╤Л ╤З╨╡╤А╨╡╨╖ ╤В╨╛╤З╨║╤Г ╨╕╨╗╨╕ ╨╖╨░╨┐╤П╤В╤Г╤О, ╨▒╨╡╨╖ ╨▒╤Г╨║╨▓: {{ result.invalid_name }}</p>
      </div>
    {% else %}
      <div class="card">
        <h3>╨Т╤Б╨╡ ╨┐╨╛╨║╨░╨╖╨░╤В╨╡╨╗╨╕ ╨▓ ╨┐╤А╨╡╨┤╨╡╨╗╨░╤Е ╨╜╨╛╤А╨╝╤Л</h3>
        <p>╨Ф╨╗╤П ╨┐╤А╨╛╤Д╨╕╨╗╨░╨║╤В╨╕╨║╨╕ ╨┤╨╛╤Б╤В╨░╤В╨╛╤З╨╜╨╛ ╨┐╨╛╤Б╨╡╤Й╨╡╨╜╨╕╤П ╤В╨╡╤А╨░╨┐╨╡╨▓╤В╨░ ╤А╨░╨╖ ╨▓ ╨│╨╛╨┤.</p>
      </div>
    {% endif %}
    <div class="note">╨Э╨░╨┐╨╛╨╝╨╕╨╜╨░╨╡╨╝: ╤А╨╡╨╖╤Г╨╗╤М╤В╨░╤В ╨╜╨╡ ╤П╨▓╨╗╤П╨╡╤В╤Б╤П ╨╝╨╡╨┤╨╕╤Ж╨╕╨╜╤Б╨║╨╕╨╝ ╨╖╨░╨║╨╗╤О╤З╨╡╨╜╨╕╨╡╨╝.</div>
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
                    summary = f"╨б╤В╨╛╨╕╤В ╨╜╨░╤З╨░╤В╤М ╤Б ╨▓╤А╨░╤З╨░: {doctors[0]}."
                else:
                    summary = "╨б╤В╨╛╨╕╤В ╨┐╨╛╤Б╨╡╤В╨╕╤В╤М: " + ", ".join(doctors) + "."
            else:
                summary = ""
            result = {"warnings": warnings, "invalid": False, "summary": summary}
    return render_template_string(
        IDX, params=PARAMS, entered=entered, result=result, today=datetime.now().strftime("%Y-%m-%d")
    )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
