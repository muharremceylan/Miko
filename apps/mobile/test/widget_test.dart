import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:akademi_ai/app/akademi_app.dart';
import 'package:akademi_ai/core/study_controller.dart';
import 'package:akademi_ai/features/quiz_screen.dart';
import 'package:akademi_ai/features/lessons_screen.dart';
import 'package:akademi_ai/features/wrong_notebook_screen.dart';
import 'fixtures.dart';

void main() {
  testWidgets('mobil ana sayfa ve test sekmesi açılır', (tester) async {
    final c = StudyController(catalog: fixtureCatalog(), store: MemoryStore());
    await tester.pumpWidget(AkademiApp(controller: c)); await tester.pumpAndSettle();
    expect(find.text('Bugünkü ilerlemen'), findsOneWidget);
    await tester.tap(find.text('Testler')); await tester.pumpAndSettle();
    expect(find.text('Akıllı Soru Bankası'), findsOneWidget);
    expect(tester.takeException(), isNull);
    await tester.pumpWidget(const SizedBox.shrink()); c.dispose();
  });
  testWidgets('ders anlatımından kısa özete geçilir', (tester) async {
    final c = StudyController(catalog: fixtureCatalog(), store: MemoryStore());
    await tester.pumpWidget(MaterialApp(home: LessonDetail(controller: c, course: c.catalog.courses.first)));
    await tester.tap(find.text('Kısa özet')); await tester.pumpAndSettle();
    expect(find.text('• Bilinmeyeni ayır.'), findsOneWidget);
    await tester.pumpWidget(const SizedBox.shrink()); c.dispose();
  });
  testWidgets('sonlu test cevaplarını ve sonucunu kaydeder', (tester) async {
    final c = StudyController(catalog: fixtureCatalog(), store: MemoryStore());
    await tester.pumpWidget(MaterialApp(home: Scaffold(body: QuizScreen(controller: c))));
    for (var i = 0; i < 3; i++) {
      await tester.ensureVisible(find.text('B) Doğru'));
      await tester.tap(find.text('B) Doğru')); await tester.pumpAndSettle();
      final next = find.text(i == 2 ? 'Test sonucunu gör' : 'Sonraki soru');
      await tester.ensureVisible(next); await tester.tap(next); await tester.pumpAndSettle();
    }
    expect(find.text('Test tamamlandı 🎉'), findsOneWidget);
    expect(c.progress.attempts.length, 3); expect(c.progress.correctCount(c.progress.attempts), 3);
    await tester.pumpWidget(const SizedBox.shrink()); c.dispose();
  });
  testWidgets('yanlış defteri ilgili soruyu gösterir', (tester) async {
    final c = StudyController(catalog: fixtureCatalog(), store: MemoryStore());
    await c.record(c.catalog.questions.first, 0);
    await tester.pumpWidget(MaterialApp(home: WrongNotebookScreen(controller: c)));
    expect(find.text('Örnek soru 0'), findsOneWidget); expect(find.text('İlgili konuya git'), findsOneWidget);
    await tester.pumpWidget(const SizedBox.shrink()); c.dispose();
  });
}
