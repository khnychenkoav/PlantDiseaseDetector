import React from 'react';

function UploadForm() {
    const handleSubmit = (event) => {
        event.preventDefault();
        // Logic to upload the image
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" accept="image/*" />
            <button type="submit">Upload</button>
        </form>
    );
}

export default UploadForm;
