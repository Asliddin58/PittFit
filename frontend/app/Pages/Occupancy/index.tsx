import { View, Text, StyleSheet, ScrollView } from "react-native";

const CURRENT_OCCUPANCY = 312;

const TYPICAL = 280;

const HOURS = [
    { day: "Monday",    open: "6:00 AM", close: "11:00 PM" },
    { day: "Tuesday",   open: "6:00 AM", close: "11:00 PM" },
    { day: "Wednesday", open: "6:00 AM", close: "11:00 PM" },
    { day: "Thursday",  open: "6:00 AM", close: "11:00 PM" },
    { day: "Friday",    open: "6:00 AM", close: "9:00 PM"  },
    { day: "Saturday",  open: "8:00 AM", close: "8:00 PM"  },
    { day: "Sunday",    open: "10:00 AM", close: "8:00 PM" },
];

const TODAY = new Date().toLocaleDateString("en-US", { weekday: "long" });

export default function Occupancy() {
    return (
        <ScrollView style={styles.scroll} contentContainerStyle={styles.container}>
            <Text style={styles.heading}>Rec Center Occupancy</Text>

            <View style={styles.card}>
                <Text style={styles.cardTitle}>Live Count</Text>
                <Text style={styles.bigNumber}>{CURRENT_OCCUPANCY}</Text>
                <Text style={styles.caption}>people currently in the rec center</Text>
                <Text style={styles.caption}></Text>
                <Text style={styles.caption}>Typical for this time: {TYPICAL} – {TYPICAL + 70}</Text>
            </View>

            <Text style={styles.sectionTitle}>Hours</Text>
            <View style={styles.card}>
                {HOURS.map((row, i) => (
                    <View key={row.day} style={[styles.hoursRow, i < HOURS.length - 1 && styles.rowBorder]}>
                        <Text style={[styles.dayText, row.day === TODAY && styles.todayText]}>{row.day}</Text>
                        <Text style={[styles.hoursText, row.day === TODAY && styles.todayText]}>
                            {row.open} – {row.close}
                        </Text>
                    </View>
                ))}
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    scroll: { flex: 1, backgroundColor: "#f3f4f6" },
    container: { padding: 16, paddingBottom: 32 },
    heading: { fontSize: 24, fontWeight: "700", color: "#111", marginBottom: 16 },
    sectionTitle: { fontSize: 16, fontWeight: "600", color: "#555", marginTop: 20, marginBottom: 8 },
    card: {
        backgroundColor: "#fff",
        borderRadius: 12,
        padding: 16,
        shadowColor: "#000",
        shadowOpacity: 0.06,
        shadowRadius: 6,
        shadowOffset: { width: 0, height: 2 },
    },
    cardTitle: { fontSize: 14, color: "#666", marginBottom: 4 },
    bigNumber: { fontSize: 64, fontWeight: "700", color: "#003594" },
    caption: { fontSize: 12, color: "#999", marginTop: 4 },
    hoursRow: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 10 },
    rowBorder: { borderBottomWidth: 1, borderBottomColor: "#f0f0f0" },
    dayText: { fontSize: 14, color: "#555" },
    hoursText: { fontSize: 14, color: "#555" },
    todayText: { color: "#003594", fontWeight: "700" },
});
