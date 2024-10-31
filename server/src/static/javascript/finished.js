const url = new URL(window.location.href);
const todoid = url.pathname.split("/")[2];

document.addEventListener("DOMContentLoaded", function () {
  const finish = document.getElementById("finished");
  if (finish) {
    finish.addEventListener("submit", async function (event) {
      event.preventDefault(); // フォームのデフォルトの送信を防ぐ

      const data = {
        todoID: todoid,
        finished: false,
      };

      const result = await fetch(`/finished/${todoid}`, {
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
