import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class PhotoScreen extends StatefulWidget {
  const PhotoScreen({super.key});
  @override
  State<PhotoScreen> createState() => _PhotoScreenState();
}
class _PhotoScreenState extends State<PhotoScreen> {
  Uint8List? photo;
  String? message;
  bool loading = false, showDemo = false;
  final ImagePicker picker = ImagePicker();
  bool validImage(Uint8List b) {
    if (b.length < 12) return false;
    return (b[0] == 0xff && b[1] == 0xd8 && b[2] == 0xff) ||
      (b[0] == 0x89 && b[1] == 0x50 && b[2] == 0x4e && b[3] == 0x47) ||
      (String.fromCharCodes(b.take(4)) == 'RIFF' && String.fromCharCodes(b.sublist(8, 12)) == 'WEBP');
  }
  Future<void> pick(ImageSource source) async {
    if (loading) return;
    setState(() { loading = true; message = null; });
    try {
      final file = await picker.pickImage(source: source, maxWidth: 2048, maxHeight: 2048);
      if (file == null) return;
      if (await file.length() > 10 * 1024 * 1024) throw const FormatException('too-large');
      final bytes = await file.readAsBytes();
      if (!validImage(bytes)) throw const FormatException('unsupported-image');
      if (mounted) setState(() { photo = bytes; showDemo = false; message = 'Görsel yalnızca bu ekranda tutulur; hiçbir AI servisine gönderilmez.'; });
    } catch (_) {
      if (mounted) setState(() => message = 'Görsel alınamadı. Kamera/galeri iznini ve JPEG, PNG veya WebP biçimini kontrol et. En fazla 10 MB kullan.');
    } finally { if (mounted) setState(() => loading = false); }
  }
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: const Text('Fotoğraftan Çözüm Demosu')),
    body: SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
      const Card(child: Padding(padding: EdgeInsets.all(20), child: Text(
        'GERÇEK AI BAĞLI DEĞİL\nAşağıdaki çözüm yüklediğin fotoğrafa ait değildir. Sabit bir örnek matematik çözümüdür.', style: TextStyle(fontWeight: FontWeight.bold, height: 1.6)))),
      const SizedBox(height: 16), Wrap(spacing: 12, runSpacing: 8, children: [
        FilledButton.icon(onPressed: loading ? null : () => pick(ImageSource.camera), icon: const Icon(Icons.camera_alt), label: const Text('Fotoğraf çek')),
        OutlinedButton.icon(onPressed: loading ? null : () => pick(ImageSource.gallery), icon: const Icon(Icons.photo_library), label: const Text('Galeriden seç'))]),
      if (loading) const Padding(padding: EdgeInsets.all(16), child: LinearProgressIndicator()),
      if (message != null) Padding(padding: const EdgeInsets.symmetric(vertical: 16), child: Text(message!)),
      if (photo != null) ...[
        Image.memory(photo!, height: 240, fit: BoxFit.contain, semanticLabel: 'Seçilen soru fotoğrafı',
          errorBuilder: (_, _, _) => const Text('Görsel açılamadı. Başka bir dosya seç.')),
        TextButton(onPressed: () => setState(() { photo = null; message = null; showDemo = false; }), child: const Text('Fotoğrafı kaldır'))],
      const SizedBox(height: 16), FilledButton(onPressed: () => setState(() => showDemo = true), child: const Text('Örnek çözüm akışını göster')),
      if (showDemo) const Card(child: Padding(padding: EdgeInsets.all(20), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Örnek: 3x + 5 = 26', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)), SizedBox(height: 16),
        Text('1. Her iki taraftan 5 çıkar: 3x = 21\n\n2. Her iki tarafı 3’e böl: x = 7\n\n3. Kontrol et: 3 × 7 + 5 = 26', style: TextStyle(fontSize: 16, height: 1.8)),
        SizedBox(height: 16), Text('Demo sonucu: x = 7. Yüklenen görsel analiz edilmedi.')])))])));
}
