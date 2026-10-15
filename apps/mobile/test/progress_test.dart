import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:akademi_ai/core/study_controller.dart';
import 'package:akademi_ai/models/progress.dart';
import 'package:akademi_ai/models/test_session.dart';
import 'fixtures.dart';

void main() {
  test('10 ve 11 cevapta günlük hedef dolu kalır', () {
    final c = fixtureCatalog();
    final day = DateTime(2026, 10, 14, 12);
    final p = Progress(c, List.generate(11, (_) => Attempt(questionId: 'q0', choice: 1, at: day)));
    expect(p.goal(day), 1);
    p.attempts.removeLast(); expect(p.goal(day), 1);
    expect(p.goal(day.add(const Duration(days: 1))), 0);
    expect(p.attempts.length, 10);
  });
  test('günlük sayaç ve ders toplamı bağımsızdır', () {
    final day = DateTime(2026, 10, 14, 12);
    final p = Progress(fixtureCatalog(), [Attempt(questionId: 'q0', choice: 0, at: day),
      Attempt(questionId: 'q1', choice: 1, at: day.add(const Duration(days: 1)))]);
    expect(p.forDay(day).length, 1);
    expect(p.forCourse('matematik').length, 2);
    expect(p.correctCount(p.attempts), 1);
  });
  test('doğru tekrar yanlış defterini temizler; geçmiş korunur', () {
    final p = Progress(fixtureCatalog(), [Attempt(questionId: 'q0', choice: 0, at: DateTime.now())]);
    expect(p.wrongQuestions.single.id, 'q0');
    p.attempts.add(Attempt(questionId: 'q0', choice: 1, at: DateTime.now()));
    expect(p.wrongQuestions, isEmpty); expect(p.attempts.length, 2);
  });
  test('test havuzu tekrarsızdır ve çift cevap sayılmaz', () {
    final session = TestSession(fixtureCatalog().questions);
    expect(session.questions.map((q) => q.id).toSet().length, 3);
    session.next(); expect(session.index, 0);
    expect(session.answer(9), false);
    for (var i = 0; i < 3; i++) {
      expect(session.answer(1), true); expect(session.answer(0), false); session.next();
    }
    expect(session.finished, true); expect(session.correctCount, 3);
    expect(session.answer(0), false); session.next(); expect(session.index, 2);
  });
  test('boş havuz cevap veya ilerleme üretmez', () {
    final session = TestSession([]); expect(session.empty, true);
    expect(session.answer(0), false); session.next(); expect(session.answers, isEmpty);
  });
  test('cevap geçmişi cihaz kaydından geri yüklenir', () async {
    final c = fixtureCatalog(), store = MemoryStore();
    final a = StudyController(catalog: c, store: store);
    await a.record(c.questions.first, 1);
    final b = StudyController(catalog: c, store: store); await b.load();
    expect(b.progress.attempts.length, 1); expect(b.progress.correctCount(b.progress.attempts), 1);
    a.dispose(); b.dispose();
  });
  test('bozuk ve geçersiz kayıtlar açılışı durdurmaz veya eski kaydı silmez', () async {
    for (final raw in ['broken', 'null', '{"version":2,"attempts":[]}',
      jsonEncode({'version':1,'attempts':[{'questionId':'missing','choice':0,'at':'2026-10-14T12:00:00Z'}]})]) {
      final store = MemoryStore()..value = raw;
      final c = StudyController(catalog: fixtureCatalog(), store: store); await c.load();
      expect(c.warning, isNotNull); expect(c.progress.attempts, isEmpty); expect(store.value, raw); c.dispose();
    }
  });
  test('okuma ve yazma hatası görünür; çalışmaya devam edilebilir', () async {
    final catalog = fixtureCatalog();
    final store = MemoryStore()..failRead = true..failWrite = true;
    final c = StudyController(catalog: catalog, store: store); await c.load();
    expect(c.warning, isNotNull); await c.record(catalog.questions.first, 0);
    expect(c.progress.attempts.length, 1); expect(c.warning, contains('kaydedilemedi')); c.dispose();
  });
  test('eşzamanlı yazmalar son ilerleme durumunu korur', () async {
    final catalog = fixtureCatalog(), store = MemoryStore();
    final c = StudyController(catalog: catalog, store: store);
    await Future.wait([c.record(catalog.questions[0], 1), c.record(catalog.questions[1], 0)]);
    expect((jsonDecode(store.value!)['attempts'] as List).length, 2); c.dispose();
  });
  test('sıfırlama kayıt ve yanlış defterini temizler', () async {
    final catalog = fixtureCatalog(); final c = StudyController(catalog: catalog, store: MemoryStore());
    await c.record(catalog.questions.first, 0); await c.reset();
    expect(c.progress.attempts, isEmpty); expect(c.progress.wrongQuestions, isEmpty); expect(c.resetVersion, 1); c.dispose();
  });
}
