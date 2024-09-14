let stepCount = 1;  // ステップのカウントを初期化

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

    // 定義したフィールドをnewStepDivに追加
    newStepDiv.appendChild(stepNumberInput);
    newStepDiv.appendChild(stepTextLabel);
    newStepDiv.appendChild(stepTextInput);

    stepFormContainer.appendChild(newStepDiv);
}