let stepCount = 1;  // ステップのカウントを初期化

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

function subIngredient() {
    const ingredientFormContainer = document.getElementById("ingredient-form-container");

    if (ingredientFormContainer.children.length > 2) {
        ingredientFormContainer.removeChild(ingredientFormContainer.lastElementChild);
    }
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
    dragHandle.innerHTML = '<i class="fa-solid fa-grip-lines"></i>' // ドラッグハンドルの表示内容
    
    // ステップ番号の表示
    const stepTextLabel = document.createElement("label");
    stepTextLabel.innerText = "作り方 " + stepCount;
    stepTextLabel.classList.add('step-number-label');

    // 入力フィールドを作成
    const stepTextInput = document.createElement("input");
    stepTextInput.type = "text";
    stepTextInput.name = "step_text"; // ステップごとに名前を変更
    stepTextInput.classList.add("form-control");

    // 作り方の写真のラベル作成
    const stepImageLabel = document.createElement("label");
    stepImageLabel.innerText = "作り方の写真"

    // 画像の入力フィールドを作成
    const stepImageInput = document.createElement("input");
    stepImageInput.type = "file";
    stepImageInput.name = "step_image"; // ステップごとに名前を変更
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

function subStep() {
    const stepFormContainer = document.getElementById("step-form-container");

    if (stepFormContainer.children.length > 1) {
        stepFormContainer.removeChild(stepFormContainer.lastElementChild);
        stepCount--;  // ステップカウントを減らす
    }
}

// Sortableを初期化
new Sortable(document.getElementById('step-form-container'), {
    handle: '.srt_hndl', // ドラッグハンドルをアイコンに変更
    animation: 150, // アニメーションのスピードを設定

    onEnd: function () {
        // 並び替え後の要素を取得
        const stepItems = document.querySelectorAll('#step-form-container li');

        // 各ステップ番号を再割り当て
        stepItems.forEach((item, index) => {
            const stepNumberLabel = item.querySelector('.step-number-label');
            const stepNumberInput = item.querySelector('input[name^="step_number"]');
            
            // stepNumberLabelが存在する場合のみ更新
            if (stepNumberLabel) {
                stepNumberLabel.innerText = `作り方 ${index + 1}`; // 番号を更新
            }

            // 隠しフィールドに新しい番号を保存
            if (stepNumberInput) {
                stepNumberInput.value = index + 1;
            }
        });
    }
});