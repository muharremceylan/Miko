import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import '../models/content.dart';

class AudioScreen extends StatefulWidget {
  const AudioScreen({super.key, required this.catalog});
  final Catalog catalog;
  @override
  State<AudioScreen> createState() => _AudioScreenState();
}
class _AudioScreenState extends State<AudioScreen> with WidgetsBindingObserver {
  final FlutterTts tts = FlutterTts();
  late String topic;
  String status = 'Dinlemek için konuyu seç.';
  bool busy = false;
  int generation = 0;
  @override
  void initState() {
    super.initState(); topic = widget.catalog.courses.first.id;
    WidgetsBinding.instance.addObserver(this);
  }
  void update(String text) { if (mounted) setState(() => status = text); }
  Future<void> stop() async {
    generation++;
    try { await tts.stop(); } catch (_) { /* Text remains available without TTS. */ }
    update('Seslendirme durduruldu.');
  }
  Future<void> play() async {
    if (busy) return;
    setState(() => busy = true);
    await stop();
    final token = generation;
    try {
      final available = await tts.isLanguageAvailable('tr-TR');
      if (!mounted || token != generation) return;
      if (available != true && available != 1) {
        update('Cihazda Türkçe ses bulunamadı. Kısa özeti aşağıdan okuyabilirsin.'); return;
      }
      await tts.setLanguage('tr-TR');
      await tts.setSpeechRate(0.45);
      await tts.awaitSpeakCompletion(true);
      if (!mounted || token != generation) return;
      final course = widget.catalog.course(topic);
      update('Sesli tekrar oynatılıyor...');
      await tts.speak('${course.name}. ${lessonText(course.short)}');
      if (mounted && token == generation) update('Sesli tekrar tamamlandı.');
    } catch (_) {
      if (mounted && token == generation) update('Türkçe seslendirme kullanılamadı. Metinden devam edebilirsin.');
    } finally { if (mounted) setState(() => busy = false); }
  }
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused || state == AppLifecycleState.inactive) unawaited(stop());
  }
  @override
  void dispose() {
    generation++; WidgetsBinding.instance.removeObserver(this); unawaited(tts.stop()); super.dispose();
  }
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: const Text('Sesli Akademi')),
    body: SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
      DropdownButtonFormField<String>(initialValue: topic,
        items: [for (final c in widget.catalog.courses) DropdownMenuItem(value: c.id, child: Text(c.subject))],
        onChanged: (v) { if (v != null) { unawaited(stop()); setState(() => topic = v); } }),
      const SizedBox(height: 20), Wrap(spacing: 12, runSpacing: 8, children: [
        FilledButton.icon(onPressed: busy ? null : play, icon: const Icon(Icons.play_arrow), label: const Text('Dinle')),
        OutlinedButton.icon(onPressed: stop, icon: const Icon(Icons.stop), label: const Text('Durdur'))]),
      const SizedBox(height: 16), Text(status), const SizedBox(height: 20),
      SelectableText(lessonText(widget.catalog.course(topic).short), style: const TextStyle(fontSize: 16, height: 1.8)),
      const SizedBox(height: 20), const Text('Ses kalitesi ve Türkçe desteği cihazına bağlıdır. Bu özellik gerçek podcast dosyası veya AI ses üretimi değildir.', style: TextStyle(fontSize: 12))])));
}
