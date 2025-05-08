chrome.webNavigation.onCompleted.addListener((details) => {
    console.log("New Wikipedia page loaded:", details.url);
    
    fetch('http://127.0.0.1:5000/api/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: details.url})
    })
    .then(res => {
        console.log('Response status:', res.status);
        console.log('Response headers:', res.headers);
        return res.text().then(text => {
            try {
                return JSON.parse(text);
            } catch (e) {
                console.error('Failed to parse JSON:', text);
                throw e;
            }
        });
    })
    .then(data => console.log('Server response:', data.response))
    .catch(err => console.error('Error:', err));
}, {
    url: [
        { hostEquals: 'en.wikipedia.org', pathContains: '/wiki/' }
    ]
});
  