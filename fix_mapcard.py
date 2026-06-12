f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

start=c.find("if (_selectedSector != null) ...[")
end=c.find("],",start)+2

new_block="""if (_selectedSector != null) ...[
          const SizedBox(height: 10),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: kSprout.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: kSprout.withValues(alpha: 0.25)),
            ),
            child: _sectorLoading
              ? const Center(child: CircularProgressIndicator())
              : _sectorData == null
                ? Text('Sector: $_selectedSector', style: const TextStyle(fontWeight: FontWeight.w700, color: kForest))
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(children: [
                        const Text('📍', style: TextStyle(fontSize: 18)),
                        const SizedBox(width: 8),
                        Expanded(child: Text('$_selectedSector • ${_sectorData!["zone"]}',
                            style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 13, color: kForest))),
                      ]),
                      const SizedBox(height: 8),
                      Text(T.rw ? 'Ibihingwa byiza:' : 'Best crops here:',
                          style: const TextStyle(fontSize: 11, color: kMuted)),
                      const SizedBox(height: 4),
                      Wrap(spacing: 6, children: [
                        for (final crop in (_sectorData!["best_crops"] as List))
                          Chip(
                            label: Text(crop.toString(), style: const TextStyle(fontSize: 11, color: Colors.white)),
                            backgroundColor: kForest,
                            padding: EdgeInsets.zero,
                            materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                          ),
                      ]),
                      const SizedBox(height: 8),
                      Text(T.rw ? _sectorData!["tip_rw"] : _sectorData!["tip_en"],
                          style: const TextStyle(fontSize: 12, color: kMuted)),
                    ],
                  ),
          ),
        ],"""

c=c[:start]+new_block+c[end:]
f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
print("SUCCESS")
