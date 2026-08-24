import { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  Text,
  StyleSheet,
  Platform,
} from "react-native";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim().length === 0) return;
    onSend(text);
    setText("");
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Ask about your production data..."
        placeholderTextColor="#4B5563"
        value={text}
        onChangeText={setText}
        onSubmitEditing={handleSend}
        editable={!disabled}
        multiline
        maxLength={500}
      />
      <TouchableOpacity
        style={[styles.button, disabled && styles.buttonDisabled]}
        onPress={handleSend}
        disabled={disabled}
      >
        <Text style={styles.buttonText}>→</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "flex-end",
    padding: 12,
    paddingBottom: Platform.OS === "ios" ? 28 : 12,
    borderTopWidth: 1,
    borderTopColor: "#2D3148",
    backgroundColor: "#0F1117",
    gap: 10,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#2D3148",
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 15,
    color: "#F1F5F9",
    backgroundColor: "#1A1D27",
    maxHeight: 120,
  },
  button: {
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: "#1E40AF",
    justifyContent: "center",
    alignItems: "center",
  },
  buttonDisabled: {
    backgroundColor: "#1A1D27",
    borderWidth: 1,
    borderColor: "#2D3148",
  },
  buttonText: {
    color: "#F1F5F9",
    fontSize: 20,
    fontWeight: "700",
  },
});
