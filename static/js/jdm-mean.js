const input = document.querySelector('#jdm-mean-input');
const loadingTag = document.querySelector('.jdm_mean-loading');
const result = document.querySelector('.jdm_mean-result');
const calculateButton = document.querySelector('.jdm_mean-calculate');


// Functions
const startLoading = () => {
    loadingTag.style.display = 'block';
    result.style.display = 'none';
}

const stopLoading = () => {
    loadingTag.style.display = 'none';
    result.style.display = 'block';
}

const fetchData = async () => {
    const url = 'http://localhost:5555/mean';
    const data = input.value;

    try {
        startLoading();
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data
            })
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }
        return response.json();


    } catch (e) {
        throw new Error(e);
    }
}

// Events
calculateButton.addEventListener('click', async () => {
    if (input.value.trim().length === 0) {
        return;
    }

    try {
        const fetchedData = await fetchData();

        console.log(`La media es de: ${fetchedData.mean}`);

        result.innerHTML = `La media es de: ${fetchedData.mean}`;

    } catch (e) {
        console.error(e);
        result.innerHTML = `Algo salió mal... ¿estás enviando un arreglo de solo números?`;
    }

    stopLoading();
})
