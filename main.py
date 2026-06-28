import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'package:http/http.dart' as http; // Standard package for REST API communication

void main() {
  runApp(MentalHealthApp());
}

// --- Application Core Configuration ---
class MentalHealthApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mental Health AI Monitor',
      theme: ThemeData(primarySwatch: Colors.teal, useMaterial3: true),
      home: AnalyticsDashboard(),
    );
  }
}

// --- Dashboard Screen: The Core Interface ---
class AnalyticsDashboard extends StatefulWidget {
  @override
  _AnalyticsDashboardState createState() => _AnalyticsDashboardState();
}

class _AnalyticsDashboardState extends State<AnalyticsDashboard> {
  bool isLoading = true;
  List<dynamic> analyticsData = [];

  @override
  void initState() {
    super.initState();
    fetchDashboardData();
  }

  // --- API Integration: Fetching Data from Backend ---
  Future<void> fetchDashboardData() async {
    try {
      // Connecting to the backend service to retrieve NLP analysis and clinical assessments
      final response = await http.get(Uri.parse('https://api.yourbackend.com/v1/dashboard/1'));
      if (response.statusCode == 200) {
        setState(() {
          analyticsData = json.decode(response.body)['data'];
          isLoading = false;
        });
      }
    } catch (e) {
      debugPrint("Error fetching dashboard data: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("AI Mental Health Analytics")),
      body: isLoading 
          ? Center(child: CircularProgressIndicator()) 
          : Column(
              children: [
                // Detailed Charting Section
                Expanded(
                  child: LineChart(
                    LineChartData(
                      lineBarsData: [
                        _buildLineBarData(Colors.blue, 0), // PHQ-9 Trends
                        _buildLineBarData(Colors.red, 1),  // GAD-7 Trends
                      ],
                    ),
                  ),
                ),
                // Detailed List View for User Journal Entries
                Expanded(child: _buildJournalList()),
              ],
            ),
    );
  }

  LineChartBarData _buildLineBarData(Color color, int index) {
    return LineChartBarData(
      spots: [FlSpot(0, 10), FlSpot(1, 8), FlSpot(2, 12)], // Placeholder for dynamic API spots
      isCurved: true,
      color: color,
      barWidth: 3,
    );
  }

  Widget _buildJournalList() {
    return ListView.builder(
      itemCount: analyticsData.length,
      itemBuilder: (context, index) {
        return ListTile(
          title: Text(analyticsData[index]['sentiment_label']),
          subtitle: Text("Analysis Confidence: ${analyticsData[index]['sentiment_score']}"),
        );
      },
    );
  }
}

// --- Data Models for Type Safety ---
class JournalEntry {
  final int userId;
  final String text;
  final DateTime timestamp;

  JournalEntry({required this.userId, required this.text, required this.timestamp});

  // Complex factory for parsing nested JSON structures
  factory JournalEntry.fromMap(Map<String, dynamic> map) {
    return JournalEntry(
      userId: map['user_id'],
      text: map['entry_text'],
      timestamp: DateTime.parse(map['analyzed_at']),
    );
  }
}

// --- Assessment Engine: Logic for Clinical Rules ---
class ClinicalAssessmentEngine {
  static String determineRiskLevel(int phq, int gad) {
    if (phq >= 15 || gad >= 15) return "CRITICAL_RISK";
    if (phq >= 10 || gad >= 10) return "MODERATE_RISK";
    return "LOW_RISK";
  }
}
