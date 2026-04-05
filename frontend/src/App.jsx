import React, { useState } from 'react';

function App() {
    const [topic, setTopic] = useState("");
    const [numSlides, setNumSlides] = useState(5);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(false);

        const formData = new FormData();
        formData.append("topic", topic);
        formData.append("num_slides", numSlides);

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'An unknown error occurred.' }));
                throw new Error(errorData.detail || 'Failed to generate presentation');
            }

            let filename = 'presentation.pptx';
            const disposition = response.headers.get('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                const matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '');
                }
            }

            const blob = await response.blob();
            
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            
            window.URL.revokeObjectURL(downloadUrl);
            document.body.removeChild(a);

            setSuccess(true);
            setTopic("");
            setNumSlides(5);
        } catch (err) {
            console.error('Generation error:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className="background-elements">
                <div className="blob purple"></div>
                <div className="blob blue"></div>
            </div>
            
            <div className="container">
                <header>
                    <h1>Auto <span className="gradient-text">PPT</span></h1>
                    <p>Generate highly intelligent PowerPoint presentations instantly.</p>
                </header>

                <main>
                    <div className="card">
                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="topic">Presentation Topic</label>
                                <input 
                                    type="text" 
                                    id="topic" 
                                    name="topic" 
                                    placeholder="e.g. The Future of Quantum Computing" 
                                    required 
                                    autoComplete="off"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    disabled={loading}
                                />
                            </div>
                            
                            <div className="form-group slide-group">
                                <label htmlFor="num_slides">Number of Slides</label>
                                <div className="range-container">
                                    <input 
                                        type="range" 
                                        id="num_slides" 
                                        name="num_slides" 
                                        min="1" 
                                        max="20" 
                                        value={numSlides} 
                                        onChange={(e) => setNumSlides(parseInt(e.target.value))}
                                        disabled={loading}
                                    />
                                    <span className="badge">{numSlides}</span>
                                </div>
                            </div>
                            
                            <button type="submit" disabled={loading}>
                                {loading ? (
                                    <div className="spinner"></div>
                                ) : (
                                    <span className="btn-text">Generate Presentation</span>
                                )}
                            </button>
                            
                            {error && <div className="message error">{error}</div>}
                            {success && <div className="message success">Presentation generated successfully!</div>}
                        </form>
                    </div>
                </main>
            </div>
        </>
    );
}

export default App;
