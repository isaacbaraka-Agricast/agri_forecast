f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/android/app/src/main/AndroidManifest.xml","r",encoding="utf-8")
c=f.read()
f.close()
old='<manifest xmlns:android="http://schemas.android.com/apk/res/android">'
new='<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n    <uses-permission android:name="android.permission.INTERNET"/>\n    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>'
c=c.replace(old,new,1)
f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/android/app/src/main/AndroidManifest.xml","w",encoding="utf-8")
f.write(c)
f.close()
print("OK")
