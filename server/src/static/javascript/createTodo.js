// import { v4 as uuidv4 } from "uuid";
document.addEventListener("DOMContentLoaded", function () {
  const createTodoForm = document.getElementById("createTodo");
  if (createTodoForm) {
    createTodoForm.addEventListener("submit", async function (event) {
      event.preventDefault(); // フォームのデフォルトの送信を防ぐ

      // フォームデータを取得
      const taskName = document.getElementById("taskName").value;
      const description = document.getElementById("description").value;
      const tag = document.getElementById("tag").value;

      if (tag == null || tag == "") {
        alert("タグを入力してください");
        window.location.href = "/createTag";
      }

      // JSON形式に変換
      const data = {
        taskName: taskName,
        description: description,
        completed: false,
        tags: tag,
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
        window.location.href = "/"; // リダイレクト
        console.log(responseData.message);
        return responseData;
      } else {
        console.error("Error:", result.statusText); // エラーメッセージを表示
      }
    });
  } else {
    console.log("createTodoForm is null");
  }
});
