document.addEventListener('DOMContentLoaded', () => {
    fetch('/graphs')
        .then(response => response.json())
        .then(graphs => {
            const uploadList = document.getElementById('upload-list');
            graphs.forEach(graph => {
                const formattedTime = new Date(graph.upload_time).toLocaleString('ru-RU').replace(',', '');
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = `${graph.filename} | ${formattedTime}`;
                li.addEventListener('click', () => loadGraph(graph.id));
                uploadList.appendChild(li);
                console.log(graph);
            });
        })
        .catch(error => console.error('Error while fetching graphs list:', error));

    function loadGraph(graphId) {
        fetch(`/graph/${graphId}`)
            .then(response => response.json())
            .catch(error => console.error('Error while loading graph:', error));
    }
});
