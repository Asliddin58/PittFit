import { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import Occupancy from "../Occupancy/index";
import Announcements from "../Announcements/index";

const PAGES = ["Occupancy", "Announcements"] as const;
type Page = typeof PAGES[number];

export default function PageSelector() {
    const [selectedPage, setSelectedPage] = useState<Page>("Occupancy");

    return (
        <View style={styles.container}>
            <View style={styles.content}>
                {selectedPage === "Occupancy" && <Occupancy />}
                {selectedPage === "Announcements" && <Announcements />}
            </View>
            <View style={styles.tabBar}>
                {PAGES.map((page) => (
                    <TouchableOpacity
                        key={page}
                        style={[styles.tab, selectedPage === page && styles.activeTab]}
                        onPress={() => setSelectedPage(page)}
                    >
                        <Text style={[styles.tabText, selectedPage === page && styles.activeTabText]}>
                            {page}
                        </Text>
                    </TouchableOpacity>
                ))}
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    content: {
        flex: 1,
    },
    tabBar: {
        flexDirection: "row",
        borderTopWidth: 1,
        borderTopColor: "#ddd",
        backgroundColor: "#fff",
    },
    tab: {
        flex: 1,
        paddingVertical: 14,
        alignItems: "center",
    },
    activeTab: {
        borderTopWidth: 2,
        borderTopColor: "#003594",
    },
    tabText: {
        fontSize: 14,
        color: "#aaa",
    },
    activeTabText: {
        color: "#003594",
        fontWeight: "600",
    },
});
