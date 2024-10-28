document.addEventListener("DOMContentLoaded", function () {
  const createTagForm = document.getElementById("createTag");
  if (createTagForm) {
    createTagForm.addEventListener("submit", async function (event) {
      event.preventDefault(); // フォームのデフォルトの送信を防ぐ

      const data = {
        tagName: document.getElementById("tagName").value,
        // フォームから値を取得
      };

      const result = await fetch("/tag", {
        method: "POST", // POSTメソッドを指定
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // JSON形式に変換
      });

      // レスポンスの処理
      if (result.ok) {
        const responseData = await result.json();
        window.location.href = "/"; // リダイレクト
        console.log(responseData.message); // 成功メッセージを表示
      } else {
        console.error("Error:", result.statusText); // エラーメッセージを表示
      }
    });
  }
});
