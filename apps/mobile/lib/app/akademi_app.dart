import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import '../core/study_controller.dart';
import '../features/home_screen.dart';
import '../features/lessons_screen.dart';
import '../features/quiz_screen.dart';
import '../features/analytics_screen.dart';
import '../features/tools_screen.dart';

class AkademiApp extends StatelessWidget {
  const AkademiApp({super.key, required this.controller});
  final StudyController controller;
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Akademi AI', debugShowCheckedModeBanner: false,
    locale: const Locale('tr'), supportedLocales: const [Locale('tr')],
    localizationsDelegates: GlobalMaterialLocalizations.delegates,
    theme: ThemeData(useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xff5265d8)),
      scaffoldBackgroundColor: const Color(0xfff5f7fc),
      appBarTheme: const AppBarTheme(centerTitle: false),
      inputDecorationTheme: const InputDecorationTheme(border: OutlineInputBorder())),
    home: StudyShell(controller: controller));
}

class StudyShell extends StatefulWidget {
  const StudyShell({super.key, required this.controller});
  final StudyController controller;
  @override
  State<StudyShell> createState() => _StudyShellState();
}
class _StudyShellState extends State<StudyShell> with WidgetsBindingObserver {
  int tab = 0;
  late final Timer timer;
  @override
  void initState() {
    super.initState(); WidgetsBinding.instance.addObserver(this);
    timer = Timer.periodic(const Duration(minutes: 1), (_) { if (mounted) setState(() {}); });
  }
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed && mounted) setState(() {});
  }
  @override
  void dispose() { timer.cancel(); WidgetsBinding.instance.removeObserver(this); super.dispose(); }
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: widget.controller, builder: (context, _) {
      final c = widget.controller;
      final screens = <Widget>[
        HomeScreen(controller: c, navigate: (i) => setState(() => tab = i)),
        LessonsScreen(controller: c), QuizScreen(key: ValueKey(c.resetVersion), controller: c),
        ToolsScreen(controller: c), AnalyticsScreen(controller: c)];
      return Scaffold(
        appBar: AppBar(title: const Text('✦ Akademi AI'), actions: const [
          Padding(padding: EdgeInsets.only(right: 16), child: Center(child: Text('KPSS · AGS', style: TextStyle(fontSize: 12))))]),
        body: SafeArea(child: Column(children: [
          if (c.warning != null) Material(color: Theme.of(context).colorScheme.errorContainer,
            child: Padding(padding: const EdgeInsets.all(12), child: Text(c.warning!, style: const TextStyle(fontSize: 13)))),
          Expanded(child: IndexedStack(index: tab, children: screens))])),
        bottomNavigationBar: NavigationBar(selectedIndex: tab,
          onDestinationSelected: (i) => setState(() => tab = i),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Ana sayfa'),
            NavigationDestination(icon: Icon(Icons.menu_book_outlined), label: 'Dersler'),
            NavigationDestination(icon: Icon(Icons.quiz_outlined), label: 'Testler'),
            NavigationDestination(icon: Icon(Icons.auto_awesome_outlined), label: 'Araçlar'),
            NavigationDestination(icon: Icon(Icons.bar_chart), label: 'Analiz')]));
    });
}
