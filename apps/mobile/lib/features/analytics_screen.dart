import 'package:flutter/material.dart';
import '../core/study_controller.dart';

class AnalyticsScreen extends StatelessWidget {
  const AnalyticsScreen({super.key, required this.controller});
  final StudyController controller;
  @override
  Widget build(BuildContext context) {
    final p = controller.progress;
    final correct = p.correctCount(p.attempts);
    final studied = controller.catalog.courses.where((c) => p.forCourse(c.id).isNotEmpty).toList();
    studied.sort((a, b) {
      final aa = p.forCourse(a.id), bb = p.forCourse(b.id);
      return (p.correctCount(aa) / aa.length).compareTo(p.correctCount(bb) / bb.length);
    });
    return ListView(padding: const EdgeInsets.all(20), children: [
      const Text('Gelişim Analizi', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
      Card(child: Padding(padding: const EdgeInsets.all(20), child: Wrap(spacing: 24, runSpacing: 12, children: [
        Text('${p.attempts.length}\nToplam soru'), Text('$correct\nDoğru'), Text('${p.attempts.length - correct}\nYanlış')]))),
      const SizedBox(height: 16), const Text('Ders bazlı performans', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      for (final c in controller.catalog.courses) Builder(builder: (_) {
        final attempts = p.forCourse(c.id);
        final rate = attempts.isEmpty ? 0.0 : p.correctCount(attempts) / attempts.length;
        return Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('${c.emoji} ${c.subject} · ${attempts.isEmpty ? 'Henüz veri yok' : '%${(rate * 100).round()}'}'),
          const SizedBox(height: 12), LinearProgressIndicator(value: rate)])));
      }),
      if (studied.isNotEmpty) Card(child: Padding(padding: const EdgeInsets.all(20), child: Text(
        '${studied.first.subject} kısa özetini gözden geçirip örnek soruları tekrar çözebilirsin. Bu öneri basit doğruluk oranına dayanır; AI önerisi değildir.'))),
      const SizedBox(height: 16), const Text('Veriler yalnızca bu cihazda saklanır. Toplamlar tekrar çözmeleri içerir. Net, süre ve gelişim grafikleri sonraki aşamadadır.', style: TextStyle(fontSize: 12)),
      const SizedBox(height: 16), OutlinedButton(onPressed: () async {
        final ok = await showDialog<bool>(context: context, builder: (context) => AlertDialog(
          title: const Text('İlerlemeyi sıfırla?'), content: const Text('Bu cihazdaki cevap geçmişi ve yanlış defteri temizlenecek.'),
          actions: [TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Vazgeç')),
            TextButton(onPressed: () => Navigator.pop(context, true), child: const Text('Sıfırla'))]));
        if (ok == true) await controller.reset();
      }, child: const Text('Cihazdaki ilerlemeyi sıfırla'))]);
  }
}
