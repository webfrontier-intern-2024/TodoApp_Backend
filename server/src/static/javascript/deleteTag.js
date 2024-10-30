const url = new URL(window.location.href);
const tagid = url.pathname.split("/")[2];

document.addEventListener("DOMContentLoaded", function () {
  const deletes = document.getElementById("deleteTag");
  if (deletes) {
    deletes.addEventListener("submit", async function (event) {
      event.preventDefault();

      const data = {
        tagID: tagid,
      };

      const result = await fetch(`/tag/${tagid}`, {
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
        window.location.href = "/tag";
      } else {
        console.error("Error:", result.statusText); // エラーメッセージを表示
      }
    });
  }
});
