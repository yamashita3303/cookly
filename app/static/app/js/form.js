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

    // 新しいステップ用のdivを作成、適用
    const newStepDiv = document.createElement("div");
    newStepDiv.classList.add("form-group");

    // ステップ番号の入力フィールドを作成（表示はさせない）
    const stepNumberInput = document.createElement("input");
    stepNumberInput.type = "hidden";
    stepNumberInput.name = "step_number";
    stepNumberInput.value = stepCount; // ステップ番号を設定

    // ステップテキストのラベル作成
    const stepTextLabel = document.createElement("label");
    stepTextLabel.setAttribute("for", "id_step_text_" + stepCount);
    stepTextLabel.innerText = "作り方 " + stepCount;

    // 入力フィールドを作成
    const stepTextInput = document.createElement("input");
    stepTextInput.type = "text";
    stepTextInput.name = "step_text";
    stepTextInput.classList.add("form-control");

    // 作り方の写真のラベル作成
    const stepImageLabel = document.createElement("label");
    stepImageLabel.setAttribute("for", "id_step_image_" + stepCount);
    stepImageLabel.innerText = "作り方の写真 " + stepCount;

    // 画像の入力フィールドを作成
    const stepImageInput = document.createElement("input");
    stepImageInput.type = "file";
    stepImageInput.name = "step_image";
    stepImageInput.classList.add("form-control");

    // 定義したフィールドをnewStepDivに追加
    newStepDiv.appendChild(stepNumberInput);
    newStepDiv.appendChild(stepTextLabel);
    newStepDiv.appendChild(stepTextInput);
    newStepDiv.appendChild(stepImageLabel);
    newStepDiv.appendChild(stepImageInput);

    stepFormContainer.appendChild(newStepDiv);
}