const url = new URL(window.location.href);
const tagid = url.searchParams.get("tagid");

document.addEventListener("DOMContentLoaded", function () {
  const createTagForm = document.getElementById("editTag");
  if (createTagForm) {
    createTagForm.addEventListener("submit", async function (event) {
      event.preventDefault();
      const name = document.getElementById("tagName").value;
      const data = {
        tagName: name,
      };

      const result = await fetch(`tag/${tagid}`, {
        method: "PUT", // POSTメソッドを指定
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // JSON形式に変換
      });

      // レスポンスの処理
      if (result.ok) {
        const responseData = await result.json();
        console.log(responseData.message); // 成功メッセージを表示
        window.location.href = "/tag";
      } else {
        console.error("Error:", result.statusText); // エラーメッセージを表示
      }
    });
  }
});
