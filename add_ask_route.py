with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "if __name__ == '__main__':"

new_route = """@app.route('/ask', methods=['POST'])
def ask_assistant():
    try:
        import requests as req
        data       = request.get_json() or {}
        question   = data.get('question', '').strip()
        farm_size  = float(data.get('farm_size_acres', 1.0))
        sector     = data.get('sector', 'Muhoza')
        lang       = data.get('lang', 'en')
        if not question:
            return jsonify({"status": "error", "message": "Question is required"}), 400

        groq_key = os.environ.get('GROQ_API_KEY')
        if not groq_key:
            return jsonify({"status": "error", "message": "AI assistant not configured"}), 503

        crop_names = {1:'Irish Potato',2:'Maize',3:'Beans',4:'Tomato',5:'Sorghum',6:'Wheat',7:'Banana'}
        base_url = f"http://localhost:{os.environ.get('PORT', 5000)}"

        summaries = []
        for cid, cname in crop_names.items():
            try:
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
                continue

        data_block = "\\n".join(summaries)

        lang_instruction = (
            "Respond in Kinyarwanda." if lang == 'rw' else "Respond in English."
        )

        system_prompt = (
            "You are AgriCast's farm advisory assistant for Musanze District, Rwanda. "
            "You ONLY use the exact numbers provided below from the live forecasting system. "
            "NEVER invent or guess numbers not given to you. "
            "Be concise, practical, and speak directly to a farmer. "
            f"The farmer has {farm_size} acres in {sector} sector. "
            f"{lang_instruction}\\n\\n"
            f"LIVE FORECAST DATA (all 7 crops, this farmer's exact farm size):\\n{data_block}"
        )

        resp = req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            },
            timeout=30
        )
        result = resp.json()
        answer = result['choices'][0]['message']['content']

        return jsonify({"status": "success", "answer": answer})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':"""

if old in content:
    content = content.replace(old, new_route, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
