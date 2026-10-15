import 'package:flutter/material.dart';
import '../core/study_controller.dart';
import '../models/content.dart';
import 'quiz_screen.dart';

class LessonsScreen extends StatelessWidget {
  const LessonsScreen({super.key, required this.controller});
  final StudyController controller;
  @override
  Widget build(BuildContext context) => ListView(padding: const EdgeInsets.all(20), children: [
    const Text('Ders Akademisi', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
    const Padding(padding: EdgeInsets.symmetric(vertical: 12), child: Text('Dört örnek ders · Konu anlatımı ve kısa özet')),
    for (final course in controller.catalog.courses) Card(child: ListTile(
      leading: Text(course.emoji, style: const TextStyle(fontSize: 28)),
      title: Text(course.subject), subtitle: Text(course.topic), trailing: const Icon(Icons.chevron_right),
      onTap: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => LessonDetail(controller: controller, course: course)))))]);
}
class LessonDetail extends StatefulWidget {
  const LessonDetail({super.key, required this.controller, required this.course});
  final StudyController controller;
  final Course course;
  @override
  State<LessonDetail> createState() => _LessonDetailState();
}
class _LessonDetailState extends State<LessonDetail> {
  bool short = false;
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: Text(widget.course.subject)),
    body: SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
      Text(widget.course.topic, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
      const SizedBox(height: 20),
      SegmentedButton<bool>(segments: const [ButtonSegment(value: false, label: Text('Anlatım')),
        ButtonSegment(value: true, label: Text('Kısa özet'))], selected: {short},
        onSelectionChanged: (v) => setState(() => short = v.first)),
      const SizedBox(height: 20), SelectableText(lessonText(short ? widget.course.short : widget.course.full),
        style: const TextStyle(fontSize: 16, height: 1.8)),
      const SizedBox(height: 20), FilledButton(onPressed: () => Navigator.push(context,
        MaterialPageRoute<void>(builder: (_) => Scaffold(appBar: AppBar(title: Text('${widget.course.subject} testi')),
          body: SafeArea(child: QuizScreen(controller: widget.controller, topic: widget.course.id))))),
        child: const Text('Bu konudan soru çöz')),
      const SizedBox(height: 12), const Text('Örnek içerik · Uzman incelemesi bekliyor.', style: TextStyle(fontSize: 12))])));
}
