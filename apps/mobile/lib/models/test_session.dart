import 'dart:math';
import 'content.dart';

class TestSession {
  TestSession(Iterable<Question> source, {Random? random})
      : questions = List<Question>.of(source)..shuffle(random);
  final List<Question> questions;
  final Map<String, int> answers = {};
  int index = 0;
  bool finished = false;
  bool get empty => questions.isEmpty;
  Question get current => questions[index];
  int? get selected => empty ? null : answers[current.id];
  bool answer(int choice) {
    if (finished || empty || selected != null || choice < 0 || choice >= current.choices.length) return false;
    answers[current.id] = choice;
    return true;
  }
  void next() {
    if (finished || empty || selected == null) return;
    if (index + 1 == questions.length) { finished = true; } else { index++; }
  }
  int get correctCount => questions.where((q) => answers[q.id] == q.correct).length;
}
