import 'package:flutter/material.dart';

class PersonalizedPlanScreen extends StatefulWidget {
  const PersonalizedPlanScreen({Key? key}) : super(key: key);

  @override
  State<PersonalizedPlanScreen> createState() => _PersonalizedPlanScreenState();
}

class _PersonalizedPlanScreenState extends State<PersonalizedPlanScreen> {
  int currentPhase = 1;
  late PageController _pageController;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('برنامه درمانی شخصی'),
        centerTitle: true,
        elevation: 0,
      ),
      body: Column(
        children: [
          // نشانگر مراحل
          _buildPhaseIndicator(),
          const SizedBox(height: 20),
          // صفحات مراحل
          Expanded(
            child: PageView(
              controller: _pageController,
              onPageChanged: (index) {
                setState(() => currentPhase = index + 1);
              },
              children: [
                _buildPhase1(),
                _buildPhase2(),
                _buildPhase3(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPhaseIndicator() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'مرحله $currentPhase از ۳',
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: LinearProgressIndicator(
              value: currentPhase / 3,
              minHeight: 8,
              backgroundColor: Colors.grey.shade300,
              valueColor: AlwaysStoppedAnimation<Color>(
                currentPhase == 1
                    ? Colors.red
                    : currentPhase == 2
                        ? Colors.orange
                        : Colors.green,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPhase1() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildPhaseHeader(
            'تطهیر و تنقیه',
            'مرحله اول',
            Colors.red,
            '۱۰ روز',
          ),
          const SizedBox(height: 20),
          _buildPhaseContent(
            'این مرحله برای تطهیر بدن از اخلاط اضافی است.',
            [
              'شربت زنجبیل روزی ۲ بار',
              'حمام آب گرم روزانه',
              'ماساژ بدن ۲ بار هفتگی',
              'استراحت کافی',
            ],
            [
              '❌ غذاهای چرب',
              '❌ فعالیت شدید',
              '❌ کار اضافی',
              '❌ استرس',
            ],
          ),
          const SizedBox(height: 20),
          _buildTrackingCard(phase: 1),
        ],
      ),
    );
  }

  Widget _buildPhase2() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildPhaseHeader(
            'تعادل‌سازی',
            'مرحله دوم',
            Colors.orange,
            '۲۰ روز',
          ),
          const SizedBox(height: 20),
          _buildPhaseContent(
            'این مرحله برای تعادل‌سازی مزاج است.',
            [
              'بابونه و رز روزی ۳ بار',
              'فعالیت بدنی معمول',
              'یوگا یا تمرینات آرام',
              'مدیتیشن ۱۵ دقیقه',
            ],
            [
              '❌ غذاهای گرم',
              '❌ استرس',
              '❌ خواب ناکافی',
              '❌ نوشیدنی‌های گرم',
            ],
          ),
          const SizedBox(height: 20),
          _buildTrackingCard(phase: 2),
        ],
      ),
    );
  }

  Widget _buildPhase3() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildPhaseHeader(
            'تثبیت و نگهداری',
            'مرحله سوم',
            Colors.green,
            '۳۰ روز',
          ),
          const SizedBox(height: 20),
          _buildPhaseContent(
            'این مرحله برای حفظ تعادل و سلامت است.',
            [
              'تریاق (پیشگیری)',
              'شربت‌های فصلی',
              'ورزش منظم',
              'خواب ۷-۸ ساعت',
            ],
            [
              '❌ تجاوز از خود',
              '❌ فشار روانی',
              '❌ غذاهای ناشناخته',
              '❌ بی‌نظمی',
            ],
          ),
          const SizedBox(height: 20),
          _buildTrackingCard(phase: 3),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _completeProgram,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
              child: const Text('تکمیل برنامه'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPhaseHeader(
    String title,
    String subtitle,
    Color color,
    String duration,
  ) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: color,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check,
                  color: Colors.white,
                  size: 20,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      subtitle,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  color: color,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  duration,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPhaseContent(
    String description,
    List<String> recommendations,
    List<String> restrictions,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          description,
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey.shade700,
          ),
        ),
        const SizedBox(height: 16),
        const Text(
          'توصیه‌های اصلی:',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        ...recommendations
            .map((rec) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.check_circle_outline,
                        color: Colors.green,
                        size: 18,
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: Text(rec)),
                    ],
                  ),
                ))
            .toList(),
        const SizedBox(height: 16),
        const Text(
          'موارد مخالف:',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        ...restrictions
            .map((res) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.cancel_outlined,
                        color: Colors.red,
                        size: 18,
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: Text(res)),
                    ],
                  ),
                ))
            .toList(),
      ],
    );
  }

  Widget _buildTrackingCard({required int phase}) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.blue.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.trending_up, color: Colors.blue),
              SizedBox(width: 8),
              Text(
                'پیگیری پیشرفت',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'روز انجام‌شده',
                      style: TextStyle(fontSize: 12, color: Colors.grey),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${(phase - 1) * 10 + 5}',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'روز باقی‌مانده',
                      style: TextStyle(fontSize: 12, color: Colors.grey),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${60 - ((phase - 1) * 10 + 5)}',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              ElevatedButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('پیشرفت ثبت شد')),
                  );
                },
                child: const Text('ثبت'),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _completeProgram() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('تبریک!'),
        content: const Text('برنامه درمانی شما با موفقیت تکمیل شد'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('بستن'),
          ),
        ],
      ),
    );
  }
}
