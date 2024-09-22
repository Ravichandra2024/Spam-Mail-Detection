var contextMenuItem = {
    "id": "money",
    "title": "Email spam detector",
    "contexts": ["selection"]
};

chrome.contextMenus.create(contextMenuItem);

chrome.contextMenus.onClicked.addListener(function (info, tab) {
    try {
        if ( info.selectionText) {
            var message = encodeURIComponent(info.selectionText);
            fetch("http://127.0.0.1:5000/?message=" + message)
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data.message) {
                        console.log(data.message);
                        chrome.storage.sync.set({ 'detect': data.message }, function () {
                        });
                    }
                })
                .catch(error => {
                    console.error('Error during fetch operation:', error);
                });
        }
    } catch (e) {
        console.error('Error:', e);
    }
});

chrome.storage.onChanged.addListener(function (changes, areaName) {
    if (areaName === 'sync' && changes.detect) {
        chrome.action.setBadgeText({ "text": changes.detect.newValue.toString() });
    }
});
chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({ 'detect': " " }, function () {
    });
    chrome.action.setBadgeText({ text: ' ' });
});
