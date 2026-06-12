f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

old='    mape = float(np.mean(np.abs((actual - predicted) / (actual + 1e-9))) * 100)\n    return {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "M'
print("found mape:", old[:50] in c)

# Find and replace the full return line
idx=c.find('return {"MAE": round(mae, 2), "RMSE": round(rmse, 2)')
end=c.find('}',idx)+1
print("return line:", repr(c[idx:end]))
