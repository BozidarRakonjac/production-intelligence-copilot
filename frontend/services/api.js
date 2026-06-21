const API_URL = "http://localhost:8000/api/v1";

export async function sendMessage(question, sessionId) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get response from server");
  }

  return response.json();
}
