// フォーム画像の取得に必要
let stepCount = 1;

// 新しい材料を追加する関数
function addIngredient() {
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

// 材料を削除する関数
function subIngredient() {
    const ingredientFormContainer = document.getElementById("ingredient-form-container");

    // 最低一つは残るように調整
    if (ingredientFormContainer.children.length > 2) {
        ingredientFormContainer.removeChild(ingredientFormContainer.lastElementChild);
    }
}

// 新しいステップを追加する関数
function addStep() {
    // ステップフォームコンテナの取得
    const stepFormContainer = document.getElementById("step-form-container");

    // 新しいステップ用のliを作成
    const newStepLi = document.createElement("li");

    // ドラッグハンドルの作成
    const dragHandle = document.createElement("span");
    dragHandle.classList.add("srt_hndl");
    dragHandle.innerHTML = '<i class="fa-solid fa-grip-lines"></i>';

    // ステップ番号の表示
    const stepTextLabel = document.createElement("label");
    const stepNumber = stepFormContainer.children.length + 1; // 現在の要素数に基づく番号
    stepTextLabel.innerText = "作り方 " + stepNumber;
    stepTextLabel.classList.add('step-number-label');

    // 入力フィールドを作成
    const stepTextInput = document.createElement("input");
    stepTextInput.type = "text";
    stepTextInput.name = "step_text"; 
    stepTextInput.classList.add("form-control");

    // 作り方の写真のラベル作成
    const stepImageLabel = document.createElement("label");
    stepImageLabel.innerText = "作り方の写真"

    // 画像の入力フィールドを作成
    const stepImageInput = document.createElement("input");
    stepImageInput.type = "file";
    stepImageInput.name = `step_image_${stepCount + 1}`;  // step_image_2, step_image_3とすることでステップを判別可能に
    stepImageInput.classList.add("form-control");

    // 新しいliに要素を追加
    newStepLi.appendChild(dragHandle);
    newStepLi.appendChild(stepTextLabel);
    newStepLi.appendChild(stepTextInput);
    newStepLi.appendChild(stepImageLabel);
    newStepLi.appendChild(stepImageInput);

    // ステップフォームコンテナに新しいliを追加
    stepFormContainer.appendChild(newStepLi);

    stepCount++;
}

// ステップを削除する関数
function subStep() {
    const stepFormContainer = document.getElementById("step-form-container");

    // 最低一つは残るように調整
    if (stepFormContainer.children.length > 1) {
        stepFormContainer.removeChild(stepFormContainer.lastElementChild);
    }
}

// Sortableを初期化
new Sortable(document.getElementById('step-form-container'), {
    // ドラッグハンドルのクラスを教える
    handle: '.srt_hndl',
    // アニメーションの速さを設定(違いがわからん)
    animation: 150,
    onEnd: function () {
        // 並び替え後の要素を取得
        const stepItems = document.querySelectorAll('#step-form-container li');

        // 各ステップ番号を再割り当て
        stepItems.forEach((item, index) => {
            const stepNumberLabel = item.querySelector('.step-number-label');
            stepNumberLabel.innerText = `作り方 ${index + 1}`;

            const stepImageInput = item.querySelector('input[type="file"]');
            stepImageInput.name = `step_image_${index + 1}`;
        });
    }
});