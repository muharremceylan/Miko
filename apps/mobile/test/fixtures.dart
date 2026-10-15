import 'package:akademi_ai/models/content.dart';
import 'package:akademi_ai/data/progress_store.dart';

Catalog fixtureCatalog() => Catalog([
  const Course(id: 'matematik', name: 'Matematik · Denklemler', emoji: '➗', full: '<h3>Denklem</h3><p>İki tarafa aynı işlem uygulanır.</p>', short: '<ul><li>Bilinmeyeni ayır.</li></ul>')
], List.generate(3, (i) => Question(id: 'q$i', topic: 'matematik', text: 'Örnek soru $i', choices: const ['Yanlış', 'Doğru'], correct: 1, explanation: 'Örnek açıklama')));

class MemoryStore implements ProgressStore {
  String? value;
  bool failRead = false, failWrite = false;
  @override
  Future<String?> read() async {
    if (failRead) throw StateError('read denied');
    return value;
  }
  @override
  Future<void> write(String text) async {
    if (failWrite) throw StateError('write denied');
    value = text;
  }
}
