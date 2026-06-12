const API_URL = "http://localhost:4000";

export async function analyzeContent(data) {
  const res = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Analysis failed");
  }
  return await res.json();
}
