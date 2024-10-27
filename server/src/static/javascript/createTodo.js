// import { v4 as uuidv4 } from "uuid";

document
  .getElementById("createTodo")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // フォームのデフォルトの送信を防ぐ

    // フォームデータを取得
    const taskName = document.getElementById("taskName").value;
    const description = document.getElementById("description").value;
    const tags = document.getElementById("tags").value;

    if (tags == null || tags == "") {
      alert("タグを入力してください");
      window.location.href = "/createTag";
    }

    // JSON形式に変換
    const data = {
      taskName: taskName,
      description: description,
    };

    // Fetch APIを使ってデータを送信
    await fetch("/todos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // JSON形式に変換
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        window.location.href = "/"; // リダイレクト
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
