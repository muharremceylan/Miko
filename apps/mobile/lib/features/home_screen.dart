import 'package:flutter/material.dart';
import '../core/study_controller.dart';
import 'lessons_screen.dart';
import 'wrong_notebook_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.controller, required this.navigate});
  final StudyController controller;
  final void Function(int) navigate;
  @override
  Widget build(BuildContext context) {
    final progress = controller.progress;
    final now = DateTime.now();
    final day = progress.forDay(now);
    final correct = progress.correctCount(day);
    return ListView(padding: const EdgeInsets.all(20), children: [
      Container(padding: const EdgeInsets.all(24), decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        gradient: const LinearGradient(colors: [Color(0xff111d42), Color(0xff334e98)])),
        child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('Merhaba! 👋', style: TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
          SizedBox(height: 8), Text('Sınav yolculuğuna bugün devam et.', style: TextStyle(color: Colors.white70))])),
      const SizedBox(height: 16),
      Card(child: Padding(padding: const EdgeInsets.all(20), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Bugünkü ilerlemen', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Wrap(spacing: 24, runSpacing: 12, children: [
          Text('${day.length}\nÇözülen soru'), Text('$correct\nDoğru cevap'),
          Text('${day.isEmpty ? '—' : '%${(100 * correct / day.length).round()}'}\nBaşarı oranı')]),
        const SizedBox(height: 20), LinearProgressIndicator(value: progress.goal(now)),
        const SizedBox(height: 12), Text(day.length >= 10 ? 'Günlük hedef tamamlandı ✓' : 'Günlük hedef: ${day.length} / 10 soru')]))),
      const SizedBox(height: 20), const Text('Hemen çalışmaya başla', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 12),
      _action(context, Icons.menu_book, 'Ders Akademisi', 'Konu anlatımı ve hızlı özet', () => navigate(1)),
      _action(context, Icons.quiz, 'Soru Bankası', 'Ders filtresi ve açıklamalı testler', () => navigate(2)),
      _action(context, Icons.bookmark_outline, 'Yanlış Defteri', '${progress.wrongQuestions.length} tekrar bekleyen soru', () => Navigator.push(context,
        MaterialPageRoute<void>(builder: (_) => WrongNotebookScreen(controller: controller)))),
      _action(context, Icons.headphones, 'Ses ve fotoğraf araçları', 'Sesli özet · açıkça etiketlenmiş çözüm demosu', () => navigate(3)),
      const SizedBox(height: 16),
      Card(child: ListTile(title: const Text('Bugünün örnek konusu'), subtitle: Text(controller.catalog.courses.first.name),
        trailing: const Icon(Icons.chevron_right), onTap: () => Navigator.push(context,
          MaterialPageRoute<void>(builder: (_) => LessonDetail(controller: controller, course: controller.catalog.courses.first))))),
      const Padding(padding: EdgeInsets.symmetric(vertical: 16), child: Text(
        'Örnek içerik sürümü. Sorular ÖSYM çıkmış soruları değildir; uzman onayı ve tam KPSS/AGS müfredatı henüz tamamlanmadı.',
        style: TextStyle(fontSize: 12, color: Colors.black54)))]);
  }
  Widget _action(BuildContext context, IconData icon, String title, String subtitle, VoidCallback action) =>
    Card(child: ListTile(leading: Icon(icon, color: Theme.of(context).colorScheme.primary), title: Text(title),
      subtitle: Text(subtitle), trailing: const Icon(Icons.chevron_right), onTap: action));
}
