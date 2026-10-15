import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'app/akademi_app.dart';
import 'core/study_controller.dart';
import 'data/progress_store.dart';
import 'models/content.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const Bootstrap());
}

class Bootstrap extends StatefulWidget {
  const Bootstrap({super.key});
  @override
  State<Bootstrap> createState() => _BootstrapState();
}
class _BootstrapState extends State<Bootstrap> {
  late Future<StudyController> loading = load();
  Future<StudyController> load() async {
    final raw = await rootBundle.loadString('assets/sample_content.json');
    final catalog = Catalog.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    final controller = StudyController(catalog: catalog, store: DeviceProgressStore());
    await controller.load();
    return controller;
  }
  @override
  Widget build(BuildContext context) => FutureBuilder<StudyController>(
    future: loading,
    builder: (context, snapshot) {
      if (snapshot.hasData) return AkademiApp(controller: snapshot.data!);
      return MaterialApp(home: Scaffold(body: Center(child: snapshot.hasError
        ? Column(mainAxisSize: MainAxisSize.min, children: [
            const Text('Örnek içerik açılamadı.'),
            FilledButton(onPressed: () => setState(() { loading = load(); }), child: const Text('Yeniden dene'))])
        : const CircularProgressIndicator())));
    });
}
