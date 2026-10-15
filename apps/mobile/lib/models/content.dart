class Course {
  const Course({required this.id, required this.name, required this.emoji,
    required this.full, required this.short});
  final String id, name, emoji, full, short;
  String get subject => name.split(' · ').first;
  String get topic => name.split(' · ').last;
  factory Course.fromJson(Map<String, dynamic> json) => Course(
    id: json['id'] as String, name: json['name'] as String,
    emoji: json['emoji'] as String, full: json['full'] as String,
    short: json['short'] as String);
}

class Question {
  const Question({required this.id, required this.topic, required this.text,
    required this.choices, required this.correct, required this.explanation});
  final String id, topic, text, explanation;
  final List<String> choices;
  final int correct;
  factory Question.fromJson(Map<String, dynamic> json) => Question(
    id: json['id'] as String, topic: json['topic'] as String,
    text: json['q'] as String, choices: List<String>.from(json['a'] as List),
    correct: json['c'] as int, explanation: json['e'] as String);
}

class Catalog {
  Catalog(this.courses, this.questions);
  final List<Course> courses;
  final List<Question> questions;
  Course course(String id) => courses.firstWhere((c) => c.id == id);
  Question question(String id) => questions.firstWhere((q) => q.id == id);
  factory Catalog.fromJson(Map<String, dynamic> json) => Catalog(
    (json['course'] as Map<String, dynamic>).values.map((v) =>
      Course.fromJson(Map<String, dynamic>.from(v as Map))).toList(),
    (json['questions'] as List).map((v) =>
      Question.fromJson(Map<String, dynamic>.from(v as Map))).toList());
}

// Only the bundled, trusted example markup is converted to plain text.
// Remote/AI content will require a separate validated content schema.
String lessonText(String html) => html
    .replaceAll(RegExp(r'</h3>'), '\n')
    .replaceAll(RegExp(r'<h3>'), '\n')
    .replaceAll(RegExp(r'<li>'), '• ')
    .replaceAll(RegExp(r'</(?:li|p|ul)>'), '\n\n')
    .replaceAll(RegExp(r'<[^>]*>'), '')
    .replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>')
    .replaceAll(RegExp(r'\n{3,}'), '\n\n').trim();
