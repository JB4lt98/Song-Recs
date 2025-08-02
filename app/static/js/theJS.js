/* Show the button*/
document.getElementById('search-button').addEventListener('click', function() {
    const resultsBox = document.getElementById('results-box');
    const imagePlaceholder = document.getElementById('image-placeholder');
    const songInfo = document.getElementById('song-info');

    if (resultsBox.style.display === 'none' || resultsBox.style.display === '') {
        resultsBox.style.display = 'block';
        imagePlaceholder.style.display = 'block'; // Show the image
        songInfo.style.display = 'block';
    } else {
        resultsBox.style.display = 'none';
        imagePlaceholder.style.display = 'none'; // Hide the image
        songInfo.style.display = 'none';
    }
});

// Fetch genres from the backend and populate the dropdown
    fetch('/get_genres')
        .then(response => response.json())
        .then(data => {
            const genreDropdown = document.getElementById('genres');
            data.genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre;
                option.textContent = genre;
                genreDropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching genres:', error));
