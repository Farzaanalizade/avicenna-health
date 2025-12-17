import 'package:flutter/material.dart';

class DiagnosticScreen extends StatefulWidget {
  const DiagnosticScreen({Key? key}) : super(key: key);

  @override
  State<DiagnosticScreen> createState() => _DiagnosticScreenState();
}

class _DiagnosticScreenState extends State<DiagnosticScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  
  // کنترل‌کننده‌های ورودی
  int pulseRate = 70;
  String selectedPulseType = 'motavasseta';
  String selectedUrineDensity = 'motavasseta';
  String selectedTongueColor = 'pink';
  
  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('تشخیصی سینا'),
        centerTitle: true,
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.amber,
          labelColor: Colors.amber,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(text: 'نبض'),
            Tab(text: 'ادرار'),
            Tab(text: 'زبان'),
            Tab(text: 'نتیجه'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildPulseTab(),
          _buildUrineTab(),
          _buildTongueTab(),
          _buildResultsTab(),
        ],
      ),
    );
  }

  Widget _buildPulseTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'تحلیل نبض',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          
          // نمایش نبض
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.red.shade50,
              borderRadius: BorderRadius.circular(15),
              border: Border.all(color: Colors.red.shade200),
            ),
            child: Column(
              children: [
                const Text(
                  'نرخ ضربان',
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                ),
                const SizedBox(height: 10),
                Text(
                  '$pulseRate',
                  style: const TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                  ),
                ),
                const SizedBox(height: 10),
                const Text(
                  'ضربه در دقیقه',
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          
          // اسلایدر نبض
          Text(
            'نرخ ضربان: $pulseRate bpm',
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
          Slider(
            value: pulseRate.toDouble(),
            min: 40,
            max: 150,
            divisions: 110,
            label: '$pulseRate bpm',
            onChanged: (value) {
              setState(() => pulseRate = value.toInt());
            },
          ),
          const SizedBox(height: 20),
          
          // نوع نبض
          const Text(
            'نوع نبض:',
            style: TextStyle(fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 10),
          DropdownButton<String>(
            value: selectedPulseType,
            isExpanded: true,
            items: [
              'motavasseta',
              'kabir',
              'saghir',
              'sare_en',
              'beth_in',
              'qavi',
              'zaeef'
            ].map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(_translatePulseType(value)),
              );
            }).toList(),
            onChanged: (String? newValue) {
              if (newValue != null) {
                setState(() => selectedPulseType = newValue);
              }
            },
          ),
          const SizedBox(height: 20),
          
          // دکمه تحلیل
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _analyzePulse,
              child: const Text('تحلیل نبض'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildUrineTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'تحلیل ادرار',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          
          // نمایش رنگ ادرار
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.yellow.shade50,
              borderRadius: BorderRadius.circular(15),
              border: Border.all(color: Colors.yellow.shade200),
            ),
            child: Column(
              children: [
                const Text('رنگ ادرار'),
                const SizedBox(height: 10),
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    color: Colors.yellow.shade300,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.yellow.shade700, width: 2),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          
          // چگالی
          const Text(
            'چگالی:',
            style: TextStyle(fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 10),
          DropdownButton<String>(
            value: selectedUrineDensity,
            isExpanded: true,
            items: ['khafif', 'motavasseta', 'saqil'].map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(_translateUrineDensity(value)),
              );
            }).toList(),
            onChanged: (String? newValue) {
              if (newValue != null) {
                setState(() => selectedUrineDensity = newValue);
              }
            },
          ),
          const SizedBox(height: 20),
          
          // صفات اضافی
          CheckboxListTile(
            title: const Text('رسوب'),
            value: false,
            onChanged: (_) {},
          ),
          CheckboxListTile(
            title: const Text('خون'),
            value: false,
            onChanged: (_) {},
          ),
          const SizedBox(height: 20),
          
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _analyzeUrine,
              child: const Text('تحلیل ادرار'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTongueTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'تحلیل زبان',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          
          // نمایش زبان (شبیه‌سازی)
          Center(
            child: Container(
              width: 120,
              height: 60,
              decoration: BoxDecoration(
                color: Colors.pink.shade300,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.pink.shade700, width: 2),
              ),
              child: const Center(
                child: Text(
                  'زبان',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 20),
          
          const Text(
            'رنگ:',
            style: TextStyle(fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 10),
          DropdownButton<String>(
            value: selectedTongueColor,
            isExpanded: true,
            items: ['pink', 'red', 'pale'].map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(_translateTongueColor(value)),
              );
            }).toList(),
            onChanged: (String? newValue) {
              if (newValue != null) {
                setState(() => selectedTongueColor = newValue);
              }
            },
          ),
          const SizedBox(height: 20),
          
          const Text(
            'پوشش:',
            style: TextStyle(fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: Wrap(
                  spacing: 8,
                  children: ['هیچ', 'سفید', 'زرد'].map((String option) {
                    return FilterChip(
                      label: Text(option),
                      onSelected: (_) {},
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _analyzeTongue,
              child: const Text('تحلیل زبان'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultsTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'خلاصه تشخیص',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          
          // مزاج
          _buildResultCard(
            title: 'مزاج تشخیص‌شده',
            value: 'متعادل',
            color: Colors.green,
          ),
          const SizedBox(height: 15),
          
          // وضعیت سلامت
          _buildResultCard(
            title: 'وضعیت سلامت',
            value: 'خوب',
            color: Colors.blue,
          ),
          const SizedBox(height: 15),
          
          // درمان‌های توصیه‌شده
          const Text(
            'درمان‌های توصیه‌شده:',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          ),
          const SizedBox(height: 10),
          _buildRecommendationList(),
          const SizedBox(height: 20),
          
          // توصیه‌های سبک زندگی
          const Text(
            'توصیه‌های سبک زندگی:',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          ),
          const SizedBox(height: 10),
          _buildLifestyleRecommendations(),
          const SizedBox(height: 20),
          
          // دکمه ذخیره
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _saveDiagnosis,
              icon: const Icon(Icons.save),
              label: const Text('ذخیره تشخیص'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultCard({
    required String title,
    required String value,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecommendationList() {
    final recommendations = [
      'شربت زنجبیل روزی دوبار',
      'مصرف میوه‌های فصلی',
      'خواب منظم ۸ ساعت',
      'ورزش سبک روزانه',
    ];

    return Column(
      children: recommendations
          .map((rec) => Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Row(
                  children: [
                    const Icon(Icons.check_circle, color: Colors.green, size: 20),
                    const SizedBox(width: 10),
                    Expanded(child: Text(rec)),
                  ],
                ),
              ))
          .toList(),
    );
  }

  Widget _buildLifestyleRecommendations() {
    final recommendations = [
      'کاهش استرس و فشار روانی',
      'استراحت کافی',
      'پرهیز از غذاهای چرب',
      'نور خورشید کافی',
    ];

    return Column(
      children: recommendations
          .map((rec) => Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Row(
                  children: [
                    const Icon(Icons.lightbulb, color: Colors.amber, size: 20),
                    const SizedBox(width: 10),
                    Expanded(child: Text(rec)),
                  ],
                ),
              ))
          .toList(),
    );
  }

  void _analyzePulse() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('تحلیل نبض انجام شد')),
    );
    _tabController.animateTo(3); // برو به نتایج
  }

  void _analyzeUrine() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('تحلیل ادرار انجام شد')),
    );
  }

  void _analyzeTongue() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('تحلیل زبان انجام شد')),
    );
  }

  void _saveDiagnosis() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('تشخیص ذخیره شد')),
    );
  }

  String _translatePulseType(String type) {
    const map = {
      'motavasseta': 'متوسط',
      'kabir': 'بزرگ (پر)',
      'saghir': 'کوچک',
      'sare_en': 'سریع',
      'beth_in': 'آهسته',
      'qavi': 'قوی',
      'zaeef': 'ضعیف',
    };
    return map[type] ?? type;
  }

  String _translateUrineDensity(String density) {
    const map = {
      'khafif': 'سبک',
      'motavasseta': 'متوسط',
      'saqil': 'سنگین',
    };
    return map[density] ?? density;
  }

  String _translateTongueColor(String color) {
    const map = {
      'pink': 'صورتی',
      'red': 'قرمز',
      'pale': 'رنگ‌پریده',
    };
    return map[color] ?? color;
  }
}
