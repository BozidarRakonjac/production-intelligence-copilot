import { useState, useRef } from "react";
import {
  View,
  ScrollView,
  Text,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  StatusBar,
} from "react-native";
import ChatBubble from "../components/ChatBubble";
import ChatInput from "../components/ChatInput";
import { sendMessage } from "../services/api";

const SUGGESTED_QUESTIONS = [
  "Give me a summary of operations this week",
  "Which machine has the most downtime?",
  "What are the most common defect types?",
  "Compare shift performance",
];

export default function ChatScreen() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollViewRef = useRef();

  const handleSend = async (question) => {
    const userMessage = { id: Date.now(), text: question, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await sendMessage(question, null);
      const botMessage = {
        id: Date.now() + 1,
        text: response.answer,
        isUser: false,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: "Connection error. Check that the backend is running.",
          isUser: false,
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
      setTimeout(
        () => scrollViewRef.current?.scrollToEnd({ animated: true }),
        100,
      );
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <StatusBar barStyle="light-content" backgroundColor="#0F1117" />

      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.statusDot} />
          <Text style={styles.headerTitle}>Production Copilot</Text>
        </View>
        <Text style={styles.headerSub}>10 machines · 90 days</Text>
      </View>

      {/* Accent line */}
      <View style={styles.accentLine} />

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messages}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.length === 0 && (
          <View style={styles.emptyState}>
            <Text style={styles.emptyTitle}>What would you like to know?</Text>
            <Text style={styles.emptySubtitle}>
              Ask about production KPIs, machine performance, quality, or
              downtime
            </Text>
            <View style={styles.suggestions}>
              {SUGGESTED_QUESTIONS.map((q, i) => (
                <View key={i} style={styles.suggestionChip}>
                  <Text
                    style={styles.suggestionText}
                    onPress={() => handleSend(q)}
                  >
                    {q}
                  </Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {messages.map((msg) => (
          <ChatBubble
            key={msg.id}
            message={msg.text}
            isUser={msg.isUser}
            isError={msg.isError}
          />
        ))}

        {loading && (
          <View style={styles.loadingRow}>
            <ActivityIndicator size="small" color="#38BDF8" />
            <Text style={styles.loadingText}>Analyzing data...</Text>
          </View>
        )}
      </ScrollView>

      <ChatInput onSend={handleSend} disabled={loading} />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0F1117",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
    paddingTop: Platform.OS === "ios" ? 54 : 16,
    paddingBottom: 14,
    backgroundColor: "#0F1117",
  },
  headerLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#10B981",
  },
  headerTitle: {
    fontSize: 17,
    fontWeight: "700",
    color: "#F1F5F9",
    letterSpacing: 0.3,
  },
  headerSub: {
    fontSize: 12,
    color: "#94A3B8",
    letterSpacing: 0.5,
  },
  accentLine: {
    height: 1,
    backgroundColor: "#38BDF8",
    opacity: 0.4,
  },
  messages: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
    paddingBottom: 8,
  },
  emptyState: {
    marginTop: 40,
    alignItems: "center",
    paddingHorizontal: 8,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: "700",
    color: "#F1F5F9",
    marginBottom: 8,
    textAlign: "center",
  },
  emptySubtitle: {
    fontSize: 14,
    color: "#94A3B8",
    textAlign: "center",
    lineHeight: 20,
    marginBottom: 28,
  },
  suggestions: {
    width: "100%",
    gap: 10,
  },
  suggestionChip: {
    backgroundColor: "#1A1D27",
    borderWidth: 1,
    borderColor: "#2D3148",
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  suggestionText: {
    color: "#38BDF8",
    fontSize: 14,
    lineHeight: 20,
  },
  loadingRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingVertical: 12,
    paddingHorizontal: 4,
  },
  loadingText: {
    color: "#94A3B8",
    fontSize: 13,
  },
});
