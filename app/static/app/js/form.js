let ingredientCount = 1;  // 材料のカウントを初期化
let stepCount = 1;  // ステップのカウントを初期化

// 新しい材料を追加する関数
function addIngredient() {
    ingredientCount++;  // 材料のカウントを増加

    // 材料フォームコンテナを取得
    const ingredientFormContainer = document.getElementById("ingredient-form-container");

    // 新しい材料用のdivを作成、適用
    const newIngredientDiv = document.createElement("div");
    newIngredientDiv.classList.add("form-group");

    // 材料名のラベル作成
    const materialLabel = document.createElement("label");
    materialLabel.innerText = "材料名";

    // 材料名フィールドを作成
    const materialInput = document.createElement("input");
    materialInput.type = "text";
    materialInput.name = "material";
    materialInput.classList.add("form-control");

    // 分量のラベル作成
    const amountLabel = document.createElement("label");
    amountLabel.innerText = "分量";

    // 分量フィールドを作成
    const amountInput = document.createElement("input");
    amountInput.type = "text";
    amountInput.name = "amount";
    amountInput.classList.add("form-control");

    // 材料名と分量を新しい材料divに追加
    newIngredientDiv.appendChild(materialLabel);
    newIngredientDiv.appendChild(materialInput);
    newIngredientDiv.appendChild(amountLabel);
    newIngredientDiv.appendChild(amountInput);

    // 材料フォームコンテナに新しい材料divを追加
    ingredientFormContainer.appendChild(newIngredientDiv);
}

// 新しいステップを追加する関数
function addStep() {
    stepCount++;  // ステップのカウントを増加

    // ステップフォームコンテナの取得
    const stepFormContainer = document.getElementById("step-form-container");

    // 新しいステップ用のliを作成
    const newStepLi = document.createElement("li");

    // ドラッグハンドルの作成
    const dragHandle = document.createElement("span");
    dragHandle.classList.add("srt_hndl");
    dragHandle.innerText = "♥"; // ドラッグハンドルの表示内容
    
    // ステップ番号の表示
    const stepTextLabel = document.createElement("label");
    stepTextLabel.innerText = "作り方 " + stepCount;

    // 入力フィールドを作成
    const stepTextInput = document.createElement("input");
    stepTextInput.type = "text";
    stepTextInput.name = "step_text_" + stepCount; // ステップごとに名前を変更
    stepTextInput.classList.add("form-control");

    // 作り方の写真のラベル作成
    const stepImageLabel = document.createElement("label");
    stepImageLabel.innerText = "作り方の写真"

    // 画像の入力フィールドを作成
    const stepImageInput = document.createElement("input");
    stepImageInput.type = "file";
    stepImageInput.name = "step_image_" + stepCount; // ステップごとに名前を変更
    stepImageInput.classList.add("form-control");

    // 新しいliに要素を追加
    newStepLi.appendChild(dragHandle); // ドラッグハンドルを追加
    newStepLi.appendChild(stepTextLabel);
    newStepLi.appendChild(stepTextInput);
    newStepLi.appendChild(stepImageLabel);
    newStepLi.appendChild(stepImageInput);

    // ステップフォームコンテナに新しいliを追加
    stepFormContainer.appendChild(newStepLi);
}

// Sortableを初期化
new Sortable(document.getElementById('step-form-container'), {
    handle: '.srt_hndl', // ドラッグハンドルを指定
    animation: 150 // アニメーションのスピードを設定
});