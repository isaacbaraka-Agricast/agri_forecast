with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """            try:
                r = req.get(f"{base_url}/forecast/{cid}",
                            params={'model': 'ensemble', 'weeks': 12, 'farm_size': farm_size},
                            timeout=10)
                d = r.json()
                fa = d.get('farmer_advice', {})
                mk = d.get('market', {})
                metrics = d.get('metrics', {})
                summaries.append(
                    f"{cname}: grow {fa.get('farmer_target_kg','?')}kg, "
                    f"needs {fa.get('required_acres','?')} acres, "
                    f"expected income ~Rwf {round(fa.get('farmer_target_kg',0) * mk.get('avg_price',0))}, "
                    f"current price {mk.get('avg_price','?')} RWF/kg, "
                    f"market signal: {mk.get('signal','balanced')}, "
                    f"model accuracy: {metrics.get('accuracy_en','?')}, "
                    f"urgency: {fa.get('urgency','?')} ({fa.get('urgency_en','')})"
                )
            except Exception:
                continue"""

new = """            try:
                r = req.get(f"{base_url}/forecast/{cid}",
                            params={'model': 'ensemble', 'weeks': 12, 'farm_size': farm_size},
                            timeout=15)
                d = r.json()
                fa = d.get('farmer_advice', {})
                mk = d.get('market', {})
                metrics = d.get('metrics', {})
                summaries.append(
                    f"{cname}: grow {fa.get('farmer_target_kg','?')}kg, "
                    f"needs {fa.get('required_acres','?')} acres, "
                    f"expected income ~Rwf {round(fa.get('farmer_target_kg',0) * mk.get('avg_price',0))}, "
                    f"current price {mk.get('avg_price','?')} RWF/kg, "
                    f"market signal: {mk.get('signal','balanced')}, "
                    f"model accuracy: {metrics.get('accuracy_en','?')}, "
                    f"urgency: {fa.get('urgency','?')} ({fa.get('urgency_en','')})"
                )
            except Exception as e:
                summaries.append(f"{cname}: data unavailable ({str(e)[:80)})")
                continue"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
