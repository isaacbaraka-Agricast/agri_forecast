with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "rb") as f:
    content = f.read()

old = b"class MainShell extends StatefulWidget {        // \xe2\x86\x90 add this"

new_page = b"""class ForgotPasswordPage extends StatefulWidget {\r
  const ForgotPasswordPage({super.key});\r
  @override\r
  State<ForgotPasswordPage> createState() => _ForgotPasswordState();\r
}\r
\r
class _ForgotPasswordState extends State<ForgotPasswordPage> {\r
  final _phoneCtrl = TextEditingController();\r
  final _nameCtrl  = TextEditingController();\r
  final _passCtrl  = TextEditingController();\r
  final _formKey   = GlobalKey<FormState>();\r
  bool _loading = false;\r
  bool _obscure = true;\r
  String? _error, _success;\r
\r
  Future<void> _reset() async {\r
    if (!_formKey.currentState!.validate()) return;\r
    setState(() { _loading = true; _error = null; _success = null; });\r
    try {\r
      final d = await ApiService.post('/forgot_password', {\r
        'phone':       _phoneCtrl.text.trim(),\r
        'full_name':   _nameCtrl.text.trim(),\r
        'new_password': _passCtrl.text,\r
      }, requireAuth: false);\r
      if (d['status'] == 'success') {\r
        setState(() => _success = T.rw\r
            ? "Ijambo ry'ibanga ryahinduwe! Injira nonaha."\r
            : 'Password reset! You can now sign in.');\r
        Future.delayed(const Duration(seconds: 2),\r
            () => Navigator.pop(context));\r
      } else {\r
        setState(() => _error = d['message'] ?? (T.rw ? 'Habayeho ikosa' : 'Reset failed'));\r
      }\r
    } catch (_) {\r
      setState(() => _error = T.rw ? 'Ntibyashobotse guhuza na seriveri.' : 'Cannot connect to server.');\r
    }\r
    if (mounted) setState(() => _loading = false);\r
  }\r
\r
  @override\r
  Widget build(BuildContext context) {\r
    return Scaffold(\r
      appBar: AppBar(\r
        title: Text(T.rw ? "Wibagiwe Ijambo ry'Ibanga" : 'Forgot Password'),\r
        leading: IconButton(\r
          icon: const Icon(Icons.arrow_back_ios_new),\r
          onPressed: () => Navigator.pop(context),\r
        ),\r
      ),\r
      body: SingleChildScrollView(\r
        padding: const EdgeInsets.all(20),\r
        child: Form(\r
          key: _formKey,\r
          child: Column(children: [\r
            const SizedBox(height: 10),\r
            const Text('\\u{1F511}', style: TextStyle(fontSize: 52)),\r
            const SizedBox(height: 12),\r
            Text(T.rw\r
                ? "Andika nimero ya telefoni n'amazina yawe wujuje kugira ngo uhindure ijambo ry'ibanga"\r
                : 'Enter your phone number and full name to verify your identity',\r
                textAlign: TextAlign.center,\r
                style: const TextStyle(fontSize: 14, color: kMuted)),\r
            const SizedBox(height: 24),\r
            _FieldCard(children: [\r
              TextFormField(\r
                controller: _phoneCtrl,\r
                keyboardType: TextInputType.phone,\r
                decoration: InputDecoration(\r
                    labelText: T.phone,\r
                    hintText: '+250 7XX XXX XXX',\r
                    prefixIcon: const Icon(Icons.phone, color: kLeaf)),\r
                validator: (v) => (v == null || v.isEmpty) ? 'Enter phone number' : null,\r
              ),\r
              const SizedBox(height: 14),\r
              TextFormField(\r
                controller: _nameCtrl,\r
                decoration: InputDecoration(\r
                    labelText: T.fullName,\r
                    prefixIcon: const Icon(Icons.person, color: kLeaf)),\r
                textCapitalization: TextCapitalization.words,\r
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Enter full name' : null,\r
              ),\r
              const SizedBox(height: 14),\r
              TextFormField(\r
                controller: _passCtrl,\r
                obscureText: _obscure,\r
                decoration: InputDecoration(\r
                  labelText: T.rw ? "Ijambo ry'ibanga rishya" : 'New Password',\r
                  prefixIcon: const Icon(Icons.lock, color: kLeaf),\r
                  suffixIcon: IconButton(\r
                    icon: Icon(_obscure ? Icons.visibility_outlined : Icons.visibility_off_outlined, color: kMuted),\r
                    onPressed: () => setState(() => _obscure = !_obscure),\r
                  ),\r
                ),\r
                validator: (v) => (v == null || v.length < 6) ? 'Minimum 6 characters' : null,\r
              ),\r
            ]),\r
            const SizedBox(height: 14),\r
            if (_error != null)   _ErrorBanner(_error!),\r
            if (_success != null) _SuccessBanner(_success!),\r
            const SizedBox(height: 20),\r
            SizedBox(\r
              width: double.infinity,\r
              child: _loading\r
                  ? const Center(child: CircularProgressIndicator(color: kSprout, strokeWidth: 3))\r
                  : ElevatedButton.icon(\r
                      onPressed: _reset,\r
                      icon: const Icon(Icons.lock_reset),\r
                      label: Text(T.rw ? "Hindura Ijambo ry'Ibanga" : 'Reset Password'),\r
                    ),\r
            ),\r
            const SizedBox(height: 30),\r
          ]),\r
        ),\r
      ),\r
    );\r
  }\r
}\r
\r
class MainShell extends StatefulWidget {        // \xe2\x86\x90 add this"""

if old in content:
    content = content.replace(old, new_page, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "wb") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
