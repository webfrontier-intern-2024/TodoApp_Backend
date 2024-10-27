document
  .getElementById("createTags")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // フォームのデフォルトの送信を防ぐ

    // フォームデータを取得
    const tags = document.getElementById("tags").value;

    // JSON形式に変換
    const data = {
      tagName: tags,
    };

    // Fetch APIを使ってデータを送信
    fetch("/tag", {
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
