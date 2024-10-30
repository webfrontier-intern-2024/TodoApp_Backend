const url = new URL(window.location.href);
const todoid = url.pathname.split("/")[2];
console.log(todoid);

document.addEventListener("DOMContentLoaded", function () {
  const deletes = document.getElementById("deleteTodo");
  if (deletes) {
    deletes.addEventListener("submit", async function (event) {
      event.preventDefault();

      const data = {
        todoID: todoid,
      };

      const result = await fetch(`/todo/${todoid}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // JSON形式に変換
      });

      // レスポンスの処理
      if (result.ok) {
        const responseData = await result.json();
        console.log(responseData.message); // 成功メッセージを表示
        window.location.href = "/";
      } else {
        console.error("Error:", result.statusText); // エラーメッセージを表示
      }
    });
  }
});
