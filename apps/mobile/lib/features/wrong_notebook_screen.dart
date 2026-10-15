import 'package:flutter/material.dart';
import '../core/study_controller.dart';
import 'quiz_screen.dart';
import 'lessons_screen.dart';

class WrongNotebookScreen extends StatelessWidget {
  const WrongNotebookScreen({super.key, required this.controller});
  final StudyController controller;
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: const Text('Yanlış Defteri')),
    body: SafeArea(child: ListenableBuilder(listenable: controller, builder: (context, _) {
      final wrong = controller.progress.wrongQuestions;
      return ListView(padding: const EdgeInsets.all(20), children: [
        const Text('Son cevabın yanlış olan sorular burada listelenir. Doğru tekrar cevabından sonra listeden çıkar; cevap geçmişi analizde korunur.'),
        const SizedBox(height: 16),
        if (wrong.isEmpty) const Card(child: Padding(padding: EdgeInsets.all(24), child: Text('Tekrar bekleyen yanlışın yok.')))
        else ...[
          FilledButton(onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) =>
            Scaffold(appBar: AppBar(title: const Text('Yanlışları tekrar çöz')), body: SafeArea(child: QuizScreen(controller: controller, onlyQuestions: List.of(wrong)))))), child: const Text('Yanlışları tekrar çöz')),
          for (final q in wrong) Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(q.text, style: const TextStyle(fontWeight: FontWeight.bold)), const SizedBox(height: 8), Text(q.explanation),
            TextButton(onPressed: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) =>
              LessonDetail(controller: controller, course: controller.catalog.course(q.topic)))), child: const Text('İlgili konuya git'))])))] ]);
    })));
}
