import 'package:shared_preferences/shared_preferences.dart';

abstract interface class ProgressStore {
  Future<String?> read();
  Future<void> write(String value);
}

class DeviceProgressStore implements ProgressStore {
  static const key = 'akademi_mobile_progress_v1';
  @override
  Future<String?> read() async => (await SharedPreferences.getInstance()).getString(key);
  @override
  Future<void> write(String value) async {
    final ok = await (await SharedPreferences.getInstance()).setString(key, value);
    if (!ok) throw StateError('Cihaz kaydı yazılamadı');
  }
}
