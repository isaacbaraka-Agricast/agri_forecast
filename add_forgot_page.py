with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = "class MainShell extends StatefulWidget {        // \xe2\x86\x90 add this"

new_page = """class ForgotPasswordPage extends StatefulWidget {
  const ForgotPasswordPage({super.key});
  @override
  State<ForgotPasswordPage> createState() => _ForgotPasswordState();
}

class _ForgotPasswordState extends State<ForgotPasswordPage> {
  final _phoneCtrl = TextEditingController();
  final _nameCtrl  = TextEditingController();
  final _passCtrl  = TextEditingController();
  final _formKey   = GlobalKey<FormState>();
  bool _loading = false;
  bool _obscure = true;
  String? _error, _success;

  Future<void> _reset() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() { _loading = true; _error = null; _success = null; });
    try {
      final d = await ApiService.post('/forgot_password', {
        'phone':       _phoneCtrl.text.trim(),
        'full_name':   _nameCtrl.text.trim(),
        'new_password': _passCtrl.text,
      }, requireAuth: false);
      if (d['status'] == 'success') {
        setState(() => _success = T.rw
            ? 'Ijambo ry\\'ibanga ryahinduwe! Injira nonaha.'
            : 'Password reset! You can now sign in.');
        Future.delayed(const Duration(seconds: 2),
            () => Navigator.pop(context));
      } else {
        setState(() => _error = d['message'] ?? (T.rw ? 'Habayeho ikosa' : 'Reset failed'));
      }
    } catch (_) {
      setState(() => _error = T.rw ? 'Ntibyashobotse guhuza na seriveri.' : 'Cannot connect to server.');
    }
    if (mounted) setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.rw ? 'Wibagiwe Ijambo ry\\'Ibanga' : 'Forgot Password'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(children: [
            const SizedBox(height: 10),
            const Text('\\u{1F511}', style: TextStyle(fontSize: 52)),
            const SizedBox(height: 12),
            Text(T.rw
                ? 'Andika nimero ya telefoni n\\'amazina yawe wujuje kugira ngo uhindure ijambo ry\\'ibanga'
                : 'Enter your phone number and full name to verify your identity',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 14, color: kMuted)),
            const SizedBox(height: 24),
            _FieldCard(children: [
              TextFormField(
                controller: _phoneCtrl,
                keyboardType: TextInputType.phone,
                decoration: InputDecoration(
                    labelText: T.phone,
                    hintText: '+250 7XX XXX XXX',
                    prefixIcon: const Icon(Icons.phone, color: kLeaf)),
                validator: (v) => (v == null || v.isEmpty) ? 'Enter phone number' : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _nameCtrl,
                decoration: InputDecoration(
                    labelText: T.fullName,
                    prefixIcon: const Icon(Icons.person, color: kLeaf)),
                textCapitalization: TextCapitalization.words,
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Enter full name' : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _passCtrl,
                obscureText: _obscure,
                decoration: InputDecoration(
                  labelText: T.rw ? 'Ijambo ry\\'ibanga rishya' : 'New Password',
                  prefixIcon: const Icon(Icons.lock, color: kLeaf),
                  suffixIcon: IconButton(
                    icon: Icon(_obscure ? Icons.visibility_outlined : Icons.visibility_off_outlined, color: kMuted),
                    onPressed: () => setState(() => _obscure = !_obscure),
                  ),
                ),
                validator: (v) => (v == null || v.length < 6) ? 'Minimum 6 characters' : null,
              ),
            ]),
            const SizedBox(height: 14),
            if (_error != null)   _ErrorBanner(_error!),
            if (_success != null) _SuccessBanner(_success!),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: _loading
                  ? const Center(child: CircularProgressIndicator(color: kSprout, strokeWidth: 3))
                  : ElevatedButton.icon(
                      onPressed: _reset,
                      icon: const Icon(Icons.lock_reset),
                      label: Text(T.rw ? 'Hindura Ijambo ry\\'Ibanga' : 'Reset Password'),
                    ),
            ),
            const SizedBox(height: 30),
          ]),
        ),
      ),
    );
  }
}

class MainShell extends StatefulWidget {        // \xe2\x86\x90 add this"""

if old in content:
    content = content.replace(old, new_page, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
