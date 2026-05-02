import { View, Text, StyleSheet, ScrollView } from "react-native";

// ─── Mock Data ────────────────────────────────────────────────────────────────
// Hardcoded announcements sorted descending by date (most recent first).
// Replace with a fetch() call to GET /announcements once Harris's endpoint
// (Sprint 5, Task 5) is merged — same pattern used in OccupancyScreen.
// FR[2.4]: announcements displayed in descending chronological order.
const ANNOUNCEMENTS = [
    {
        id: 1,
        category: "Hours",
        title: "Holiday Hours — Memorial Day",
        message: "The Rec Center will operate on reduced hours (8 AM – 6 PM) on Memorial Day, May 26.",
        date: "May 20, 2025",
    },
    {
        id: 2,
        category: "Closure",
        title: "Pool Closure — Maintenance",
        message: "The lap pool will be closed May 22–23 for routine maintenance. All other facilities remain open.",
        date: "May 18, 2025",
    },
    {
        id: 3,
        category: "Event",
        title: "New Group Fitness Schedule",
        message: "Updated group fitness class times are now live. Check the front desk for the full schedule.",
        date: "May 15, 2025",
    },
    {
        id: 4,
        category: "Feature",
        title: "Basketball Court Reservations Open",
        message: "You can now reserve a basketball court up to 48 hours in advance through the booking feature.",
        date: "May 10, 2025",
    },
];

// Badge color per category
const CATEGORY_COLORS: Record<string, string> = {
    Hours:   "#003594",
    Closure: "#C84B31",
    Event:   "#0F6E56",
    Feature: "#7B5EA7",
};

export default function Announcements() {
    return (
        <ScrollView style={styles.scroll} contentContainerStyle={styles.container}>
            <Text style={styles.heading}>Announcements</Text>

            {ANNOUNCEMENTS.map((item, i) => (
                <View
                    key={item.id}
                    style={[styles.card, i < ANNOUNCEMENTS.length - 1 && styles.cardGap]}
                >
                    {/* Title row + category badge */}
                    <View style={styles.cardHeader}>
                        <Text style={styles.cardTitle} numberOfLines={2}>
                            {item.title}
                        </Text>
                        <View style={[styles.badge, { backgroundColor: CATEGORY_COLORS[item.category] ?? "#555" }]}>
                            <Text style={styles.badgeText}>{item.category}</Text>
                        </View>
                    </View>

                    {/* Body */}
                    <Text style={styles.message}>{item.message}</Text>

                    {/* Date */}
                    <Text style={styles.date}>{item.date}</Text>
                </View>
            ))}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    scroll:     { flex: 1, backgroundColor: "#f3f4f6" },
    container:  { padding: 16, paddingBottom: 32 },
    heading:    { fontSize: 24, fontWeight: "700", color: "#111", marginBottom: 16 },

    card: {
        backgroundColor: "#fff",
        borderRadius: 12,
        padding: 16,
        shadowColor: "#000",
        shadowOpacity: 0.06,
        shadowRadius: 6,
        shadowOffset: { width: 0, height: 2 },
    },
    cardGap:    { marginBottom: 12 },

    cardHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "flex-start",
        marginBottom: 8,
        gap: 8,
    },
    cardTitle:  { flex: 1, fontSize: 15, fontWeight: "600", color: "#111", lineHeight: 21 },

    badge: {
        borderRadius: 6,
        paddingHorizontal: 8,
        paddingVertical: 3,
        alignSelf: "flex-start",
    },
    badgeText:  { fontSize: 11, fontWeight: "600", color: "#fff", textTransform: "uppercase", letterSpacing: 0.4 },

    message:    { fontSize: 13, color: "#555", lineHeight: 19, marginBottom: 10 },
    date:       { fontSize: 12, color: "#999" },
});
