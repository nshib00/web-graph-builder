document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const graphImage = document.getElementById('graph-image');
    const uploadList = document.getElementById('upload-list');

    // обработка загрузки файла
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!fileInput.files[0]) return;

        try {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            const response = await fetch(
                '/upload', { 
                    method: 'POST',
                    body: formData 
                });
            const result = await response.json();
            
            graphImage.src = result.image;
            graphImage.style.display = 'block';
            await loadGraphsList();
            
        } catch (error) {
            console.error('Upload error:', error);
        }
    });
    
    async function loadGraphsList() {
        try {
            const response = await fetch('/graphs');
            const graphs = await response.json();
            
            uploadList.innerHTML = '';
            graphs.forEach(graph => {
                const formattedTime = new Date(graph.upload_time).toLocaleString('ru-RU').replace(',', '');
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = `${graph.filename} | ${formattedTime}`;
                li.addEventListener('click', () => loadGraph(graph.id));
                uploadList.appendChild(li);
            });
        } catch (error) {
            console.error('Error while fetching graphs list:', error);
        }
    }

    async function loadGraph(graphId) {
        try {
            const response = await fetch(`/graph/${graphId}`);
            const data = await response.json();
            graphImage.src = data.image;
            graphImage.style.display = 'block';
        } catch (error) {
            console.error('Error while loading graph:', error);
        }
    }
    loadGraphsList();
});