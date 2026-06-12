f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

old='from sklearn.metrics import mean_absolute_error, mean_squared_error'
new='from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score'
c=c.replace(old,new,1)

old='return {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "MAPE": round(mape, 2)}'
new='r2 = float(r2_score(actual, predicted))\n    return {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "MAPE": round(mape, 2), "R2": round(r2, 4)}'
c=c.replace(old,new,1)
print("OK" if "R2" in c else "FAILED")

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
