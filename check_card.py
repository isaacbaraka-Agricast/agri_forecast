f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

# Find the sector info card and replace its child content
start=c.find("if (_selectedSector != null) ...[")
end=c.find("],",start)+2
old_block=c[start:end]
print("Found block length:",len(old_block))
print("Last 100 chars:",repr(old_block[-100:]))
