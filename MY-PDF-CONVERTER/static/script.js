document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const fileInput = document.querySelector('input[type="file"]');
    const submitBtn = document.querySelector('button');
    const loader = document.getElementById('loader');

    form.onsubmit = (e) => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file first!");
            e.preventDefault();
            return;
        }

        // Show the 'Glass' loader and hide the button
        submitBtn.style.display = 'none';
        loader.style.display = 'block';
        
        // Add a nice "Processing" text effect
        loader.querySelector('p').innerText = "Processing your file... ✨";
    };

    // Real-time validation: Change UI color if file type is wrong
    fileInput.onchange = () => {
        const fileName = fileInput.value;
        const extension = fileName.split('.').pop().toLowerCase();
        const direction = document.querySelector('select').value;

        if (direction === 'to_doc' && extension !== 'pdf') {
            alert("Please select a PDF file!");
            fileInput.value = ''; // Reset
        } else if (direction === 'to_pdf' && extension !== 'docx') {
            alert("Please select a Word (.docx) file!");
            fileInput.value = ''; // Reset
        }
    };
});