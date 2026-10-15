import 'package:flutter/material.dart';
import '../core/study_controller.dart';
import 'audio_screen.dart';
import 'photo_screen.dart';
import 'wrong_notebook_screen.dart';

class ToolsScreen extends StatelessWidget {
  const ToolsScreen({super.key, required this.controller});
  final StudyController controller;
  @override
  Widget build(BuildContext context) => ListView(padding: const EdgeInsets.all(20), children: [
    const Text('Çalışma Araçları', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
    const SizedBox(height: 16),
    Card(child: ListTile(leading: const Icon(Icons.headphones), title: const Text('Sesli Akademi'), subtitle: const Text('Cihazın Türkçe sesiyle kısa özetler'),
      onTap: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => AudioScreen(catalog: controller.catalog))))),
    Card(child: ListTile(leading: const Icon(Icons.photo_camera), title: const Text('Fotoğraftan çözüm demosu'), subtitle: const Text('Görsel seçimi var · Gerçek AI bağlı değil'),
      onTap: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => const PhotoScreen())))),
    Card(child: ListTile(leading: const Icon(Icons.bookmark_outline), title: const Text('Yanlış Defteri'), subtitle: const Text('Tekrar çöz ve ilgili konuyu aç'),
      onTap: () => Navigator.push(context, MaterialPageRoute<void>(builder: (_) => WrongNotebookScreen(controller: controller))))),
    const SizedBox(height: 16), const Card(child: Padding(padding: EdgeInsets.all(20), child: Text(
      'AI öğretmen, kişisel çalışma koçu, gerçek podcastler ve çıkmış sorular sonraki geliştirme aşamasındadır. Şu anda sahte AI yanıtı üretilmez.')))]);
}
