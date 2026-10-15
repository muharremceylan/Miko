import 'dart:convert';
import 'package:flutter/foundation.dart';
import '../data/progress_store.dart';
import '../models/content.dart';
import '../models/progress.dart';

class StudyController extends ChangeNotifier {
  StudyController({required this.catalog, required this.store}) : progress = Progress(catalog);
  final Catalog catalog;
  final ProgressStore store;
  Progress progress;
  String? warning;
  int resetVersion = 0;
  // Serialize writes so a slower earlier save cannot replace newer progress.
  Future<void> _pending = Future.value();
  Future<void> load() async {
    try {
      final raw = await store.read();
      if (raw != null) {
        final json = jsonDecode(raw);
        if (json is! Map || json['version'] != 1 || json['attempts'] is! List) {
          throw const FormatException('Uyumsuz kayıt');
        }
        final attempts = (json['attempts'] as List).map((v) =>
          Attempt.fromJson(Map<String, dynamic>.from(v as Map), catalog)).toList();
        progress = Progress(catalog, attempts);
      }
    } catch (_) {
      warning = 'Cihaz kaydı okunamadı. Geçici ilerlemeyle devam edebilirsin. Eski kayıt yeni cevap veya sıfırlamaya kadar değiştirilmez.';
    }
    notifyListeners();
  }
  Future<void> record(Question q, int choice, {DateTime? now}) {
    if (choice < 0 || choice >= q.choices.length) return Future.value();
    progress.attempts.add(Attempt(questionId: q.id, choice: choice, at: now ?? DateTime.now()));
    notifyListeners();
    return _save();
  }
  Future<void> reset() {
    progress = Progress(catalog);
    resetVersion++;
    warning = null;
    notifyListeners();
    return _save();
  }
  Future<void> _save() {
    final value = jsonEncode({'version': 1,
      'attempts': progress.attempts.map((a) => a.toJson()).toList()});
    _pending = _pending.then((_) async {
      try { await store.write(value); warning = null; }
      catch (_) { warning = 'İlerleme cihaza kaydedilemedi. Sayfa veya uygulama kapanınca yeni kayıtlar kaybolabilir.'; }
      notifyListeners();
    });
    return _pending;
  }
}
