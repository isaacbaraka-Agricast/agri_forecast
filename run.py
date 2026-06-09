import traceback
import sys

print("Python:", sys.version)
print("About to import app...")

try:
    import app as application
    print("Import OK")
    print("About to run...")
    application.app.run(debug=False, host='127.0.0.1', port=5000)
except SystemExit as e:
    print("SystemExit caught:", e)
    traceback.print_exc()
except Exception as e:
    print("Exception caught:", e)
    traceback.print_exc()
