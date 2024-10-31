const url = new URL(window.location.href);
const todoid = url.searchParams.get("todoid");

document.addEventListener("DOMContentLoaded", function () {
  const createTagForm = document.getElementById("editTodo");
  if (createTagForm) {
    createTagForm.addEventListener("submit", async function (event) {
      event.preventDefault(); // フォームのデフォルトの送信を防ぐ
      const description = document.getElementById("description")?.value;
      const tag = document.getElementById("tag")?.value;
      const taskName = document.getElementById("taskName").value;
      const limit_at = document.getElementById("limit_at").value;
      const data = {
        todoID: todoid,
        taskName: taskName,
        description: description,
        limit_at: limit_at,
        tagID: tag,
      };
      console.log(data["todoID"]);

      const result = await fetch(`todo/${todoid}`, {
        method: "PUT", // POSTメソッドを指定
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // JSON形式に変換
      });

      // レスポンスの処理
      if (result.ok) {
        const responseData = await result.json();
        // リダイレクト
        console.log(responseData.message); // 成功メッセージを表示
        window.location.href = "/";
      } else {
        console.error("Error:", result.statusText);
        window.location.href = `/error?${result.statusText}`;
        // エラーメッセージを表示
      }
    });
  }
});
