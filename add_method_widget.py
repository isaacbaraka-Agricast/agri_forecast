with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = """/// Model dropdown
class _ModelDropdown extends StatelessWidget {"""

new = """/// Method explanation card — shown under the model dropdown
const Map<String, Map<String, String>> kMethodExplain = {
  'arima': {
    'icon': '📉',
    'title_en': 'ARIMA — Statistical',
    'title_rw': 'ARIMA — Imibare',
    'text_en': 'Looks at past patterns and seasonal cycles in the data to predict what comes next. Works well for crops with steady, repeating demand.',
    'text_rw': "Irebera ku byagenze mu bihe byashize n'ibisanzwe bisubiramo mu mwaka kugira ngo iteganye ibizaba. Ikora neza ku bihingwa bifite ibisabwa bihoraho kandi bisubiramo.",
  },
  'randomforest': {
    'icon': '🌳',
    'title_en': 'Random Forest — Machine Learning',
    'title_rw': "Ishyamba ry'Uburumbu — Ikoranabuhanga",
    'text_en': 'Combines many small decision rules learned from past data to make one strong prediction. Handles sudden changes in demand well.',
    'text_rw': "Ihuza amategeko menshi mato yigiriwe ku makuru yashize kugira ngo igere ku iteganyabikorwa rimwe rikomeye. Ikora neza iyo ibisabwa byahindutse vuba.",
  },
  'lstm': {
    'icon': '🧠',
    'title_en': 'LSTM — Deep Learning',
    'title_rw': "LSTM — Kwiga Byimbitse",
    'text_en': 'A neural network that remembers long sequences of past demand to spot complex trends humans might miss. Needs more data to be accurate.',
    'text_rw': "Ni uburyo bw'ubwenge bw'ikoranabuhanga bwibuka uruhererekane rurerure rw'ibisabwa byashize kugira ngo rumenye imigendekere igoye. Bisaba amakuru menshi kugira ngo bibe nyabwo.",
  },
  'ensemble': {
    'icon': '⚖️',
    'title_en': 'Ensemble — Combined',
    'title_rw': 'Ensemble — Bivanze',
    'text_en': 'Averages the predictions of all four methods together. Usually more stable than any single method, but not always the most accurate per crop.',
    'text_rw': "Ifatanya iteganyabikorwa ry'uburyo bune hamwe rikabarwa impuzandengo. Akenshi iba ihamye kurusha uburyo bumwe, ariko si ko buri gihe iba ari yo nziza ku gihingwa runaka.",
  },
};

class _MethodExplainCard extends StatelessWidget {
  final String model;
  const _MethodExplainCard({required this.model});
  @override
  Widget build(BuildContext context) {
    final ex = kMethodExplain[model] ?? kMethodExplain['ensemble']!;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: kSprout.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: kSprout.withValues(alpha: 0.25)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(ex['icon']!, style: const TextStyle(fontSize: 18)),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(T.rw ? ex['title_rw']! : ex['title_en']!,
                    style: const TextStyle(
                        fontSize: 12.5, fontWeight: FontWeight.w700, color: kForest)),
                const SizedBox(height: 3),
                Text(T.rw ? ex['text_rw']! : ex['text_en']!,
                    style: const TextStyle(
                        fontSize: 11.5, color: kMuted, height: 1.35)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// Model dropdown
class _ModelDropdown extends StatelessWidget {"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
