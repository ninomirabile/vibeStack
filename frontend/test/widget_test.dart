import "package:flutter_test/flutter_test.dart";
import "package:vibestack_frontend/main.dart";

void main() {
  testWidgets("VibeStackApp builds smoke test", (WidgetTester tester) async {
    await tester.pumpWidget(const VibeStackApp());
    expect(find.byType(VibeStackApp), findsOneWidget);
  });
}
