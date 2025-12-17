import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import '../controllers/analysis_controller.dart';
import '../models/diagnostic_models.dart';

class AnalysisResultsScreen extends StatefulWidget {
  final int diagnosisId;

  const AnalysisResultsScreen({
    Key? key,
    required this.diagnosisId,
  }) : super(key: key);

  @override
  State<AnalysisResultsScreen> createState() => _AnalysisResultsScreenState();
}

class _AnalysisResultsScreenState extends State<AnalysisResultsScreen>
    with SingleTickerProviderStateMixin {
  final AnalysisController _controller = Get.find();
  late TabController _tabController;

  // State variables
  bool _isLoadingMatches = false;
  bool _isLoadingRecommendations = false;
  dynamic _matches;
  dynamic _recommendations;
  dynamic _comparison;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadResults();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadResults() async {
    try {
      setState(() {
        _isLoadingMatches = true;
        _isLoadingRecommendations = true;
        _errorMessage = null;
      });

      // Load all three endpoints in parallel
      final results = await Future.wait([
        _controller.getKnowledgeMatches(widget.diagnosisId),
        _controller.getRecommendations(widget.diagnosisId),
        _controller.compareTraditions(widget.diagnosisId),
      ]);

      setState(() {
        _matches = results[0];
        _recommendations = results[1];
        _comparison = results[2];
        _isLoadingMatches = false;
        _isLoadingRecommendations = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'خطا در بارگیری نتایج: ${e.toString()}';
        _isLoadingMatches = false;
        _isLoadingRecommendations = false;
      });
      Get.snackbar('خطا', _errorMessage!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('نتایج تحلیل'),
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'تطابق‌ها', icon: Icon(Icons.search)),
            Tab(text: 'توصیه‌ها', icon: Icon(Icons.medical_services)),
            Tab(text: 'مقایسه', icon: Icon(Icons.compare_arrows)),
          ],
        ),
      ),
      body: _errorMessage != null
          ? _buildErrorWidget()
          : TabBarView(
              controller: _tabController,
              children: [
                _buildMatchesTab(),
                _buildRecommendationsTab(),
                _buildComparisonTab(),
              ],
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _loadResults,
        tooltip: 'بارگیری مجدد',
        child: const Icon(Icons.refresh),
      ),
    );
  }

  // ============ TAB 1: Matches ============
  Widget _buildMatchesTab() {
    if (_isLoadingMatches) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_matches == null) {
      return const Center(child: Text('هیچ نتیجه‌ای یافت نشد'));
    }

    final matches = _matches['matches'] as Map?;
    if (matches == null) {
      return const Center(child: Text('خطا در پردازش نتایج'));
    }

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Avicenna Matches
        _buildTraditionMatchesCard(
          tradition: 'داروی سنتی ایرانی (ابن سینا)',
          icon: Icons.health_and_safety,
          color: Colors.amber,
          matches: matches['avicenna_matches'] as List? ?? [],
        ),
        const SizedBox(height: 16),

        // TCM Matches
        _buildTraditionMatchesCard(
          tradition: 'طب چینی سنتی',
          icon: Icons.yin_yang,
          color: Colors.red,
          matches: matches['tcm_matches'] as List? ?? [],
        ),
        const SizedBox(height: 16),

        // Ayurveda Matches
        _buildTraditionMatchesCard(
          tradition: 'آیورودا (طب هندی)',
          icon: Icons.spa,
          color: Colors.green,
          matches: matches['ayurveda_matches'] as List? ?? [],
        ),
      ],
    );
  }

  Widget _buildTraditionMatchesCard({
    required String tradition,
    required IconData icon,
    required Color color,
    required List matches,
  }) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: color.withOpacity(0.3), width: 2),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(12)),
            ),
            child: Row(
              children: [
                Icon(icon, color: color, size: 28),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        tradition,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                      Text(
                        '${matches.length} تطابق یافت شد',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          if (matches.isEmpty)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                'تطابقی برای این سنت یافت نشد',
                style: TextStyle(color: Colors.grey[500]),
              ),
            )
          else
            ...matches.asMap().entries.map((entry) {
              final index = entry.key;
              final match = entry.value as Map;
              return _buildMatchItem(match, index + 1, color);
            }).toList(),
        ],
      ),
    );
  }

  Widget _buildMatchItem(Map match, int index, Color color) {
    final confidence = (match['confidence'] as num?)?.toDouble() ?? 0.0;
    final displayName = match['disease_name'] ??
        match['pattern_name'] ??
        match['name'] ??
        'Unknown';

    return Column(
      children: [
        if (index > 1)
          Divider(height: 1, color: Colors.grey[300]),
        Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  CircleAvatar(
                    radius: 18,
                    backgroundColor: color.withOpacity(0.2),
                    child: Text(
                      '$index',
                      style: TextStyle(
                        color: color,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          displayName,
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                        const SizedBox(height: 4),
                        LinearProgressIndicator(
                          value: confidence,
                          backgroundColor: Colors.grey[300],
                          valueColor:
                              AlwaysStoppedAnimation<Color>(color),
                          minHeight: 6,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    '${(confidence * 100).toStringAsFixed(1)}%',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: color,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              // Supporting findings
              if (match['supporting_findings'] != null)
                Text(
                  'ویژگی‌های تشخیصی: ${match['supporting_findings'].join(', ')}',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[700],
                  ),
                ),
              // Severity
              if (match['severity'] != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Chip(
                    label: Text(match['severity']),
                    backgroundColor: _getSeverityColor(match['severity'])
                        .withOpacity(0.2),
                    labelStyle: TextStyle(
                      color: _getSeverityColor(match['severity']),
                      fontSize: 12,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }

  Color _getSeverityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'high':
      case 'شدید':
        return Colors.red;
      case 'moderate':
      case 'متوسط':
        return Colors.orange;
      case 'low':
      case 'خفیف':
        return Colors.green;
      default:
        return Colors.blue;
    }
  }

  // ============ TAB 2: Recommendations ============
  Widget _buildRecommendationsTab() {
    if (_isLoadingRecommendations) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_recommendations == null) {
      return const Center(child: Text('هیچ توصیه‌ای یافت نشد'));
    }

    final recs = _recommendations['recommendations'] as Map?;
    if (recs == null || recs.isEmpty) {
      return const Center(child: Text('هیچ توصیه‌ای موجود نیست'));
    }

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (recs.containsKey('avicenna'))
          _buildRecommendationCard(
            tradition: 'داروی سنتی ایرانی',
            icon: Icons.health_and_safety,
            color: Colors.amber,
            recommendations: recs['avicenna'] as Map? ?? {},
          ),
        if (recs.containsKey('avicenna')) const SizedBox(height: 16),
        if (recs.containsKey('tcm'))
          _buildRecommendationCard(
            tradition: 'طب چینی سنتی',
            icon: Icons.yin_yang,
            color: Colors.red,
            recommendations: recs['tcm'] as Map? ?? {},
          ),
        if (recs.containsKey('tcm')) const SizedBox(height: 16),
        if (recs.containsKey('ayurveda'))
          _buildRecommendationCard(
            tradition: 'آیورودا',
            icon: Icons.spa,
            color: Colors.green,
            recommendations: recs['ayurveda'] as Map? ?? {},
          ),
      ],
    );
  }

  Widget _buildRecommendationCard({
    required String tradition,
    required IconData icon,
    required Color color,
    required Map recommendations,
  }) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: color.withOpacity(0.3), width: 2),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(12)),
            ),
            child: Row(
              children: [
                Icon(icon, color: color, size: 28),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    tradition,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Herbs
          if (recommendations['herbs'] != null)
            _buildRecommendationSection(
              title: '🌿 گیاهان دارویی',
              items: recommendations['herbs'] as List? ?? [],
              color: color,
            ),
          // Diet
          if (recommendations['diet_recommendations'] != null)
            _buildRecommendationSection(
              title: '🍽️ توصیه‌های غذایی',
              items: recommendations['diet_recommendations'] as List? ?? [],
              color: color,
            ),
          // Lifestyle
          if (recommendations['lifestyle_recommendations'] != null)
            _buildRecommendationSection(
              title: '🏃 توصیه‌های سبک زندگی',
              items: recommendations['lifestyle_recommendations'] as List? ?? [],
              color: color,
            ),
          // Treatments
          if (recommendations['treatment_protocols'] != null)
            _buildRecommendationSection(
              title: '⚕️ پروتکل‌های درمانی',
              items: recommendations['treatment_protocols'] as List? ?? [],
              color: color,
            ),
        ],
      ),
    );
  }

  Widget _buildRecommendationSection({
    required String title,
    required List items,
    required Color color,
  }) {
    return Column(
      children: [
        Divider(height: 1, color: Colors.grey[300]),
        Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                  color: color,
                ),
              ),
              const SizedBox(height: 8),
              ...items.map((item) {
                String displayText = item is String
                    ? item
                    : (item is Map
                        ? item['name'] ?? item['description'] ?? item.toString()
                        : item.toString());

                return Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(
                    children: [
                      Icon(Icons.check_circle, size: 16, color: color),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          displayText,
                          style: const TextStyle(fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                );
              }).toList(),
            ],
          ),
        ),
      ],
    );
  }

  // ============ TAB 3: Comparison ============
  Widget _buildComparisonTab() {
    if (_isLoadingMatches) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_comparison == null) {
      return const Center(child: Text('نتایج مقایسه در دسترس نیست'));
    }

    final comp = _comparison['comparison'] as Map?;
    if (comp == null) {
      return const Center(child: Text('خطا در پردازش مقایسه'));
    }

    final traditions = comp['traditions'] as Map? ?? {};
    final consensusAreas = comp['consensus_areas'] as List? ?? [];

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Consensus
        if (consensusAreas.isNotEmpty)
          Card(
            elevation: 2,
            color: Colors.green[50],
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.done_all, color: Colors.green[700]),
                      const SizedBox(width: 8),
                      Text(
                        'نقاط توافق',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.green[700],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ...consensusAreas
                      .map((item) => Padding(
                            padding: const EdgeInsets.only(bottom: 4),
                            child: Text('• $item'),
                          ))
                      .toList(),
                ],
              ),
            ),
          ),
        if (consensusAreas.isNotEmpty) const SizedBox(height: 16),
        // Tradition Details
        _buildTraditionComparison('Avicenna', traditions['avicenna'], Colors.amber),
        const SizedBox(height: 12),
        _buildTraditionComparison('TCM', traditions['tcm'], Colors.red),
        const SizedBox(height: 12),
        _buildTraditionComparison('Ayurveda', traditions['ayurveda'], Colors.green),
      ],
    );
  }

  Widget _buildTraditionComparison(
    String name,
    Map? tradition,
    Color color,
  ) {
    if (tradition == null) {
      return const SizedBox.shrink();
    }

    final totalMatches = tradition['total_matches'] as int? ?? 0;
    final topMatch = tradition['top_match'] as Map?;

    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: color,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  name,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                Chip(
                  label: Text('$totalMatches تطابق'),
                  backgroundColor: color.withOpacity(0.2),
                  labelStyle: TextStyle(
                    fontSize: 12,
                    color: color,
                  ),
                ),
              ],
            ),
            if (topMatch != null) ...[
              const SizedBox(height: 8),
              Text(
                'بهترین تطابق:',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 4),
              Text(
                topMatch['disease_name'] ??
                    topMatch['pattern_name'] ??
                    'Unknown',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              if (topMatch['confidence'] != null) ...[
                const SizedBox(height: 4),
                Row(
                  children: [
                    Expanded(
                      child: LinearProgressIndicator(
                        value: (topMatch['confidence'] as num).toDouble(),
                        backgroundColor: Colors.grey[300],
                        valueColor: AlwaysStoppedAnimation<Color>(color),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      '${((topMatch['confidence'] as num) * 100).toStringAsFixed(1)}%',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: color,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildErrorWidget() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.error_outline,
            size: 64,
            color: Colors.red[300],
          ),
          const SizedBox(height: 16),
          Text(
            _errorMessage ?? 'یک خطای نامعلوم رخ داد',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 16),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: _loadResults,
            icon: const Icon(Icons.refresh),
            label: const Text('تلاش مجدد'),
          ),
        ],
      ),
    );
  }
}
