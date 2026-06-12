// =============================================================
// main.dart — Agri Forecast System v7.0
// Automated Demand Forecasting — Musanze District, Rwanda
// Author : BARAKA ISAAC (2305000514)
// Supervisor: Dr MUSABE JEAN BOSCO
// University of Kigali — School of Computing & IT — BBIT 2026
// =============================================================
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_map/flutter_map.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:latlong2/latlong.dart';
import 'package:fl_chart/fl_chart.dart';
// =============================================================
// COLORS (must be AFTER imports)
// =============================================================

const Color kLeaf    = Color(0xFF2E7D32);
const Color kSprout  = Color(0xFF66BB6A);
const Color kRed     = Color(0xFFE53935);
const Color kAmber   = Color(0xFFFFA000);
const Color kLime    = Color(0xFFCDDC39);
const Color kSkyPale = Color(0xFFE3F2FD);
const Color kStraw   = Color(0xFFFFB74D);
const Color kBlue    = Color(0xFF1565C0);
const Color kText    = Color(0xFF1B1B1B);
const Color kBg      = Color(0xFFFFFFFF);
const Color kCard    = Color(0xFFFFFFFF);
const Color kForest  = Color(0xFF0F1F0F);
const Color kMuted   = Color(0xFF567056);
const Color kBorder  = Color(0xFFD0E0D0);
void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
  ));
  runApp(const AgriForecastApp());
}

// =============================================================
//  CONFIG & CONSTANTS
// =============================================================
const String _apiBase = 'https://agriforecast-production.up.railway.app';
  
// =============================================================
//  TRANSLATION ENGINE
// =============================================================
class T {
  static bool rw = false;
  static void toggle() => rw = !rw;

  static String s(String en, String kiny) => rw ? kiny : en;

  static String get appName       => s('Agri Forecast',              'Agri Sisitemu');
  static String get tagline       => s('Smart Farming · Musanze',    'Ubuhinzi Bwiza · Musanze');
  static String get home          => s('Home',                       'Ahabanza');
  static String get forecast      => s('Forecast',                   'Iteganyabikorwa');
  static String get price         => s('Price',                      'Igiciro');
  static String get compare       => s('Compare',                    'Gereranya');
  static String get market        => s('Market',                     'Isoko');
  static String get alerts        => s('Alerts',                     'Imenyesha');
  static String get seasonal      => s('Seasonal',                   'Ibihe');
  static String get history       => s('History',                    'Amasoko');
  static String get selectCrop    => s('Select Crop',                'Hitamo Igihingwa');
  static String get selectModel   => s('Select Model',               'Hitamo Indorerezi');
  static String get loading       => s('Loading…',                   'Gutegereza…');
  static String get error         => s('Error occurred',             'Habaye ikosa');
  static String get getForecast   => s('Run Forecast',               'Gena Iteganyabikorwa');
  static String get getPrice      => s('Get Price Forecast',         'Bona Igiciro');
  static String get runCompare    => s('Run Comparison',             'Gereranya');
  static String get week          => s('Week',                       'Icyumweru');
  static String get advice        => s('Farmer Advice',              "Inama z'Umuhinzi");
  static String get fullName      => s('Full Name',                  'Amazina Yose');
  static String get phone         => s('Phone Number',               'Nomero ya Telefoni');
  static String get password      => s('Password',                   'Ijambo ry\'Ibanga');
  static String get signIn        => s('Sign In',                    'Injira');
  static String get signUp        => s('Create Account',             'Iyandikishe');
  static String get noAccount     => s('No account?',                'Nta konti?');
  static String get hasAccount    => s('Have an account?',           'Ufite konti?');
  static String get logout        => s('Logout',                     'Sohoka');
  static String get role          => s('Role',                       'Uruhare');
  static String get weeksAhead    => s('Weeks Ahead',                'Ibyumweru Bizaza');
  static String get bestSell      => s('Best Sell',                  'Igihe Cyiza');
  static String get maxPrice      => s('Peak Price',                 'Igiciro Kinini');
  static String get sector        => s('Sectors',                    'Inzego');
  static String get refresh       => s('Refresh',                    'Vugurura');
  static String get reports          => s('Reports',                    'Raporo');
static String get profile          => s('Profile',                    'Umwirondoro');
static String get generatePdf      => s('Generate PDF Report',        'Kora Raporo ya PDF');
static String get generating       => s('Generating…',               'Gutegura…');
static String get reportConfig     => s('Report Configuration',       'Ibizashyirwa mu Raporo');
static String get reportConfigSub  => s('Choose crop, model and weeks to include', 'Hitamo igihingwa, indorerezi n\'ibyumweru');
static String get reportContents   => s('Report Contents',            'Ibizashyirwa mu Raporo');
static String get demandTable      => s('Demand Forecast Table',      'Iteganyabikorwa ry\'Ibyo Bisabwa');
static String get priceTable       => s('Price Forecast Table',       'Iteganyabikorwa ry\'Igiciro');
static String get seasonAdvice     => s('Season & Advice',            'Ibihe n\'Inama');
static String get farmerTips       => s('Farmer tips & best-sell timing', 'Inama z\'umuhinzi');
static String get modelMetrics     => s('Model Metrics',              'Imibare y\'Indorerezi');
static String get pdfSaveInfo      => s('The PDF report can be saved to your device, shared, or printed directly.', 'Raporo ya PDF irashobora gusohoka kuri telefoni cyangwa gusohokeshwa kuri porinteri.');
static String get accountDetails   => s('Account Details',            'Amakuru y\'Konti');
static String get fullNameLbl      => s('Full Name',                  'Amazina');
static String get phoneLbl         => s('Phone',                      'Telefoni');
static String get roleLbl          => s('Role',                       'Uruhare');
static String get sectorLbl        => s('Sector',                     'Inzego');
static String get systemInfo       => s('System Info',                'Amakuru ya Sisitemu');
static String get about            => s('About',                      'Ibyerekeye App');
static String get cropsLbl         => s('Crops',                      'Ibihingwa');
static String get modelsLbl        => s('Models',                     'Indorerezi');
static String get demandHigh       => s('High Demand Expected',       'Isoko Rinshi Ry\'iteganywa');
static String get demandLow        => s('Low Demand Warning',         'Icyemezo: Isoko Riguye');
static String get demandStable     => s('Demand Stable This Week',    'Isoko Ry\'ubu Ryiringaniye');
static String get weeksAheadFull   => s('weeks ahead',                'ibyumweru bizaza');
static String get reportsBanner    => s('Generate PDF forecast & price reports', 'Kora raporo ya PDF y\'iteganyabikorwa');
  static String get cropPortfolio => s('Crop Portfolio',             'Ibihingwa bya Musanze');
  static String get marketSnap    => s('Market Snapshot',            "Amakuru y'Isoko");
  static String get overview      => s('Overview',                   'Ahabanza');
  static String get seasonA       => s('Season A · Sep–Feb',         'Igihe A · Nzeri–Gashyantare');
  static String get seasonB       => s('Season B · Mar–Jun',         'Igihe B · Werurwe–Kamena');
  static String get seasonC       => s('Season C · Jul–Aug',         'Igihe C · Nyakanga–Kanama');
  static String get plantingReco     => s('Planting Recommendation',        'Inama yo Gutera');
static String get peakMarketDemand => s('Peak Market Demand',             'Isoko Rinini Ryiteganywa');
static String get plantKg          => s('Plant (kg)',                     'Gutera (kg)');
static String get bags50kg         => s('50kg Bags',                      'Amasashi 50kg');
static String get weeksLeft        => s('Weeks Left',                     'Ibyumweru Bisigaye');
static String get untilPeak        => s('until peak',                     'kugeza ku isoko');
static String get toPrep           => s('to prepare',                     'agomba gutegurwa');
static String get inclBuffer       => s('incl. 25% buffer',               'hamwe na buffer ya 25%');
static String get whenToPlant      => s('When to Plant',                  'Igihe cyo Gutera');
static String get gotIt            => s('Got it',                         'Byumvikane');
static String get plantingUrgent   => s('Buy from market now — not enough time to grow',
                                        'Banza uguze aho bihari — nta gihe gihagije cyo gutera');
static String get plantNow         => s('Plant immediately!',             'Tera ubu ako kanya!');
static String get plantSoon        => s('Plant within 2–3 weeks',         'Tera mu byumweru 2–3 bizaza');
static String get plantLater       => s('You have time — plant within 1–2 months',
                                        'Ufite igihe gihagije — tera mu mezi 1–2');
static String get targetSupply     => s('Target supply note',             'Intego y\'Umusaruro');
static String get postHarvestNote  => s(
    'This includes 20% post-harvest loss buffer.',
    'Ibi birimo 20% ibaziwe nyuma yo gusarura.');
static String get peakWeekLabel    => s('Week',                           'Icyumweru');
static String get inclLoss         => s('incl. 20% loss',                 'hamwe na 20% babireka');
}

// =============================================================
//  CROP & MODEL DATA
// =============================================================
class CropInfo {
  final int id;
  final String en, rw, icon;
  final Color color;
  const CropInfo(this.id, this.en, this.rw, this.icon, this.color);
  String get name => T.rw ? rw : en;
}

const List<CropInfo> kCrops = [
  CropInfo(1, 'Irish Potato', 'Ibirayi',    '🥔', Color(0xFF8B6914)),
  CropInfo(2, 'Maize',        'Ibigori',    '🌽', Color(0xFFD4A017)),
  CropInfo(3, 'Beans',        'Ibishyimbo', '🫘', Color(0xFF6D4C41)),
  CropInfo(4, 'Tomato',       'Inyanya',    '🍅', Color(0xFFC0392B)),
  CropInfo(5, 'Sorghum',      'Isorgho',    '🌾', Color(0xFF29A329)),
  CropInfo(6, 'Bananas',      'Umuneke',    '🍌', Color(0xFFE67E22)),
  CropInfo(7, 'Wheat',        'Ingano',     '🌾', Color(0xFFD4A017)),
];

const List<Map<String, String>> kModels = [
  {'value': 'arima',        'en': 'ARIMA — Statistical',  'rw': 'ARIMA'},
  {'value': 'randomforest', 'en': 'Random Forest — ML',   'rw': "Ishyamba ry'Uburumbu"},
  {'value': 'lstm',         'en': 'LSTM — Deep Learning', 'rw': 'LSTM (Kwiga Igihe)'},
  {'value': 'ensemble',     'en': 'Ensemble — Best',      'rw': 'Ensemble (Nziza)'},
];
const Map<String, Color> kModelColors = {
  'arima':        Color(0xFF1A6E1A),
  'randomforest': Color(0xFF2471A3),
  'lstm':         Color(0xFF8E44AD),
  'ensemble':     Color(0xFFC0392B),
};

CropInfo cropById(int id) => kCrops.firstWhere(
    (c) => c.id == id, orElse: () => kCrops.first);

// =============================================================
//  API SERVICE
// =============================================================
class ApiService {
  static String? _token;

  static void setToken(String token) => _token = token;
  static void clearToken() => _token = null;

  static Map<String, String> _headers({bool withAuth = true}) {
    final h = <String, String>{'Content-Type': 'application/json'};
    if (withAuth && _token != null) {
      h['Authorization'] = 'Bearer $_token';
    }
    return h;
  }

  static Future<Map<String, dynamic>> get(
    String path, {
    bool requireAuth = true,
  }) async {
    final res = await http
        .get(
          Uri.parse('$_apiBase$path'),
          headers: _headers(withAuth: requireAuth),
        )
        .timeout(const Duration(seconds: 30));

    if (res.statusCode == 401) {
      throw Exception('Session expired. Please log in again.');
    }

    if (res.statusCode != 200) {
      throw Exception('HTTP ${res.statusCode}');
    }

    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  static Future<Map<String, dynamic>> post(
    String path,
    Map<String, dynamic> body, {
    bool requireAuth = false,
  }) async {
    final res = await http
        .post(
          Uri.parse('$_apiBase$path'),
          headers: _headers(withAuth: requireAuth),
          body: jsonEncode(body),
        )
        .timeout(const Duration(seconds: 30));

    if (res.statusCode == 401) {
      throw Exception('Session expired. Please log in again.');
    }

    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}

// =============================================================
//  HELPERS
// =============================================================
String fmtNum(num v) {
  if (v >= 1000000) return '${(v / 1000000).toStringAsFixed(1)}M';
  if (v >= 1000)    return '${(v / 1000).toStringAsFixed(0)}k';
  return v.round().toString();
}

String fmtFull(num v) {
  final s = v.round().toString();
  final buf = StringBuffer();
  for (int i = 0; i < s.length; i++) {
    if (i > 0 && (s.length - i) % 3 == 0) buf.write(',');
    buf.write(s[i]);
  }
  return buf.toString();
}

String seasonLabel(String s) => switch (s) {
  'A' => T.seasonA,
  'B' => T.seasonB,
  'C' => T.seasonC,
  _   => 'Unknown',
};

Color seasonColor(String s) => switch (s) {
  'A' => kLeaf,
  'B' => kStraw,
  'C' => kRed,
  _   => kMuted,
};

String _season(int month) {
  if (month >= 9 || month <= 2) return 'A';
  if (month <= 6) return 'B';
  return 'C';
}

// =============================================================
//  THEME
// =============================================================
ThemeData buildTheme() => ThemeData(
  useMaterial3: true,
  fontFamily: 'Roboto',
  colorScheme: ColorScheme.fromSeed(
    seedColor: kLeaf,
    brightness: Brightness.light,
  ),
  scaffoldBackgroundColor: kBg,
  cardTheme: CardThemeData(
    color: kCard,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(16),
      side: const BorderSide(color: kBorder),
    ),
    margin: EdgeInsets.zero,
  ),
  appBarTheme: const AppBarTheme(
    backgroundColor: kForest,
    foregroundColor: Colors.white,
    elevation: 0,
    centerTitle: false,
    titleTextStyle: TextStyle(
      color: Color(0xFFE8F5E9),
      fontSize: 18,
      fontWeight: FontWeight.w700,
      letterSpacing: 0.3,
    ),
    systemOverlayStyle: SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: kLeaf,
      foregroundColor: Colors.white,
      elevation: 0,
      padding: const EdgeInsets.symmetric(vertical: 15, horizontal: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14),
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: kBorder),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: kBorder),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: kSprout, width: 2),
    ),
    filled: true,
    fillColor: Colors.white,
    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
    labelStyle: const TextStyle(color: kMuted, fontSize: 14),
  ),
  bottomNavigationBarTheme: const BottomNavigationBarThemeData(
    backgroundColor: Colors.white,
    selectedItemColor: kLeaf,
    unselectedItemColor: kMuted,
    type: BottomNavigationBarType.fixed,
    elevation: 12,
    selectedLabelStyle: TextStyle(fontSize: 11, fontWeight: FontWeight.w700),
    unselectedLabelStyle: TextStyle(fontSize: 11),
  ),
  chipTheme: ChipThemeData(
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
  ),
);

// =============================================================
//  ROOT APP
// =============================================================
class AgriForecastApp extends StatefulWidget {
  const AgriForecastApp({super.key});
  @override
  State<AgriForecastApp> createState() => _AgriForecastAppState();
}

class _AgriForecastAppState extends State<AgriForecastApp> {
  @override
  Widget build(BuildContext context) => MaterialApp(
    debugShowCheckedModeBanner: false,
    title: 'Agri Forecast — Musanze',
    theme: buildTheme(),
    home: const SplashScreen(),
  );
}

// =============================================================
//  SPLASH SCREEN
// =============================================================
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});
  @override
  State<SplashScreen> createState() => _SplashState();
}

class _SplashState extends State<SplashScreen>
    with TickerProviderStateMixin {
  late AnimationController _logoCtrl, _textCtrl;
  late Animation<double>   _logoFade, _logoScale, _textFade, _textSlide;
  bool _apiOnline = false;

  @override
  void initState() {
    super.initState();
    _logoCtrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 900));
    _textCtrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 700));

    _logoFade  = CurvedAnimation(parent: _logoCtrl, curve: Curves.easeOut);
    _logoScale = Tween<double>(begin: 0.6, end: 1.0)
        .animate(CurvedAnimation(parent: _logoCtrl, curve: Curves.elasticOut));
    _textFade  = CurvedAnimation(parent: _textCtrl, curve: Curves.easeOut);
    _textSlide = Tween<double>(begin: 30, end: 0)
        .animate(CurvedAnimation(parent: _textCtrl, curve: Curves.easeOut));

    _logoCtrl.forward();
    Future.delayed(const Duration(milliseconds: 400),
        () => _textCtrl.forward());
    _checkApi();
    Future.delayed(const Duration(milliseconds: 3200), _goToLogin);
  }

  Future<void> _checkApi() async {
    try {
      await ApiService.get('/api/status');
      if (mounted) setState(() => _apiOnline = true);
    } catch (_) {}
  }

  void _goToLogin() {
    if (mounted) {
      Navigator.pushReplacement(context,
          PageRouteBuilder(
            pageBuilder: (_, a, __) => const LoginPage(),
            transitionsBuilder: (_, a, __, child) =>
                FadeTransition(opacity: a, child: child),
            transitionDuration: const Duration(milliseconds: 500),
          ));
    }
  }

  @override
  void dispose() {
    _logoCtrl.dispose();
    _textCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [kForest, Color(0xFF1A5C1A), Color(0xFF1F7A1F)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: Stack(
            children: [
              // Background grain pattern
              Positioned.fill(
                child: CustomPaint(painter: _DotGridPainter()),
              ),

              Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Animated logo
                    ScaleTransition(
                      scale: _logoScale,
                      child: FadeTransition(
                        opacity: _logoFade,
                        child: Container(
                          width: 110,
                          height: 110,
                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.1),
                            shape: BoxShape.circle,
                            border: Border.all(
                                color: kLime.withValues(alpha: 0.4), width: 2),
                          ),
                          child: const Center(
                            child: Text('🌾',
                                style: TextStyle(fontSize: 56)),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 28),

                    // Animated text
                    AnimatedBuilder(
                      animation: _textCtrl,
                      builder: (_, child) => Transform.translate(
                        offset: Offset(0, _textSlide.value),
                        child: FadeTransition(
                          opacity: _textFade,
                          child: child,
                        ),
                      ),
                      child: const Column(children: [
                        Text('Agri Forecast',
                            style: TextStyle(
                              color: Color(0xFFE8F5E9),
                              fontSize: 34,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 1.2,
                            )),
                        SizedBox(height: 6),
                        Text('Automated Demand Forecasting',
                            style: TextStyle(
                                color: Color(0xFF89B889), fontSize: 14)),
                        SizedBox(height: 4),
                        Text('Musanze District · Northern Province · Rwanda',
                            style: TextStyle(
                                color: Color(0xFF5E8C5E), fontSize: 12)),
                        SizedBox(height: 6),
                        Text('University of Kigali · BBIT 2026',
                            style: TextStyle(
                                color: Color(0xFF3D6B3D), fontSize: 11)),
                      ]),
                    ),

                    const SizedBox(height: 60),

                    // API status indicator
                    AnimatedContainer(
                      duration: const Duration(milliseconds: 400),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 18, vertical: 8),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.08),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(
                            color: Colors.white.withValues(alpha: 0.15)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 8, height: 8,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: _apiOnline ? kLime : kAmber,
                              boxShadow: [
                                BoxShadow(
                                  color: (_apiOnline ? kLime : kAmber)
                                      .withValues(alpha: 0.5),
                                  blurRadius: 6,
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 8),
                          Text(
                            _apiOnline
                                ? 'API Connected'
                                : 'Connecting to server…',
                            style: const TextStyle(
                                color: Color(0xFF89B889), fontSize: 12),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 28),
                    const SizedBox(
                      width: 28, height: 28,
                      child: CircularProgressIndicator(
                        color: kLime,
                        strokeWidth: 2.5,
                      ),
                    ),
                  ],
                ),
              ),

              // Footer
              const Positioned(
                bottom: 20, left: 0, right: 0,
                child: Text(
                  'BARAKA ISAAC (2305000514) · Supervisor: Dr MUSABE JEAN BOSCO',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Color(0xFF3D6B3D), fontSize: 10),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// Dot grid background painter
class _DotGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = Colors.white.withValues(alpha: 0.04);
    const gap = 28.0;
    for (double x = 0; x < size.width; x += gap) {
      for (double y = 0; y < size.height; y += gap) {
        canvas.drawCircle(Offset(x, y), 1.5, paint);
      }
    }
  }

  @override
  bool shouldRepaint(_) => false;
}

// =============================================================
//  SESSION STATE
// =============================================================
class UserSession {
  static String name   = '';
  static String phone  = '';
  static String role   = '';
  static String sector = '';
  static double farmSizeAcres = 1.0;
  static bool loggedIn = false;

  static void set(
    Map<String, dynamic> d, {
    String? token,
  }) {
    name   = d['full_name'] ?? '';
    phone  = d['phone'] ?? '';
    role   = d['role'] ?? 'farmer';
    sector = d['sector'] ?? '';
    farmSizeAcres = double.tryParse(d['farm_size_acres'].toString()) ?? 1.0;
    loggedIn = true;

    if (token != null) {
      ApiService.setToken(token);
    }
  }

  static Map<String,dynamic>? lastForecast;
  static int? lastCropId;
  static String? lastModel;
  static void saveForecast(Map<String,dynamic> d,int cid,String m){lastForecast=d;lastCropId=cid;lastModel=m;}
  static void clear(){name=phone=role=sector='';loggedIn=false;lastForecast=null;lastCropId=null;lastModel=null;ApiService.clearToken();}

  static String get roleEmoji => switch (role) {
        'buyer' => '🛒',
        'cooperative' => '🤝',
        'extension' => '📋',
        _ => '🌱',
      };
}

//// =============================================================
//  LOGIN PAGE (FIXED)
// =============================================================
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginState();
}

class _LoginState extends State<LoginPage>
    with SingleTickerProviderStateMixin {
  final _phoneCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  bool _loading = false;
  bool _obscure = true;
  String? _error;

  late AnimationController _shakeCtrl;
  late Animation<double> _shake;

  @override
  void initState() {
    super.initState();

    _shakeCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );

    _shake = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _shakeCtrl, curve: Curves.elasticOut),
    );
  }

  @override
  void dispose() {
    _shakeCtrl.dispose();
    _phoneCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }

  // =============================================================
  // LOGIN FUNCTION (FIXED WITH TOKEN)
  // =============================================================
  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final d = await ApiService.post('/login', {
        'phone': _phoneCtrl.text.trim(),
        'password': _passCtrl.text,
      });

      if (d['status'] == 'success') {
        final token = d['token'] as String?;

        UserSession.set(
          d['user'] as Map<String, dynamic>,
          token: token,
        );

        if (mounted) {
          Navigator.pushReplacement(
            context,
            PageRouteBuilder(
              pageBuilder: (_, a, __) =>  const MainShell(),
              transitionsBuilder: (_, a, __, child) =>
                  FadeTransition(opacity: a, child: child),
              transitionDuration: const Duration(milliseconds: 400),
            ),
          );
        }
      } else {
        setState(() {
          _error = d['message'] ?? 'Login failed';
        });
        _shakeCtrl.forward(from: 0);
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
      _shakeCtrl.forward(from: 0);
    }

    if (mounted) {
      setState(() => _loading = false);
    }
  }

  // =============================================================
  // UI
  // =============================================================
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [kForest, Color(0xFF1A5C1A)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            child: Column(
              children: [
                const SizedBox(height: 30),

                const Text('🌾', style: TextStyle(fontSize: 64)),
                const SizedBox(height: 12),

                const Text(
                  'Agri Forecast',
                  style: TextStyle(
                    color: Color(0xFFE8F5E9),
                    fontSize: 28,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 1,
                  ),
                ),

                const Text(
                  'Musanze District · Rwanda',
                  style: TextStyle(
                    color: Color(0xFF89B889),
                    fontSize: 13,
                  ),
                ),

                const SizedBox(height: 36),

                AnimatedBuilder(
                  animation: _shake,
                  builder: (_, child) => Transform.translate(
                    offset: Offset(
                      math.sin(_shake.value * math.pi * 6) *
                          (1 - _shake.value) *
                          8,
                      0,
                    ),
                    child: child,
                  ),
                  child: Container(
                    padding: const EdgeInsets.all(28),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.2),
                          blurRadius: 40,
                          offset: const Offset(0, 16),
                        ),
                      ],
                    ),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                T.signIn,
                                style: const TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.w800,
                                  color: kForest,
                                ),
                              ),
                              _LangToggle(onChanged: (v) => setState(() {})),
                            ],
                          ), 

                          const SizedBox(height: 22),

                          TextFormField(
                            controller: _phoneCtrl,
                            keyboardType: TextInputType.phone,
                            decoration: InputDecoration(
                              labelText: T.phone,
                              hintText: '+250 7XX XXX XXX',
                              prefixIcon: const Icon(
                                Icons.phone_android,
                                color: kLeaf,
                              ),
                            ),
                            validator: (v) =>
                                (v == null || v.isEmpty)
                                    ? 'Enter phone number'
                                    : null,
                          ),

                          const SizedBox(height: 16),

                          TextFormField(
                            controller: _passCtrl,
                            obscureText: _obscure,
                            decoration: InputDecoration(
                              labelText: T.password,
                              prefixIcon: const Icon(Icons.lock, color: kLeaf),
                              suffixIcon: IconButton(
                                icon: Icon(
                                  _obscure
                                      ? Icons.visibility_outlined
                                      : Icons.visibility_off_outlined,
                                  color: kMuted,
                                ),
                                onPressed: () =>
                                    setState(() => _obscure = !_obscure),
                              ),
                            ),
                            validator: (v) =>
                                (v == null || v.length < 4)
                                    ? 'Enter password'
                                    : null,
                            onFieldSubmitted: (_) => _login(),
                          ),

                          if (_error != null) ...[
                            const SizedBox(height: 14),
                            _ErrorBanner(_error!),
                          ],

                          const SizedBox(height: 22),

                          SizedBox(
                            width: double.infinity,
                            child: _loading
                                ? const Center(
                                    child: CircularProgressIndicator(
                                      color: kSprout,
                                      strokeWidth: 3,
                                    ),
                                  )
                                : ElevatedButton.icon(
                                    onPressed: _login,
                                    icon: const Icon(Icons.login),
                                    label: Text(T.signIn),
                                  ),
                          ),

                          const SizedBox(height: 14),

                          Center(
                            child: TextButton(
                              onPressed: () => Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => const RegisterPage(),
                                ),
                              ),
                              child: Text(
                                '${T.noAccount} ${T.signUp}',
                                style: const TextStyle(
                                  color: kLeaf,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 30),

              ],
            ),
          ),
        ),
      ),
    );
  }
}

                
// =============================================================
//  REGISTER PAGE
// =============================================================
class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});
  @override
  State<RegisterPage> createState() => _RegisterState();
}

class _RegisterState extends State<RegisterPage> {
  final _nameCtrl  = TextEditingController();
  final _phoneCtrl = TextEditingController();
  final _passCtrl  = TextEditingController();
  final _formKey   = GlobalKey<FormState>();
  String _role     = 'farmer';
  String _sector   = 'Muhoza';
  bool   _loading  = false;
  bool   _obscure  = true;
  String? _error, _success;

  static const _sectors = ['Muhoza', 'Kinigi', 'Cyuve', 'Busogo', 'Shingiro'];
  static const _roles = [
    {'value': 'farmer',      'label': '🌱 Farmer / Umuhinzi'},
    {'value': 'buyer',       'label': '🛒 Buyer / Umuguzimbuto'},
    {'value': 'cooperative', 'label': '🤝 Cooperative / Koperative'},
    {'value': 'extension',   'label': '📋 Extension Officer'},
  ];

  Future<void> _register() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() { _loading = true; _error = null; _success = null; });
    try {
      final d = await ApiService.post('/register', {
        'full_name': _nameCtrl.text.trim(),
        'phone':     _phoneCtrl.text.trim(),
        'password':  _passCtrl.text,
        'role':      _role,
        'sector':    _sector,
      });
      if (d['status'] == 'success') {
        setState(() => _success = 'Account created! Please sign in.');
        Future.delayed(const Duration(seconds: 2),
            () => Navigator.pushReplacement(context,
                MaterialPageRoute(builder: (_) => const LoginPage())));
      } else {
        setState(() => _error = d['message'] ?? 'Registration failed');
      }
    } catch (_) {
      setState(() => _error = 'Cannot connect to server.');
    }
    if (mounted) setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.signUp),
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
            const Text('🌿', style: TextStyle(fontSize: 52)),
            const SizedBox(height: 12),
            Text(T.rw
                ? 'Iyandikishe — Agri Forecast'
                : 'Create your account',
                style: const TextStyle(
                    fontSize: 20, fontWeight: FontWeight.w800,
                    color: kForest)),
            const SizedBox(height: 24),

            _FieldCard(children: [
              TextFormField(
                controller: _nameCtrl,
                decoration: InputDecoration(
                    labelText: T.fullName,
                    prefixIcon: const Icon(Icons.person, color: kLeaf)),
                textCapitalization: TextCapitalization.words,
                validator: (v) => (v == null || v.trim().isEmpty)
                    ? 'Enter full name' : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _phoneCtrl,
                keyboardType: TextInputType.phone,
                decoration: InputDecoration(
                    labelText: T.phone,
                    hintText: '+250 7XX XXX XXX',
                    prefixIcon: const Icon(Icons.phone, color: kLeaf)),
                validator: (v) => (v == null || v.isEmpty)
                    ? 'Enter phone number' : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _passCtrl,
                obscureText: _obscure,
                decoration: InputDecoration(
                  labelText: T.password,
                  prefixIcon: const Icon(Icons.lock, color: kLeaf),
                  suffixIcon: IconButton(
                    icon: Icon(_obscure
                        ? Icons.visibility_outlined
                        : Icons.visibility_off_outlined,
                        color: kMuted),
                    onPressed: () => setState(() => _obscure = !_obscure),
                  ),
                ),
                validator: (v) => (v == null || v.length < 6)
                    ? 'Minimum 6 characters' : null,
              ),
              const SizedBox(height: 14),
              DropdownButtonFormField<String>(
                initialValue: _role,
                decoration: InputDecoration(
                    labelText: T.role,
                    prefixIcon: const Icon(Icons.badge, color: kLeaf)),
                items: _roles.map((r) => DropdownMenuItem<String>(
                    value: r['value'],
                    child: Text(r['label']!))).toList(),
                onChanged: (v) => setState(() => _role = v!),
              ),
              const SizedBox(height: 14),
              DropdownButtonFormField<String>(
                initialValue: _sector,
                decoration: InputDecoration(
                    labelText: T.sector,
                    prefixIcon: const Icon(Icons.location_on, color: kLeaf)),
                items: _sectors.map((s) => DropdownMenuItem<String>(
                    value: s, child: Text(s))).toList(),
                onChanged: (v) => setState(() => _sector = v!),
              ),
            ]),

            const SizedBox(height: 14),

            if (_error != null)   _ErrorBanner(_error!),
            if (_success != null) _SuccessBanner(_success!),

            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: _loading
                  ? const Center(child: CircularProgressIndicator(
                      color: kSprout, strokeWidth: 3))
                  : ElevatedButton.icon(
                      onPressed: _register,
                      icon: const Icon(Icons.check_circle_outline),
                      label: Text(T.signUp),
                    ),
            ),
            const SizedBox(height: 12),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(
                '${T.hasAccount} ${T.signIn}',
                style: const TextStyle(
                    color: kLeaf, fontWeight: FontWeight.w600),
              ),
            ),
            const SizedBox(height: 30),
          ]),
        ),
      ),
    );
  }
}

// =============================================================
//  MAIN SHELL (Bottom Nav + Pages)
// =============================================================
class MainShell extends StatefulWidget {        // ← add this
  const MainShell({super.key});
  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {   // ← already there
  int _tab = 0;
    // Shared state — set by Forecast & Price pages, read by Reports
  Map<String, dynamic>? lastForecastData;
  Map<String, dynamic>? lastPriceData;

  void _refresh() => setState(() {});

  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();
    _pages = [
      const OverviewPage(),
      ForecastPage(onResult: (d) => setState(() { lastForecastData = d; UserSession.saveForecast(d, d["crop_id"] ?? 1, d["model"] ?? "ensemble"); })),
      PricePage(onResult: (d) => setState(() => lastPriceData = d)),
      const ComparePage(),
      const AlertsPage(),
      ReportsPage(
        getForecastData: () => lastForecastData,
        getPriceData:    () => lastPriceData,
      ),
      const ProfilePage(),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(children: [
          const Text('🌾 ', style: TextStyle(fontSize: 20)),
          Text(T.appName),
        ]),
        actions: [
          _LangToggle(onChanged: (_) => _refresh()),
          const SizedBox(width: 4),
          PopupMenuButton(
            icon: CircleAvatar(
              backgroundColor: kLime.withValues(alpha: 0.25),
              radius: 16,
              child: Text(UserSession.roleEmoji,
                  style: const TextStyle(fontSize: 14)),
            ),
            itemBuilder: (context) => <PopupMenuEntry<dynamic>>[
              PopupMenuItem(
                enabled: false,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(UserSession.name,
                        style: const TextStyle(
                            fontWeight: FontWeight.w700, color: kForest)),
                    Text(UserSession.role,
                        style: const TextStyle(color: kMuted, fontSize: 12)),
                    Text(UserSession.sector,
                        style: const TextStyle(color: kMuted, fontSize: 12)),
                  ],
                ),
              ),
              const PopupMenuDivider(),
              PopupMenuItem(
                value: 'logout',
                child: Row(children: [
                  const Icon(Icons.logout, size: 18, color: kRed),
                  const SizedBox(width: 8),
                  Text(T.logout, style: const TextStyle(color: kRed)),
                ]),
              ),
            ],
            onSelected: (v) {
              if (v == 'logout') {
                UserSession.clear();
                Navigator.pushReplacement(context,
                    MaterialPageRoute(builder: (_) => const LoginPage()));
              }
            },
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: IndexedStack(index: _tab, children: _pages),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _tab,
        onTap: (i) => setState(() => _tab = i),
        items: [
          BottomNavigationBarItem(
              icon: const Icon(Icons.home_outlined),
              activeIcon: const Icon(Icons.home),
              label: T.home),
          BottomNavigationBarItem(
              icon: const Icon(Icons.bar_chart_outlined),
              activeIcon: const Icon(Icons.bar_chart),
              label: T.forecast),
          BottomNavigationBarItem(
              icon: const Icon(Icons.attach_money),
              activeIcon: const Icon(Icons.monetization_on),
              label: T.price),
          BottomNavigationBarItem(
              icon: const Icon(Icons.compare_arrows),
              activeIcon: const Icon(Icons.compare_arrows),
              label: T.compare),
          BottomNavigationBarItem(
              icon: const Icon(Icons.notifications_outlined),
              activeIcon: const Icon(Icons.notifications),
              label: T.alerts),
          BottomNavigationBarItem(
              icon: const Icon(Icons.picture_as_pdf_outlined),
              activeIcon: const Icon(Icons.picture_as_pdf),
              label: T.reports),
          BottomNavigationBarItem(
              icon: const Icon(Icons.person_outline),
              activeIcon: const Icon(Icons.person),
              label: T.profile),
        ],
      ),
    );
  }
}

// =============================================================
//  OVERVIEW PAGE
// =============================================================
class OverviewPage extends StatefulWidget {
  const OverviewPage({super.key});
  @override
  State<OverviewPage> createState() => _OverviewPageState();
}

class _OverviewPageState extends State<OverviewPage> {
  Map<String, dynamic>? _status;
  Map<String, dynamic>? _insights;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (_status == null) _load();
  }

  Future<void> _load() async {
    setState(() { _loading = true; _error = null; });
    try {
      final results = await Future.wait([
        ApiService.get('/api/status'),
        ApiService.get('/market_insights'),
      ]);
      if (mounted) {
        setState(() {
        _status   = results[0];
        _insights = results[1];
        _loading  = false;
      });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
        _error   = '$e';
        _loading = false;
      });
      }
    }
  }

  String _currentSeason() {
    final m = DateTime.now().month;
    return _season(m);
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      color: kSprout,
      onRefresh: _load,
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
        children: [
          // Welcome banner
          _WelcomeBanner(season: _currentSeason()),
const SizedBox(height: 16),
_WeatherCard(),
const SizedBox(height: 16),

          // Musanze sectors map
          _SectionHeader(T.rw ? 'Ikarita y\'Akarere ka Musanze' : 'Musanze District Map'),
          const SizedBox(height: 10),
          const _MusanzeMap(),
          const SizedBox(height: 16),

          // KPI strip
          _loading
              ? const _LoadingCard()
              : _status != null
                  ? _KpiStrip(status: _status!)
                  : const SizedBox(),

          const SizedBox(height: 16),

          // Season cards
          _SeasonStrip(current: _currentSeason()),
          const SizedBox(height: 16),

          // Crop grid
          _SectionHeader(T.cropPortfolio),
          const SizedBox(height: 10),
          _CropGrid(),
          const SizedBox(height: 16),

          // Market snapshot
          _SectionHeader(T.marketSnap),
          const SizedBox(height: 10),

          if (_loading)
            const _LoadingCard()
          else if (_error != null)
            _ErrorBanner(_error!)
          else if (_insights != null)
            _MarketSnapshotList(
                insights: _insights!['insights'] as List? ?? []),
        ],
      ),
    );
  }
}


// =============================================================
//  MUSANZE DISTRICT MAP
// =============================================================
class _MusanzeMap extends StatefulWidget {
  const _MusanzeMap();
  @override
  State<_MusanzeMap> createState() => _MusanzeMapState();
}

class _MusanzeMapState extends State<_MusanzeMap> {
  String? _selectedSector;
  Map<String,dynamic>? _sectorData;
  bool _sectorLoading = false;

  Future<void> _loadSector(String name) async {
    setState(() { _sectorLoading = true; _sectorData = null; });
    try {
      final d = await ApiService.get('/sector/$name');
      setState(() { _sectorData = d; _sectorLoading = false; });
    } catch(_) { setState(() => _sectorLoading = false); }
  }

  static const _sectors = [
    {'name': 'Muhoza',   'lat': -1.4986, 'lng': 29.6344},
    {'name': 'Musanze',  'lat': -1.5100, 'lng': 29.6350},
    {'name': 'Kinigi',   'lat': -1.4500, 'lng': 29.5800},
    {'name': 'Busogo',   'lat': -1.5500, 'lng': 29.5900},
    {'name': 'Cyuve',    'lat': -1.4200, 'lng': 29.6100},
    {'name': 'Gacaca',   'lat': -1.5800, 'lng': 29.6600},
    {'name': 'Gashaki',  'lat': -1.4800, 'lng': 29.7000},
    {'name': 'Gataraga', 'lat': -1.5300, 'lng': 29.6700},
    {'name': 'Kimonyi',  'lat': -1.5700, 'lng': 29.6200},
    {'name': 'Muko',     'lat': -1.4300, 'lng': 29.6500},
    {'name': 'Nyange',   'lat': -1.5400, 'lng': 29.5600},
    {'name': 'Shingiro', 'lat': -1.4700, 'lng': 29.5500},
  ];

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          height: 280,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: kBorder),
          ),
          clipBehavior: Clip.hardEdge,
          child: FlutterMap(
            options: MapOptions(
              initialCenter: const LatLng(-1.4986, 29.6344),
              initialZoom: 11.5,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.agri_mobile',
              ),
              MarkerLayer(
                markers: _sectors.map((s) {
                  final isSelected = _selectedSector == s['name'];
                  return Marker(
                    point: LatLng(s['lat'] as double, s['lng'] as double),
                    width: isSelected ? 120 : 90,
                    height: isSelected ? 50 : 36,
                    child: GestureDetector(
                      onTap: () {
                        final n = s['name'] as String;
                        setState(() => _selectedSector = isSelected ? null : n);
                        if (!isSelected) _loadSector(n);
                      },
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: isSelected ? kForest : kSprout,
                          borderRadius: BorderRadius.circular(20),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withValues(alpha: 0.2),
                              blurRadius: 4,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text('📍', style: TextStyle(fontSize: 10)),
                            const SizedBox(width: 3),
                            Flexible(
                              child: Text(
                                s['name'] as String,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 10,
                                  fontWeight: FontWeight.w700,
                                ),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }).toList(),
              ),
            ],
          ),
        ),
        if (_selectedSector != null) ...[
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
        ],
      ],
    );
  }
}

class _WelcomeBanner extends StatelessWidget {
  final String season;
  const _WelcomeBanner({required this.season});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [kForest, Color(0xFF1A5C1A), Color(0xFF1F7A1F)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
              color: kForest.withValues(alpha: 0.3),
              blurRadius: 16,
              offset: const Offset(0, 6)),
        ],
      ),
      padding: const EdgeInsets.all(22),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  T.rw
                      ? 'Murakaza neza, ${UserSession.name.split(' ').first}!'
                      : 'Welcome, ${UserSession.name.split(' ').first}!',
                  style: const TextStyle(
                    color: Color(0xFFE8F5E9),
                    fontSize: 20,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 4),
                Text(T.tagline,
                    style: const TextStyle(
                        color: Color(0xFF89B889), fontSize: 12)),
                const SizedBox(height: 12),
                Row(children: [
                  _SeasonPill(season),
                  const SizedBox(width: 8),
                  _RolePill(UserSession.roleEmoji, UserSession.role),
                ]),
              ],
            ),
          ),
          const Text('🌾', style: TextStyle(fontSize: 52, height: 1)),
        ],
      ),
    );
  }
}

class _SeasonPill extends StatelessWidget {
  final String season;
  const _SeasonPill(this.season);
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
    decoration: BoxDecoration(
      color: seasonColor(season).withValues(alpha: 0.25),
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: seasonColor(season).withValues(alpha: 0.4)),
    ),
    child: Text(
      '🗓 Season $season',
      style: const TextStyle(
          color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600),
    ),
  );
}

class _RolePill extends StatelessWidget {
  final String emoji, role;
  const _RolePill(this.emoji, this.role);
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
    decoration: BoxDecoration(
      color: Colors.white.withValues(alpha: 0.12),
      borderRadius: BorderRadius.circular(20),
    ),
    child: Text(
      '$emoji ${role.toUpperCase()}',
      style: const TextStyle(
          color: Color(0xFF89B889), fontSize: 10, fontWeight: FontWeight.w600),
    ),
  );
}

class _KpiStrip extends StatelessWidget {
  final Map<String, dynamic> status;
  const _KpiStrip({required this.status});

  @override
  Widget build(BuildContext context) {
    final items = [
      {'icon': '🌱', 'val': '${status["crops"] ?? 7}',          'lbl': T.rw ? 'Ibihingwa' : 'Crops'},
      {'icon': '🤖', 'val': '5',                                  'lbl': T.rw ? 'Indorerezi' : 'Models'},
      {'icon': '🗺️', 'val': '${status["sectors"] ?? 5}',         'lbl': T.rw ? 'Inzego' : 'Sectors'},
      {'icon': '📦', 'val': fmtNum(status["db_records"] ?? 0),   'lbl': T.rw ? 'Amakuru' : 'Records'},
    ];
    return Row(
      children: items.asMap().entries.map((e) => Expanded(
        child: Container(
          margin: EdgeInsets.only(left: e.key == 0 ? 0 : 8),
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 6),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(14),
            border: const Border(top: BorderSide(color: kSprout, width: 3)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.04),
                blurRadius: 8, offset: const Offset(0, 3)),
            ],
          ),
          child: Column(children: [
            Text(e.value['icon']!, style: const TextStyle(fontSize: 22)),
            const SizedBox(height: 4),
            Text(e.value['val']!,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w900,
                  color: kForest,
                )),
            Text(e.value['lbl']!,
                style: const TextStyle(fontSize: 9, color: kMuted),
                textAlign: TextAlign.center),
          ]),
        ),
      )).toList(),
    );
  }
}

class _SeasonStrip extends StatelessWidget {
  final String current;
  const _SeasonStrip({required this.current});

  @override
  Widget build(BuildContext context) {
    final seasons = [
      ('A', T.seasonA, T.rw ? 'Itera gikomeye. Isoko rinini ry\'ibihingwa.' : 'Primary planting & harvest. Peak demand.'),
      ('B', T.seasonB, T.rw ? 'Itera rya kabiri. Isoko rizamuka Kamena.' : 'Second planting cycle. Rising demand mid-June.'),
      ('C', T.seasonC, T.rw ? 'Igihe cy\'icyuho. Ibiciro bizamuka 20–35%.' : 'Dry season. Prices peak 20–35%.'),
    ];
    return Row(
      children: seasons.asMap().entries.map((e) {
        final (s, name, desc) = e.value;
        final isCurrent = s == current;
        return Expanded(
          child: Container(
            margin: EdgeInsets.only(left: e.key == 0 ? 0 : 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isCurrent ? kSkyPale : Colors.white,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(
                color: isCurrent ? kSprout : kBorder,
                width: isCurrent ? 1.5 : 1,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(s,
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w900,
                      color: seasonColor(s),
                    )),
                const SizedBox(height: 3),
                Text(name,
                    style: TextStyle(
                      fontSize: 9,
                      fontWeight: FontWeight.w700,
                      color: isCurrent ? kForest : kMuted,
                    )),
                const SizedBox(height: 4),
                Text(desc,
                    style: const TextStyle(fontSize: 8, color: kMuted),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis),
                if (isCurrent) ...[
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: kSprout,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(T.rw ? 'Ubu' : 'Now',
                        style: const TextStyle(
                            color: Colors.white,
                            fontSize: 8,
                            fontWeight: FontWeight.w700)),
                  ),
                ],
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}

class _CropGrid extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 4,
        childAspectRatio: 0.88,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
      ),
      itemCount: kCrops.length,
      itemBuilder: (ctx, i) {
        final c = kCrops[i];
        return InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: () {}, // Could jump to forecast
          child: Container(
            decoration: BoxDecoration(
              color: c.color.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: c.color.withValues(alpha: 0.2)),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(c.icon, style: const TextStyle(fontSize: 26)),
                const SizedBox(height: 5),
                Text(c.name,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 9,
                      fontWeight: FontWeight.w700,
                      color: c.color,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _MarketSnapshotList extends StatelessWidget {
  final List insights;
  const _MarketSnapshotList({required this.insights});

  Color _statusColor(String s) => switch (s) {
    'High'    => kSprout,
    'Low'     => kRed,
    'Rising'  => kSprout,
    'Falling' => kRed,
    _         => kAmber,
  };

  Widget _statusChip(String s) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
    decoration: BoxDecoration(
      color: _statusColor(s).withValues(alpha: 0.12),
      borderRadius: BorderRadius.circular(8),
      border: Border.all(color: _statusColor(s).withValues(alpha: 0.3)),
    ),
    child: Text(s,
        style: TextStyle(
          color: _statusColor(s),
          fontSize: 10,
          fontWeight: FontWeight.w700,
        )),
  );

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListView.separated(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        itemCount: insights.length,
        separatorBuilder: (_, __) =>
            const Divider(height: 1, color: kBorder),
        itemBuilder: (_, i) {
          final r   = insights[i] as Map<String, dynamic>;
          final cid = r['crop_id'] as int;
          final c   = cropById(cid);
          return Padding(
            padding: const EdgeInsets.symmetric(
                horizontal: 16, vertical: 12),
            child: Row(children: [
              Text(c.icon, style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(r['crop_name'] as String? ?? c.name,
                        style: const TextStyle(
                            fontWeight: FontWeight.w700,
                            fontSize: 13,
                            color: kForest)),
                    const SizedBox(height: 2),
                    Text(
                      '${fmtFull(r["last_qty_kg"] as num? ?? 0)} kg  ·  '
                      '${fmtFull(r["last_price_rwf"] as num? ?? 0)} RWF/kg',
                      style: const TextStyle(
                          fontSize: 11, color: kMuted,
                          fontFamily: 'monospace'),
                    ),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  _statusChip(r['status'] as String? ?? ''),
                  const SizedBox(height: 4),
                  _statusChip(r['price_status'] as String? ?? ''),
                ],
              ),
            ]),
          );
        },
      ),
    );
  }
}
// =============================================================
//  WEATHER CARD
// =============================================================
class _WeatherCard extends StatefulWidget {
  @override
  State<_WeatherCard> createState() => _WeatherCardState();
}

class _WeatherCardState extends State<_WeatherCard> {
  Map<String, dynamic>? _weather;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final d = await ApiService.get('/weather', requireAuth: false);
      if (mounted) setState(() { _weather = d; _loading = false; });
    } catch (_) {
      if (mounted) setState(() => _loading = false);
    }
  }

  String _rainLabel(num rain) {
    if (rain == 0) return T.rw ? 'Nta mvura' : 'No rain';
    if (rain < 5)  return T.rw ? 'Mvura nke' : 'Light rain';
    if (rain < 20) return T.rw ? 'Mvura' : 'Moderate rain';
    return T.rw ? 'Mvura nyinshi' : 'Heavy rain';
  }

  String _rainEmoji(num rain) {
    if (rain == 0) return '☀️';
    if (rain < 5)  return '🌦️';
    if (rain < 20) return '🌧️';
    return '⛈️';
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: kSkyPale,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: kBorder),
        ),
        child: const Center(
          child: SizedBox(width: 20, height: 20,
            child: CircularProgressIndicator(color: kSprout, strokeWidth: 2)),
        ),
      );
    }
    if (_weather == null) return const SizedBox();

    final cur  = _weather!['current'] as Map<String, dynamic>;
    final fc   = (_weather!['forecast'] as List).take(4).toList();
    final temp = (cur['temperature'] as num).toStringAsFixed(1);
    final hum  = cur['humidity'] as num;
    final rain = (cur['rain'] as num?) ?? 0;
    final wind = (cur['windspeed'] as num).toStringAsFixed(1);

    return Container(
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF1565C0), Color(0xFF1976D2)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: kBlue.withValues(alpha: 0.3),
            blurRadius: 16,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      padding: const EdgeInsets.all(18),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Row(children: [
            const Icon(Icons.wb_sunny_outlined, color: Colors.white70, size: 16),
            const SizedBox(width: 6),
            Text(
              T.rw ? '🌦 Ikirere — Musanze' : '🌦 Weather — Musanze',
              style: const TextStyle(
                color: Colors.white70, fontSize: 12, fontWeight: FontWeight.w600),
            ),
          ]),
          const SizedBox(height: 12),

          // Current temp + condition
          Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                _rainEmoji(rain),
                style: const TextStyle(fontSize: 44),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '$temp°C',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 36,
                      fontWeight: FontWeight.w900,
                      height: 1,
                    ),
                  ),
                  Text(
                    _rainLabel(rain),
                    style: const TextStyle(
                      color: Colors.white70, fontSize: 13),
                  ),
                ],
              ),
              const Spacer(),
              // Extra stats
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  _WeatherStat('💧', '$hum%',     T.rw ? 'Ubunyufu' : 'Humidity'),
                  const SizedBox(height: 6),
                  _WeatherStat('💨', '${wind}km/h', T.rw ? 'Umuyaga' : 'Wind'),
                ],
              ),
            ],
          ),
          const SizedBox(height: 14),

          // 4-day forecast strip
          Container(
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 4),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: fc.asMap().entries.map((e) {
                final day  = e.value as Map<String, dynamic>;
                final date = (day['date'] as String).substring(5); // MM-DD
                final max  = (day['max_temp'] as num).toStringAsFixed(0);
                final min  = (day['min_temp'] as num).toStringAsFixed(0);
                final r    = (day['rain'] as num?) ?? 0;
                return Column(children: [
                  Text(e.key == 0 ? (T.rw ? 'Uyu' : 'Today') : date,
                      style: const TextStyle(
                          color: Colors.white70, fontSize: 9)),
                  const SizedBox(height: 4),
                  Text(_rainEmoji(r),
                      style: const TextStyle(fontSize: 18)),
                  const SizedBox(height: 2),
                  Text('$max°',
                      style: const TextStyle(
                          color: Colors.white,
                          fontSize: 11,
                          fontWeight: FontWeight.w700)),
                  Text('$min°',
                      style: const TextStyle(
                          color: Colors.white60, fontSize: 10)),
                ]);
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}

class _WeatherStat extends StatelessWidget {
  final String emoji, value, label;
  const _WeatherStat(this.emoji, this.value, this.label);
  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Text(emoji, style: const TextStyle(fontSize: 12)),
      const SizedBox(width: 4),
      Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(value, style: const TextStyle(
            color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700)),
        Text(label, style: const TextStyle(
            color: Colors.white60, fontSize: 9)),
      ]),
    ],
  );
}
// =============================================================
//  FORECAST PAGE
// =============================================================
Map<String, dynamic> _calcPlantingAdvice(Map<String, dynamic> forecastData) {
  final fc       = forecastData['forecast'] as List;
  final cropName = forecastData['crop_name'] as String? ?? '';
  final demands  = fc.map((f) => (f['demand_kg'] as num?)?.toDouble() ?? 0.0).toList();
  final maxD     = demands.reduce(math.max);
  final minD     = demands.reduce(math.min);
  final avgD     = demands.reduce((a, b) => a + b) / demands.length;
  final peakWeek = demands.indexOf(maxD) + 1;
  final peakDate = fc[peakWeek - 1]['date'] as String? ?? '';

  // Use backend farmer_advice if available, else fall back to simple calc
  final fa = forecastData['farmer_advice'] as Map<String, dynamic>?;
  final mk = forecastData['market']        as Map<String, dynamic>?;

  final plantingKg     = fa != null ? ((fa['plant_target_kg']  as num?)?.toInt()  ?? (maxD * 1.44).round()) : (maxD * 1.44).round();
  final targetKg       = fa != null ? ((fa['farmer_target_kg'] as num?)?.toInt()  ?? (maxD * 1.20).round()) : (maxD * 1.20).round();
  final seedBags       = fa != null ? ((fa['seed_bags_needed'] as num?)?.toInt()  ?? 1)                     : 1;
  final bagKg          = fa != null ? ((fa['bag_kg']           as num?)?.toInt()  ?? 50)                    : 50;
  final requiredAcres  = fa != null ? ((fa['required_acres']   as num?)?.toDouble() ?? 0.0)                 : 0.0;
  final weeksToPlant   = fa != null ? ((fa['weeks_until_plant'] as num?)?.toInt() ?? peakWeek)              : peakWeek;
  final plantByDate    = fa != null ? (fa['plant_by_date']     as String? ?? '')                            : '';
  final urgency        = fa != null ? (fa['urgency']           as String? ?? 'flexible')                    : 'flexible';
  final urgencyMsg     = fa != null ? (T.rw ? fa['urgency_rw'] : fa['urgency_en']) as String? ?? ''        : '';
  final marketShare    = fa != null ? ((fa['market_share_pct'] as num?)?.toDouble() ?? 0.0)                : 0.0;
  final farmSize       = fa != null ? ((fa['farm_size_acres']  as num?)?.toDouble() ?? 1.5)                : 1.5;

  final marketSignal   = mk != null ? (mk['signal']    as String? ?? 'balanced')                           : 'balanced';
  final signalMsg      = mk != null ? (T.rw ? mk['signal_rw'] : mk['signal_en']) as String? ?? ''         : '';
  final trendMsg       = mk != null ? (T.rw ? mk['trend_rw']  : mk['trend_en'])  as String? ?? ''         : '';
  final peakDemandKg   = mk != null ? ((mk['peak_demand_kg']  as num?)?.toInt()  ?? maxD.round())         : maxD.round();

  return {
    'crop_name':       cropName,
    'peak_week':       peakWeek,
    'peak_date':       peakDate,
    'peak_demand_kg':  peakDemandKg,
    'avg_demand_kg':   avgD.round(),
    'min_demand_kg':   minD.round(),
    'target_kg':       targetKg,
    'planting_kg':     plantingKg,
    'seed_bags':       seedBags,
    'bag_kg':          bagKg,
    'required_acres':  requiredAcres,
    'farm_size':       farmSize,
    'market_share':    marketShare,
    'weeks_to_plant':  weeksToPlant,
    'plant_by_date':   plantByDate,
    'urgency':         urgency,
    'urgency_msg':     urgencyMsg,
    'market_signal':   marketSignal,
    'signal_msg':      signalMsg,
    'trend_msg':       trendMsg,
    'bags_50kg':       (targetKg / 50).ceil(),
    'weeks_to_peak':   peakWeek,
    'planting_window': urgencyMsg,
  };
}
class ForecastPage extends StatefulWidget {
  final ValueChanged<Map<String, dynamic>>? onResult;
  const ForecastPage({super.key, this.onResult});
  @override
  State<ForecastPage> createState() => _ForecastPageState();
}

class _ForecastPageState extends State<ForecastPage> {
  int    _cropId = 1;
  String _model  = 'ensemble';
  int    _weeks  = 12;
  bool   _loading = false;
  Map<String, dynamic>? _result;
  String? _error;

  Future<void> _fetch() async {
    setState(() { _loading = true; _error = null; _result = null; });
    try {
      final d = await ApiService.get(
          '/forecast/$_cropId?model=$_model&weeks=$_weeks&farm_size=${UserSession.farmSizeAcres > 0 ? UserSession.farmSizeAcres : 1.0}');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
      widget.onResult?.call(d);
      if (mounted) {
        await Future.delayed(const Duration(milliseconds: 300));
        if (mounted) {
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            backgroundColor: Colors.transparent,
            builder: (_) => _PlantingAdviceSheet(
              advice: _calcPlantingAdvice(d),
            ),
          );
        }
      }
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
      children: [
        // Controls card
        _ControlCard(
          title: T.forecast,
          subtitle: T.rw
              ? 'Hitamo igihingwa, indorerezi n\'ibihe'
              : 'Choose crop, model and forecast horizon',
          children: [
            _CropDropdown(
              value: _cropId,
              onChanged: (v) => setState(() => _cropId = v),
            ),
            const SizedBox(height: 12),
            _ModelDropdown(
              value: _model,
              onChanged: (v) => setState(() => _model = v),
            ),
            const SizedBox(height: 12),
            _WeeksSlider(
              value: _weeks,
              onChanged: (v) => setState(() => _weeks = v),
            ),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _fetch,
                icon: _loading
                    ? const SizedBox(width: 18, height: 18,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.bar_chart),
                label: Text(T.getForecast),
              ),
            ),
          ],
        ),

        const SizedBox(height: 12),

        if (_error != null) _ErrorBanner(_error!),

        if (_result != null) ...[
          const SizedBox(height: 4),
          _ForecastResultView(data: _result!),
        ],
      ],
    );
  }
}

class _ForecastResultView extends StatelessWidget {
  final Map<String, dynamic> data;
  const _ForecastResultView({required this.data});

  @override
  Widget build(BuildContext context) {
    final fc      = data['forecast'] as List;
    final metrics = data['metrics']  as Map<String, dynamic>?;
    final advice  = data['advice']   as Map<String, dynamic>?;
    final breakDn = data['breakdown'] as Map<String, dynamic>?;
    final cropNm  = data['crop_name']  as String? ?? '';
    final model   = data['model']      as String? ?? '';

    if (fc.isEmpty) return const SizedBox();

    final demands  = fc.map((f) => (f['demand_kg'] as num?)?.toDouble() ?? 0.0).toList();
    final maxD     = demands.reduce(math.max);
    final minD     = demands.reduce(math.min);

    final spots   = fc.asMap().entries
        .map((e) => FlSpot(e.key.toDouble(), demands[e.key])).toList();
    final hiSpots = fc.asMap().entries
        .map((e) => FlSpot(e.key.toDouble(),
            (e.value['upper_kg'] as num?)?.toDouble() ?? 0.0)).toList();
    final loSpots = fc.asMap().entries
        .map((e) => FlSpot(e.key.toDouble(),
            (e.value['lower_kg'] as num?)?.toDouble() ?? 0.0)).toList();

    return Column(children: [
      // Chart card
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('$cropNm — $model',
                  style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 15,
                      color: kForest)),
              Text(
                '${data['weeks'] ?? 16}-week demand forecast · Musanze',
                style: const TextStyle(fontSize: 11, color: kMuted),
              ),
              const SizedBox(height: 6),
              // Peak / trough badges
              Row(children: [
                _MiniKpi('Peak', '${fmtNum(maxD)} kg', kSprout),
                const SizedBox(width: 8),
                _MiniKpi('Low', '${fmtNum(minD)} kg', kRed),
                const SizedBox(width: 8),
                _MiniKpi('Bags',
                    '${((maxD / ((data["unit_kg"] as num?) ?? 50)).ceil())}',
                    kStraw),
              ]),
              const SizedBox(height: 14),
              SizedBox(
                height: 230,
                child: LineChart(LineChartData(
                  clipData: const FlClipData.all(),
                  lineBarsData: [
                    // CI band upper
                    LineChartBarData(
                      spots: hiSpots,
                      isCurved: true,
                      color: Colors.transparent,
                      belowBarData: BarAreaData(
                        show: true,
                        gradient: LinearGradient(
                          colors: [kSprout.withValues(alpha: 0.07),
                                   kSprout.withValues(alpha: 0.01)],
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                        ),
                      ),
                      dotData: const FlDotData(show: false),
                      barWidth: 0,
                    ),
                    // CI lower
                    LineChartBarData(
                      spots: loSpots,
                      isCurved: true,
                      color: Colors.transparent,
                      dotData: const FlDotData(show: false),
                      barWidth: 0,
                    ),
                    // Main forecast line
                    LineChartBarData(
                      spots: spots,
                      isCurved: true,
                      curveSmoothness: 0.35,
                      color: kLeaf,
                      barWidth: 3,
                      belowBarData: BarAreaData(
                        show: true,
                        gradient: LinearGradient(
                          colors: [kLeaf.withValues(alpha: 0.1),
                                   kLeaf.withValues(alpha: 0.01)],
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                        ),
                      ),
                      dotData: FlDotData(
                        show: true,
                        getDotPainter: (s, _, __, idx) {
                          final v = demands[idx];
                          final color = v == maxD
                              ? kLime
                              : v == minD ? kRed : kLeaf;
                          return FlDotCirclePainter(
                              radius: v == maxD || v == minD ? 5 : 3,
                              color: color,
                              strokeWidth: 2,
                              strokeColor: Colors.white);
                        },
                      ),
                    ),
                  ],
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(
                        sideTitles: SideTitles(
                          showTitles: true,
                          reservedSize: 48,
                          getTitlesWidget: (v, m) => Text(
                              fmtNum(v),
                              style: const TextStyle(
                                  fontSize: 9, color: kMuted)),
                        )),
                    bottomTitles: AxisTitles(
                        sideTitles: SideTitles(
                          showTitles: true,
                          interval: (fc.length / 4).ceilToDouble(),
                          getTitlesWidget: (v, m) => Text(
                              'W${v.toInt() + 1}',
                              style: const TextStyle(
                                  fontSize: 9, color: kMuted)),
                        )),
                    rightTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false)),
                    topTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false)),
                  ),
                  gridData: FlGridData(
                    show: true,
                    getDrawingHorizontalLine: (_) => const FlLine(
                        color: kBorder, strokeWidth: 1),
                    getDrawingVerticalLine: (_) => FlLine(
                        color: kBorder.withValues(alpha: 0.5), strokeWidth: 1),
                  ),
                  borderData: FlBorderData(
                      show: true,
                      border: Border.all(color: kBorder)),
                  lineTouchData: LineTouchData(
                    touchTooltipData: LineTouchTooltipData(
                      getTooltipColor: (_) => kForest.withValues(alpha: 0.9),
                      getTooltipItems: (spots) => spots.map((s) {
                        if (s.barIndex != 2) return null;
                        return LineTooltipItem(
                          'W${(s.x + 1).toInt()}  ${fmtFull(s.y.round())} kg',
                          const TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.w600),
                        );
                      }).toList(),
                    ),
                  ),
                )),
              ),
            ],
          ),
        ),
      ),

      const SizedBox(height: 12),

      // Metrics card
      if (metrics != null)
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const _SectionHeader('Model Accuracy Metrics', small: true),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    _MetricChip('MAE',  fmtNum((metrics['MAE'] as num?)?.toDouble() ?? 0),  Colors.orange),
                    _MetricChip('RMSE', fmtNum((metrics['RMSE'] as num?)?.toDouble() ?? 0), kBlue),
                    _MetricChip('MAPE', '${metrics['MAPE']}%', Colors.purple),
                    _MetricChip('R²',   '${metrics['R2'] ?? 'N/A'}',    kSprout),
                  ],
                ),
              ],
            ),
          ),
        ),

      const SizedBox(height: 12),

      // Ensemble breakdown
      if (breakDn != null && breakDn.isNotEmpty)
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const _SectionHeader('Ensemble Breakdown', small: true),
                const SizedBox(height: 10),
                ...breakDn.entries.map((e) {
                  final w = (e.value['weight'] as num?)?.toDouble() ?? 0;
                  final color = kModelColors[e.key] ?? kLeaf;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Row(children: [
                      SizedBox(
                        width: 90,
                        child: Text(e.key.toUpperCase(),
                            style: TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.w700,
                                color: color)),
                      ),
                      Expanded(
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(4),
                          child: LinearProgressIndicator(
                            value: w,
                            backgroundColor: kBorder,
                            valueColor: AlwaysStoppedAnimation(color),
                            minHeight: 10,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text('${(w * 100).round()}%',
                          style: const TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.w700,
                              color: kForest,
                              fontFamily: 'monospace')),
                    ]),
                  );
                }),
              ],
            ),
          ),
        ),

      const SizedBox(height: 12),

      // Advice card
      if (advice != null)
        _AdviceCard(
          text: T.rw
              ? (advice['tip_rw'] as String? ?? '')
              : (advice['tip_en'] as String? ?? ''),
        ),

      const SizedBox(height: 12),

      // Forecast table
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _SectionHeader(
                T.rw ? 'Amakuru Yuzuye' : 'Weekly Forecast Details',
                small: true,
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  headingRowColor: WidgetStateProperty.all(kSkyPale),
                  headingTextStyle: const TextStyle(
                      fontWeight: FontWeight.w700,
                      color: kForest,
                      fontSize: 12),
                  dataTextStyle: const TextStyle(
                      fontSize: 11, fontFamily: 'monospace'),
                  columnSpacing: 16,
                  columns: [
                    DataColumn(label: Text(T.week)),
                    const DataColumn(label: Text('Date')),
                    const DataColumn(label: Text('Demand kg')),
                    const DataColumn(label: Text('CI Low')),
                    const DataColumn(label: Text('CI High')),
                    const DataColumn(label: Text('Bags')),
                    const DataColumn(label: Text('Season')),
                  ],
                  rows: fc.map((row) {
                    final d  = (row['demand_kg'] as num?)?.toDouble() ?? 0;
                    final s  = row['season'] as String? ?? 'A';
                    final isHi = d == maxD;
                    final isLo = d == minD;
                    return DataRow(
                      color: WidgetStateProperty.all(
                          isHi ? kSkyPale : isLo
                              ? kRed.withValues(alpha: 0.05) : null),
                      cells: [
                        DataCell(Text('W${row["week"]}',
                            style: const TextStyle(fontWeight: FontWeight.w700))),
                        DataCell(Text('${row["date"]}')),
                        DataCell(Text(fmtFull(d.round()),
                            style: TextStyle(
                                fontWeight: isHi || isLo
                                    ? FontWeight.w700 : FontWeight.normal,
                                color: isHi ? kSprout : isLo ? kRed : kText))),
                        DataCell(Text(fmtFull(
                            (row['lower_kg'] as num?)?.round() ?? 0))),
                        DataCell(Text(fmtFull(
                            (row['upper_kg'] as num?)?.round() ?? 0))),
                        DataCell(Text('${row["demand_bags"] ?? 0}')),
                        DataCell(_SeasonBadge(s)),
                      ],
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
        ),
      ),
    ]);
  }
}
// =============================================================
//  PLANTING ADVICE SHEET
// =============================================================
class _PlantingAdviceSheet extends StatelessWidget {
  final Map<String, dynamic> advice;
  const _PlantingAdviceSheet({required this.advice});

  String _fmtK(int v) {
    if (v >= 1000) return '${(v / 1000).toStringAsFixed(1)}k';
    return '$v';
  }

  @override
  Widget build(BuildContext context) {
    final cropName    = advice['crop_name']     as String;
    final peakWeek    = advice['peak_week']      as int;
    final peakDate    = advice['peak_date']      as String;
    final peakKg      = advice['peak_demand_kg'] as int;
    final targetKg    = advice['target_kg']      as int;
    final plantingKg  = advice['planting_kg']    as int;
    final seedBags    = advice['seed_bags']      as int;
    final bagKg       = advice['bag_kg']         as int;
    final requiredAcres = (advice['required_acres'] as num).toDouble();
    final farmSize    = (advice['farm_size']     as num).toDouble();
    final marketShare = (advice['market_share']  as num).toDouble();
    final weeksToPlant = advice['weeks_to_plant'] as int;
    final plantByDate = advice['plant_by_date']  as String;
    final urgency     = advice['urgency']        as String;
    final urgencyMsg  = advice['urgency_msg']    as String;
    final marketSignal = advice['market_signal'] as String;
    final signalMsg   = advice['signal_msg']     as String;
    final trendMsg    = advice['trend_msg']      as String;
    final weeksLeft   = advice['weeks_to_peak']  as int;
    final window      = urgencyMsg;
    final crop       = kCrops.firstWhere(
        (c) => c.en == cropName || c.rw == cropName,
        orElse: () => kCrops.first);

    final urgencyColor = weeksLeft <= 4 ? kRed
        : weeksLeft <= 10 ? kAmber
        : kBlue;

    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 40, height: 4,
              decoration: BoxDecoration(
                color: kBorder,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 16),

            Row(children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: kSprout.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Text(crop.icon,
                    style: const TextStyle(fontSize: 28)),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '🌱 ${T.plantingReco}',
                      style: const TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w800,
                          color: kForest),
                    ),
                    Text(cropName,
                        style: const TextStyle(
                            fontSize: 13, color: kMuted)),
                  ],
                ),
              ),
            ]),
            const SizedBox(height: 20),

            // ── HERO: Grow X kg + Expected Revenue ─────────────────
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [kForest, Color(0xFF1A6E1A)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    T.rw ? 'Igice cyawe cyo gutera:' : 'Your growing target:',
                    style: const TextStyle(color: Color(0xFF89B889), fontSize: 12),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    '${_fmtK(targetKg)} kg',
                    style: const TextStyle(
                        color: Colors.white,
                        fontSize: 38,
                        fontWeight: FontWeight.w900,
                        height: 1.0),
                  ),
                  Text(
                    T.rw
                        ? 'Tera $cropName uyu mwaka'
                        : 'Grow $cropName this season',
                    style: const TextStyle(
                        color: Color(0xFF89B889), fontSize: 13),
                  ),
                  const SizedBox(height: 14),
                  Container(
                    height: 1,
                    color: Colors.white.withValues(alpha: 0.15),
                  ),
                  const SizedBox(height: 14),
                  Row(children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            T.rw ? 'Inyungu iteganijwe' : 'Expected income',
                            style: const TextStyle(
                                color: Color(0xFF89B889), fontSize: 11),
                          ),
                          const SizedBox(height: 3),
                          Text(
                            'Rwf ${_fmtK((targetKg * (advice["avg_price"] as num? ?? 500)).round())}',
                            style: const TextStyle(
                                color: Colors.white,
                                fontSize: 20,
                                fontWeight: FontWeight.w800),
                          ),
                        ],
                      ),
                    ),
                    Container(width: 1, height: 36, color: Colors.white.withValues(alpha: 0.15)),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            T.rw ? 'Ibihe byiza kugurisha' : 'Best sell week',
                            style: const TextStyle(
                                color: Color(0xFF89B889), fontSize: 11),
                          ),
                          const SizedBox(height: 3),
                          Text(
                            'Wk $peakWeek · $peakDate',
                            style: const TextStyle(
                                color: Colors.white,
                                fontSize: 14,
                                fontWeight: FontWeight.w700),
                          ),
                        ],
                      ),
                    ),
                  ]),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // ── Farm stats bar (compact, no market share %) ─────────
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: kSprout.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: kSprout.withValues(alpha: 0.2)),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _FarmStat('🏡', T.rw ? 'Inzara' : 'Farm',
                      '${farmSize.toStringAsFixed(1)} ac'),
                  _FarmStat('🌾', T.rw ? 'Akare' : 'Acres needed',
                      '${requiredAcres.toStringAsFixed(2)} ac'),
                  _FarmStat('📅', T.rw ? 'Ibyumweru' : 'Weeks left',
                      '$weeksToPlant'),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // ── 3 KPI cards ─────────────────────────────────────────
            Row(children: [
              Expanded(child: _AdviceKpi(
                icon: '🌱',
                label: T.rw ? 'Gutera (kg)' : 'Plant (kg)',
                value: _fmtK(plantingKg),
                color: kSprout,
                sub: T.rw ? 'hamwe na 20%' : 'incl. 20% buffer',
              )),
              const SizedBox(width: 10),
              Expanded(child: _AdviceKpi(
                icon: '📦',
                label: T.rw ? 'Amasaho' : 'Seed Bags',
                value: '$seedBags',
                color: kStraw,
                sub: '$bagKg kg/bag',
              )),
              const SizedBox(width: 10),
              Expanded(child: _AdviceKpi(
                icon: '⏰',
                label: T.rw ? 'Ibyumweru' : 'Wks to Plant',
                value: '$weeksToPlant',
                color: urgencyColor,
                sub: T.rw ? 'mbere yo gutera' : 'before deadline',
              )),
            ]),
            const SizedBox(height: 14),

            // ── When to plant ────────────────────────────────────────
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: kSkyPale,
                borderRadius: BorderRadius.circular(14),
                border: const Border(
                    left: BorderSide(color: kSprout, width: 4)),
              ),
              child: Row(children: [
                const Text('📅', style: TextStyle(fontSize: 22)),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(T.rw ? 'Igihe cyo Gutera' : 'When to Plant',
                          style: const TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 12,
                              color: kForest)),
                      const SizedBox(height: 2),
                      Text(urgencyMsg.isNotEmpty ? urgencyMsg : window,
                          style: const TextStyle(
                              fontSize: 13,
                              color: kText,
                              height: 1.5)),
                      if (plantByDate.isNotEmpty) ...[
                        const SizedBox(height: 4),
                        Text(
                          '${T.rw ? "Teranya:" : "Plant by:"} $plantByDate',
                          style: const TextStyle(
                              fontSize: 11,
                              color: kMuted,
                              fontWeight: FontWeight.w600),
                        ),
                      ],
                    ],
                  ),
                ),
              ]),
            ),
            const SizedBox(height: 14),

            // ── Market signal (oversupply / shortage / balanced) ─────
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: marketSignal == 'oversupply_risk'
                    ? kRed.withValues(alpha: 0.06)
                    : marketSignal == 'shortage_risk'
                        ? kSprout.withValues(alpha: 0.06)
                        : kAmber.withValues(alpha: 0.06),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(
                  color: marketSignal == 'oversupply_risk'
                      ? kRed.withValues(alpha: 0.25)
                      : marketSignal == 'shortage_risk'
                          ? kSprout.withValues(alpha: 0.25)
                          : kAmber.withValues(alpha: 0.25),
                ),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    marketSignal == 'oversupply_risk' ? '⚠️'
                        : marketSignal == 'shortage_risk' ? '🚀' : '✅',
                    style: const TextStyle(fontSize: 20),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          marketSignal == 'oversupply_risk'
                              ? (T.rw ? 'Icyitonderwa: Isoko' : 'Market Warning')
                              : marketSignal == 'shortage_risk'
                                  ? (T.rw ? 'Amahirwe: Isoko' : 'Market Opportunity')
                                  : (T.rw ? 'Isoko Iringaniye' : 'Market Balanced'),
                          style: TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 12,
                              color: marketSignal == 'oversupply_risk'
                                  ? kRed : marketSignal == 'shortage_risk'
                                      ? kSprout : kAmber),
                        ),
                        const SizedBox(height: 4),
                        Text(signalMsg,
                            style: const TextStyle(
                                fontSize: 12, color: kText, height: 1.5)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),

            // ── Why this forecast ────────────────────────────────────
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: kAmber.withValues(alpha: 0.07),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: kAmber.withValues(alpha: 0.25)),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('💡', style: TextStyle(fontSize: 20)),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(trendMsg,
                        style: const TextStyle(
                            fontSize: 12, color: kText, height: 1.6)),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(context),
                child: Text(T.gotIt),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FarmStat extends StatelessWidget {
  final String icon, label, value;
  const _FarmStat(this.icon, this.label, this.value);
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(icon, style: const TextStyle(fontSize: 18)),
        const SizedBox(height: 2),
        Text(value,
            style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w800,
                color: kForest)),
        Text(label,
            style: const TextStyle(fontSize: 10, color: kMuted)),
      ],
    );
  }
}

class _AdviceKpi extends StatelessWidget {
  final String icon, label, value, sub;
  final Color color;
  const _AdviceKpi({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
    required this.sub,
  });

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 8),
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.08),
      borderRadius: BorderRadius.circular(14),
      border: Border.all(color: color.withValues(alpha: 0.2)),
    ),
    child: Column(children: [
      Text(icon, style: const TextStyle(fontSize: 20)),
      const SizedBox(height: 4),
      Text(value,
          style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w900,
              color: color)),
      const SizedBox(height: 2),
      Text(label,
          textAlign: TextAlign.center,
          style: const TextStyle(
              fontSize: 9,
              color: kForest,
              fontWeight: FontWeight.w600)),
      Text(sub,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 8, color: kMuted)),
    ]),
  );
}
// =============================================================
//  PRICE PAGE
// =============================================================
class PricePage extends StatefulWidget {
  final ValueChanged<Map<String, dynamic>>? onResult;
  const PricePage({super.key, this.onResult});
  @override
  State<PricePage> createState() => _PricePageState();
}

class _PricePageState extends State<PricePage> {
  int    _cropId  = 1;
  String _model   = 'ensemble';
  int    _weeks   = 12;
  bool   _loading = false;
  Map<String, dynamic>? _result;
  String? _error;

  Future<void> _fetch() async {
    setState(() { _loading = true; _error = null; _result = null; });
    try {
      final d = await ApiService.get(
          '/price_forecast/$_cropId?model=$_model&weeks=$_weeks');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
widget.onResult?.call(d);
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
      children: [
        _ControlCard(
          title: T.price,
          subtitle: T.rw
              ? 'Teganya igiciro cy\'ibihingwa mu RWF'
              : 'Predict weekly crop prices in RWF/kg',
          children: [
            _CropDropdown(
                value: _cropId,
                onChanged: (v) => setState(() => _cropId = v)),
            const SizedBox(height: 12),
            _ModelDropdown(
                value: _model,
                onChanged: (v) => setState(() => _model = v)),
            const SizedBox(height: 12),
            _WeeksSlider(
                value: _weeks,
                onChanged: (v) => setState(() => _weeks = v)),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _fetch,
                icon: _loading
                    ? const SizedBox(width: 18, height: 18,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.attach_money),
                label: Text(T.getPrice),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        if (_error != null) _ErrorBanner(_error!),
        if (_result != null) _PriceResultView(data: _result!),
      ],
    );
  }
}

class _PriceResultView extends StatelessWidget {
  final Map<String, dynamic> data;
  const _PriceResultView({required this.data});

  @override
  Widget build(BuildContext context) {
    final fc      = data['forecast'] as List;
    final advice  = data['advice']   as Map<String, dynamic>?;
    final cropNm  = data['crop_name']   as String? ?? '';
    final model   = data['model']       as String? ?? '';
    final bestWk  = data['best_week']   as int? ?? 1;
    final maxP    = (data['max_price']  as num?)?.toDouble() ?? 0;
    final minP    = (data['min_price']  as num?)?.toDouble() ?? 0;
    final curP    = (data['current_price'] as num?)?.toDouble() ?? 0;

    final prices  = fc.map((f) => (f['price_rwf'] as num?)?.toDouble() ?? 0.0).toList();

    final barGroups = fc.asMap().entries.map((e) {
      final v     = prices[e.key];
      final color = v == maxP ? kSprout : v == minP ? kRed : kStraw;
      return BarChartGroupData(x: e.key, barRods: [
        BarChartRodData(
          toY: v,
          color: color,
          width: math.min(32.0, 320.0 / fc.length),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(5)),
          backDrawRodData: BackgroundBarChartRodData(
            show: true,
            toY: maxP * 1.15,
            color: kBorder.withValues(alpha: 0.4),
          ),
        ),
      ]);
    }).toList();

    return Column(children: [
      // KPI row
      Row(children: [
        Expanded(child: _StatChip('Current', '${fmtNum(curP)} RWF', kMuted)),
        const SizedBox(width: 8),
        Expanded(child: _StatChip(T.maxPrice, '${fmtNum(maxP)} RWF', kSprout)),
        const SizedBox(width: 8),
        Expanded(child: _StatChip(T.bestSell, 'Week $bestWk', kStraw)),
      ]),
      const SizedBox(height: 12),

      // Bar chart
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('$cropNm — $model Price Forecast',
                  style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 15, color: kForest)),
              Text('RWF/kg · ${data["weeks"]}-week outlook',
                  style: const TextStyle(fontSize: 11, color: kMuted)),
              const SizedBox(height: 14),
              SizedBox(
                height: 220,
                child: BarChart(BarChartData(
                  barGroups: barGroups,
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(
                        sideTitles: SideTitles(
                          showTitles: true,
                          reservedSize: 54,
                          getTitlesWidget: (v, m) => Text(
                              fmtNum(v),
                              style: const TextStyle(
                                  fontSize: 9, color: kMuted)),
                        )),
                    bottomTitles: AxisTitles(
                        sideTitles: SideTitles(
                          showTitles: true,
                          interval: (fc.length / 4).ceilToDouble(),
                          getTitlesWidget: (v, m) => Text(
                              'W${v.toInt() + 1}',
                              style: const TextStyle(
                                  fontSize: 9, color: kMuted)),
                        )),
                    rightTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false)),
                    topTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false)),
                  ),
                  gridData: FlGridData(
                    show: true,
                    getDrawingHorizontalLine: (_) =>
                        const FlLine(color: kBorder, strokeWidth: 1),
                    drawVerticalLine: false,
                  ),
                  borderData: FlBorderData(show: false),
                  barTouchData: BarTouchData(
                    touchTooltipData: BarTouchTooltipData(
                      getTooltipColor: (_) => kForest.withValues(alpha: 0.9),
                      getTooltipItem: (g, _, r, __) =>
                          BarTooltipItem(
                            'W${g.x + 1}\n${fmtFull(r.toY.round())} RWF',
                            const TextStyle(
                                color: Colors.white,
                                fontSize: 11,
                                fontWeight: FontWeight.w600),
                          ),
                    ),
                  ),
                )),
              ),
            ],
          ),
        ),
      ),
      const SizedBox(height: 12),

      // Advice
      if (advice != null)
        _AdviceCard(
          icon: '💰',
          text: T.rw
              ? (advice['tip_rw'] as String? ?? '')
              : (advice['tip_en'] as String? ?? ''),
        ),
      const SizedBox(height: 12),

      // Price table
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _SectionHeader(
                T.rw ? "Amakuru y'Igiciro" : 'Weekly Price Details',
                small: true),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  headingRowColor: WidgetStateProperty.all(kSkyPale),
                  headingTextStyle: const TextStyle(
                      fontWeight: FontWeight.w700,
                      color: kForest, fontSize: 12),
                  dataTextStyle: const TextStyle(
                      fontSize: 11, fontFamily: 'monospace'),
                  columnSpacing: 14,
                  columns: const [
                    DataColumn(label: Text('Wk')),
                    DataColumn(label: Text('Date')),
                    DataColumn(label: Text('Price RWF')),
                    DataColumn(label: Text('CI Low')),
                    DataColumn(label: Text('CI High')),
                    DataColumn(label: Text('Trend')),
                  ],
                  rows: fc.map((row) {
                    final p    = (row['price_rwf'] as num?)?.toDouble() ?? 0;
                    final isHi = p == maxP;
                    final isLo = p == minP;
                    final up   = row['trend'] == 'up';
                    return DataRow(
                      color: WidgetStateProperty.all(
                          isHi ? kSkyPale
                              : isLo ? kRed.withValues(alpha: 0.05) : null),
                      cells: [
                        DataCell(Text('W${row["week"]}',
                            style: const TextStyle(fontWeight: FontWeight.w700))),
                        DataCell(Text('${row["date"]}')),
                        DataCell(Text(fmtFull(p.round()),
                            style: TextStyle(
                                fontWeight: isHi || isLo
                                    ? FontWeight.w700 : FontWeight.normal,
                                color: isHi ? kSprout : isLo ? kRed : kText))),
                        DataCell(Text(fmtFull(
                            (row['lower_kg'] as num?)?.round() ?? 0))),
                        DataCell(Text(fmtFull(
                            (row['upper_kg'] as num?)?.round() ?? 0))),
                        DataCell(Row(children: [
                          Icon(up ? Icons.arrow_upward : Icons.arrow_downward,
                              size: 13,
                              color: up ? kSprout : kRed),
                          Text(up ? 'Up' : 'Down',
                              style: TextStyle(
                                  color: up ? kSprout : kRed,
                                  fontWeight: FontWeight.w600)),
                        ])),
                      ],
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
        ),
      ),
    ]);
  }
}

// =============================================================
//  COMPARE PAGE
// =============================================================
class ComparePage extends StatefulWidget {
  const ComparePage({super.key});
  @override
  State<ComparePage> createState() => _ComparePageState();
}

class _ComparePageState extends State<ComparePage> {
  int  _cropId = 1;
  int  _weeks  = 12;
  bool _loading = false;
  Map<String, dynamic>? _result;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (UserSession.lastCropId != null) _cropId = UserSession.lastCropId!;
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() { _loading = true; _error = null; _result = null; });
    try {
      final d = await ApiService.get(
          '/compare/$_cropId?weeks=$_weeks');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }

  static const _medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'];

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
      children: [
        _ControlCard(
          title: T.compare,
          subtitle: T.rw
              ? 'Gereranya indorerezi 5 zegeranya'
              : 'Compare all 4 models for your last forecasted crop',
          children: [
            _CropDropdown(
                value: _cropId,
                onChanged: (v) => setState(() => _cropId = v)),
            const SizedBox(height: 12),
            _WeeksSlider(
                value: _weeks,
                onChanged: (v) => setState(() => _weeks = v)),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _fetch,
                icon: _loading
                    ? const SizedBox(width: 18, height: 18,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.compare_arrows),
                label: Text(T.runCompare),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        if (_error != null) _ErrorBanner(_error!),
        if (_result != null) ..._buildResult(_result!),
      ],
    );
  }

  List<Widget> _buildResult(Map<String, dynamic> d) {
    final models = d['models'] as Map<String, dynamic>;
    final fc     = d['dates']  as List;

    // Collect ranked by MAPE
    final ranked = models.entries
        .where((e) => (e.value['metrics'] as Map?)?.containsKey('MAPE') == true)
        .map((e) => {
              'name': e.key,
              ...(e.value['metrics'] as Map<String, dynamic>),
            })
        .toList()
      ..sort((a, b) =>
          ((a['MAPE'] as num?)?.toDouble() ?? 0).compareTo((b['MAPE'] as num?)?.toDouble() ?? 0));

    // Multi-line chart datasets
    final datasets = models.entries.map((e) {
      final name    = e.key;
      final fcs     = (e.value['forecast'] as List? ?? [])
          .asMap()
          .entries
          .map((x) => FlSpot(x.key.toDouble(),
              (x.value as num?)?.toDouble() ?? 0.0))
          .toList();
      final color = kModelColors[name] ?? kLeaf;
      final isEns = name == 'ensemble';
      return LineChartBarData(
        spots: fcs,
        isCurved: true,
        color: color,
        barWidth: isEns ? 3 : 1.5,
        dotData: const FlDotData(show: false),
        dashArray: isEns ? null : [6, 4],
      );
    }).toList();

    // Max Y for scale
    double maxY = 0;
    for (final e in models.entries) {
      final fcs = (e.value['forecast'] as List? ?? []);
      for (final v in fcs) {
        if (((v as num?)?.toDouble() ?? 0.0) > maxY) maxY = (v)!.toDouble();
      }
    }

    return [
      // Legend
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                T.rw ? 'Ishusho y\'Iteganyabikorwa' : 'Forecast Overlay — All Models',
                style: const TextStyle(
                    fontWeight: FontWeight.w800,
                    fontSize: 15, color: kForest)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 14, runSpacing: 6,
                children: kModelColors.entries.map((e) => Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 20, height: 3,
                      decoration: BoxDecoration(
                        color: e.value,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                    const SizedBox(width: 5),
                    Text(e.key.toUpperCase(),
                        style: const TextStyle(
                            fontSize: 10, fontWeight: FontWeight.w600,
                            color: kMuted)),
                  ],
                )).toList(),
              ),
              const SizedBox(height: 14),
              SizedBox(
                height: 240,
                child: LineChart(LineChartData(
                  lineBarsData: datasets,
                  minY: 0,
                  maxY: maxY * 1.1,
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(sideTitles: SideTitles(
                      showTitles: true, reservedSize: 52,
                      getTitlesWidget: (v, m) => Text(
                          fmtNum(v),
                          style: const TextStyle(fontSize: 9, color: kMuted)),
                    )),
                    bottomTitles: AxisTitles(sideTitles: SideTitles(
                      showTitles: true,
                      interval: (fc.length / 4).ceilToDouble(),
                      getTitlesWidget: (v, m) => Text(
                          'W${v.toInt() + 1}',
                          style: const TextStyle(fontSize: 9, color: kMuted)),
                    )),
                    rightTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false)),
                    topTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false)),
                  ),
                  gridData: FlGridData(
                    show: true,
                    getDrawingHorizontalLine: (_) =>
                        const FlLine(color: kBorder, strokeWidth: 1),
                    drawVerticalLine: false,
                  ),
                  borderData: FlBorderData(
                      show: true,
                      border: Border.all(color: kBorder)),
                )),
              ),
            ],
          ),
        ),
      ),
      const SizedBox(height: 12),

      // Accuracy leaderboard
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _SectionHeader(
                T.rw ? 'Gereranya Imibare' : 'Accuracy Leaderboard',
                small: true),
              const SizedBox(height: 10),
              ...ranked.asMap().entries.map((e) {
                final m     = e.value;
                final name  = m['name'] as String;
                final mape  = (m['MAPE'] as num?)?.toDouble() ?? 0;
                final color = kModelColors[name] ?? kLeaf;
                final maxMape = ranked.isNotEmpty
                    ? (ranked.last['MAPE'] as num?)?.toDouble() ?? 1.0 : 1;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: Row(children: [
                    Text(_medals[e.key],
                        style: const TextStyle(fontSize: 18)),
                    const SizedBox(width: 8),
                    SizedBox(
                      width: 80,
                      child: Text(name.toUpperCase(),
                          style: TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.w700,
                              color: color)),
                    ),
                    Expanded(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(4),
                        child: LinearProgressIndicator(
                          value: (1 - mape / math.max(maxMape, 1))
                              .clamp(0.0, 1.0),
                          backgroundColor: kBorder,
                          valueColor: AlwaysStoppedAnimation(color),
                          minHeight: 10,
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text('${mape.toStringAsFixed(1)}%',
                        style: const TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w700,
                            color: kForest,
                            fontFamily: 'monospace')),
                  ]),
                );
              }),
            ],
          ),
        ),
      ),
      const SizedBox(height: 12),

      // Full metrics table
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _SectionHeader(
                T.rw ? 'Amakuru Yuzuye y\'Imibare' : 'Full Metrics Table',
                small: true),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  headingRowColor: WidgetStateProperty.all(
                      kForest.withValues(alpha: 0.08)),
                  headingTextStyle: const TextStyle(
                      fontWeight: FontWeight.w700,
                      color: kForest, fontSize: 12),
                  dataTextStyle: const TextStyle(
                      fontSize: 11, fontFamily: 'monospace'),
                  columnSpacing: 16,
                  columns: const [
                    DataColumn(label: Text('Model')),
                    DataColumn(label: Text('MAE')),
                    DataColumn(label: Text('RMSE')),
                    DataColumn(label: Text('MAPE%')),
                    DataColumn(label: Text('R²')),
                    DataColumn(label: Text('Rank')),
                  ],
                  rows: ranked.asMap().entries.map((e) {
                    final m    = e.value;
                    final name = m['name'] as String;
                    final best = e.key == 0;
                    return DataRow(
                      color: WidgetStateProperty.all(
                          best ? kSkyPale : null),
                      cells: [
                        DataCell(Text(name.toUpperCase(),
                            style: TextStyle(
                              fontWeight: FontWeight.w700,
                              color: kModelColors[name] ?? kLeaf,
                            ))),
                        DataCell(Text(
                            fmtNum((m['MAE'] as num?)?.toDouble() ?? 0))),
                        DataCell(Text(
                            fmtNum((m['RMSE'] as num?)?.toDouble() ?? 0))),
                        DataCell(Text('${m["MAPE"]}%',
                            style: TextStyle(
                                color: best ? kSprout : kText,
                                fontWeight: best
                                    ? FontWeight.w700 : FontWeight.normal))),
                        DataCell(Text('${m["R2"]}')),
                        DataCell(Text(_medals[e.key],
                            style: const TextStyle(fontSize: 16))),
                      ],
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
        ),
      ),
    ];
  }
}

// =============================================================
//  ALERTS PAGE
// =============================================================
class AlertsPage extends StatefulWidget {
  const AlertsPage({super.key});
  @override
  State<AlertsPage> createState() => _AlertsPageState();
}

class _AlertsPageState extends State<AlertsPage> {
  int  _cropId  = 1;
  bool _loading = false;
  Map<String, dynamic>? _result;
  String? _error;

  @override
  void initState() {
    super.initState();
    // Auto-use last forecasted crop
    if (UserSession.lastCropId != null) _cropId = UserSession.lastCropId!;
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() { _loading = true; _error = null; _result = null; });
    try {
      final d = await ApiService.get('/alerts/$_cropId');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }

  Color _sevColor(String s) => switch (s) {
    'high'   => kRed,
    'medium' => kAmber,
    'low'    => kStraw,
    _        => kBlue,
  };

  IconData _sevIcon(String s) => switch (s) {
    'high'   => Icons.warning_rounded,
    'medium' => Icons.info_outline,
    'low'    => Icons.notifications_outlined,
    _        => Icons.lightbulb_outline,
  };

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
      children: [
        _ControlCard(
          title: T.alerts,
          subtitle: T.rw
              ? 'Imenyesha y\'AI ishingiye ku iteganyabikorwa rya ibyumweru 8'
              : 'AI-generated alerts based on 8-week ensemble forecast',
          children: [
            _CropDropdown(
                value: _cropId,
                onChanged: (v) => setState(() => _cropId = v)),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _fetch,
                icon: _loading
                    ? const SizedBox(width: 18, height: 18,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.notifications_active),
                label: Text(T.rw ? 'Shyira Imenyesha' : 'Load Alerts'),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        if (_error != null) _ErrorBanner(_error!),
        if (_result != null) ...[
          // Season header
          Container(
            padding: const EdgeInsets.symmetric(
                horizontal: 16, vertical: 10),
            decoration: BoxDecoration(
              color: seasonColor(
                  _result!['season'] as String? ?? 'A').withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: seasonColor(
                    _result!['season'] as String? ?? 'A').withValues(alpha: 0.3),
              ),
            ),
            child: Row(children: [
              Text(
                '🗓 ${_result!["season_label"] ?? ""}',
                style: TextStyle(
                  fontWeight: FontWeight.w700,
                  fontSize: 13,
                  color: seasonColor(_result!['season'] as String? ?? 'A'),
                ),
              ),
              const Spacer(),
              Text(
                '${_result!["total"] ?? 0} alert(s)',
                style: const TextStyle(color: kMuted, fontSize: 12),
              ),
            ]),
          ),
          const SizedBox(height: 12),

          // Alert cards
          ...(_result!['alerts'] as List? ?? []).map((a) {
            final sev  = a['level'] as String? ?? 'info';
            final col  = _sevColor(sev);
            final icon = _sevIcon(sev);
            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(14),
                border: Border(left: BorderSide(color: col, width: 4)),
                boxShadow: [
                  BoxShadow(
                    color: col.withValues(alpha: 0.08),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(children: [
                    Icon(icon, color: col, size: 20),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        a['title_en'] as String? ?? '',
                        style: TextStyle(
                          fontWeight: FontWeight.w800,
                          fontSize: 13,
                          color: col,
                        ),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: col.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(sev.toUpperCase(),
                          style: TextStyle(
                              color: col,
                              fontSize: 9,
                              fontWeight: FontWeight.w700)),
                    ),
                  ]),
                  const SizedBox(height: 8),
                  Text(
                    T.rw
                        ? (a['msg_rw'] as String? ?? '')
                        : (a['msg_en'] as String? ?? ''),
                    style: const TextStyle(
                        fontSize: 13, color: kText, height: 1.6),
                  ),
                  if ((a['value'] as num? ?? 0) > 0) ...[
                    const SizedBox(height: 8),
                    Text(
                      'Week ${a["week"]}  ·  '
                      '${((a["change_pct"] as num?) ?? 0) >= 0 ? "+" : ""}'
                      '${a["change_pct"]}% vs avg  ·  '
                      '${fmtFull(a["value"] as num? ?? 0)}',
                      style: const TextStyle(
                          fontSize: 10,
                          color: kMuted,
                          fontFamily: 'monospace'),
                    ),
                  ],
                ],
              ),
            );
          }),
        ],
      ],
    );
  }
}

// =============================================================
//  SHARED WIDGETS
// =============================================================

/// Reusable control panel card
class _ControlCard extends StatelessWidget {
  final String title, subtitle;
  final List<Widget> children;
  const _ControlCard({
    required this.title,
    required this.subtitle,
    required this.children,
  });

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(18),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style: const TextStyle(
                  fontWeight: FontWeight.w800,
                  fontSize: 17,
                  color: kForest)),
          const SizedBox(height: 3),
          Text(subtitle,
              style: const TextStyle(fontSize: 12, color: kMuted)),
          const SizedBox(height: 18),
          ...children,
        ],
      ),
    ),
  );
}

/// Crop dropdown
class _CropDropdown extends StatelessWidget {
  final int value;
  final ValueChanged<int> onChanged;
  const _CropDropdown({required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) => DropdownButtonFormField<int>(
    initialValue: value,
    decoration: InputDecoration(
      labelText: T.selectCrop,
      prefixIcon: const Icon(Icons.eco_outlined, color: kLeaf),
    ),
    items: kCrops.map((c) => DropdownMenuItem<int>(
      value: c.id,
      child: Text('${c.icon}  ${c.name}'),
    )).toList(),
    onChanged: (v) { if (v != null) onChanged(v); },
  );
}

/// Model dropdown
class _ModelDropdown extends StatelessWidget {
  final String value;
  final ValueChanged<String> onChanged;
  const _ModelDropdown({required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) => DropdownButtonFormField<String>(
    initialValue: value,
    decoration: InputDecoration(
      labelText: T.selectModel,
      prefixIcon: const Icon(Icons.model_training, color: kLeaf),
    ),
    items: kModels.map((m) => DropdownMenuItem<String>(
      value: m['value'],
      child: Text(T.rw ? m['rw']! : m['en']!),
    )).toList(),
    onChanged: (v) { if (v != null) onChanged(v); },
  );
}

/// Weeks slider
class _WeeksSlider extends StatelessWidget {
  final int value;
  final ValueChanged<int> onChanged;
  const _WeeksSlider({required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Row(children: [
        Text('${T.weeksAhead}: ',
            style: const TextStyle(
                fontSize: 13, color: kMuted, fontWeight: FontWeight.w500)),
        Text('$value',
            style: const TextStyle(
                fontSize: 13, color: kForest, fontWeight: FontWeight.w700)),
        Text(T.rw ? ' ibyumweru' : ' weeks',
            style: const TextStyle(fontSize: 13, color: kMuted)),
      ]),
      Slider(
        value: value.toDouble(),
        min: 4, max: 24,
        divisions: 5,
        activeColor: kSprout,
        inactiveColor: kBorder,
        label: '$value',
        onChanged: (v) => onChanged(v.round()),
      ),
    ],
  );
}

class _SectionHeader extends StatelessWidget {
  final String text;
  final bool small;
  const _SectionHeader(this.text, {this.small = false});

  @override
  Widget build(BuildContext context) => Text(text,
      style: TextStyle(
        fontWeight: FontWeight.w800,
        fontSize: small ? 14 : 16,
        color: kForest,
      ));
}

class _FieldCard extends StatelessWidget {
  final List<Widget> children;
  const _FieldCard({required this.children});

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(18),
      child: Column(children: children),
    ),
  );
}

class _LangToggle extends StatefulWidget {
  final ValueChanged<bool> onChanged;
  const _LangToggle({required this.onChanged});

  @override
  State<_LangToggle> createState() => _LangToggleState();
}

class _LangToggleState extends State<_LangToggle> {
  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Text('EN',
          style: TextStyle(
              fontSize: 11,
              fontWeight: T.rw ? FontWeight.normal : FontWeight.w700,
              color: T.rw ? kMuted : kLeaf)),
      Transform.scale(
        scale: 0.8,
        child: Switch(
          value: T.rw,
          activeThumbColor: kStraw,
          onChanged: (v) {
            T.rw = v;
            widget.onChanged(v);
            setState(() {});
          },
        ),
      ),
      Text('RW',
          style: TextStyle(
              fontSize: 11,
              fontWeight: T.rw ? FontWeight.w700 : FontWeight.normal,
              color: T.rw ? kStraw : kMuted)),
    ],
  );
}

class _ErrorBanner extends StatelessWidget {
  final String message;
  const _ErrorBanner(this.message);

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(14),
    margin: const EdgeInsets.only(bottom: 8),
    decoration: BoxDecoration(
      color: kRed.withValues(alpha: 0.08),
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: kRed.withValues(alpha: 0.3)),
    ),
    child: Row(children: [
      const Icon(Icons.error_outline, color: kRed, size: 20),
      const SizedBox(width: 10),
      Expanded(
          child: Text(message,
              style: const TextStyle(color: kRed, fontSize: 13))),
    ]),
  );
}

class _SuccessBanner extends StatelessWidget {
  final String message;
  const _SuccessBanner(this.message);

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(14),
    margin: const EdgeInsets.only(bottom: 8),
    decoration: BoxDecoration(
      color: kSprout.withValues(alpha: 0.08),
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: kSprout.withValues(alpha: 0.3)),
    ),
    child: Row(children: [
      const Icon(Icons.check_circle_outline, color: kSprout, size: 20),
      const SizedBox(width: 10),
      Expanded(
          child: Text(message,
              style: const TextStyle(color: kSprout, fontSize: 13))),
    ]),
  );
}

class _AdviceCard extends StatelessWidget {
  final String text;
  final String icon;
  const _AdviceCard({required this.text, this.icon = '💡'});

  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 8),
    decoration: BoxDecoration(
      color: kSkyPale,
      borderRadius: BorderRadius.circular(14),
      border: const Border(left: BorderSide(color: kSprout, width: 4)),
    ),
    padding: const EdgeInsets.all(16),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(icon, style: const TextStyle(fontSize: 26)),
        const SizedBox(width: 12),
        Expanded(
          child: Text(text,
              style: const TextStyle(
                  fontSize: 13, color: Color(0xFF2D4A2D), height: 1.7)),
        ),
      ],
    ),
  );
}

class _LoadingCard extends StatelessWidget {
  const _LoadingCard();

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(28),
      child: Center(
        child: Column(children: [
          const CircularProgressIndicator(
              color: kSprout, strokeWidth: 3),
          const SizedBox(height: 14),
          Text(T.loading,
              style: const TextStyle(color: kMuted, fontSize: 13)),
        ]),
      ),
    ),
  );
}

class _SeasonBadge extends StatelessWidget {
  final String season;
  const _SeasonBadge(this.season);

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
    decoration: BoxDecoration(
      color: seasonColor(season).withValues(alpha: 0.12),
      borderRadius: BorderRadius.circular(8),
    ),
    child: Text('S$season',
        style: TextStyle(
            color: seasonColor(season),
            fontSize: 10,
            fontWeight: FontWeight.w700)),
  );
}

class _MetricChip extends StatelessWidget {
  final String label, value;
  final Color color;
  const _MetricChip(this.label, this.value, this.color);

  @override
  Widget build(BuildContext context) => Column(children: [
    Text(value,
        style: TextStyle(
            color: color,
            fontWeight: FontWeight.w900,
            fontSize: 17)),
    Text(label,
        style: const TextStyle(
            fontSize: 10, color: kMuted, fontWeight: FontWeight.w500)),
  ]);
}

class _StatChip extends StatelessWidget {
  final String label, value;
  final Color color;
  const _StatChip(this.label, this.value, this.color);

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.07),
      borderRadius: BorderRadius.circular(14),
      border: Border.all(color: color.withValues(alpha: 0.2)),
    ),
    child: Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
      Text(value,
          style: TextStyle(
              color: color,
              fontWeight: FontWeight.w900,
              fontSize: 15),
          textAlign: TextAlign.center),
      const SizedBox(height: 2),
      Text(label,
          style: const TextStyle(fontSize: 10, color: kMuted),
          textAlign: TextAlign.center),
    ]),
  );
}

class _MiniKpi extends StatelessWidget {
  final String label, value;
  final Color color;
  const _MiniKpi(this.label, this.value, this.color);

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.10),
      borderRadius: BorderRadius.circular(10),
    ),
    child: Column(children: [
      Text(value,
          style: TextStyle(
              color: color,
              fontWeight: FontWeight.w800,
              fontSize: 12)),
      Text(label,
          style: const TextStyle(fontSize: 9, color: kMuted)),
    ]),
  );
}
// =============================================================
//  REPORTS PAGE
// =============================================================
class _ReportItem extends StatelessWidget {
  final String icon, title, subtitle;
  const _ReportItem(this.icon, this.title, this.subtitle);

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 12),
    child: Row(children: [
      Text(icon, style: const TextStyle(fontSize: 22)),
      const SizedBox(width: 12),
      Expanded(
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title,
              style: const TextStyle(
                  fontWeight: FontWeight.w700,
                  fontSize: 13,
                  color: kForest)),
          Text(subtitle,
              style: const TextStyle(fontSize: 11, color: kMuted)),
        ]),
      ),
      const Icon(Icons.check_circle, color: kSprout, size: 18),
    ]),
  );
}
class ReportsPage extends StatefulWidget {
  final Map<String, dynamic>? Function() getForecastData;
  final Map<String, dynamic>? Function() getPriceData;
  const ReportsPage({
    super.key,
    required this.getForecastData,
    required this.getPriceData,
  });
  @override
  State<ReportsPage> createState() => _ReportsPageState();
}

class _ReportsPageState extends State<ReportsPage> {
  bool _generating = false;

  Future<void> _generatePdf({bool share=false}) async {
    final forecastData = widget.getForecastData();
    final priceData    = widget.getPriceData();

    if (forecastData == null && priceData == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(T.rw
            ? 'Banza ukore iteganyabikorwa no kubona igiciro mbere!'
            : 'Please run a Forecast and Price forecast first!'),
        backgroundColor: kAmber,
      ));
      return;
    }

    setState(() => _generating = true);
    try {
      final pdf      = pw.Document();
      final cropName = forecastData?['crop_name'] ?? priceData?['crop_name'] ?? '';
      final model    = forecastData?['model']     ?? priceData?['model']     ?? '';
      final fc       = (forecastData?['forecast'] as List?) ?? [];
      final prices   = (priceData?['forecast']   as List?) ?? [];

      pdf.addPage(pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.all(32),
        build: (pw.Context context) => [
          // Header
          pw.Container(
            padding: const pw.EdgeInsets.all(16),
            decoration: pw.BoxDecoration(
              color: PdfColors.green900,
              borderRadius: pw.BorderRadius.circular(8),
            ),
            child: pw.Column(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Text('AGRI FORECAST REPORT',
                    style: pw.TextStyle(
                        color: PdfColors.white,
                        fontSize: 22,
                        fontWeight: pw.FontWeight.bold)),
                pw.Text('Musanze District · Northern Province · Rwanda',
                    style: const pw.TextStyle(color: PdfColors.green200, fontSize: 11)),
                pw.SizedBox(height: 4),
                pw.Text('Crop: $cropName  |  Model: $model  |  Weeks: ${fc.length}',
                    style: const pw.TextStyle(color: PdfColors.green100, fontSize: 11)),
                pw.Text(
                    'Generated: ${DateTime.now().toString().substring(0, 16)}'
                    '  |  User: ${UserSession.name}',
                    style: const pw.TextStyle(color: PdfColors.green200, fontSize: 10)),
              ],
            ),
          ),
          pw.SizedBox(height: 20),

          // Demand section
          if (fc.isNotEmpty) ...[
            pw.Text('DEMAND FORECAST',
                style: pw.TextStyle(
                    fontSize: 14,
                    fontWeight: pw.FontWeight.bold,
                    color: PdfColors.green900)),
            pw.SizedBox(height: 6),
            // Summary KPIs
            pw.Row(children: [
              _pdfKpi('Peak Demand',
                  '${fc.map((r) => (r["demand_kg"] as num?) ?? 0).reduce((a, b) => a > b ? a : b)} kg'),
              pw.SizedBox(width: 16),
              _pdfKpi('Low Demand',
                  '${fc.map((r) => (r["demand_kg"] as num?) ?? 0).reduce((a, b) => a < b ? a : b)} kg'),
              pw.SizedBox(width: 16),
              _pdfKpi('Weeks', '${fc.length}'),
            ]),
            pw.SizedBox(height: 8),
            pw.Table(
              border: pw.TableBorder.all(color: PdfColors.grey300, width: 0.5),
              children: [
                pw.TableRow(
                  decoration: const pw.BoxDecoration(color: PdfColors.green100),
                  children: ['Week', 'Date', 'Demand (kg)', 'CI Low', 'CI High', 'Bags', 'Season']
                      .map((h) => pw.Padding(
                            padding: const pw.EdgeInsets.symmetric(horizontal: 6, vertical: 4),
                            child: pw.Text(h,
                                style: pw.TextStyle(
                                    fontWeight: pw.FontWeight.bold,
                                    fontSize: 9,
                                    color: PdfColors.green900)),
                          ))
                      .toList(),
                ),
                ...fc.map((row) => pw.TableRow(
                      children: [
                        'W${row["week"]}',
                        '${row["date"]}',
                        '${row["demand_kg"]}',
                        '${row["lower_kg"]}',
                        '${row["upper_kg"]}',
                        '${row["demand_bags"] ?? "-"}',
                        'S${row["season"] ?? "A"}',
                      ]
                          .map((cell) => pw.Padding(
                                padding: const pw.EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                                child: pw.Text(cell, style: const pw.TextStyle(fontSize: 8)),
                              ))
                          .toList(),
                    )),
              ],
            ),
            pw.SizedBox(height: 20),
          ],

          // Price section
          if (prices.isNotEmpty) ...[
            pw.Text('PRICE FORECAST',
                style: pw.TextStyle(
                    fontSize: 14,
                    fontWeight: pw.FontWeight.bold,
                    color: PdfColors.green900)),
            pw.SizedBox(height: 6),
            pw.Row(children: [
              _pdfKpi('Peak Price',
                  '${prices.map((r) => (r["price_rwf"] as num?) ?? 0).reduce((a, b) => a > b ? a : b)} RWF'),
              pw.SizedBox(width: 16),
              _pdfKpi('Current Price',
                  '${priceData?["current_price"] ?? "-"} RWF'),
              pw.SizedBox(width: 16),
              _pdfKpi('Best Week',
                  'W${priceData?["best_week"] ?? "-"}'),
            ]),
            pw.SizedBox(height: 8),
            pw.Table(
              border: pw.TableBorder.all(color: PdfColors.grey300, width: 0.5),
              children: [
                pw.TableRow(
                  decoration: const pw.BoxDecoration(color: PdfColors.green100),
                  children: ['Week', 'Date', 'Price RWF/kg', 'CI Low', 'CI High', 'Trend']
                      .map((h) => pw.Padding(
                            padding: const pw.EdgeInsets.symmetric(horizontal: 6, vertical: 4),
                            child: pw.Text(h,
                                style: pw.TextStyle(
                                    fontWeight: pw.FontWeight.bold,
                                    fontSize: 9,
                                    color: PdfColors.green900)),
                          ))
                      .toList(),
                ),
                ...prices.map((row) => pw.TableRow(
                      children: [
                        'W${row["week"]}',
                        '${row["date"]}',
                        '${row["price_rwf"]}',
                        '${row["lower_kg"]}',
                        '${row["upper_kg"]}',
                        '${row["trend"] ?? "-"}',
                      ]
                          .map((cell) => pw.Padding(
                                padding: const pw.EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                                child: pw.Text(cell, style: const pw.TextStyle(fontSize: 8)),
                              ))
                          .toList(),
                    )),
              ],
            ),
            pw.SizedBox(height: 20),
          ],

          // Advice
          if (forecastData?['advice'] != null) ...[
            pw.Text('FARMER ADVICE',
                style: pw.TextStyle(
                    fontSize: 14,
                    fontWeight: pw.FontWeight.bold,
                    color: PdfColors.green900)),
            pw.SizedBox(height: 6),
            pw.Container(
              padding: const pw.EdgeInsets.all(12),
              decoration: pw.BoxDecoration(
                color: PdfColors.green50,
                borderRadius: pw.BorderRadius.circular(6),
                border: pw.Border.all(color: PdfColors.green200),
              ),
              child: pw.Text(
                forecastData!['advice']['tip_en'] as String? ?? '',
                style: const pw.TextStyle(fontSize: 10),
              ),
            ),
            pw.SizedBox(height: 16),
          ],

          // Footer
          pw.Divider(color: PdfColors.green300),
          pw.Text(
            'BARAKA ISAAC (2305000514) · Supervisor: Dr MUSABE JEAN BOSCO'
            ' · University of Kigali · BBIT 2026',
            style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey),
            textAlign: pw.TextAlign.center,
          ),
        ],
      ));

      final bytes = await pdf.save();
      if (share) {
        await Printing.sharePdf(bytes: bytes, filename: 'AgriCast_Planting_Plan.pdf');
      } else {
        // Save to downloads
        final dir = await getExternalStorageDirectory();
        final file = File('\${dir!.path}/AgriCast_Planting_Plan.pdf');
        await file.writeAsBytes(bytes);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('PDF saved to \${file.path}'),
            backgroundColor: kForest,
            duration: const Duration(seconds: 4),
          ));
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('${T.error}: $e'), backgroundColor: kRed));
      }
    }
    if (mounted) setState(() => _generating = false);
  }

  pw.Widget _pdfKpi(String label, String value) => pw.Container(
    padding: const pw.EdgeInsets.symmetric(horizontal: 12, vertical: 8),
    decoration: pw.BoxDecoration(
      color: PdfColors.green50,
      borderRadius: pw.BorderRadius.circular(6),
      border: pw.Border.all(color: PdfColors.green200),
    ),
    child: pw.Column(children: [
      pw.Text(value,
          style: pw.TextStyle(
              fontWeight: pw.FontWeight.bold,
              fontSize: 11,
              color: PdfColors.green900)),
      pw.Text(label,
          style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey)),
    ]),
  );

  @override
  Widget build(BuildContext context) {
    final forecastData = widget.getForecastData();
    final priceData    = widget.getPriceData();
    final hasData      = forecastData != null || priceData != null;
    final cropName     = forecastData?['crop_name'] ?? priceData?['crop_name'] ?? '—';
    final model        = forecastData?['model']     ?? priceData?['model']     ?? '—';
    final weeks        = (forecastData?['forecast'] as List?)?.length
                      ?? (priceData?['forecast']   as List?)?.length
                      ?? 0;

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
      children: [
        // Header banner
        Container(
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [kForest, Color(0xFF1A5C1A)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(20),
          ),
          padding: const EdgeInsets.all(22),
          child: Row(children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('📄 ${T.reports}',
                      style: const TextStyle(
                          color: Color(0xFFE8F5E9),
                          fontSize: 22,
                          fontWeight: FontWeight.w800)),
                  const SizedBox(height: 4),
                  Text(T.reportsBanner,
                      style: const TextStyle(
                          color: Color(0xFF89B889), fontSize: 12)),
                ],
              ),
            ),
            const Text('📊', style: TextStyle(fontSize: 44)),
          ]),
        ),
        const SizedBox(height: 16),

        // Status card — what's loaded
        Card(
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _SectionHeader(
                  T.rw ? 'Amakuru Afashwe' : 'Loaded Data',
                  small: true),
                const SizedBox(height: 12),
                if (!hasData)
                  _AdviceCard(
                    icon: '⚠️',
                    text: T.rw
                        ? 'Nta makuru afashwe. Genda ku Iteganyabikorwa no Kubona Igiciro mbere, maze ugaruke hano.'
                        : 'No data loaded yet. Go to the Forecast and Price tabs first, run them, then come back here to print.',
                  )
                else ...[
                  _InfoRowSimple(Icons.eco,           T.rw ? 'Igihingwa' : 'Crop',   cropName),
                  _InfoRowSimple(Icons.model_training, T.rw ? 'Indorerezi' : 'Model', model),
                  _InfoRowSimple(Icons.calendar_today, T.rw ? 'Ibyumweru' : 'Weeks',  '$weeks'),
                  const SizedBox(height: 8),
                  Row(children: [
                    _StatusDot(forecastData != null, T.rw ? 'Iteganyabikorwa' : 'Demand Forecast'),
                    const SizedBox(width: 16),
                    _StatusDot(priceData != null, T.rw ? 'Igiciro' : 'Price Forecast'),
                  ]),
                ],
              ],
            ),
          ),
        ),
        const SizedBox(height: 12),

        // Download + Share buttons
        Row(children: [
          Expanded(
            child: ElevatedButton.icon(
              onPressed: _generating ? null : () => _generatePdf(share: false),
            icon: _generating
                ? const SizedBox(width: 18, height: 18,
                    child: CircularProgressIndicator(
                        color: Colors.white, strokeWidth: 2))
                : const Icon(Icons.picture_as_pdf),
            label: Text(_generating ? T.generating : T.generatePdf),
            style: ElevatedButton.styleFrom(
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
        ]),
        const SizedBox(height: 16),

        // What goes in the PDF
        if (hasData)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _SectionHeader(T.reportContents, small: true),
                  const SizedBox(height: 12),
                  if (forecastData != null)
                    _ReportItem('📋', T.demandTable,
                        '$cropName · $weeks ${T.weeksAheadFull} · $model'),
                  if (priceData != null)
                    _ReportItem('💰', T.priceTable,
                        '$cropName · RWF/kg · $model'),
                  _ReportItem('💡', T.seasonAdvice, T.farmerTips),
                  _ReportItem('📐', T.modelMetrics, 'MAE · RMSE · MAPE · R²'),
                ],
              ),
            ),
          ),

        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: kSkyPale,
            borderRadius: BorderRadius.circular(14),
            border: const Border(left: BorderSide(color: kSprout, width: 4)),
          ),
          child: Row(children: [
            const Text('💡', style: TextStyle(fontSize: 26)),
            const SizedBox(width: 12),
            Expanded(
              child: Text(T.pdfSaveInfo,
                  style: const TextStyle(
                      fontSize: 13,
                      color: Color(0xFF2D4A2D),
                      height: 1.6)),
            ),
          ]),
        ),
      ],
    );
  }
}

// Small helpers used only by ReportsPage
class _InfoRowSimple extends StatelessWidget {
  final IconData icon;
  final String label, value;
  const _InfoRowSimple(this.icon, this.label, this.value);
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Row(children: [
      Icon(icon, size: 18, color: kLeaf),
      const SizedBox(width: 10),
      SizedBox(width: 90,
          child: Text(label,
              style: const TextStyle(fontSize: 12, color: kMuted))),
      Text(value,
          style: const TextStyle(
              fontSize: 13, fontWeight: FontWeight.w700, color: kForest)),
    ]),
  );
}

class _StatusDot extends StatelessWidget {
  final bool ready;
  final String label;
  const _StatusDot(this.ready, this.label);
  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Container(
        width: 10, height: 10,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: ready ? kSprout : kBorder,
        ),
      ),
      const SizedBox(width: 6),
      Text(label,
          style: TextStyle(
              fontSize: 11,
              color: ready ? kForest : kMuted,
              fontWeight: ready ? FontWeight.w700 : FontWeight.normal)),
    ],
  );
}
// =============================================================
//  PROFILE PAGE
// =============================================================
class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});
  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  Map<String, dynamic>? _status;
  bool _editingFarm = false;
  bool _saving = false;
  late TextEditingController _farmCtrl;

  @override
  void initState() {
    super.initState();
    _farmCtrl = TextEditingController(text: UserSession.farmSizeAcres.toStringAsFixed(1));
    _loadStatus();
  }

  @override
  void dispose() {
    _farmCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadStatus() async {
    try {
      final d = await ApiService.get('/api/status');
      if (mounted) setState(() => _status = d);
    } catch (_) {}
  }

  Future<void> _saveFarmSize() async {
    final acres = double.tryParse(_farmCtrl.text);
    if (acres == null || acres <= 0 || acres > 100) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(T.rw ? 'Injiza ingano y\'inzara iri hagati ya 0.1 na 100' : 'Enter farm size between 0.1 and 100 acres'),
        backgroundColor: kRed,
      ));
      return;
    }
    setState(() => _saving = true);
    try {
      final d = await ApiService.post('/profile/update', {'farm_size_acres': acres, 'sector': UserSession.sector});
      if (d['status'] == 'success') {
        UserSession.farmSizeAcres = acres;
        setState(() { _editingFarm = false; _saving = false; });
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(T.rw ? 'Inzara yahinduwe: ${acres.toStringAsFixed(1)} ac' : 'Farm size updated: ${acres.toStringAsFixed(1)} acres'),
          backgroundColor: kForest,
        ));
      } else {
        throw Exception(d['message']);
      }
    } catch (e) {
      setState(() => _saving = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('${T.error}: $e'),
        backgroundColor: kRed,
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 30),
      children: [
        Container(
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [kForest, Color(0xFF1A5C1A)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(20),
          ),
          padding: const EdgeInsets.all(24),
          child: Column(children: [
            CircleAvatar(
              radius: 40,
              backgroundColor: kLime.withValues(alpha: 0.2),
              child: Text(UserSession.roleEmoji,
                  style: const TextStyle(fontSize: 40)),
            ),
            const SizedBox(height: 14),
            Text(UserSession.name,
                style: const TextStyle(
                    color: Color(0xFFE8F5E9),
                    fontSize: 22,
                    fontWeight: FontWeight.w800)),
            const SizedBox(height: 4),
            Text(UserSession.phone,
                style: const TextStyle(color: Color(0xFF89B889), fontSize: 13)),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _ProfilePill(UserSession.role.toUpperCase(), kLime),
                const SizedBox(width: 8),
                if (UserSession.sector.isNotEmpty)
                  _ProfilePill(UserSession.sector, kStraw),
              ],
            ),
          ]),
        ),
        const SizedBox(height: 16),

        Card(
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _SectionHeader(T.accountDetails, small: true),
                const SizedBox(height: 14),
                _InfoRow(Icons.person,     T.fullNameLbl, UserSession.name),
                _InfoRow(Icons.phone,      T.phoneLbl,    UserSession.phone),
                _InfoRow(Icons.badge,      T.roleLbl,     UserSession.role.toUpperCase()),
                if (UserSession.sector.isNotEmpty)
                  _InfoRow(Icons.location_on, T.sectorLbl, UserSession.sector),
                _InfoRow(Icons.agriculture, T.rw ? 'Ingano y\'Inzara' : 'Farm Size', '${UserSession.farmSizeAcres.toStringAsFixed(1)} acres'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Farm size editor
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: kSprout.withValues(alpha: 0.08),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: kSprout.withValues(alpha: 0.25)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                const Icon(Icons.edit, size: 16, color: kForest),
                const SizedBox(width: 6),
                Text(T.rw ? 'Hindura Ingano y\'Inzara' : 'Update Farm Size',
                    style: const TextStyle(fontWeight: FontWeight.w700, color: kForest)),
              ]),
              const SizedBox(height: 12),
              Row(children: [
                Expanded(
                  child: TextField(
                    controller: _farmCtrl,
                    keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    decoration: InputDecoration(
                      labelText: T.rw ? 'Ingano (hectare)' : 'Size (acres)',
                      suffixText: T.rw ? 'ac' : 'acres',
                      border: const OutlineInputBorder(),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                ElevatedButton(
                  onPressed: _saving ? null : _saveFarmSize,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: kForest,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                  ),
                  child: _saving
                      ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : Text(T.rw ? 'Bika' : 'Save'),
                ),
              ]),
            ],
          ),
        ),
        const SizedBox(height: 12),

        if (_status != null)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _SectionHeader(T.systemInfo, small: true),
                  const SizedBox(height: 14),
                  _InfoRow(Icons.dns,           'API Version', _status!['version'] ?? '3.2'),
                  _InfoRow(Icons.check_circle,  'Status',      _status!['status']  ?? 'running'),
                  _InfoRow(Icons.eco,           T.cropsLbl,    '${(_status!['crops']  as List?)?.length ?? 7}'),
                  _InfoRow(Icons.model_training, T.modelsLbl,  '${(_status!['models'] as List?)?.length ?? 4}'),
                ],
              ),
            ),
          ),
        const SizedBox(height: 12),

        Card(
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _SectionHeader(T.about, small: true),
                const SizedBox(height: 14),
                const _InfoRow(Icons.agriculture,      'Project',    'Agri Forecast — Musanze'),
                _InfoRow(Icons.school,           T.rw ? 'Umwanditsi' : 'Author',     'BARAKA ISAAC (2305000514)'),
                _InfoRow(Icons.supervisor_account, T.rw ? 'Umujyanama' : 'Supervisor', 'Dr MUSABE JEAN BOSCO'),
                _InfoRow(Icons.account_balance,  T.rw ? 'Kaminuza' : 'University',   'University of Kigali'),
                _InfoRow(Icons.calendar_today,   T.rw ? 'Porogaramu' : 'Program',    'BBIT 2026'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 20),

        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () {
              UserSession.clear();
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => const LoginPage()),
              );
            },
            icon: const Icon(Icons.logout, color: kRed),
            label: Text(T.logout,
                style: const TextStyle(color: kRed, fontWeight: FontWeight.w700)),
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: kRed),
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ),
      ],
    );
  }
}

class _ProfilePill extends StatelessWidget {
  final String label;
  final Color color;
  const _ProfilePill(this.label, this.color);

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.2),
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: color.withValues(alpha: 0.4)),
    ),
    child: Text(label,
        style: TextStyle(
            color: color, fontSize: 11, fontWeight: FontWeight.w700)),
  );
}

class _InfoRow extends StatelessWidget {
  final IconData icon;
  final String label, value;
  const _InfoRow(this.icon, this.label, this.value);

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 12),
    child: Row(children: [
      Icon(icon, size: 18, color: kLeaf),
      const SizedBox(width: 10),
      SizedBox(
        width: 100,
        child: Text(label,
            style: const TextStyle(
                fontSize: 12, color: kMuted, fontWeight: FontWeight.w500)),
      ),
      Expanded(
        child: Text(value,
            style: const TextStyle(
                fontSize: 13, color: kForest, fontWeight: FontWeight.w600)),
      ),
    ]),
  );
}
