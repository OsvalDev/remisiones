const addBoxFields = ()=> {
    const container = document.getElementById('inputContianer');
    const nFields = parseInt(document.getElementById('numFields').value, 10) + 1;
    document.getElementById('numFields').value = nFields;
    const newDiv = document.createElement('div');
    newDiv.className = 'flex mb-2';

    const inputText = document.createElement('input');
    inputText.type = 'text';
    inputText.name = `type${nFields}`;
    inputText.id =  `type${nFields}`;
    inputText.className = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pink-500 focus:border-pink-500 block w-1/2 p-2.5 mx-2';

    const inputNumber = document.createElement('input');
    inputNumber.type = 'number';
    inputNumber.name = `cant${nFields}`;
    inputNumber.id = `cant${nFields}`;
    inputNumber.className = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pink-500 focus:border-pink-500 block w-1/2 p-2.5 mx-2';

    newDiv.appendChild(inputText);
    newDiv.appendChild(inputNumber);

    container.appendChild(newDiv);

}

document.getElementById('btnAddBoxes').onclick = addBoxFields;