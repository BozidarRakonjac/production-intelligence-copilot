import { View, Text, StyleSheet } from "react-native";

export default function ChatBubble({ message, isUser }) {
  return (
    <View
      style={[styles.bubble, isUser ? styles.userBubble : styles.botBubble]}
    >
      <Text style={isUser ? styles.userText : styles.botText}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  bubble: {
    maxWidth: "80%",
    padding: 12,
    borderRadius: 16,
    marginVertical: 4,
  },
  userBubble: {
    backgroundColor: "#2563eb",
    alignSelf: "flex-end",
    borderBottomRightRadius: 4,
  },
  botBubble: {
    backgroundColor: "#f1f5f9",
    alignSelf: "flex-start",
    borderBottomLeftRadius: 4,
  },
  userText: {
    color: "#ffffff",
    fontSize: 15,
  },
  botText: {
    color: "#1e293b",
    fontSize: 15,
  },
});
