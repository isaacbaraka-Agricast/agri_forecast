f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="                _InfoRow(Icons.agriculture, T.rw ? 'Farm Size' : 'Farm Size', '${UserSession.farmSizeAcres.toStringAsFixed(1)} acres'),\n              ],\n            ),\n          ),\n        ),"

new="""                _InfoRow(Icons.agriculture, T.rw ? 'Ingano y\\'Inzara' : 'Farm Size', '${UserSession.farmSizeAcres.toStringAsFixed(1)} acres'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Farm size editor
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: kSprout.withValues(alpha: 0.08),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: kSprout.withValues(alpha: 0.25)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                const Icon(Icons.edit, size: 16, color: kForest),
                const SizedBox(width: 6),
                Text(T.rw ? 'Hindura Ingano y\\'Inzara' : 'Update Farm Size',
                    style: const TextStyle(fontWeight: FontWeight.w700, color: kForest)),
              ]),
              const SizedBox(height: 12),
              Row(children: [
                Expanded(
                  child: TextField(
                    controller: _farmCtrl,
                    keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    decoration: InputDecoration(
                      labelText: T.rw ? 'Ingano (hectare)' : 'Size (acres)',
                      suffixText: T.rw ? 'ac' : 'acres',
                      border: const OutlineInputBorder(),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                ElevatedButton(
                  onPressed: _saving ? null : _saveFarmSize,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: kForest,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                  ),
                  child: _saving
                      ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : Text(T.rw ? 'Bika' : 'Save'),
                ),
              ]),
            ],
          ),
        ),"""

if old in c:
    c=c.replace(old,new,1)
    print("OK")
else:
    print("FAILED")

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
