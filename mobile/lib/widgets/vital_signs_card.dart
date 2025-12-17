import 'package:flutter/material.dart';

class VitalSignsCard extends StatelessWidget {
  final String title;
  final String value;
  final String unit;
  final IconData icon;
  final Color color;
  final bool isAlert;
  final String? normalRange;

  const VitalSignsCard({
    required this.title,
    required this.value,
    required this.unit,
    required this.icon,
    required this.color,
    this.isAlert = false,
    this.normalRange,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: isAlert ? color.withOpacity(0.1) : Colors.grey[50],
        border: Border.all(
          color: isAlert ? color : Colors.grey[300]!,
          width: isAlert ? 2 : 1,
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 8),
          Text(
            title,
            style: TextStyle(fontSize: 12, color: Colors.grey[600]),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                value,
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
              const SizedBox(width: 4),
              Text(
                unit,
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
            ],
          ),
          if (normalRange != null) ...[
            const SizedBox(height: 4),
            Text(
              'Normal: $normalRange',
              style: TextStyle(fontSize: 10, color: Colors.grey[500]),
            ),
          ],
        ],
      ),
    );
  }
}
