import { v4 as uuidv4 } from "./node_modules/uuid/dist/esm-browser/index.js";

document.addEventListener("DOMContentLoaded", function () {
  // パスを調整
  const createTodoForm = document.getElementById("createTodos");
  createTodoForm.addEventListener("submit", async function (event) {
    event.preventDefault(); // フォームのデフォルトの送信を防ぐ

    // フォームデータを取得
    const taskName = document.getElementById("taskName")?.value;
    const description = document.getElementById("description")?.value;
    const tag = document.getElementById("tag")?.value;

    if (tag == null || tag == "") {
      alert("タグを入力してください");
      window.location.href = "/createTag";
    }
    // JSON形式に変換
    const data = {
      todoID: uuidv4(),
      taskName: taskName,
      description: description,
      finished: false,
      tagID: tag,
    };

    // Fetch APIを使ってデータを送信
    const result = await fetch("/todo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // JSON形式に変換
    });

    if (result.ok) {
      const responseData = await result.json();
      // console.log("Response:", responseData);
      window.location.href = "/"; // リダイレクト
      console.log(responseData.message);
    } else {
      const errorData = await result.json(); // エラーレスポンスをJSON形式で取得
      console.error("Error:", errorData);
    }
  });
});
