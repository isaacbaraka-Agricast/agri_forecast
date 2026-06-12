f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="            style: ElevatedButton.styleFrom(\n                backgroundColor: hasData ? kRed : kMuted,\n                foregroundColor: Colors.white,\n                padding: const EdgeInsets.symmetric(vertical: 16)),\n          ),\n        ),"

new="""            style: ElevatedButton.styleFrom(
                backgroundColor: hasData ? kForest : kMuted,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16)),
          ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: ElevatedButton.icon(
              onPressed: _generating ? null : () => _generatePdf(share: true),
              icon: const Icon(Icons.share),
              label: Text(T.rw ? 'Sangira' : 'Share'),
              style: ElevatedButton.styleFrom(
                backgroundColor: hasData ? kBlue : kMuted,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16)),
            ),
          ),
        ]),"""

if old in c:
    c=c.replace(old,new,1)
    print("SUCCESS")
else:
    print("FAILED")

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
