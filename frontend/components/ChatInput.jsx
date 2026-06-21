import { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  Text,
  StyleSheet,
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
        value={text}
        onChangeText={setText}
        onSubmitEditing={handleSend}
        editable={!disabled}
      />
      <TouchableOpacity
        style={styles.button}
        onPress={handleSend}
        disabled={disabled}
      >
        <Text style={styles.buttonText}>Send</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: "#e2e8f0",
    backgroundColor: "#ffffff",
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#cbd5e1",
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginRight: 8,
    fontSize: 15,
  },
  button: {
    backgroundColor: "#2563eb",
    borderRadius: 20,
    paddingHorizontal: 16,
    justifyContent: "center",
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "600",
  },
});
