import 'content.dart';

class Attempt {
  const Attempt({required this.questionId, required this.choice, required this.at});
  final String questionId;
  final int choice;
  final DateTime at;
  Map<String, dynamic> toJson() => {'questionId': questionId,
    'choice': choice, 'at': at.toUtc().toIso8601String()};
  factory Attempt.fromJson(Map<String, dynamic> json, Catalog catalog) {
    final id = json['questionId'];
    final choice = json['choice'];
    final at = DateTime.tryParse(json['at'] is String ? json['at'] as String : '');
    if (id is! String || choice is! int || at == null ||
        !catalog.questions.any((q) => q.id == id && choice >= 0 && choice < q.choices.length)) {
      throw const FormatException('Geçersiz cevap kaydı');
    }
    return Attempt(questionId: id, choice: choice, at: at);
  }
}

class Progress {
  Progress(this.catalog, [List<Attempt>? attempts]) : attempts = attempts ?? [];
  final Catalog catalog;
  final List<Attempt> attempts;
  bool correct(Attempt a) => catalog.question(a.questionId).correct == a.choice;
  List<Attempt> forDay(DateTime now) => attempts.where((a) {
    final local = a.at.toLocal();
    final day = now.toLocal();
    return local.year == day.year && local.month == day.month && local.day == day.day;
  }).toList();
  int correctCount(Iterable<Attempt> values) => values.where(correct).length;
  double goal(DateTime now) => (forDay(now).length / 10).clamp(0.0, 1.0).toDouble();
  List<Attempt> forCourse(String topic) => attempts.where((a) =>
    catalog.question(a.questionId).topic == topic).toList();
  List<Question> get wrongQuestions {
    final latest = <String, Attempt>{};
    for (final a in attempts) { latest[a.questionId] = a; }
    return latest.values.where((a) => !correct(a)).map((a) =>
      catalog.question(a.questionId)).toList();
  }
}
