import 'package:flutter/material.dart';
import '../core/study_controller.dart';
import '../models/content.dart';
import '../models/test_session.dart';

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key, required this.controller, this.topic, this.onlyQuestions});
  final StudyController controller;
  final String? topic;
  final List<Question>? onlyQuestions;
  @override
  State<QuizScreen> createState() => _QuizScreenState();
}
class _QuizScreenState extends State<QuizScreen> {
  late String topic;
  late TestSession session;
  @override
  void initState() { super.initState(); topic = widget.topic ?? 'all'; start(); }
  void start() {
    session = TestSession(widget.onlyQuestions ?? widget.controller.catalog.questions.where((q) => topic == 'all' || q.topic == topic));
  }
  @override
  Widget build(BuildContext context) {
    final q = session.empty ? null : session.current;
    final selected = session.selected;
    return ListView(padding: const EdgeInsets.all(20), children: [
      const Text('Akıllı Soru Bankası', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
      const SizedBox(height: 16),
      if (widget.onlyQuestions == null && widget.topic == null) DropdownButtonFormField<String>(
        initialValue: topic, decoration: const InputDecoration(labelText: 'Ders seç'),
        items: [const DropdownMenuItem(value: 'all', child: Text('Karma test')),
          for (final c in widget.controller.catalog.courses) DropdownMenuItem(value: c.id, child: Text(c.subject))],
        onChanged: (v) { if (v != null) setState(() { topic = v; start(); }); }),
      const SizedBox(height: 16),
      if (session.empty) const Card(child: Padding(padding: EdgeInsets.all(24), child: Text('Bu seçimde soru bulunmuyor.')))
      else if (session.finished) Card(child: Padding(padding: const EdgeInsets.all(24), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Test tamamlandı 🎉', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16), Text('${session.answers.length} soru\n${session.correctCount} doğru · ${session.answers.length - session.correctCount} yanlış\nBaşarı: %${(100 * session.correctCount / session.answers.length).round()}', style: const TextStyle(fontSize: 18, height: 1.8)),
        const SizedBox(height: 16), FilledButton(onPressed: () => setState(start), child: const Text('Yeni test başlat')),
        const SizedBox(height: 8), const Text('Yeni test aynı örnek havuzdan hazırlanır.')])) )
      else if (q != null) Card(child: Padding(padding: const EdgeInsets.all(20), child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Text('${widget.controller.catalog.course(q.topic).subject} · Soru ${session.index + 1} / ${session.questions.length}'),
        const SizedBox(height: 16), Text(q.text, style: const TextStyle(fontSize: 20, height: 1.5, fontWeight: FontWeight.w600)),
        const SizedBox(height: 16),
        for (var i = 0; i < q.choices.length; i++) Padding(padding: const EdgeInsets.only(bottom: 10),
          child: OutlinedButton(style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.all(16), alignment: Alignment.centerLeft,
            disabledForegroundColor: Colors.black87,
            backgroundColor: selected == null ? null : i == q.correct ? Colors.green.shade100 : selected == i ? Colors.red.shade100 : null),
            onPressed: selected != null ? null : () {
              if (!session.answer(i)) return;
              widget.controller.record(q, i);
              setState(() {});
            }, child: Text('${String.fromCharCode(65 + i)}) ${q.choices[i]}'))),
        if (selected != null) ...[
          Text(selected == q.correct ? '✓ Doğru cevap!' : 'Birlikte inceleyelim', style: const TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 8), Text(q.explanation, style: const TextStyle(height: 1.7)),
          const SizedBox(height: 16), FilledButton(onPressed: () => setState(session.next),
            child: Text(session.index + 1 == session.questions.length ? 'Test sonucunu gör' : 'Sonraki soru'))]]))),
      const SizedBox(height: 16), const Text('Sorular özgün örneklerdir; ÖSYM çıkmış soruları değildir. Tam sınav simülasyonu ve süreli test henüz yok.', style: TextStyle(fontSize: 12, color: Colors.black54))]);
  }
}
