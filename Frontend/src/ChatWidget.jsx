import { useState } from "react";

export default function ChatWidget() {
  const [msgs, setMsgs] = useState([
    { role: "bot", text: "Hi. Ask me anything about your policy or claims." },
  ]);

  const [text, setText] = useState("");

  async function send() {
    const msg = text.trim();
    if (!msg) return;

    setMsgs((m) => [...m, { role: "user", text: msg }]);
    setText("");

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    const data = await res.json();
    setMsgs((m) => [...m, { role: "bot", text: data.answer }]);
  }

  return (
    <div>
      {msgs.map((m, i) => (
        <div key={i}>
          <b>{m.role}:</b> {m.text}
        </div>
      ))}

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your question"
      />

      <button onClick={send}>Send</button>
    </div>
  );
}
