with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = """            _ModelDropdown(
              value: _model,
              onChanged: (v) => setState(() => _model = v),
            ),
            const SizedBox(height: 12),
            _WeeksSlider(
              value: _weeks,
              onChanged: (v) => setState(() => _weeks = v),
            ),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _fetch,"""

new = """            _ModelDropdown(
              value: _model,
              onChanged: (v) => setState(() => _model = v),
            ),
            const SizedBox(height: 10),
            _MethodExplainCard(model: _model),
            const SizedBox(height: 12),
            _WeeksSlider(
              value: _weeks,
              onChanged: (v) => setState(() => _weeks = v),
            ),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _fetch,"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
