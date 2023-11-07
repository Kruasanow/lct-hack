document.addEventListener('DOMContentLoaded', function () {
    const addValueButton = document.getElementById('addValueButton');
    const addValueButton1 = document.getElementById('addValueButton1');
    const outputValues = document.getElementById('outputValues');
    const enteredValues = new Set(); // Множество для хранения введенных значений

    var resArr = []; // Создаем пустой массив для сохранения результатов

    // Функция для обновления значения в скрытом поле формы
    function updateHiddenInput() {
        const hiddenInput = document.getElementById('resArr');
        hiddenInput.value = JSON.stringify(resArr);
    }

    addValueButton.addEventListener('click', () => {
        const checkOper = '&';
        const InputedData = document.getElementById('InputedData').value;
        const Operators = document.getElementById('Operators').value;
        const curvalue = document.getElementById('curvalue').value;

        // Проверка, что все значения не пусты
        if (InputedData.trim() === '' || Operators.trim() === '' || curvalue.trim() === '') {
            return;
        }

        const inputValue = `${InputedData} ${Operators} ${curvalue} ${checkOper}`;

        if (!enteredValues.has(inputValue)) {
            enteredValues.add(inputValue);

            const outputValueDiv = document.createElement('div');
            outputValueDiv.classList.add('output-value');
            outputValueDiv.textContent = inputValue;
            outputValues.appendChild(outputValueDiv);

            // Если количество элементов в .output-container больше 3, делаем его скроллером
            if (outputValues.children.length > 3) {
                outputValues.style.overflowY = 'scroll';
            }

            // Добавляем значение в resArr
            resArr.push(inputValue);
            console.log(resArr); // Выводим resArr в консоль после каждого добавления
        }
        updateHiddenInput();
    });

    addValueButton1.addEventListener('click', () => {
        const checkOper = '|';
        const InputedData = document.getElementById('InputedData').value;
        const Operators = document.getElementById('Operators').value;
        const curvalue = document.getElementById('curvalue').value;

        // Проверка, что все значения не пусты
        if (InputedData.trim() === '' || Operators.trim() === '' || curvalue.trim() === '') {
            return;
        }

        const inputValue = `${InputedData} ${Operators} ${curvalue} ${checkOper}`;

        if (!enteredValues.has(inputValue)) {
            enteredValues.add(inputValue);

            const outputValueDiv = document.createElement('div');
            outputValueDiv.classList.add('output-value');
            outputValueDiv.textContent = inputValue;
            outputValues.appendChild(outputValueDiv);

            // Если количество элементов в .output-container больше 3, делаем его скроллером
            if (outputValues.children.length > 3) {
                outputValues.style.overflowY = 'scroll';
            }

            // Добавляем значение в resArr
            resArr.push(inputValue);
            console.log(resArr); // Выводим resArr в консоль после каждого добавления
        }
        updateHiddenInput();
    });
    updateHiddenInput();
});
