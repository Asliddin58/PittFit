import AsyncStorage from "@react-native-async-storage/async-storage"
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator, TextInput } from "react-native";
import { useState } from "react";

const BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:5001";

export default function Index() {
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSSOLogin = async () => {
        setLoading(true);
        const response = await fetch(`${BASE_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        if (!response.ok) {
            alert(data.error);
            setLoading(false);
            return;
        }

        await AsyncStorage.setItem("token", data.token);
        // TODO: Redirect to dashboard on authentication
        alert("Logged in!");
        setLoading(false);
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.pitt}>Pitt</Text>
                <Text style={styles.fit}>Fit</Text>
            </View>

            <Text style={styles.subtitle}>Sign in with your Pitt account</Text>

            <TextInput
                style={styles.input}
                placeholder="Email"
                placeholderTextColor="#aaa"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                placeholderTextColor="#aaa"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />

            <TouchableOpacity style={styles.button} onPress={handleSSOLogin} disabled={loading}>
                {loading ? (
                    <ActivityIndicator color="#fff" />
                ) : (
                    <Text style={styles.buttonText}>Sign in with Pitt SSO</Text>
                )}
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#1a1a2e",
        padding: 24,
    },
    header: {
        flexDirection: "row",
        marginBottom: 12,
    },
    pitt: {
        fontSize: 64,
        fontWeight: "bold",
        color: "#003594",
        fontFamily: "Georgia",
        fontStyle: "italic",
        letterSpacing: 2,
    },
    fit: {
        fontSize: 72,
        fontWeight: "bold",
        color: "#FFB81C",
        fontFamily: "Impact",
        letterSpacing: -2,
    },
    subtitle: {
        fontSize: 16,
        color: "#aaa",
        marginBottom: 48,
    },
    input: {
        width: "100%",
        backgroundColor: "#2a2a3e",
        borderRadius: 8,
        paddingVertical: 14,
        paddingHorizontal: 16,
        color: "#fff",
        fontSize: 16,
        marginBottom: 12,
    },
    button: {
        backgroundColor: "#003594",
        paddingVertical: 16,
        paddingHorizontal: 40,
        borderRadius: 8,
        width: "100%",
        alignItems: "center",
    },
    buttonText: {
        color: "#fff",
        fontSize: 16,
        fontWeight: "600",
    },
});

