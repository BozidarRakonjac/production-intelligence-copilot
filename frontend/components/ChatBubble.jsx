import { View, Text, StyleSheet } from "react-native";
import Markdown from "react-native-markdown-display";

export default function ChatBubble({ message, isUser, isError }) {
  if (isUser) {
    return (
      <View style={styles.userBubble}>
        <Text style={styles.userText}>{message}</Text>
      </View>
    );
  }

  return (
    <View style={[styles.botBubble, isError && styles.errorBubble]}>
      <Markdown style={markdownStyles}>{message}</Markdown>
    </View>
  );
}

const styles = StyleSheet.create({
  userBubble: {
    maxWidth: "80%",
    padding: 12,
    paddingHorizontal: 16,
    borderRadius: 18,
    borderBottomRightRadius: 4,
    backgroundColor: "#1E40AF",
    alignSelf: "flex-end",
    marginVertical: 4,
  },
  botBubble: {
    maxWidth: "92%",
    padding: 14,
    borderRadius: 18,
    borderBottomLeftRadius: 4,
    backgroundColor: "#1A1D27",
    borderWidth: 1,
    borderColor: "#2D3148",
    alignSelf: "flex-start",
    marginVertical: 4,
  },
  errorBubble: {
    borderColor: "#F59E0B",
  },
  userText: {
    color: "#ffffff",
    fontSize: 15,
    lineHeight: 22,
  },
});

const markdownStyles = {
  body: {
    color: "#E2E8F0",
    fontSize: 14,
    lineHeight: 22,
  },
  strong: {
    fontWeight: "700",
    color: "#F1F5F9",
  },
  em: {
    color: "#94A3B8",
    fontStyle: "italic",
  },
  table: {
    borderWidth: 1,
    borderColor: "#2D3148",
    borderRadius: 8,
    marginVertical: 10,
    overflow: "hidden",
  },
  thead: {
    backgroundColor: "#0F1117",
  },
  th: {
    padding: 8,
    fontWeight: "700",
    color: "#38BDF8",
    fontSize: 12,
    letterSpacing: 0.5,
  },
  td: {
    padding: 8,
    color: "#CBD5E1",
    fontSize: 13,
    borderTopWidth: 1,
    borderTopColor: "#2D3148",
  },
  tr: {
    backgroundColor: "#1A1D27",
  },
  bullet_list: {
    marginVertical: 6,
  },
  list_item: {
    marginVertical: 3,
    color: "#E2E8F0",
  },
  heading1: {
    fontSize: 17,
    fontWeight: "700",
    color: "#F1F5F9",
    marginTop: 12,
    marginBottom: 6,
  },
  heading2: {
    fontSize: 15,
    fontWeight: "700",
    color: "#38BDF8",
    marginTop: 10,
    marginBottom: 4,
  },
  heading3: {
    fontSize: 14,
    fontWeight: "600",
    color: "#94A3B8",
    marginTop: 8,
    marginBottom: 4,
  },
  blockquote: {
    backgroundColor: "#0F1117",
    borderLeftWidth: 3,
    borderLeftColor: "#38BDF8",
    paddingLeft: 12,
    paddingVertical: 6,
    marginVertical: 8,
    borderRadius: 4,
  },
  code_inline: {
    backgroundColor: "#0F1117",
    color: "#38BDF8",
    borderRadius: 4,
    paddingHorizontal: 6,
    fontFamily: "monospace",
    fontSize: 12,
  },
  hr: {
    backgroundColor: "#2D3148",
    height: 1,
    marginVertical: 10,
  },
};
